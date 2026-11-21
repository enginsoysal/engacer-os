"""Native pipe streaming, inherited grants and repeated complete group cleanup."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 import replay7
 loader=replay7.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  source=ROOT/'tests/m14/global146_run.py';raw=source.read_bytes();text=raw.decode();before="try:mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())";after="try:\n  mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())\n  mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/child147.exe',fixture.read_bytes())"
  replacements=[('from global146_build import build','from pipe147_build import probe as build'),('stage6/global-native','stage7/pipe-native'),('stage6/apps','stage7/apps'),('m146-window-apps','m147-window-apps'),('m146-global-native','m147-pipe-native'),('M146_GLOBAL_MEMORY_OWNERSHIP_QUOTA_THREADS_PASS','M147_NATIVE_PIPE_INHERITED_1M_SHA_EOF_QUOTA_PASS'),('concurrent_alloc_free_rounds=200','transferred_bytes=1048576'),('Owned global-memory ABI, handle/LocalAlloc separation, allocation quota and native thread concurrency; not original application qualification','Own callers of production native pipes: 1 MiB child stream/hash, duplication, inherited stderr EOF, quotas and ordinary privilege refusal; not original WiX or MSI installation qualification'),(before,after),("retained=f.stats(g)[0]-before;assert retained==0,(cycle,retained);", "retained=f.stats(g)[0]-before;assert retained==0,(cycle,retained);assert ui.integer(g,'pipe_resident147',True)==0;assert int.from_bytes(ui.memory(g,ui.symbol('pipe_waits147',8,True)[0],8),'little')>0;")]
  for a,b in replacements:assert text.count(a)==1,(a,text.count(a));text=text.replace(a,b)
  out=ROOT/'build/m14-native/stage7/pipe-native';out.mkdir(parents=True,exist_ok=True);(out/'observer.json').write_bytes((json.dumps(dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),replacements=replacements),indent=2)+'\n').encode());namespace={'__file__':str(source),'__name__':'pipe147_derived'};exec(compile(text,str(source),'exec'),namespace);namespace['main']()
 finally:
  sys.meta_path.remove(loader);out=ROOT/'build/m14-native/stage7/pipe-native';out.mkdir(parents=True,exist_ok=True);(out/'dependencies.json').write_bytes((json.dumps(replay7.observed,indent=2)+'\n').encode())
if __name__=='__main__':main()
