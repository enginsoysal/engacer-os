"""Host-only deterministic allocation/metadata checks on production mapping code."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools

def main():
 out=ROOT/'build/m14-native/stage6/mapping-host';out.mkdir(parents=True,exist_ok=True);exe=out/'mapping.exe';subprocess.run([pinned_tools()['clang'],'-std=c17','-O2','-Wall','-Wextra','-Werror','-Wno-unused-function','-Iinclude','tests/m14/mapping146_host.c','-o',str(exe)],cwd=ROOT,check=True);result=json.loads(subprocess.check_output([str(exe)],cwd=ROOT));assert result['passed'];result['source_sha256']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ['include/engine/winmap146.h','kernel/windows8/mapping146.inc','tests/m14/mapping146_host.c','tests/m14/mapping146_host.py']};(out/'results.json').write_bytes((json.dumps(result,indent=2)+'\n').encode());print(json.dumps(result,indent=2))
if __name__=='__main__':main()
