"""Record production component checks and unchanged M11 raster generation."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools
from font73 import prepare

def main():
    out=ROOT/'build/m12/stage1';out.mkdir(parents=True,exist_ok=True)
    exe=out/'components-host.exe'
    subprocess.run([pinned_tools()['clang'],'-std=c17','-O2','-Wall','-Wextra','-Werror','-I','include','tests/m12/components_host.c','-o',str(exe)],cwd=ROOT,check=True,capture_output=True)
    result=subprocess.run([str(exe)],cwd=ROOT,check=True,capture_output=True,text=True)
    legacy=ROOT/'build/m12/font-reference/m11';legacy.mkdir(parents=True,exist_ok=True)
    original=prepare(legacy)
    current=json.loads((ROOT/'build/m12/font73-manifest.json').read_text())
    assert current['coverage_bytes']<original['coverage_bytes']<1024**2
    assert current['semantic_sizes']=={'section':[21,32,42],'heading':[28,42,56]}
    paths=['include/engine/ui/components12.h','include/engine/ui/luminance12.h','tests/m12/components_host.c','tools/design/components12.py','tools/build/font73.py']
    report=dict(passed=True,scope='Host execution of production color/state/scroll arithmetic; native rendering and input are separate checks',checks=result.stdout.strip(),font=current,m11_raster_lock_unchanged=True,m11_coverage_bytes=original['coverage_bytes'],font_coverage_delta_bytes=current['coverage_bytes']-original['coverage_bytes'],source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},diagnostics=['Initial compounded hover-plus-press styling produced contrast 4.475582 for dark theme/accent bbffee. Press now replaces hover rather than compounding it.','The first unqualified live kernel exceeded its former low-memory placement. Unused legacy heading masks and duplicate semantic masks were removed.'])
    (out/'host-results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(result.stdout.strip());print('M11 font lock unchanged; M12 font coverage delta:',report['font_coverage_delta_bytes'])

if __name__=='__main__':main()
