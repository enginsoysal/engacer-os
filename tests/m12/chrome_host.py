"""Run production caption rules and the preserved normal-icon geometry oracle."""
import hashlib,json,subprocess,sys
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
    measures=json.loads(reports['chrome_host']);assert measures['geometry_points']>1000000 and measures['styles']==384 and measures['tinted_pixels']>100000
    paths=['include/engine/ui/chrome12.h','include/engine/ui/components12.h','include/engine/ui/icons12.h','include/engine/ui/icons12_data.h','tests/m12/chrome_host.c','tests/m12/icons_host.c']
    report=dict(passed=True,stage='M12.4',checks=reports,measurements=measures,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},scope='Host geometry/styles/tinted rows and all normal-icon raster geometry; native input/rendering are separately qualified')
    (OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
if __name__=='__main__':main()
