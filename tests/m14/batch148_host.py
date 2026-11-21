"""Production bounded batch parser guards; no script or file operations run on the host."""
import ctypes as c,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
def main():
 out=ROOT/'build/m14-native/stage8/batch-host';out.mkdir(parents=True,exist_ok=True);t=pinned_tools();command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-c',ROOT/'tests/m14/batch148_host.c','-o',out/'batch.obj']);command([t['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'batch.dll'),out/'batch.obj']);lib=c.CDLL(str(out/'batch.dll'));lib.segment148.argtypes=[c.c_wchar_p,c.POINTER(c.c_uint),c.c_wchar_p,c.c_void_p,c.c_uint];checks=[]
 def run(line,expected,capacity=512):
  offset=c.c_uint();actual=[]
  while offset.value<len(line):
   buffer=(c.c_ushort*(capacity+16))(*([0x9b9b]*(capacity+16)));result=lib.segment148(line,c.byref(offset),'C:\\Owned tests\\cleanup.bat',buffer,capacity);assert bytes(buffer)[capacity*2:]==b'\x9b' *32
   if result<0:actual.append(result);break
   if not result:break
   actual.append(c.wstring_at(c.addressof(buffer)))
  assert actual==expected,(line,actual,expected);checks.append(line)
 run('timeout /t 2 /nobreak >nul',['timeout /t 2 /nobreak'])
 run('(goto) 2>nul & del "%~f0"',['(goto)','del "C:\\Owned tests\\cleanup.bat"'])
 run('del "C:\\Owned tests\\a&b.exe"',['del "C:\\Owned tests\\a&b.exe"'])
 run('@echo off',['echo off']);run('del "x" & del "y"',['del "x"','del "y"'])
 for line in ['del %PATH%','del %','del %~','del %~f','del "unterminated','del x | del y','del x >file','del x <nul','del x ^& del y']:
  run(line,[-87 if line=='del "unterminated'else -50])
 run('del "%~f0"',[-1816],8)
 sources=['user/windows8/tools147.h','user/windows8/batch148.h','tests/m14/batch148_host.c','tests/m14/batch148_host.py'];report=dict(passed=True,scope=__doc__,checks=checks,sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources});(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS bounded batch parser guards',len(checks))
if __name__=='__main__':main()
