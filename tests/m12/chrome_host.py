"""Run production caption rules and the preserved normal-icon geometry oracle."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools
OUT=ROOT/'build/m12/stage4/chrome-host'
def main():
    OUT.mkdir(parents=True,exist_ok=True);reports={}
    for name in ('chrome_host','icons_host'):
        exe=OUT/(name+'.exe')
        subprocess.run([pinned_tools()['clang'],'-std=c17','-O2','-Wall','-Wextra','-Werror','-I','include','tests/m12/'+name+'.c','-o',str(exe)],cwd=ROOT,check=True)
        result=subprocess.run([str(exe)],cwd=ROOT,check=True,capture_output=True,text=True)
        reports[name]=result.stdout.strip()
    report=dict(passed=True,stage='M12.4',checks=reports,scope='Host geometry/styles/tinted rows and all normal-icon raster geometry; native input/rendering are separately qualified')
    (OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
if __name__=='__main__':main()
