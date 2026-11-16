"""Exercise native vector rules and render a review atlas from production rows."""
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools
OUT=ROOT/'build/m12/stage2'

def icon(exe,number,size,theme):
    raw=subprocess.check_output([str(exe),'dump',str(number),str(size),str(theme)])
    assert len(raw)==size*size*4
    data=[]
    for value, in struct.iter_unpack('<I',raw):
        alpha=value>>24
        data.append(tuple(min(255,(((value>>shift)&255)*255+alpha//2)//alpha) if alpha else 0 for shift in (16,8,0))+(alpha,))
    image=Image.new('RGBA',(size,size));image.putdata(data);return image

def main():
    OUT.mkdir(parents=True,exist_ok=True);exe=OUT/'icons-host.exe'
    command=[pinned_tools()['clang'],'-std=c17','-O2','-Wall','-Wextra','-Werror','-I','include','tests/m12/icons_host.c','-o',str(exe)]
    result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
    if result.returncode:raise RuntimeError(result.stderr)
    tested=subprocess.run([str(exe)],cwd=ROOT,check=True,capture_output=True,text=True)
    catalog=json.loads((ROOT/'docs/architecture/figures/m12-icons/catalog.json').read_text())
    for theme in (0,1):
        sheet=Image.new('RGBA',(8*140,8*106),'#f8fafc' if not theme else '#161d27');draw=ImageDraw.Draw(sheet)
        for item in catalog['icons']:
            i=item['id'];x=(i%8)*140;y=(i//8)*106
            sheet.alpha_composite(icon(exe,i,64,theme),(x+38,y+3))
            draw.text((x+8,y+75),item['name'],fill='#17212f' if not theme else '#e8edf5')
        sheet.convert('RGB').save(OUT/f'icons-{"dark" if theme else "light"}.png')
    paths=['include/engine/ui/icons12.h','include/engine/ui/icons12_data.h','kernel/core/icons12.inc','tools/design/icons12.py','tests/m12/icons_host.c']
    report=dict(passed=True,stage='M12.2',scope='Host execution of production geometry/raster rules and independent geometry reference; native binding and input are separate checks',checks=tested.stdout.strip(),icons=len(catalog['icons']),temporary_row_bytes=128*4,raster_cache_bytes=0,allocations_in_renderer=0,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths})
    (OUT/'host-results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(tested.stdout.strip())

if __name__=='__main__':main()
