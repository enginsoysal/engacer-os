"""Compare the production C sampler against original masks and fresh Inter pixels."""
import ctypes as c
import hashlib
import json
import random
import re
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, features
import PIL

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/build'))
import font73
import font146
from m1 import command, pinned_tools


def layout_checks(out, tools):
    source = (ROOT / 'kernel/core/graphics73.inc').read_text()
    face = source[source.index('static const font73_face *face73('):source.index('#ifdef FONT146_PACKET\nunsigned ui73_measure')]
    measure_at = source.index('unsigned ui73_measure(')
    new_measure, rest = source[measure_at:].split('\n#else\n', 1)
    old_measure = rest.split('\n#endif\n', 1)[0]
    layout_at = source.index('static unsigned font_previous146(')
    new_layout, rest = source[layout_at:].split('\n#else\n', 1)
    old_layout = rest.split('\n#endif\n', 1)[0]
    prefix = '''#include "font73.h"
#include <engine/ui/font146.h>
#include <engine/desktop/text146.h>
static unsigned scale73=2,rows_count,overflow;
static char rows[8][256];
void*memset(void*out,int value,size_t count){volatile unsigned char*p=out;for(size_t n=0;n<count;++n)p[n]=(unsigned char)value;return out;}
static void text73(unsigned x,unsigned y,const char*s,unsigned role,uint32_t color){(void)x;(void)y;(void)role;(void)color;if(rows_count==8){overflow=1;return;}unsigned n=0;while(s[n]&&n<255){rows[rows_count][n]=s[n];++n;}rows[rows_count][n]=0;++rows_count;}
static void serial_text(const char*s){(void)s;overflow=1;}
'''
    suffix = '''
__declspec(dllexport) unsigned run_editor_glyph146(const char*text,unsigned bytes,unsigned at,char*out){return text_glyph146(text,at,bytes,out);}
__declspec(dllexport) unsigned run_layout146(unsigned mode,unsigned scale,unsigned width,unsigned role,const char*text,char*out,unsigned capacity,unsigned*count,unsigned*failed){
 scale73=scale;rows_count=overflow=0;memset(rows,0,sizeof(rows));
 if(mode)ui73_paragraph(0,0,width,8,text,0);else ui73_fit(0,0,width,text,role,0);
 unsigned used=0;for(unsigned row=0;row<rows_count;++row){unsigned n=0;do{if(used>=capacity)return 0;out[used++]=rows[row][n];}while(rows[row][n++]);}*count=rows_count;*failed=overflow;return used;
}
'''
    libraries = []
    identities = {}
    for name, measure, layout in [('retained-ascii', old_measure, old_layout), ('packet-unicode', new_measure, new_layout)]:
        text = prefix + face + measure + layout + suffix
        path = out / (name + '.c')
        path.write_bytes(text.encode())
        command([tools['clang'], '--target=x86_64-pc-windows-msvc', '-std=c17', '-O2',
                 '-Wall', '-Wextra', '-Werror', '-ffreestanding', '-fno-builtin', '-fno-stack-protector',
                 '-DENGINE_M12', '-DENGINE_M11', '-I', ROOT / 'include', '-I', out,
                 '-c', path, '-o', out / (name + '.obj')])
        command([tools['lld-link'], '/dll', '/noentry', '/nodefaultlib', '/timestamp:0',
                 '/export:run_layout146', out / (name + '.obj'), '/out:' + str(out / (name + '.dll'))])
        lib = c.CDLL(str(out / (name + '.dll')))
        lib.run_layout146.argtypes = [c.c_uint] * 4 + [c.c_char_p, c.c_void_p, c.c_uint, c.POINTER(c.c_uint), c.POINTER(c.c_uint)]
        lib.run_editor_glyph146.argtypes=[c.c_char_p,c.c_uint,c.c_uint,c.c_void_p]
        lib.run_editor_glyph146.restype=c.c_uint
        libraries.append(lib)
        identities[name] = hashlib.sha256(text.encode()).hexdigest()

    def run(lib, mode, scale, width, role, text):
        storage = (c.c_ubyte * 8194)()
        storage[0] = storage[-1] = 173
        count, failed = c.c_uint(), c.c_uint()
        size = lib.run_layout146(mode, scale, width, role, text.encode(), c.byref(storage, 1), 8192, c.byref(count), c.byref(failed))
        assert storage[0] == storage[-1] == 173 and size <= 8192
        rows = bytes(storage[1:1 + size]).split(b'\0')[:-1] if size else []
        assert len(rows) == count.value
        return rows, failed.value

    ascii_count = unicode_count = 0
    for scale in (2, 3, 4):
        for role in (1, 3, 5):
            for width in (0, 1, 7, 16, 32, 57, 100, 250, 1000):
                for mode in (0, 1):
                    for text in ('', 'Original 7-Zip archive', 'Memory usage\nwith more words.', 'a' * 260):
                        assert run(libraries[0], mode, scale, width, role, text) == run(libraries[1], mode, scale, width, role, text)
                        ascii_count += 1
                    for text in ('m146-é.txt', 'Engacer ĞğİıŞş €', '😀😀', 'a' * 251 + 'é', 'a' * 250 + '€', 'a' * 249 + '😀', 'é' * 130):
                        rows, _ = run(libraries[1], mode, scale, width, role, text)
                        for row in rows:
                            row.decode('utf-8', errors='strict')
                            assert len(row) <= 255
                        unicode_count += 1
    editor_steps=0
    for text in ('ASCII text','Aé€😀\tZ\r\nnext','é'*128,'ĞğİıŞş €','a'*251+'é'):
        raw=text.encode();at=0
        for char in text:
            storage=(c.c_ubyte*7)();storage[0]=storage[-1]=173
            next_at=libraries[1].run_editor_glyph146(raw,len(raw),at,c.byref(storage,1))
            assert next_at==at+len(char.encode()) and bytes(storage[1:6]).split(b'\0')[0]==(' 'if char=='\t'else char).encode()
            assert storage[0]==storage[-1]==173
            at=next_at;editor_steps+=1
    randomizer=random.Random(146)
    for _ in range(10000):
        raw=randomizer.randbytes(randomizer.randrange(1,65));at=randomizer.randrange(len(raw)+1)
        storage=(c.c_ubyte*7)();storage[0]=storage[-1]=173
        next_at=libraries[1].run_editor_glyph146(raw,len(raw),at,c.byref(storage,1))
        assert (at<next_at<=len(raw))if at<len(raw)else next_at==at
        assert storage[0]==storage[-1]==173 and 0 in storage[1:6]
    return dict(editor_scalar_steps=editor_steps,editor_malformed_bounds_checks=10000,
                retained_ascii_layout_cases=ascii_count, unicode_layout_cases=unicode_count,
                extracted_production_sha256=identities)


