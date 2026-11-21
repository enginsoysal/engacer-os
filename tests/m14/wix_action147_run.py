"""Native pilot of the unchanged original WiX action with a test-only real MSI session owner."""
import hashlib,json,sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 import replay7
 loader=replay7.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  source=ROOT/'tests/m14/global146_run.py';raw=source.read_bytes();text=raw.decode();before="try:mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())"
  after="""try:
  prefix='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/'
  mounted.put(prefix+'7zFM.exe',fixture.read_bytes())
  mounted.put(prefix+'msi.dll',(fixture.parent/'msi147/msi.dll').read_bytes())
  mounted.put(prefix+'wix147.dll',(fixture.parent/'wix147.dll').read_bytes())
  mounted.put(prefix+'quiet-child147.exe',(fixture.parent/'quiet-child147.exe').read_bytes())
  package=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/npp.8.9.9.1.Installer.x64.msi';data=package.read_bytes();assert hashlib.sha256(data).hexdigest()=='e3b0607a092ce2604fbdac027db2c94915995e8e568ebd226f8c5493c2f61a80'
  mounted.put('/Users/Owner/Downloads/'+package.name,data)"""
  replacements=[('from global146_build import build','from wix_action147_build import build'),('stage6/global-native','stage7/wix-action-pilot'),('stage6/apps','stage7/apps'),('m146-window-apps','m147-window-apps'),('m146-global-native','m147-wix-action-pilot'),('range(21)','range(1)'),('M146_GLOBAL_MEMORY_OWNERSHIP_QUOTA_THREADS_PASS','M147_ORIGINAL_WIX_DEFERRED_CHILD_OUTPUT_PASS'),('concurrent_alloc_free_rounds=200',"original_deferred_action_calls=1,peak_native_managed_pages=struct.unpack('<Q',ui.memory(g,ui.symbol('info8',installed=True)[0]+24,8))[0]"),('Owned global-memory ABI, handle/LocalAlloc separation, allocation quota and native thread concurrency; not original application qualification','Original unchanged WiX deferred action and own output child through real MSI services in a test-only session-owner DLL; not authored Notepad++ copy/delete, full installation or unmodified production service qualification'),(before,after),('assert \'M147_ORIGINAL_WIX_DEFERRED_CHILD_OUTPUT_PASS\' in text,text',"assert 'M147_ORIGINAL_WIX_DEFERRED_CHILD_OUTPUT_PASS' in text and 'M147_REAL_WIX_CAPTURED_CHILD_OUTPUT' in text,text"),('except Exception:report[\'error\']=ui.q.clean(traceback.format_exc());raise',"except Exception:\n  report['error']=ui.q.clean(traceback.format_exc());(out/'serial-failed.log').write_bytes(g.log().encode());raise")]
  for a,b in replacements:assert text.count(a)==1,(a,text.count(a));text=text.replace(a,b)
  out=ROOT/'build/m14-native/stage7/wix-action-pilot';out.mkdir(parents=True,exist_ok=True);(out/'observer.json').write_bytes((json.dumps(dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),replacements=replacements),indent=2)+'\n').encode());namespace={'__file__':str(source),'__name__':'wix_action147_derived'};exec(compile(text,str(source),'exec'),namespace);namespace['main']()
 finally:sys.meta_path.remove(loader)
if __name__=='__main__':main()
