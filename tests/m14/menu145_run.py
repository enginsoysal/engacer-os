"""Ordinary native menu input, original-style callbacks and retained-page oracle."""
import argparse,hashlib,json,os,struct,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
from window144_native import ui,c,f,t,clone,library,StoppedDisk,task,output,wait
from original_window_trace4 import views,wait_for
from menu145_build import build
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--cycles',type=int,default=1);args=parser.parse_args();assert 1<=args.cycles<=21
 out=ROOT/'build/m14-native/stage5/menu145-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out;fixture=build();meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage5/apps/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m145-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m145-menu-native');mounted=StoppedDisk(disk,library())
 try:mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())
 finally:mounted.close()
 report=dict(passed=False,build_id=meta['build_id'],scope='Owned native menu fixture, not original application qualification',clone=cloned,fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest(),cycles=[])
 try:
  boot=ui.guest(work/'menus',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19);task(g,p,12005);before=f.stats(g)[0]
   for cycle in range(args.cycles):
    at=len(g.log());p.desktop(12100,True,settle=False);g.wait('M8_CPL3_CREATED',at);wait(g,'M145_MENU_READY');p.drain();root=next(v for v in views(g)if v['class_name']=='Menu145');assert root['menu_height']==24
    scale=c.flag(g,'scale73')/2
    def click(x,y):p.move(int(x*scale),int(y*scale));p.down(True);p.down(False);p.drain()
    def opened():
     click(root['bounds'][0]+20,root['bounds'][1]+52)
     popup=wait_for(g,lambda:next((v for v in views(g)if v['class_name']=='Engacer.Menu145'and v['visible']),None));p.drain();return popup
    def row(popup,index):
     x,y,_,_=popup['bounds'];click(root['bounds'][0]+1+x+1+50,root['bounds'][1]+40+root['menu_height']+y+1+2+index*24+12)
    popup=opened()
    if cycle==0:c.shot(g,'native-menu-and-client')
    row(popup,1);assert 'M145_MENU_ACCEPT'not in output(g);assert any(v['handle']==popup['handle']and v['visible']for v in views(g));c.key(g,'esc');wait_for(g,lambda:not any(v['class_name']=='Engacer.Menu145'for v in views(g)))
    popup=opened();row(popup,0);wait(g,'M145_MENU_ACCEPT');wait_for(g,lambda:not any(v['class_name']=='Engacer.Menu145'for v in views(g)))
    popup=opened();row(popup,2);c.key(g,'down');c.key(g,'ret');wait(g,'M145_MENU_NESTED');wait_for(g,lambda:not any(v['class_name']=='Engacer.Menu145'for v in views(g)))
    p.desktop(49002,True);g.wait('M8_JOB_DONE',at);p.drain();state,command,status=struct.unpack('<3I',ui.memory(g,ui.symbol('info8',installed=True)[0],12));assert state==2 and status==0 and'M145_MENU_LIFETIME_PASS'in output(g),(state,command,status,output(g));retained=f.stats(g)[0]-before;assert retained==0,retained;assert len(t.records(g))==1 and t.records(g)[0]['token']==front['token']
    report['cycles'].append(dict(cycle=cycle+1,menu_client_geometry=True,disabled_command_refused=True,pointer_command=True,nested_keyboard_command=True,escape_cancel=True,callback_balance=True,retained_pages=retained))
   report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