def main():
    out = ROOT / 'build/m14-native/stage6/font-host'
    baseline = out / 'm13'
    baseline.mkdir(parents=True, exist_ok=True)
    retained = font73.prepare(baseline)
    text = (baseline / 'font73.h').read_text()
    faces = [tuple(map(int, row.split(','))) for row in re.findall(r'\{([^{}]+)\}', re.search(r'font73_faces\[\]=\{(.*?)\};', text)[1])]
    glyphs = [tuple(map(int, row.split(','))) for row in re.findall(r'\{([^{}]+)\}', re.search(r'font73_glyphs\[\]=\{(.*?)\};', text)[1])]
    data = bytes(map(int, re.search(r'font73_data\[\]=\{([^}]*)\}', text)[1].split(',')))
    updated, masks, extras, report = font146.repack(ROOT / 'third_party/inter', faces, glyphs, data)
    candidate = font73.header(ROOT / 'third_party/inter', faces, updated, masks, extras)
    (out / 'font73.h').write_bytes(candidate.encode())
    tools = pinned_tools()
    command([tools['clang'], '--target=x86_64-pc-windows-msvc', '-std=c17', '-O2',
             '-Wall', '-Wextra', '-Werror', '-ffreestanding', '-fno-builtin',
             '-fno-stack-protector', '-I', ROOT / 'include', '-I', out,
             '-c', ROOT / 'tests/m14/font146_host.c', '-o', out / 'font.obj'])
    names = ['license146', 'raster146', 'lookup146', 'scalars146', 'packets146']
    command([tools['lld-link'], '/dll', '/noentry', '/nodefaultlib', '/timestamp:0',
             *['/export:' + name for name in names], out / 'font.obj', '/out:' + str(out / 'font.dll')])
    lib = c.CDLL(str(out / 'font.dll'))
    bytep = c.POINTER(c.c_ubyte)
    intp = c.POINTER(c.c_int)
    lib.raster146.argtypes = [c.c_uint, c.c_uint, bytep, c.c_uint, intp]
    lib.lookup146.argtypes = [c.c_uint, c.c_uint, intp]
    lib.scalars146.argtypes = [c.c_char_p, c.c_uint, c.POINTER(c.c_uint32), c.POINTER(c.c_uint), c.c_uint]
    lib.packets146.argtypes = [bytep, c.c_uint, bytep, c.c_uint, c.POINTER(c.c_uint)]
    pixels = 0

    def compare(extra, index, expected, metrics):
        nonlocal pixels
        storage = (c.c_ubyte * (len(expected) + 2))()
        storage[0] = storage[-1] = 173
        actual = (c.c_int * 6)()
        assert lib.raster146(extra, index, c.cast(c.byref(storage, 1), bytep), len(expected), actual)
        assert storage[0] == storage[-1] == 173
        assert bytes(storage[1:-1]) == expected, (extra, index)
        assert list(actual)[:5] == list(metrics), (extra, index, list(actual), metrics)
        pixels += len(expected)

    for index, (offset, size, width, height, x, y, advance) in enumerate(glyphs):
        expected = bytearray()
        for at in range(offset, offset + size, 2):
            expected.extend(bytes([data[at + 1]]) * data[at])
        compare(0, index, expected, (width, height, x, y, advance))
    for index, (code, base, descriptor) in enumerate(extras):
        size = report['extra_faces'][index // len(font146.CODES)]
        font = ImageFont.truetype(str(ROOT / 'third_party/inter/Inter.ttf'), size)
        font.set_variation_by_axes([min(32, max(14, size)), 400])
        x, y, right, bottom = font.getbbox(chr(code), anchor='ls')
        width, height = right - x, bottom - y
        image = Image.new('L', (max(1, width), max(1, height)))
        ImageDraw.Draw(image).text((-x, -y), chr(code), font=font, fill=255, anchor='ls')
        expected = image.tobytes() if width and height else b''
        compare(1, index, expected, (width, height, x, y, round(font.getlength(chr(code)))))
    for face in range(len(faces)):
        metrics = (c.c_int * 6)()
        fallback = (c.c_int * 6)()
        assert lib.lookup146(face, ord('?'), fallback)
        assert lib.lookup146(face, 0x1f600, metrics) and list(metrics) == list(fallback)
    utf8 = 'Aé€😀z'.encode()
    scalars = (c.c_uint32 * 16)()
    positions = (c.c_uint * 16)()
    assert lib.scalars146(utf8, len(utf8), scalars, positions, 16) == 5
    assert list(scalars)[:5] == [65, 233, 8364, 0x1f600, 122]
    assert list(positions)[:5] == [1, 3, 6, 10, 11]
    randomizer = random.Random(146)
    for turn in range(10000):
        raw = randomizer.randbytes(randomizer.randrange(128))
        source = (c.c_ubyte * max(1, len(raw))).from_buffer_copy(raw or b'\0')
        storage = (c.c_ubyte * 4098)()
        storage[0] = storage[-1] = 173
        written = c.c_uint()
        status = lib.packets146(source, len(raw), c.cast(c.byref(storage, 1), bytep), 4096, c.byref(written))
        assert status in (-1, 0, 122) and written.value <= 4096
        assert storage[0] == storage[-1] == 173
        text = bytes(value or 1 for value in raw[:15])
        count = lib.scalars146(text, len(text), scalars, positions, 16)
        assert count <= len(text) and all(0 < positions[n] <= len(text) for n in range(count))
    lock = dict(pillow=PIL.__version__, freetype=features.version('freetype2'),
                header_sha256=hashlib.sha256(candidate.encode()).hexdigest())
    layout = layout_checks(out, tools)
    report.update(passed=True, scope='Supporting hosted C codec/sampler proof; not native rendering qualification',
                  retained_baseline=retained, exact_reference_pixels=pixels,
                  malformed_packet_utf8_rounds=10000, proposed_raster_lock=lock,
                  layout=layout,
                  sources={path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in
                           ['tools/build/font73.py', 'tools/build/font146.py', 'include/engine/ui/font146.h',
                            'kernel/core/graphics73.inc', 'kernel/desktop/session.c', 'include/engine/desktop/text146.h', 'tests/m14/font146_host.c', 'tests/m14/font146_host.py']})
    (out / 'results.json').write_bytes((json.dumps(report, indent=2) + '\n').encode())
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
