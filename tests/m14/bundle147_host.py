"""Exercise the shared EFI/kernel boot-module parser against bounded corrupt input."""
import ctypes,hashlib,json,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command

def main():
 out=ROOT/'build/m14-native/stage7/bundle-host';out.mkdir(parents=True,exist_ok=True);t=pinned_tools();obj=out/'bundle.obj';dll=out/'bundle.dll'
 command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-I',ROOT/'include','-c',ROOT/'tests/m14/bundle147_host.c','-o',obj])
 command([t['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(dll),obj]);lib=ctypes.CDLL(str(dll));lib.parse147.argtypes=[ctypes.c_void_p,ctypes.c_size_t];checks=0
 def check(data,expected):
  nonlocal checks
  b=ctypes.create_string_buffer(bytes(data));assert lib.parse147(b,len(data))==expected;(checks:=checks+1)
 base=b'0'*48+struct.pack('<8sQ32s',b'ENGMSI81',3,hashlib.sha256(b'abc').digest())+b'abc'
 ext=struct.pack('<8sIIII32s32s',b'ENGMS147',1,2,5,4,hashlib.sha256(b'hello').digest(),hashlib.sha256(b'test').digest())+b'hellotest'
 check(base,1);check(base+ext,2)
 for n in range(len(base+ext)):
  if n!=len(base):check((base+ext)[:n],0)
 for off in [48,56,60,99,107,111,115,119]:
  bad=bytearray(base+ext);bad[off]^=128;check(bad,0)
 ext2=struct.pack('<8sIIIII32s32s32s',b'ENGMS147',2,3,5,4,6,hashlib.sha256(b'hello').digest(),hashlib.sha256(b'test').digest(),hashlib.sha256(b'elf123').digest())+b'hellotestelf123'
 check(base+ext2,3)
 for n in range(len(base+ext2)):
  if n!=len(base):check((base+ext2)[:n],0)
 for off in [107,111,115,119,123]:
  bad=bytearray(base+ext2);bad[off]^=128;check(bad,0)
 check(base+ext2+b'x',0)
 check(base+ext+b'x',0);check(base+ext+b'x'*(4*1024*1024),0)
 assert lib.parse147(None,200)==0;checks+=1
 report=dict(passed=True,checks=checks,scope='Shared production boot-bundle shape parser; content SHA verified separately by the kernel, not a native boot result',sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ['include/engine/winbundle147.h','tests/m14/bundle147_host.c','tests/m14/bundle147_host.py']})
 (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS boot bundle checks',checks)
if __name__=='__main__':main()
