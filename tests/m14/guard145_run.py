"""Native unavailable-import containment and honest optional discovery."""
import hashlib,json,os,struct,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
from window144_native import ui,c,f,t,clone,library,StoppedDisk,task,output
from guard145_build import build
from refusal145_decode import decode

def main():
 out=ROOT/'build/m14-native/stage5/guard-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out;fixture=build();meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage5/apps/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m145-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m145-guard-native');mounted=StoppedDisk(disk,library())
 try:mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())
 finally:mounted.close()
 report=dict(passed=False,build_id=meta['build_id'],scope='Owned unavailable-import containment only; no original application compatibility proof',clone=cloned,fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest())
 try:
  boot=ui.guest(work/'guard',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19);task(g,p,12005);before=f.stats(g)[0];at=len(g.log());p.desktop(12100,True);g.wait('M8_CPL3_CREATED',at);g.wait('M8_JOB_FAILED',at);p.drain();text=output(g);state,command,status=struct.unpack('<3I',ui.memory(g,ui.symbol('info8',installed=True)[0],12));assert state==3 and status and'M145_GUARD_DISCOVERY_PASS'in text and'Unavailable Win32 API caller='in text,(state,status,text)
   trace=decode(fixture,text);assert trace and trace['resolved']and trace['dll']=='shlwapi.dll'and trace['symbol']=='PathIsRelativeW',trace
   assert len(t.records(g))==1 and t.records(g)[0]['token']==front['token'];assert ui.integer(g,'ui_resident144',True)==0;retained=f.stats(g)[0]-before;assert retained==0,retained;c.shot(g,'explicit-unavailable-import');value=task(g,p,12005);assert'Mapped original image: 7z.exe'in value and'7-Zip'in value
   report.update(passed=True,optional_discovery_returns_null=True,static_call_refused=True,retained_pages=retained,subsequent_original_console_success=True,call_site=trace,refusal_output=text);(out/'serial.log').write_bytes(g.log().encode())
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
