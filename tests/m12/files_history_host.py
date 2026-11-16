"""Host location/history rules; actual filesystem and input checks are separate."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools
OUT=ROOT/'build/m12/stage5/history-host'
def main():
    OUT.mkdir(parents=True,exist_ok=True);exe=OUT/'history.exe'
    subprocess.run([pinned_tools()['clang'],'-std=c17','-O2','-Wall','-Wextra','-Werror','-I','include','tests/m12/files_history_host.c','-o',str(exe)],cwd=ROOT,check=True)
    r=subprocess.run([str(exe)],check=True,capture_output=True,text=True)
    paths=['include/engine/ui/files12.h','tests/m12/files_history_host.c']
    result=dict(passed=True,stage='M12.5',checks=r.stdout.strip(),history_bytes_per_window=2216,history_slots_per_window=8,added_history_bytes_per_window=160,allocations=0,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths})
    (OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
if __name__=='__main__':main()
