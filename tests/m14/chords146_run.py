"""Real Ctrl-letter versus special-key input; read-only observation and ordinary keys."""
import hashlib,json,os,struct,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
from window144_native import ui,c,f,t,clone,library,StoppedDisk,task,output
from chords146_build import build
from original_window_trace4 import wait_for

def main():
 out=ROOT/'build/m14-native/stage6/chords-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out;fixture=build();meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage6/apps/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m146-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m146-chords-native');mounted=StoppedDisk(disk,library())
 try:mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())
 finally:mounted.close()
 report=dict(passed=False,build_id=meta['build_id'],scope='Owned ordinary physical Ctrl+C/H/I/J and Ctrl+Backspace/Tab/Enter virtual-key identity and consumed Control state; not universal keyboard qualification',clone=cloned,fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest())
 try:
  boot=ui.guest(work/'chords',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19);task(g,p,12005);before=f.stats(g)[0];at=len(g.log());p.desktop(12100,True,settle=False);g.wait('M8_CPL3_CREATED',at);wait_for(g,lambda:'M146_CHORD_READY'in output(g));c.shot(g,'control-shortcut-window')
   checks=[]
   for key,marker in [('c','C'),('h','H'),('i','I'),('j','J'),('backspace','BACKSPACE'),('tab','TAB'),('ret','ENTER')]:
    c.key(g,'ctrl',key);wait_for(g,lambda:'M146_CHORD_'+marker+'\n'in output(g));checks.append(key)
   g.wait('M8_JOB_DONE',at);p.drain();assert 'M146_CHORD_IDENTITY_PASS'in output(g),output(g)
   assert len(t.records(g))==1 and t.records(g)[0]['token']==front['token'];assert ui.integer(g,'ui_resident144',True)==0
   retained=f.stats(g)[0]-before;assert retained==0,retained
   report.update(passed=True,keys=checks,retained_pages=retained,output=output(g))
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
