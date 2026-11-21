"""Read-only original Windows condition-mask reference against the shared native encoder."""
import ctypes as C,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
def main():
 out=ROOT/'build/m14-native/stage8/version-reference';out.mkdir(parents=True,exist_ok=True);t=pinned_tools()
 source=ROOT/'tests/m14/version148_host.c';header=ROOT/'user/windows8/version-mask148.h'
 command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-c',source,'-o',out/'reference.obj'])
 command([t['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'reference.dll'),out/'reference.obj'])
 native=C.CDLL(str(out/'reference.dll')).condition148;original=C.WinDLL('kernel32').VerSetConditionMask
 for f in [native,original]:f.argtypes=[C.c_uint64,C.c_uint32,C.c_ubyte];f.restype=C.c_uint64
 cases=[]
 for mask in [0,7,0x123456789abcdef0,0xffffffffffffffff]:
  for type in [0,*[1<<bit for bit in range(32)],3,0xff,0xffffffff]:
   for condition in [*range(9),255]:
    expected=original(mask,type,condition);actual=native(mask,type,condition);assert actual==expected,(mask,type,condition,actual,expected)
    cases.append(dict(mask=mask,type=type,condition=condition,result=expected))
 report=dict(passed=True,scope=__doc__,cases=cases,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,header,Path(__file__)]})
 (out/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,cases=len(cases))))
if __name__=='__main__':main()
