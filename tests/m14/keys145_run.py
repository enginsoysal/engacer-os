"""Real mouse/keyboard list selection, veto, activation and reentrant replacement."""
import argparse,hashlib,json,os,struct,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
from window144_native import ui,c,f,t,clone,library,StoppedDisk,task,output
from original_window_trace4 import views
from keys145_build import build
def wait(g,marker):
 deadline=time.monotonic()+30
 while time.monotonic()<deadline:
  text=output(g)
  if 'M145_KEYS_FAIL'in text:raise AssertionError(text)
  if marker in text:return text
  state,command,status=struct.unpack('<3I',ui.memory(g,ui.symbol('info8',installed=True)[0],12))
  if state==3 or(state==2 and status):raise AssertionError((state,command,status,text))
  time.sleep(.03)
 raise TimeoutError((marker,output(g)))
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--cycles',type=int,default=1);args=parser.parse_args();assert 1<=args.cycles<=21
 out=ROOT/'build/m14-native/stage5/keys-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out;fixture=build();meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage5/apps/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m145-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m145-keys-native');mounted=StoppedDisk(disk,library())
 try:mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())
 finally:mounted.close()
 report=dict(passed=False,build_id=meta['build_id'],scope='Owned native consumed-input state fixture; not general keyboard compatibility',clone=cloned,fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest(),cycles=[])
 try:
  boot=ui.guest(work/'keys-input',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19);task(g,p,12005);before=f.stats(g)[0]
   for cycle in range(args.cycles):
    at=len(g.log());p.desktop(12100,True,settle=False);g.wait('M8_CPL3_CREATED',at);wait(g,'M145_KEYS_READY');p.drain();root=next(v for v in views(g)if v['class_name']=='Keys145');scale=c.flag(g,'scale73')/2
    c.key(g,'a');wait(g,'M145_KEYS_QUEUE_PASS')
    p.move(int((root['bounds'][0]+80)*scale),int((root['bounds'][1]+100)*scale));p.drain()
    g.qmp('send-key',{'keys':[{'type':'qcode','data':'ctrl'}],'hold-time':600});time.sleep(.06);p.down(True);p.down(False)
    wait(g,'M145_KEYS_SNAPSHOT_PASS');wait(g,'M145_KEYS_RELEASE_PASS')
    p.desktop(49002,True);g.wait('M8_JOB_DONE',at);p.drain();state,command,status=struct.unpack('<3I',ui.memory(g,ui.symbol('info8',installed=True)[0],12));assert state==2 and not status and'M145_KEYS_LIFETIME_PASS'in output(g),(state,command,status,output(g));retained=f.stats(g)[0]-before;assert retained==0;assert len(t.records(g))==1 and t.records(g)[0]['token']==front['token']
    report['cycles'].append(dict(cycle=cycle+1,consumed_state=True,no_remove_preserves_state=True,posted_input_cannot_fabricate=True,physical_release_preserves_unconsumed_snapshot=True,cursor_queries_do_not_consume_edges=True,retained_pages=retained))
   report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
