"""Own lazy FLS state/callback checks with simulated current native-thread rows."""
import ctypes as c,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools

def main():
 out=ROOT/'build/m14-native/stage7/fls-host';out.mkdir(parents=True,exist_ok=True);t=pinned_tools()
 command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-I',ROOT/'include','-c',ROOT/'tests/m14/fls147_host.c','-o',out/'fls.obj'])
 command([t['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'fls.dll'),out/'fls.obj']);lib=c.CDLL(str(out/'fls.dll'));live={};state={'fail':False,'peak':0};checks=0
 A=c.CFUNCTYPE(c.c_void_p,c.c_size_t);R=c.CFUNCTYPE(None,c.c_void_p);C=c.CFUNCTYPE(None,c.c_void_p)
 @A
 def allocate(n):
  if state['fail']:return None
  b=c.create_string_buffer(n);address=c.addressof(b);live[address]=b;state['peak']=max(state['peak'],sum(c.sizeof(v)for v in live.values()));return address
 @R
 def release(p):assert p in live;del live[p]
 lib.init147.argtypes=[A,R];lib.init147(allocate,release);lib.allocate_fls147.argtypes=[c.c_uint64];lib.allocate_fls147.restype=c.c_uint;lib.get_fls147.restype=c.c_uint64;lib.set_fls147.argtypes=[c.c_uint,c.c_uint64]
 def check(value):
  nonlocal checks
  assert value;checks+=1
 state['fail']=True;check(lib.allocate_fls147(0)==0xffffffff and lib.error_get147()==8 and not live);state['fail']=False
 for cycle in range(21):
  indices=[lib.allocate_fls147(0)for _ in range(64)];check(indices==list(range(64)));check(lib.allocate_fls147(0)==0xffffffff and lib.error_get147()==259)
  for row in range(16):
   lib.row_set147(row)
   for index in indices:check(lib.get_fls147(index)==0);check(lib.set_fls147(index,(row+1)*1000+index))
  for row in range(16):
   lib.row_set147(row)
   for index in indices:check(lib.get_fls147(index)==(row+1)*1000+index)
   lib.exit_fls147()
   for index in indices:check(lib.get_fls147(index)==0)
  for index in indices:check(lib.free_fls147(index)==1)
  check(not live);check(not lib.free_fls147(0) and lib.error_get147()==87);check(not lib.set_fls147(0,1));check(not lib.get_fls147(0) and lib.error_get147()==87)
  called=[];reentered=[]
  @C
  def callback(value):
   called.append(value);slot=lib.allocate_fls147(0);reentered.append(slot!=0xffffffff and lib.free_fls147(slot)==1)
  index=lib.allocate_fls147(c.cast(callback,c.c_void_p).value)
  for row in range(16):lib.row_set147(row);check(lib.set_fls147(index,row+1))
  check(lib.free_fls147(index)==1);check(called==list(range(1,17)) and all(reentered));check(not live)
  called.clear();index=lib.allocate_fls147(c.cast(callback,c.c_void_p).value)
  for row in range(16):lib.row_set147(row);check(lib.set_fls147(index,row+1));lib.exit_fls147();check(lib.get_fls147(index)==0)
  check(called==list(range(1,17)));check(lib.free_fls147(index)==1 and not live)
 sources=['user/windows8/fls147.inc','tests/m14/fls147_host.c','tests/m14/fls147_host.py'];report=dict(passed=True,checks=checks,cycles=21,peak_host_allocation_bytes=state['peak'],retained_allocations=len(live),scope='Own FLS state and callbacks with simulated rows; not native thread/fiber or original CRT qualification',sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources});(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS own FLS checks',checks)
if __name__=='__main__':main()
