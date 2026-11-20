"""Supporting host allocation-failure checks; native ABI tests remain mandatory."""
import ctypes,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command

def main():
 out=ROOT/'build/m14-native/stage6/global-host';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',ROOT/'tests/m14/global146_host.c','-o',out/'global.obj'])
 command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'global.dll'),out/'global.obj'])
 lib=ctypes.CDLL(str(out/'global.dll'));lib.verify146.restype=ctypes.c_int;result=lib.verify146();assert result==0,result
 report=dict(passed=True,scope='Supporting host core with deterministic metadata/payload allocation failure; not real native allocator, thread or Windows application qualification',checks=15,sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ['user/windows8/global-memory146.inc','tests/m14/global146_host.c','tests/m14/global146_host.py']})
 (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS host global-memory allocation rollback and stale handles')

if __name__=='__main__':main()
