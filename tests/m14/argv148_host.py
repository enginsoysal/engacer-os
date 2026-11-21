"""Production shell parser versus Windows; supporting reference, not guest proof."""
import ctypes as c,hashlib,itertools,json,random,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 out=ROOT/'build/m14-native/stage8/argv-host';out.mkdir(parents=True,exist_ok=True)
 binary=out/'argv148.dll';subprocess.run(['clang','-shared','-O2','-Wall','-Wextra','-Werror',str(ROOT/'tests/m14/argv148_host.c'),'-o',str(binary)],check=True,cwd=ROOT)
 dll=c.CDLL(str(binary));own=dll.parse148;reference=c.WinDLL('shell32').CommandLineToArgvW
 own.argtypes=reference.argtypes=[c.c_wchar_p,c.POINTER(c.c_int)];own.restype=reference.restype=c.POINTER(c.c_wchar_p)
 dll.release148.argtypes=[c.c_void_p];free=c.WinDLL('kernel32').LocalFree;free.argtypes=[c.c_void_p];free.restype=c.c_void_p
 values=['a','a b',' a b','\t a',' ','\t','""','"a b" c','"a"b c','abc"de f','p '+r'"C:\Program Files\App" -install','p É 🚀']
 values += ['p '+''.join(chars) for n in range(1,7) for chars in itertools.product('a \\"',repeat=n)]
 rng=random.Random(148);values += [rng.choice(['','p ','"C:\\program files\\p" ',' \t'])+''.join(rng.choice('ab \\"\t')for _ in range(rng.randrange(1,80)))for _ in range(5000)]
 failures=[]
 for text in values:
  x=c.c_int();y=c.c_int();a=own(text,c.byref(x));b=reference(text,c.byref(y))
  try:
   actual=[a[i]for i in range(x.value)] if a else None;expected=[b[i]for i in range(y.value)] if b else None
   if actual!=expected:failures.append(dict(input=text,actual=actual,expected=expected))
  finally:
   if a:dll.release148(a)
   if b:free(b)
 report=dict(passed=not failures,scope=__doc__,checks=len(values),differences=failures,sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ['user/windows8/argv148.inc','tests/m14/argv148_host.c','tests/m14/argv148_host.py']})
 (out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(checks=len(values),difference_count=len(failures),first=failures[:12]),indent=2));assert not failures
if __name__=='__main__':main()
