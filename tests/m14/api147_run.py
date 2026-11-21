"""Native exported MSI API probe in a private clone on the frozen service candidate."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 import replay7
 loader=replay7.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  source=ROOT/'tests/m14/global146_run.py';raw=source.read_bytes();text=raw.decode();before="try:mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())";after="try:\n  mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())\n  mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/msi.dll',(fixture.parent/'msi147/msi.dll').read_bytes())"
  replacements=[('from global146_build import build','from api147_build import build'),('stage6/global-native','stage7/api-native'),('stage6/apps','stage7/apps'),('m146-window-apps','m147-window-apps'),('m146-global-native','m147-api-native'),('M146_GLOBAL_MEMORY_OWNERSHIP_QUOTA_THREADS_PASS','M147_NATIVE_MSI_EXPORT_RECORD_UNICODE_THREADS_PASS'),('concurrent_alloc_free_rounds=200','native_record_thread_rounds=400'),('Owned global-memory ABI, handle/LocalAlloc separation, allocation quota and native thread concurrency; not original application qualification','Production exported MSI record/Unicode APIs, DLL lifetime and native threads on frozen stage7 OS; not original WiX or MSI installation qualification'),(before,after)]
  for a,b in replacements:assert text.count(a)==1,(a,text.count(a));text=text.replace(a,b)
  out=ROOT/'build/m14-native/stage7/api-native';out.mkdir(parents=True,exist_ok=True);(out/'observer.json').write_bytes((json.dumps(dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),replacements=replacements),indent=2)+'\n').encode());namespace={'__file__':str(source),'__name__':'api147_derived'};exec(compile(text,str(source),'exec'),namespace);namespace['main']()
 finally:
  sys.meta_path.remove(loader);out=ROOT/'build/m14-native/stage7/api-native';out.mkdir(parents=True,exist_ok=True);(out/'dependencies.json').write_bytes((json.dumps(replay7.observed,indent=2)+'\n').encode())
if __name__=='__main__':main()
