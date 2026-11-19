"""Compile and execute the production DLL lifetime dispatcher with owned callbacks."""
import ctypes,hashlib,json,os,sys,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command
work=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Build/m14/lifetime2'/uuid.uuid4().hex
work.mkdir(parents=True)
tools=pinned_tools()
command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-ffreestanding','-fno-builtin','-ffunction-sections','-fdata-sections','-I',ROOT/'include','-I',ROOT/'user/windows8','-c',ROOT/'tests/m14/lifetime2.c','-o',work/'test.obj'])
command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/opt:ref','/out:'+str(work/'test.dll'),work/'test.obj'])
module=ctypes.CDLL(str(work/'test.dll'));module.test_lifetime.restype=ctypes.c_uint
status=module.test_lifetime()
report=dict(passed=status==0,result=status,scope='Host production-dispatcher check only; not CPL3/native Windows acceptance',checks=['reverse attachment order','non-null process-termination reserved argument','no callback for EXE','no duplicate callback for detached DLL','no callback for no-entry DLL','recursive cleanup guard','idempotent cleanup','mappings retained throughout notifications'],source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['user/windows8/lifetime142.inc','user/windows8/module142.h','tests/m14/lifetime2.c']})
out=ROOT/'evidence/M14/2/development/lifetime-host.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report));assert status==0
