"""Production quoting vs Windows argument parser and owned utility pattern reference."""
import ctypes as c,hashlib,json,random,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools

def main():
 out=ROOT/'build/m14-native/stage7/tools-host';out.mkdir(parents=True,exist_ok=True);t=pinned_tools();command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',ROOT/'tests/m14/tools147_host.c','-o',out/'tools.obj']);command([t['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'tools.dll'),out/'tools.obj']);lib=c.CDLL(str(out/'tools.dll'));U=c.c_uint;P=c.c_void_p;lib.parse147.argtypes=[c.c_wchar_p,U,P,U,P];lib.destination147.argtypes=[c.c_wchar_p,c.c_wchar_p,P,U];shell=c.WinDLL('shell32');shell.CommandLineToArgvW.argtypes=[c.c_wchar_p,P];shell.CommandLineToArgvW.restype=P;kernel=c.WinDLL('kernel32');kernel.LocalFree.argtypes=[P];rng=random.Random(147);checks=0
 def check(value):
  nonlocal checks
  assert value;checks+=1
 vectors=[['tool.exe','a b.xml','nativeLang.xml*','/Y','/Q'],['tool.exe','','trailing\\','quote"inside','a\\\\"b']]
 alphabet='abCD19 \\"\t\u00e9\u03bb\U0001f600'
 for _ in range(2500):vectors.append(['C:\\Program Files\\Tools\\tool.exe']+[''.join(rng.choice(alphabet)for _ in range(rng.randrange(32)))for _ in range(rng.randrange(1,10))])
 for args in vectors:
  line=subprocess.list2cmdline(args);storage=(c.c_ushort*2064)(*([0x9b9b]*2064));offsets=(U*16)();count=lib.parse147(line,0,storage,2048,offsets);check(count==len(args));actual=[c.wstring_at(c.addressof(storage)+2*offsets[i])for i in range(count)];check(actual==args);n=U();raw=shell.CommandLineToArgvW(line,c.byref(n));check(bool(raw))
  try:expected=[c.cast(raw,c.POINTER(c.c_wchar_p))[i]for i in range(n.value)];check(expected==actual)
  finally:kernel.LocalFree(raw)
  check(bytes(storage)[4096:]==b'\x9b'*32)
 for line in ['tool.exe "unterminated','tool.exe '+('x'*2048),' '.join(['tool.exe']+['x']*16)]:
  storage=(c.c_ushort*2064)(*([0x9b9b]*2064));offsets=(U*16)();check(lib.parse147(line,0,storage,2048,offsets)<0 and bytes(storage)[4096:]==b'\x9b'*32)
 for line in ['cmd.exe /C del a & del b','cmd.exe /C del a|del b','cmd.exe /C del %PATH%','cmd.exe /C del "a%PATH%b"','cmd.exe /C del a>out','cmd.exe /C del a^b']:
  storage=(c.c_ushort*2048)();offsets=(U*16)();check(lib.parse147(line,1,storage,2048,offsets)==-50)
 for source,target,expected in [('C:\\Lang\\french.xml','C:\\App\\nativeLang.xml*','C:\\App\\nativeLang.xml'),('source.xml','copy.txt*','copy.txt'),('source.xml','nativeLang.*','nativeLang.xml'),('C:\\a.b\\source.xml','literal.xml','literal.xml')]:
  output=(c.c_ushort*528)(*([0x9b9b]*528));check(lib.destination147(source,target,output,512)==1 and c.wstring_at(c.addressof(output))==expected and bytes(output)[1024:]==b'\x9b'*32)
 for source,target in [('source*.xml','copy.xml'),('source.xml','copy?'),('source.xml','copy*'),('source','copy.*'),('source.xml','bad*\\copy.xml*')]:
  output=(c.c_ushort*528)(*([0x9b9b]*528));check(lib.destination147(source,target,output,512)==0 and bytes(output)[1024:]==b'\x9b'*32)
 reference=json.loads((ROOT/'evidence/M14/7/development/helpers-reference.json').read_text(encoding='utf-8'));check(reference['passed']and reference['owned_fixture_removed']);sources=['user/windows8/tools147.h','tests/m14/tools147_host.c','tests/m14/tools147_host.py'];report=dict(passed=True,scope=__doc__,checks=checks,reference_vectors=len(vectors),sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources});(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS native helper argument/pattern checks',checks)
if __name__=='__main__':main()
