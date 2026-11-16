"""Pure native filename ordering and responsive presentation geometry checks."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools
def main():
 out=ROOT/'build/m12/stage6/presentation-host';out.mkdir(parents=True,exist_ok=True);exe=out/'presentation.exe'
 subprocess.run([pinned_tools()['clang'],'-std=c17','-O2','-Wall','-Wextra','-Werror','-I','include','tests/m12/fileview_host.c','-o',str(exe)],cwd=ROOT,check=True)
 run=subprocess.run([str(exe)],check=True,capture_output=True,text=True)
 paths=['include/engine/ui/fileview12.h','tests/m12/fileview_host.c']
 report=dict(passed=True,stage='M12.6',checks=run.stdout.strip(),allocations=0,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths})
 (out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
if __name__=='__main__':main()
