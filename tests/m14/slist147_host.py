"""Own atomic flush vs public host list producers; no original app execution."""
import concurrent.futures,ctypes as c,hashlib,json,random,sys,threading
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools

def main():
 out=ROOT/'build/m14-native/stage7/slist-host';out.mkdir(parents=True,exist_ok=True);t=pinned_tools()
 command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-I',ROOT/'include','-c',ROOT/'tests/m14/slist147_host.c','-o',out/'slist.obj'])
 command([t['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'slist.dll'),out/'slist.obj']);lib=c.CDLL(str(out/'slist.dll'));lib.initialize147.argtypes=[c.c_void_p];lib.flush147.argtypes=[c.c_void_p];lib.flush147.restype=c.c_void_p;lib.feature147.argtypes=[c.c_uint]*4
 native=c.WinDLL('kernel32',use_last_error=True);native.InterlockedPushEntrySList.argtypes=[c.c_void_p,c.c_void_p];native.InterlockedPushEntrySList.restype=c.c_void_p;native.QueryDepthSList.argtypes=[c.c_void_p];native.QueryDepthSList.restype=c.c_ushort;checks=0
 def check(value):
  nonlocal checks
  assert value;checks+=1
 def aligned(n):
  buf=c.create_string_buffer(n+16);return buf,(c.addressof(buf)+15)&~15
 storage,head=aligned(16);nodes,base=aligned(4096*16)
 def chain(first,seen):
  count=0
  while first:
   check(base<=first<base+4096*16 and (first-base)%16==0 and first not in seen);seen.add(first);count+=1;check(count<=4096);first=c.c_void_p.from_address(first).value
  return count
 for count in [0,1,2,63,128,1024,4096]:
  lib.initialize147(head);check(c.string_at(head,16)==b'\0'*16)
  for i in range(count):native.InterlockedPushEntrySList(head,base+i*16)
  check(native.QueryDepthSList(head)==count);first=lib.flush147(head);seen=set();check(chain(first,seen)==count);check(native.QueryDepthSList(head)==0 and not lib.flush147(head));check(not count or first==base+(count-1)*16)
 # Independent Windows producers contend with the own 128-bit atomic flush.
 for turn in range(10):
  lib.initialize147(head);start=threading.Barrier(5);done=[False]*4
  def produce(worker):
   start.wait()
   for i in range(1024):native.InterlockedPushEntrySList(head,base+(worker*1024+i)*16)
   done[worker]=True
  seen=set()
  with concurrent.futures.ThreadPoolExecutor(4)as executor:
   jobs=[executor.submit(produce,i)for i in range(4)];start.wait()
   while not all(done):chain(lib.flush147(head),seen)
   for job in jobs:job.result()
  chain(lib.flush147(head),seen);check(len(seen)==4096 and native.QueryDepthSList(head)==0)
 rng=random.Random(147);bits={2:('d',8),3:('d',23),6:('d',25),8:('d',4),10:('d',26),12:('e',20),13:('c',0),14:('c',13),36:('c',9),37:('c',19),38:('c',20)}
 for _ in range(1000):
  values={name:rng.getrandbits(32)for name in ['c','d','e']}
  for feature in range(80):
   expected=1 if feature==9 else int(bool(values[bits[feature][0]]&(1<<bits[feature][1])))if feature in bits else 0
   check(lib.feature147(feature,values['c'],values['d'],values['e'])==expected)
 sources=['user/windows8/slist147.inc','user/windows8/processor147.h','tests/m14/slist147_host.c','tests/m14/slist147_host.py'];report=dict(passed=True,checks=checks,concurrent_rounds=10,nodes_per_round=4096,scope='Own atomic flush with independent public Windows API producers and pure feature-policy checks; not native Engacer or original CRT qualification',sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources});(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS atomic SLIST and feature checks',checks)
if __name__=='__main__':main()
