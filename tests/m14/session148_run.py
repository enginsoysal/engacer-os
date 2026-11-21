"""Native private-worker process/message/shell/GDI lifetimes, SRW contention and heap release; not shipped-route acceptance."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 from exe148_probe_build import build
 private,inputs=build();production=private.parent/'WINDOWS8.ELF'
 import replay8
 loader=replay8.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  source=ROOT/'tests/m14/global146_run.py';raw=source.read_bytes();text=raw.decode()
  replacements=[('from global146_build import build','from session148_build import build'),('stage6/global-native','stage8/session-native'),('stage6/apps','stage8/apps'),('m146-window-apps','m148-window-apps'),('m146-global-native','m148-session-native'),('M146_GLOBAL_MEMORY_OWNERSHIP_QUOTA_THREADS_PASS','M148_NATIVE_SESSION_MESSAGES_SRW_PASS'),('range(21)','range(3)'),('assert ui.integer(g,\'ui_resident144\',True)==0','assert ui.integer(g,\'ui_resident144\',True)==1'),('assert retained==0,(cycle,retained)','assert retained==(1 if cycle==0 else 0),(cycle,retained);before=f.stats(g)[0]'),('concurrent_alloc_free_rounds=200','writer_threads=4,reader_threads=4,writer_operations=4000'),('Owned global-memory ABI, handle/LocalAlloc separation, allocation quota and native thread concurrency; not original application qualification',__doc__)]
  for before,after in replacements:assert text.count(before)==1,(before,text.count(before));text=text.replace(before,after)
  needle="try:mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())"
  assert text.count(needle)==1
  text=text.replace(needle,"try:\n  mounted.put('/System/Windows/runtime8.elf',production.read_bytes())\n  mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())")
  out=ROOT/'build/m14-native/stage8/session-native';out.mkdir(parents=True,exist_ok=True)
  (out/'observer.json').write_bytes((json.dumps(dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),replacements=replacements,production_worker_inputs=inputs,production_worker_sha256=hashlib.sha256(production.read_bytes()).hexdigest()),indent=2)+'\n').encode())
  namespace=dict(__file__=str(source),__name__='session148_derived',production=production);exec(compile(text,str(source),'exec'),namespace);namespace['main']()
 finally:sys.meta_path.remove(loader)
if __name__=='__main__':main()
