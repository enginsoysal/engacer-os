"""Real mouse/keyboard list selection, veto, activation and reentrant replacement."""
import argparse,hashlib,json,os,struct,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
from window144_native import ui,c,f,t,clone,library,StoppedDisk,task,output,wait
from original_window_trace4 import views
from list145_build import build
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--cycles',type=int,default=1);args=parser.parse_args();assert 1<=args.cycles<=21
 out=ROOT/'build/m14-native/stage5/list-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out;fixture=build();meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage5/apps/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m145-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m145-list-native');mounted=StoppedDisk(disk,library())
 try:mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())
 finally:mounted.close()
 report=dict(passed=False,build_id=meta['build_id'],scope='Owned native list fixture; not complete original app navigation qualification',clone=cloned,fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest(),cycles=[])
 try:
  boot=ui.guest(work/'list-input',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19);task(g,p,12005);before=f.stats(g)[0]
   for cycle in range(args.cycles):
    at=len(g.log());p.desktop(12100,True,settle=False);g.wait('M8_CPL3_CREATED',at);wait(g,'M145_LIST_READY');p.drain();root=next(v for v in views(g)if v['class_name']=='List145');child=next(v for v in views(g)if v['class_name']=='SysListView32');scale=c.flag(g,'scale73')/2
    def point(row):
     x,y,_,_=child['bounds'];p.move(int((root['bounds'][0]+1+x+1+40)*scale),int((root['bounds'][1]+40+y+1+28+row*24+12)*scale))
    def click(row):point(row);p.down(True);p.down(False);p.drain()
    click(0);wait(g,'M145_LIST_SELECT_ONLY');assert 'M145_LIST_DOUBLE_ACTIVATE'not in output(g)
    if cycle==0:c.shot(g,'single-click-selects')
    time.sleep(.6);point(0);p.down(True);p.down(False);p.down(True);p.down(False);p.drain();wait(g,'M145_LIST_DOUBLE_ACTIVATE')
    click(1);wait(g,'M145_LIST_VETO_PRESERVED');click(2);c.key(g,'ret');wait(g,'M145_LIST_ENTER_ACTIVATE');c.key(g,'r');wait(g,'M145_LIST_ARMED');click(0);wait(g,'M145_LIST_MUTATED');c.key(g,'v');wait(g,'M145_LIST_REENTRANT_SAFE')
    p.desktop(49002,True);g.wait('M8_JOB_DONE',at);p.drain();state,command,status=struct.unpack('<3I',ui.memory(g,ui.symbol('info8',installed=True)[0],12));assert state==2 and not status and'M145_LIST_LIFETIME_PASS'in output(g),(state,command,status,output(g));retained=f.stats(g)[0]-before;assert retained==0;assert len(t.records(g))==1 and t.records(g)[0]['token']==front['token']
    report['cycles'].append(dict(cycle=cycle+1,single_click_only_selects=True,double_click_activates=True,enter_activates=True,veto_preserves_old_selection=True,equal_sized_callback_replacement_safe=True,retained_pages=retained))
   report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
