"""Current production component contrast and focus math in an isolated stage."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools
out=ROOT/'build/m12/stage18/access-host';out.mkdir(parents=True,exist_ok=True);exe=out/'contrast.exe'
subprocess.run([pinned_tools()['clang'],'-std=c17','-O2','-Wall','-Wextra','-Werror','-I','include','tests/m12/components_host.c','-o',str(exe)],cwd=ROOT,check=True,capture_output=True)
result=subprocess.run([str(exe)],cwd=ROOT,check=True,capture_output=True,text=True)
paths=['include/engine/ui/components12.h','include/engine/ui/luminance12.h','tests/m12/components_host.c','tests/m12/final_host18.py']
report=dict(passed=True,scope='Actual production Light/Dark/high-contrast palettes, control states and focus/scroll bounds; disabled text is not asserted as normal enabled text. Native keyboard/pixel/display tests are separate.',checks=[result.stdout.strip()],source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths});(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report),flush=True)
