"""Independent exhaustive modifier combinations; host core checks, not native qualification."""
import ctypes as c,json,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command
out=ROOT/'build/m14-native/stage5/keys-host';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-I',ROOT/'include','-c',ROOT/'tests/m14/keys145_host.c','-o',out/'keys.obj'])
command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'keys.dll'),out/'keys.obj'])
lib=c.CDLL(str(out/'keys.dll'));lib.state145.argtypes=[c.c_uint]*5;lib.state145.restype=c.c_uint
lib.queue_size145.restype=c.c_uint
queue_bytes=lib.queue_size145();assert queue_bytes<=4096
checks=0
for raw in range(256):
 collapsed=(1 if raw&0x11 else 0)|(2 if raw&0x22 else 0)|(4 if raw&0x44 else 0)
 for mouse in range(8):
  for caps in range(2):
   flags=collapsed|(mouse<<20)|(caps<<16);expected=raw|((bool(raw&0x22))<<8)|((bool(raw&0x11))<<9)|((bool(raw&0x44))<<10)|(mouse<<11)|(caps<<14)
   assert lib.state145(raw,flags,0x200,0,0)==expected
   assert lib.state145(raw,flags,0x200,0,1)==0
   checks+=2
 assert lib.state145(raw,collapsed,0x100,65,0)&0x8000
 assert not lib.state145(raw,collapsed,0x101,65,0)&0x8000
 checks+=2
result=dict(passed=True,scope='Host core only; not native input qualification',assertions=checks,queue_structure_bytes=queue_bytes,queue_allocation_pages=1,sources={str(p):hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ['include/engine/winkeys145.h','tests/m14/keys145_host.c']})
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
