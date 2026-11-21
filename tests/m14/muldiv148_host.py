"""Production signed scaling versus Windows; supporting reference, not guest proof."""
import ctypes as c,hashlib,itertools,json,random,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 out=ROOT/'build/m14-native/stage8/muldiv-host';out.mkdir(parents=True,exist_ok=True);binary=out/'muldiv148.dll'
 subprocess.run(['clang','-shared','-O2','-Wall','-Wextra','-Werror',str(ROOT/'tests/m14/muldiv148_host.c'),'-o',str(binary)],check=True,cwd=ROOT)
 own=c.CDLL(str(binary)).scale148;reference=c.WinDLL('kernel32').MulDiv
 own.argtypes=reference.argtypes=[c.c_int]*3;own.restype=reference.restype=c.c_int
 values=[-2147483648,-2147483647,-100000,-96,-7,-3,-2,-1,0,1,2,3,7,96,100000,2147483646,2147483647]
 cases=list(itertools.product(values,repeat=3));rng=random.Random(148);cases += [tuple(rng.randrange(-2147483648,2147483648)for _ in range(3))for _ in range(10000)]
 differences=[]
 for args in cases:
  actual=own(*args);expected=reference(*args)
  if actual!=expected:differences.append(dict(args=args,actual=actual,expected=expected))
 report=dict(passed=not differences,scope=__doc__,checks=len(cases),differences=differences,sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ['user/windows8/muldiv148.inc','tests/m14/muldiv148_host.c','tests/m14/muldiv148_host.py']})
 (out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(checks=len(cases),difference_count=len(differences),first=differences[:12]),indent=2));assert not differences
if __name__=='__main__':main()
