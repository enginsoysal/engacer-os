"""Observe the unmodified installed 7-Zip GUI; missing dependencies remain failures."""
import hashlib,json,os,struct,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];os.environ['ENGACER12_IMAGE']='EngacerOS-M14STAGE4'
sys.path[:0]=[str(ROOT/'tests/m12'),str(ROOT/'tests/m13')]
import taskbar_observe as t
ui=t.ui;c=t.c;f=t.f
from access_fixtures16 import clone
import capture14
capture14.bind(ui)
def main():
 out=ROOT/'build/m14-native/stage4/original-gui-probe';out.mkdir(parents=True,exist_ok=True);c.OUT=out
 base=json.loads((ROOT/'build/m14-native/stage4/apps/results.json').read_text(encoding='utf-8'));assert base['passed']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m144-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m144-original-gui')
 original=ui.s.s.document(disk,'/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',8*1024**2)
 digest=hashlib.sha256(original).hexdigest();assert digest=='a12710799d5cb9b3076b86dd0f92d4a503b7062bc3efac62b7f4cb8a74e05931'
 report=dict(original_gui_qualified=False,stage='M14.4 diagnostic',build_id=base['build_id'],original_sha256=digest,clone=cloned)
 try:
  boot=ui.guest(work/'original',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);before=f.stats(g)[0];at=len(g.log());p.desktop(12100,True,settle=False);g.wait('M8_CPL3_CREATED',at)
   deadline=time.monotonic()+30
   while time.monotonic()<deadline:
    raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384)
    if struct.unpack_from('<I',raw)[0]!=1:break
    time.sleep(.05)
   p.drain();c.shot(g,'original-gui-observation');raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384)
   state,command,status=struct.unpack_from('<3I',raw);report.update(state=state,status=status,message=raw[304:496].split(b'\0')[0].decode(errors='replace'),output=raw[496:].split(b'\0')[0].decode(errors='replace'),native_windows=t.records(g),retained_pages=f.stats(g)[0]-before)
   if state==1:w8cancel=12008;p.desktop(w8cancel,True);g.wait('M8_JOB_FAILED',at)
   (out/'serial.log').write_bytes(g.log().encode())
 except Exception:report['observer_error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
