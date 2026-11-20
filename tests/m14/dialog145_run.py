"""Native original-style dialog callbacks, input, owner safety and resource cleanup."""
import argparse,hashlib,json,os,struct,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
from window144_native import ui,c,f,t,clone,library,StoppedDisk,task,output,drag
from original_window_trace4 import views
from dialog145_build import build

def until(g,predicate,seconds=25):
 deadline=time.monotonic()+seconds
 while time.monotonic()<deadline:
  text=output(g)
  if 'M145_DIALOG_FAIL'in text:raise AssertionError(text)
  state,command,status=struct.unpack('<3I',ui.memory(g,ui.symbol('info8',installed=True)[0],12))
  if state==3 or(state==2 and status):raise AssertionError((state,command,status,text))
  result=predicate()
  if result:return result
  time.sleep(.03)
 raise TimeoutError((output(g),views(g)))

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--cycles',type=int,default=21);args=parser.parse_args();assert 1<=args.cycles<=21
 out=ROOT/'build/m14-native/stage5/dialog-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out;fixture=build();meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage5/apps/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m145-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m145-dialog-native');mounted=StoppedDisk(disk,library());folder='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/'
 try:mounted.put(folder+'7zFM.exe',(fixture/'dialog.exe').read_bytes());mounted.put(folder+'dialogs145.dll',(fixture/'dialogs145.dll').read_bytes())
 finally:mounted.close()
 report=dict(passed=False,stage='M14.5',build_id=meta['build_id'],scope='Owned modal callback/template/input/rollback fixture, not original app task acceptance',clone=cloned,fixture_sha256=hashlib.sha256((fixture/'dialog.exe').read_bytes()).hexdigest(),cycles=[])
 try:
  boot=ui.guest(work/'modal',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19);task(g,p,12005);before=f.stats(g)[0]
   for cycle in range(args.cycles):
    at=len(g.log());p.desktop(12100,True,settle=False);g.wait('M8_CPL3_CREATED',at);until(g,lambda:'M145_DIALOG_READY'in output(g));p.drain();root=next(v for v in views(g)if v['class_name']=='NativeModal145');assert root['enabled']and len(t.records(g))==2
    c.key(g,'a');modal=until(g,lambda:next((v for v in views(g)if v['class_name']=='#32770'and v['visible']),None));p.drain();assert not next(v for v in views(g)if v['handle']==root['handle'])['enabled']
    scale=c.flag(g,'scale73')/2
    if cycle==0:
     # A fixed modal has neither interactive resizing nor minimize/maximize boxes.
     mx,my,mw,mh=modal['bounds'];original_bounds=list(modal['bounds'])
     drag(g,p,mx+mw-4,my+mh-4,mx+mw+20,my+mh+14)
     assert next(v for v in views(g)if v['handle']==modal['handle'])['bounds']==original_bounds
     for offset in (114,70):
      p.move(int((mx+mw-offset)*scale),int((my+20)*scale));p.down(True);p.down(False);p.drain()
      current=next(v for v in views(g)if v['handle']==modal['handle'])
      assert current['visible']and not(current['style']&0x21000000)and current['bounds']==original_bounds
     report['fixed_dialog_resize_refused']=True;report['absent_caption_actions_refused']=True
    # The disabled owner's exposed close button cannot close it or steal focus.
    x,y,w,h=root['bounds'];p.move(int((x+w-24)*scale),int((y+20)*scale));p.down(True);p.down(False);p.drain();assert any(v['handle']==modal['handle']and v['visible']for v in views(g))
    c.key(g,'x');until(g,lambda:any(v['parent']==modal['handle']and v['class_name']=='Edit'and v['title'].startswith('xEditable')for v in views(g)))
    if cycle==0:c.shot(g,'standard-dialog-native-input')
    button=next(v for v in views(g)if v['parent']==modal['handle']and v['class_name']=='Button'and v['title']=='OK');bx,by,bw,bh=button['bounds'];mx,my,_,_=modal['bounds'];p.move(int((mx+1+bx+bw//2)*scale),int((my+40+by+bh//2)*scale));p.down(True);p.down(False);p.drain()
    until(g,lambda:'M145_STANDARD_DIALOG_PASS'in output(g));assert next(v for v in views(g)if v['handle']==root['handle'])['enabled']
    c.key(g,'b');until(g,lambda:any(v['class_name']=='#32770'and v['visible']for v in views(g)));p.drain()
    if cycle==0:c.shot(g,'extended-dialog-cancel')
    c.key(g,'esc');until(g,lambda:'M145_EXTENDED_DIALOG_PASS'in output(g));p.drain();assert next(v for v in views(g)if v['handle']==root['handle'])['enabled']
    p.desktop(49002,True);g.wait('M8_JOB_DONE',at);p.drain();state,command,status=struct.unpack('<3I',ui.memory(g,ui.symbol('info8',installed=True)[0],12));assert state==2 and status==0 and'M145_DIALOG_LIFETIME_PASS'in output(g),(state,command,status,output(g));retained=f.stats(g)[0]-before;assert retained==0,(cycle,retained)
    assert len(t.records(g))==1 and t.records(g)[0]['token']==front['token'];report['cycles'].append(dict(cycle=cycle+1,standard_pointer_accept=True,extended_keyboard_cancel=True,disabled_owner_close_refused=True,partial_creation_rollback=True,malformed_and_template_quota_refused=True,initialization_time_end=True,retained_pages=retained,exit_status=status))
   report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
