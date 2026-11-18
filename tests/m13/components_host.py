"""Exhaust production color/state rules independently; never write accepted M12 output."""
import argparse,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--stage',type=int,required=True,choices=range(1,13));stage=parser.parse_args().stage
 assert not (ROOT/f'evidence/M13/{stage}/publication-results.json').exists(),'Accepted evidence is immutable'
 out=ROOT/f'build/m13/stage{stage}';out.mkdir(parents=True,exist_ok=True);exe=out/'components-host.exe'
 subprocess.run([pinned_tools()['clang'],'-std=c17','-O2','-Wall','-Wextra','-Werror','-DENGINE_M13','-I','include','tests/m12/components_host.c','-o',str(exe)],cwd=ROOT,check=True,capture_output=True)
 result=subprocess.run([str(exe)],capture_output=True,text=True)
 (out/'host-results.json').write_text(json.dumps(dict(passed=result.returncode==0,stdout=result.stdout,stderr=result.stderr),indent=2)+'\n',encoding='utf-8')
 print(result.stdout,result.stderr);assert result.returncode==0
if __name__=='__main__':main()
