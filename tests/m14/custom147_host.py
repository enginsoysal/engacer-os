"""Own synchronous-action cleanup, authored return policy and injected API failure paths."""
import ctypes as c,hashlib,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
class Result(c.Structure):_fields_=[('invoked',c.c_uint),('body',c.c_uint),('continued',c.c_uint),('engine_error',c.c_uint)]
def library():
 lib=c.CDLL(str(ROOT/'build/m14-native/stage7/custom-host/custom.dll'));lib.invoke147.argtypes=[c.c_uint,c.c_uint,c.c_uint,c.POINTER(Result)];lib.invoke147.restype=c.c_uint;return lib

def main():
 out=ROOT/'build/m14-native/stage7/custom-host';out.mkdir(parents=True,exist_ok=True);t=pinned_tools();command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-I',ROOT/'include','-c',ROOT/'tests/m14/custom147_host.c','-o',out/'custom.obj']);command([t['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'custom.dll'),out/'custom.obj']);lib=library();checks=0
 def check(value):
  nonlocal checks
  assert value;checks+=1
 for kind in [3073,3137]:
  for body in [0,1602,1603,259,1626,0xffffffff]:
   result=Result();status=lib.invoke147(kind,body,0,c.byref(result));ignored=kind==3137 and body!=0;check(status==(0 if ignored else body));check(result.invoked==1 and result.body==body and result.continued==ignored and not result.engine_error);check(lib.stat147(10)==0 and lib.stat147(9)==0);check([lib.stat147(12+i)for i in range(lib.stat147(11))]==list(range(1,11)))
  for failure,error in [(1,126),(2,127),(4,8),(8,8),(16,6),(32,6),(64,6),(256,6),(512,31)]:
   result=Result();check(lib.invoke147(kind,0,failure,c.byref(result))==1603 and result.engine_error==error and not result.continued);check(lib.stat147(10)==0 and lib.stat147(9)==0)
   if failure==1:check(lib.stat147(0)==1 and lib.stat147(1)==0 and lib.stat147(2)==0)
   elif failure==256:check(lib.stat147(0)==0 and lib.stat147(1)==0 and lib.stat147(2)==0)
   else:check(lib.stat147(1)==1)
 for kind in [1,51,3138,3265,0,0xffffffff]:
  result=Result();check(lib.invoke147(kind,0,0,c.byref(result))==50 and result.engine_error==50 and lib.stat147(0)==0)
 p=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--join-failure'],cwd=ROOT,capture_output=True);check(p.returncode==93)
 sources=['user/windows8/msi-custom147.c','user/windows8/msi-custom147.h','user/windows8/msi-plan147.h','tests/m14/custom147_host.c','tests/m14/custom147_host.py'];report=dict(passed=True,scope=__doc__+' Host adapters execute the callback synchronously; real action-thread and original DLL qualification are separate.',checks=checks,original_dll_executed_on_host=False,failed_join_preserves_executable_module=True,sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources});(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS deferred action dispatcher checks',checks)
if __name__=='__main__':
 if '--join-failure'in sys.argv:
  lib=library();hook_type=c.CFUNCTYPE(None,c.c_char_p)
  @hook_type
  def fatal(text):os._exit(93 if lib.stat147(1)==0 and lib.stat147(7)==0 else 94)
  lib.fatal_hook147.argtypes=[hook_type];lib.fatal_hook147(fatal);result=Result();lib.invoke147(3073,0,128,c.byref(result));os._exit(95)
 else:main()
