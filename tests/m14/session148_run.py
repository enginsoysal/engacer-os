"""Native private-worker identity/display/process/message/shell/GDI lifetimes, DC/SRW contention and heap release; not shipped-route acceptance."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 from rtc148_observer import begin as rtc_begin148,end as rtc_end148
 from exe148_probe_build import build
 private,inputs=build();production=private.parent/'WINDOWS8.ELF'
 import replay8
 loader=replay8.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  source=ROOT/'tests/m14/global146_run.py';raw=source.read_bytes();text=raw.decode()
  replacements=[('from global146_build import build','from session148_build import build'),('stage6/global-native','stage8/session-native'),('stage6/apps','stage8/apps'),('m146-window-apps','m148-window-apps'),('m146-global-native','m148-session-native'),('M146_GLOBAL_MEMORY_OWNERSHIP_QUOTA_THREADS_PASS','M148_NATIVE_SESSION_MESSAGES_SRW_PASS'),('range(21)','range(3)'),('assert ui.integer(g,\'ui_resident144\',True)==0','assert ui.integer(g,\'ui_resident144\',True)==1'),('assert retained==0,(cycle,retained)','assert retained==(1 if cycle==0 else 0),(cycle,retained);before=f.stats(g)[0]'),('concurrent_alloc_free_rounds=200','writer_threads=4,reader_threads=4,writer_operations=4000,desktop_dc_rounds=512'),('Owned global-memory ABI, handle/LocalAlloc separation, allocation quota and native thread concurrency; not original application qualification',__doc__)]
  for before,after in replacements:assert text.count(before)==1,(before,text.count(before));text=text.replace(before,after)
  needle="try:mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())"
  assert text.count(needle)==1
  text=text.replace(needle,"try:\n  mounted.put('/System/Windows/runtime8.elf',production.read_bytes())\n  mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())")
  fault_call='    text=task(g,p,12100);'
  assert text.count(fault_call)==1
  text=text.replace(fault_call,"    fault=rtc_begin148(g,ui) if cycle==1 else None\n    try:text=task(g,p,12100)\n    finally:\n     if fault:report['rtc_fault_injection']=rtc_end148(g,fault)\n    ")
  marker="report.update(passed=True,cycles=samples,subsequent_original_console_success=True,output=text);"
  assert text.count(marker)==1
  text=text.replace(marker,"delivered=g.log().count('M148_NATIVE_SHELL_ASSOCIATIONS_REFRESH');assert delivered==3,delivered;"+marker+"report['native_shell_refresh_deliveries']=delivered;")
  failure="except Exception:report['error']=ui.q.clean(traceback.format_exc());raise"
  assert text.count(failure)==1
  text=text.replace(failure,"except Exception:\n  if 'g' in locals():(out/'serial.log').write_bytes(g.log().encode())\n  report['error']=ui.q.clean(traceback.format_exc());raise")
  out=ROOT/'build/m14-native/stage8/session-native';out.mkdir(parents=True,exist_ok=True)
  executed=out/'executed-observer.py';executed.write_bytes(text.encode())
  (out/'observer.json').write_bytes((json.dumps(dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),replacements=replacements,runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),rtc_observer_sha256=hashlib.sha256((ROOT/'tests/m14/rtc148_observer.py').read_bytes()).hexdigest(),production_worker_inputs=inputs,production_worker_sha256=hashlib.sha256(production.read_bytes()).hexdigest()),indent=2)+'\n').encode())
  namespace=dict(__file__=str(source),__name__='session148_derived',production=production,rtc_begin148=rtc_begin148,rtc_end148=rtc_end148);exec(compile(text,str(executed),'exec'),namespace)
  original_clone=namespace['clone'];owned=[]
  def capture_clone(*args,**kwargs):
   result=original_clone(*args,**kwargs);owned.append(result[1]);return result
  namespace['clone']=capture_clone;namespace['main']();assert len(owned)==1
  report=json.loads((out/'results.json').read_text())
  try:
   from shell148_readback import validate
   report['windows_native_link_readback']=validate(owned[0],namespace['StoppedDisk'],namespace['library'],out)
  except BaseException:
   import traceback
   report['passed']=False;report['windows_link_readback_error']=namespace['ui'].q.clean(traceback.format_exc());raise
  finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
 finally:sys.meta_path.remove(loader)
if __name__=='__main__':main()
