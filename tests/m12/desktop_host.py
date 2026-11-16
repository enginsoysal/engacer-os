"""Independent layout/neighbor qualification; native behavior is tested separately."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/build'))
from m2 import pinned_tools
OUT=ROOT/'build/m12/stage3';OUT.mkdir(parents=True,exist_ok=True)
exe=OUT/'desktop-host.exe'
subprocess.run([pinned_tools()['clang'],'-std=c17','-O2','-Wall','-Wextra','-Werror','-I','include','tests/m12/desktop_host.c','-o',str(exe)],cwd=ROOT,check=True)
result=subprocess.run([str(exe)],cwd=ROOT,capture_output=True,text=True,check=True)
report=dict(passed=True,stage='M12.3',checks=result.stdout.strip(),source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ('include/engine/ui/desktop12.h','tests/m12/desktop_host.c')})
(OUT/'host-results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(result.stdout.strip())
