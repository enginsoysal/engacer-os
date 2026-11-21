"""Original WiX native DLL admission investigation in a private clone on the frozen service candidate."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 import replay7
 loader=replay7.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  source=ROOT/'tests/m14/global146_run.py';raw=source.read_bytes();text=raw.decode();before="try:mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())";after="try:\n  mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())\n  mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/msi.dll',(fixture.parent/'msi147/msi.dll').read_bytes())\n  mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/wix147.dll',(fixture.parent/'wix147.dll').read_bytes())"
  replacements=[('from global146_build import build','from wix147_build import build'),('stage6/global-native','stage7/wix-native'),('stage6/apps','stage7/apps'),('m146-window-apps','m147-window-apps'),('m146-global-native','m147-wix-native'),('M146_GLOBAL_MEMORY_OWNERSHIP_QUOTA_THREADS_PASS','M147_ORIGINAL_WIX_NATIVE_LOAD_EXPORT_UNLOAD_PASS'),('concurrent_alloc_free_rounds=200','native_original_dll_load_unload=1,peak_native_managed_pages=struct.unpack('<Q',ui.memory(g,ui.symbol('info8',installed=True)[0]+24,8))[0]'),('Owned global-memory ABI, handle/LocalAlloc separation, allocation quota and native thread concurrency; not original application qualification','Original unchanged WiX native DLL load/export/unload only; not custom-action execution or MSI installation qualification'),(before,after)]
  for a,b in replacements:assert text.count(a)==1,(a,text.count(a));text=text.replace(a,b)
  out=ROOT/'build/m14-native/stage7/wix-native';out.mkdir(parents=True,exist_ok=True);(out/'observer.json').write_bytes((json.dumps(dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),replacements=replacements),indent=2)+'\n').encode());namespace={'__file__':str(source),'__name__':'wix147_derived'};exec(compile(text,str(source),'exec'),namespace);namespace['main']()
 finally:
  sys.meta_path.remove(loader);out=ROOT/'build/m14-native/stage7/wix-native';out.mkdir(parents=True,exist_ok=True);(out/'dependencies.json').write_bytes((json.dumps(replay7.observed,indent=2)+'\n').encode())
if __name__=='__main__':main()
