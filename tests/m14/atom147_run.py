"""Twenty-one native global-atom lifetimes and retained original-console regression."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 import replay7
 loader=replay7.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  source=ROOT/'tests/m14/global146_run.py';raw=source.read_bytes();text=raw.decode();before="try:mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())";after="try:\n  mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())\n  mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/atom-child147.exe',(fixture.parent/'atom-child147.exe').read_bytes())"
  replacements=[('from global146_build import build','from atom147_build import build'),('stage6/global-native','stage7/atom-native'),('stage6/apps','stage7/apps'),('m146-window-apps','m147-window-apps'),('m146-global-native','m147-atom-native'),('M146_GLOBAL_MEMORY_OWNERSHIP_QUOTA_THREADS_PASS','M147_NATIVE_GLOBAL_ATOM_CREATOR_EXIT_REFERENCES_PASS'),('concurrent_alloc_free_rounds=200','creator_exit_reference_checks=1'),('Owned global-memory ABI, handle/LocalAlloc separation, allocation quota and native thread concurrency; not original application qualification','Own global atom parent/child API callers verify shared identity, creator exit, reference release, first-case names, integer atoms and bounded output; no full custom-action installation qualification'),(before,after)]
  for a,b in replacements:assert text.count(a)==1,(a,text.count(a));text=text.replace(a,b)
  out=ROOT/'build/m14-native/stage7/atom-native';out.mkdir(parents=True,exist_ok=True);(out/'observer.json').write_bytes((json.dumps(dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),replacements=replacements),indent=2)+'\n').encode());namespace={'__file__':str(source),'__name__':'atom147_derived'};exec(compile(text,str(source),'exec'),namespace);namespace['main']()
 finally:sys.meta_path.remove(loader)
if __name__=='__main__':main()
