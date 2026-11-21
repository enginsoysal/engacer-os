"""Native fixed/movable global memory, ownership, quotas and thread cleanup."""
import hashlib,json,os,struct,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
from window144_native import ui,c,f,t,clone,library,StoppedDisk,task,output
from session148_build import build

def main():
 out=ROOT/'build/m14-native/stage8/session-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out;fixture=build();meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage8/apps/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m148-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m148-session-native');mounted=StoppedDisk(disk,library())
 try:
  mounted.put('/System/Windows/runtime8.elf',production.read_bytes())
  mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())
 finally:mounted.close()
 report=dict(passed=False,build_id=meta['build_id'],scope='Native private-worker identity/display/process/message/shell/GDI lifetimes, DC/SRW contention and heap release; not shipped-route acceptance.',clone=cloned,fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest())
 try:
  boot=ui.guest(work/'global',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19);task(g,p,12005);before=f.stats(g)[0];samples=[]
   for cycle in range(3):
    fault=rtc_begin148(g,ui) if cycle==1 else None
    try:text=task(g,p,12100)
    finally:
     if fault:report['rtc_fault_injection']=rtc_end148(g,fault)
    assert 'M148_NATIVE_SESSION_MESSAGES_SRW_PASS' in text,text
    assert len(t.records(g))==1 and t.records(g)[0]['token']==front['token'];assert ui.integer(g,'ui_resident144',True)==1
    retained=f.stats(g)[0]-before;assert retained==(1 if cycle==0 else 0),(cycle,retained);before=f.stats(g)[0];samples.append(dict(cycle=cycle+1,retained_pages=retained,writer_threads=4,reader_threads=4,writer_operations=4000,desktop_dc_rounds=512))
   c.shot(g,'global-memory-lifetimes');value=task(g,p,12005);assert 'Mapped original image: 7z.exe' in value and '7-Zip' in value
   delivered=g.log().count('M148_NATIVE_SHELL_ASSOCIATIONS_REFRESH');assert delivered==3,delivered;report.update(passed=True,cycles=samples,subsequent_original_console_success=True,output=text);report['native_shell_refresh_deliveries']=delivered;(out/'serial.log').write_bytes(g.log().encode())

 except Exception:
  if 'g' in locals():(out/'serial.log').write_bytes(g.log().encode())
  report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
