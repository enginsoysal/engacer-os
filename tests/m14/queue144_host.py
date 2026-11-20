"""Bounded queue contract against an independent Python message sequence."""
import ctypes as c
import hashlib,json,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command
class Message(c.Structure):
 _fields_=[('window',c.c_uint64),('wp',c.c_uint64),('lp',c.c_uint64),('message',c.c_uint32),('time',c.c_uint32),('x',c.c_int32),('y',c.c_int32),('reserved',c.c_uint32*2)]
class Filter(c.Structure):
 _fields_=[('window',c.c_uint64),('first',c.c_uint32),('last',c.c_uint32),('remove',c.c_uint32),('reserved',c.c_uint32)]
def main():
 out=ROOT/'build/m14-native/stage4/queue-host';out.mkdir(parents=True,exist_ok=True)
 tools=pinned_tools();obj=out/'queue.obj';dll=out/'queue.dll'
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-std=c17','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-I',ROOT/'include','-c',ROOT/'tests/m14/queue144_host.c','-o',obj])
 command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(dll),obj])
 lib=c.CDLL(str(dll));lib.push144.argtypes=[c.POINTER(Message),c.c_uint32];lib.peek144.argtypes=[c.POINTER(Filter),c.POINTER(Message)];lib.purge144.argtypes=[c.c_uint64]
 rng=random.Random(144);reference=[];steps=100000;accepted=0;rejected=0
 def same(m):return (m.window,m.message,m.wp,m.lp,m.time,m.x,m.y)
 for turn in range(steps):
  action=rng.randrange(10)
  if action<6:
   m=Message();m.window=rng.randrange(1,5);m.message=rng.choice([0x100,0x101,0x102,0x200,0x10,0x12,0x400]);m.wp=turn;m.lp=rng.getrandbits(64);m.time=turn;m.x=rng.randrange(-32768,32768);m.y=-m.x;native=rng.randrange(2)
   replace=bool(native and reference and m.message==0x200 and reference[-1][1]==0x200 and reference[-1][0]==m.window)
   expected=replace or len(reference)<(64 if native else 56)
   assert bool(lib.push144(c.byref(m),native))==expected,(turn,'admission')
   if expected:
    accepted+=1
    if replace:reference[-1]=same(m)
    else:reference.append(same(m))
   else:rejected+=1
  elif action<9:
   window=rng.choice([0,1,2,3,4,2**64-1]);lo,hi=rng.choice([(0,0),(0x100,0x102),(0x200,0x200),(0x400,0x500)]);remove=rng.randrange(2);f=Filter(window,lo,hi,remove,0);m=Message()
   expected=next((i for i,v in enumerate(reference) if v[1]==0x12 or ((window==0 or (v[0]==0 if window==2**64-1 else window==v[0])) and ((lo==0 and hi==0) or lo<=v[1]<=hi))),None)
   assert bool(lib.peek144(c.byref(f),c.byref(m)))==(expected is not None),(turn,'filter')
   if expected is not None:
    assert same(m)==reference[expected],(turn,'ordering')
    if remove:reference.pop(expected)
  else:
   window=rng.randrange(1,5);lib.purge144(window);reference[:]=[v for v in reference if v[0]!=window]
  assert lib.count144()==len(reference),(turn,'count')
 # Saturating app posts must preserve the native input reserve and old messages.
 lib.reset144();m=Message();m.window=1;m.message=0x100
 for i in range(56):m.wp=i;assert lib.push144(c.byref(m),0)
 assert not lib.push144(c.byref(m),0)
 for i in range(8):m.wp=56+i;assert lib.push144(c.byref(m),1)
 assert not lib.push144(c.byref(m),1)
 for i in range(64):
  result=Message();assert lib.peek144(c.byref(Filter(0,0,0,1,0)),c.byref(result));assert result.wp==i
 assert lib.count144()==0
 report=dict(passed=True,stage='M14.4 development',scope='Host-only bounded queue contract, not native GUI qualification',randomized_steps=steps,accepted=accepted,rejected=rejected,queue_bytes=64*c.sizeof(Message),native_reserve=8,sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ('include/engine/winqueue144.h','include/engine/winui144.h','tests/m14/queue144_host.c','tests/m14/queue144_host.py')})
 (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report))
if __name__=='__main__':main()
