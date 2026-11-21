"""Native atomic SLIST flush vs independent inline producers and CPU feature policy."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 import replay7
 loader=replay7.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  source=ROOT/'tests/m14/global146_run.py';raw=source.read_bytes();text=raw.decode();replacements=[('from global146_build import build','from slist147_build import build'),('stage6/global-native','stage7/slist-native'),('stage6/apps','stage7/apps'),('m146-window-apps','m147-window-apps'),('m146-global-native','m147-slist-native'),('M146_GLOBAL_MEMORY_OWNERSHIP_QUOTA_THREADS_PASS','M147_NATIVE_SLIST_ATOMIC_PRODUCERS_CPU_POLICY_PASS'),('concurrent_alloc_free_rounds=200','native_atomic_producer_nodes=256'),('Owned global-memory ABI, handle/LocalAlloc separation, allocation quota and native thread concurrency; not original application qualification','Own native atomic SLIST flush vs four independent inline CPU producers and corrected usable processor features; not original CRT or custom-action qualification')]
  for a,b in replacements:assert text.count(a)==1,(a,text.count(a));text=text.replace(a,b)
  out=ROOT/'build/m14-native/stage7/slist-native';out.mkdir(parents=True,exist_ok=True);(out/'observer.json').write_bytes((json.dumps(dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),replacements=replacements),indent=2)+'\n').encode());namespace={'__file__':str(source),'__name__':'fls147_derived'};exec(compile(text,str(source),'exec'),namespace);namespace['main']()
 finally:
  sys.meta_path.remove(loader);out=ROOT/'build/m14-native/stage7/slist-native';out.mkdir(parents=True,exist_ok=True);(out/'dependencies.json').write_bytes((json.dumps(replay7.observed,indent=2)+'\n').encode())
if __name__=='__main__':main()
