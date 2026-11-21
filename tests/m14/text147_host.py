"""UTF-16 MSI string sizing and malformed Unicode against Python codecs."""
import ctypes,hashlib,json,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command

def main():
 out=ROOT/'build/m14-native/stage7/text-host';out.mkdir(parents=True,exist_ok=True);t=pinned_tools()
 command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-c',ROOT/'tests/m14/text147_host.c','-o',out/'text.obj'])
 command([t['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'text.dll'),out/'text.obj']);lib=ctypes.CDLL(str(out/'text.dll'));lib.from147.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_uint];lib.to147.argtypes=[ctypes.c_char_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_uint)];checks=0
 rng=random.Random(147);texts=['','ASCII','\u00e9\u20ac\U0001f600','\U0010ffff','x'*4096]
 for _ in range(100):texts.append(''.join(chr(rng.choice([rng.randrange(1,0xd800),rng.randrange(0xe000,0x110000)]))for _ in range(rng.randrange(1,30))))
 for text in texts:
  raw=text.encode();wide=text.encode('utf-16-le');source=ctypes.create_string_buffer(wide+b'\0\0')
  for cap in [1,len(raw)+1,len(raw)+2]:
   target=(ctypes.c_ubyte*(cap+8))(*([0x9b]*(cap+8)));code=lib.from147(source,target,cap);assert bytes(target)[cap:]==b'\x9b'*8;checks+=1
   if cap>len(raw):assert code==0 and bytes(target)[:len(raw)+1]==raw+b'\0';checks+=1
   else:assert code==1816;checks+=1
  for cap in [0,1,len(wide)//2,len(wide)//2+1,len(wide)//2+2]:
   target=(ctypes.c_ubyte*(cap*2+8))(*([0x9b]*(cap*2+8)));size=ctypes.c_uint(cap);code=lib.to147(raw,target,ctypes.byref(size));assert size.value==len(wide)//2 and bytes(target)[cap*2:]==b'\x9b'*8;checks+=1
   assert code==(0 if cap>len(wide)//2 else 234);checks+=1
   if cap>len(wide)//2:assert bytes(target)[:len(wide)+2]==wide+b'\0\0';checks+=1
   elif cap:bytes(target)[:cap*2].decode('utf-16-le');checks+=1
 for raw in [b'\x80',b'\xc0\xaf',b'\xe0\x80\x80',b'\xed\xa0\x80',b'\xf4\x90\x80\x80',b'\xf0\x9f']:
  target=(ctypes.c_uint16*16)(*([0x9b9b]*16));size=ctypes.c_uint(16);assert lib.to147(raw,target,ctypes.byref(size))==1113 and list(target)==[0x9b9b]*16;checks+=1
 for units in [[0xd800,0],[0xdc00,0],[0xd800,65,0]]:
  target=ctypes.create_string_buffer(64);source=(ctypes.c_uint16*len(units))(*units);assert lib.from147(source,target,64)==1113;checks+=1
 sources=['user/windows8/msi-text147.h','tests/m14/text147_host.c','tests/m14/text147_host.py'];report=dict(passed=True,checks=checks,scope='Production bounded MSI Unicode conversion/output sizing; not original custom-action qualification',sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources});(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS MSI Unicode checks',checks)
if __name__=='__main__':main()
