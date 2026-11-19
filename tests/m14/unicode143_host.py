"""Compile only our codec/table on the host and compare independent official data."""
from array import array
import ctypes as c
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import uuid

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command


def main():
    out=ROOT/'build/m14-native/stage3/unicode-host'
    work=out/uuid.uuid4().hex
    work.mkdir(parents=True)
    source=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/3/CaseFolding-17.0.0.txt'
    provenance=json.loads((ROOT/'third_party/unicode/provenance.json').read_text(encoding='utf-8'))
    raw=source.read_bytes()
    assert hashlib.sha256(raw).hexdigest()==provenance['sources']['case_folding']['sha256']
    spec=importlib.util.spec_from_file_location('unicode_generator143',ROOT/'tools/build/unicode143.py')
    generator=importlib.util.module_from_spec(spec);spec.loader.exec_module(generator)
    generated,manifest=generator.generate(source)
    assert generated==(ROOT/'kernel/windows8/unicode-table143.inc').read_bytes()
    assert manifest==(ROOT/'third_party/unicode/case-map143.json').read_bytes()
    expected=array('I',range(0x110000))
    count=0
    for line in raw.decode('utf-8').splitlines():
        row=line.split('#',1)[0].strip()
        if not row:continue
        cp,status,mapping,*_=[part.strip() for part in row.split(';')]
        if status in ('C','S'):
            values=mapping.split();assert len(values)==1
            expected[int(cp,16)]=int(values[0],16);count+=1
    tools=pinned_tools();obj=work/'codec.obj';dll=work/'codec.dll'
    command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-ffreestanding',
             '-fno-builtin','-fno-stack-protector','-Wall','-Wextra','-Werror',
             '-c',ROOT/'tests/m14/unicode143_host.c','-o',obj])
    command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(dll),obj])
    lib=c.CDLL(str(dll))
    lib.validate_fold143.argtypes=[c.POINTER(c.c_uint32),c.c_uint32];lib.validate_fold143.restype=c.c_uint32
    reference=(c.c_uint32*len(expected)).from_buffer(expected)
    assert lib.validate_fold143(reference,len(expected))==0
    lib.validate_scalars143.restype=c.c_uint32;assert lib.validate_scalars143()==0
    lib.decode8_host143.argtypes=[c.c_char_p,c.c_uint,c.POINTER(c.c_uint),c.POINTER(c.c_uint32)]
    lib.decode16_host143.argtypes=[c.POINTER(c.c_uint16),c.c_uint,c.POINTER(c.c_uint),c.POINTER(c.c_uint32)]
    lib.encode8_host143.argtypes=[c.c_uint32,c.c_void_p,c.c_uint,c.POINTER(c.c_uint)]
    lib.encode16_host143.argtypes=[c.c_uint32,c.c_void_p,c.c_uint,c.POINTER(c.c_uint)]
    malformed=[b'\x80',b'\xc0\x80',b'\xc1\xbf',b'\xc2',b'\xe0\x80\x80',
               b'\xe1\x80',b'\xed\xa0\x80',b'\xf0\x80\x80\x80',
               b'\xf4\x90\x80\x80',b'\xf5\x80\x80\x80',b'\xff',b'\xe2\x82',b'\xf0\x9f\x92']
    for text in malformed:
        at=c.c_uint();value=c.c_uint32(0xa55aa55a)
        assert not lib.decode8_host143(text,len(text),c.byref(at),c.byref(value))
        assert at.value==0 and value.value==0xa55aa55a
    for units in ([0xd800],[0xdc00],[0xdfff],[0xdbff,65],[0xd800,0xd800]):
        data=(c.c_uint16*len(units))(*units);at=c.c_uint();value=c.c_uint32(17)
        assert not lib.decode16_host143(data,len(units),c.byref(at),c.byref(value))
        assert at.value==0 and value.value==17
    points=[0,0x41,0x7f,0x80,0x7ff,0x800,0xd7ff,0xe000,0xffff,0x10000,0x10428,0x1f642,0x10ffff]
    for cp in points:
        expected8=chr(cp).encode('utf-8');expected16=chr(cp).encode('utf-16-le')
        body=c.create_string_buffer(b'\xa5'*8);at=c.c_uint()
        assert lib.encode8_host143(cp,body,4,c.byref(at)) and body.raw[:at.value]==expected8
        assert body.raw[at.value:]==b'\xa5'*(8-at.value)+b'\0'
        wide=c.create_string_buffer(b'\xa5'*8);at=c.c_uint()
        assert lib.encode16_host143(cp,wide,2,c.byref(at)) and wide.raw[:at.value*2]==expected16
        for cap in range(len(expected8)):
            guarded=c.create_string_buffer(b'\xa5'*8);at=c.c_uint()
            assert not lib.encode8_host143(cp,guarded,cap,c.byref(at)) and at.value==0
            assert guarded.raw==b'\xa5'*8+b'\0'
    for cp in [0xd800,0xdfff,0x110000,0xffffffff]:
        body=c.create_string_buffer(8);at=c.c_uint()
        assert not lib.encode8_host143(cp,body,8,c.byref(at)) and not at.value
        assert not lib.encode16_host143(cp,body,4,c.byref(at)) and not at.value
    lib.equal_host143.argtypes=[c.c_char_p,c.c_uint,c.c_char_p,c.c_uint]
    for left,right,equal in [('Owner','OWNER',True),('Straße','STRAẞE',True),
                             ('Straße','STRASSE',False),('σ','ς',True),('é','e\u0301',False),
                             ('İ','i',False),('𐐨','𐐀',True)]:
        a,b=left.encode('utf-8'),right.encode('utf-8')
        assert lib.equal_host143(a,len(a),b,len(b))==equal,(left,right)
    assert hashlib.sha256((ROOT/'third_party/unicode/LICENSE.txt').read_bytes()).hexdigest()==provenance['sources']['license']['sha256']
    files=['kernel/windows8/unicode143.inc','kernel/windows8/unicode-table143.inc',
           'tools/build/unicode143.py','tests/m14/unicode143_host.c','tests/m14/unicode143_host.py']
    result=dict(passed=True,scope='Host compiled kernel codec/table; not native path or registry qualification',
                source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files},
                official_mapping_pairs=count,all_codepoints_compared=0x110000,
                valid_scalar_roundtrips=0x110000-2048,malformed_utf8_cases=len(malformed),
                malformed_utf16_cases=5,independent_reference_boundaries=points,
                read_only_case_component_bytes=json.loads(manifest)['read_only_component_bytes'],
                windows_nls_equivalence_claimed=False)
    (out/'results.json').write_bytes((json.dumps(result,indent=2)+'\n').encode('utf-8'))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
