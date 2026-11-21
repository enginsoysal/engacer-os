"""Production shell path operation vs native Windows strings, no vendor app execution."""
import ctypes as c,hashlib,itertools,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 out=ROOT/'build/m14-native/stage8/pathappend-host';out.mkdir(parents=True,exist_ok=True)
 source=ROOT/'tests/m14/pathappend148_host.c';binary=out/'pathappend148.dll'
 subprocess.run(['clang','-shared','-O2','-Wall','-Wextra','-Werror',str(source),'-o',str(binary)],check=True,cwd=ROOT)
 own=c.CDLL(str(binary)).append148;reference=c.WinDLL('shlwapi').PathAppendW
 own.argtypes=reference.argtypes=[c.c_wchar_p,c.c_wchar_p]
 bases=['','a','a\\','C:','C:\\','C:\\Windows\\System32','a\\b','..\\a','.\\a','a\\..\\x','\\\\s\\share','É\\🚀']
 suffixes=['','b','\\b','\\\\server\\share','D:\\b','D:b','..\\b','.','..','b/../c','b\\..\\..\\c','b.','b..','b.\\c','b \\c','b\\','a\\\\b','É\\🚀']
 pairs=list(itertools.product(bases,suffixes))+[('a'*n,'b'*m)for n in [0,1,250,257,258,259,260]for m in [0,1,2,8,259,260]]
 differences=[]
 for base,more in pairs:
  actual=c.create_unicode_buffer(base,1024);expected=c.create_unicode_buffer(base,1024)
  units=c.cast(actual,c.POINTER(c.c_uint16));guard=max(260,len(base.encode('utf-16-le'))//2+1)
  for i in range(guard,1024):units[i]=0x9b9b
  a=bool(own(actual,more));b=bool(reference(expected,more))
  assert all(units[i]==0x9b9b for i in range(guard,1024)),('Out-of-bounds write',base,more)
  if a!=b or actual.value!=expected.value:differences.append(dict(base=base,more=more,actual=[a,actual.value],expected=[b,expected.value]))
 report=dict(passed=not differences,scope=__doc__,checks=len(pairs),differences=differences,sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ['user/windows8/pathappend148.inc','tests/m14/pathappend148_host.c','tests/m14/pathappend148_host.py']})
 (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(dict(checks=len(pairs),differences=differences),indent=2));assert not differences
if __name__=='__main__':main()
