"""Own native owner/modal/capture tasks using ordinary pointer and keyboard input."""
import argparse,hashlib,json,os,struct,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tests/m14'))
from window144_native import ui,c,f,t,clone,library,StoppedDisk,task,output,wait
from original_window_trace4 import views
from owner144_build import build

def native_at(g,bounds):
 raw=ui.memory(g,ui.symbol('model',installed=True)[0],224)
 return next(record for record in t.records(g)if list(struct.unpack_from('<4i',raw,record['slot']*28))==bounds)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--cycles',type=int,default=21);args=parser.parse_args();assert 1<=args.cycles<=21
 out=ROOT/'build/m14-native/stage4/owner-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out;fixture=build()/'owner.exe';meta=json.loads(ui.manifest_path12().read_text());base=json.loads((ROOT/'build/m14-native/stage4/apps/results.json').read_text());assert base['passed']and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m144-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m144-owner-native');mounted=StoppedDisk(disk,library())
 try:mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())
 finally:mounted.close()
 report=dict(passed=False,scope='Owned native owner/modal/input-capture/admission fixture; not original application qualification',build_id=meta['build_id'],fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest(),clone=cloned,cycles=[])
 try:
  boot=ui.guest(work/'owners',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19);task(g,p,12005);before=f.stats(g)[0]
   for turn in range(args.cycles):
    p.logical(88,70,True);p.drain();selected_before=ui.integer(g,'desktop_selection11',True);assert selected_before
    at=len(g.log());p.desktop(12100,True);g.wait('M8_CPL3_CREATED',at);wait(g,'M144_MODAL_READY');p.drain();assert len(t.records(g))==3,t.records(g)
    owner=native_at(g,[80,80,400,260]);modal=native_at(g,[650,140,400,260]);descriptions=views(g);owned_view=next(v for v in descriptions if v['title']=='Disabled owner');assert not owned_view['enabled'];assert next(v for v in descriptions if v['title']=='Owned modal')['owner']==owned_view['handle']
    desktop_focus_before=ui.integer(g,'desktop_focus11',True);assert not desktop_focus_before
    p.logical(454,100,True);p.drain();assert ui.integer(g,'desktop_focus11',True)==desktop_focus_before and ui.integer(g,'desktop_selection11',True)==selected_before,'disabled owner click changed desktop focus or selection'
    c.key(g,'m');wait(g,'M144_MODAL_KEYBOARD_PASS');f.right(g,p,454,100);p.drain();assert not ui.integer(g,'context11',True),'disabled owner opened a native context menu'
    assert len(t.records(g))==3 and f.model(g)[0]==modal['slot'],(t.records(g),f.model(g));assert not any(r[4]==owner['token']and 49000<=r[5]<=49003 for r in f.controls(g))
    if turn==0:c.shot(g,'disabled-owner-and-modal')
    p.logical(1024,160,True);wait(g,'M144_MODAL_CLOSED');p.drain();assert len(t.records(g))==2;t.focus(g,p,owner);c.key(g,'p');wait(g,'M144_OWNER_RESPONSIVE')
    scale=c.flag(g,'scale73')/2;p.move(int(120*scale),int(170*scale));p.down(True);wait(g,'M144_CAPTURE_READY');p.move(int(20*scale),int(40*scale));wait(g,'M144_CAPTURE_OUTSIDE');p.down(False);wait(g,'M144_CAPTURE_RELEASED');p.drain();t.focus(g,p,owner)
    c.key(g,'c');wait(g,'M144_OWNED_VISIBLE');p.drain();palette=native_at(g,[650,440,400,260]);t.focus(g,p,owner);p.drain();order=list(ui.memory(g,ui.symbol('model',installed=True)[0]+224,8));assert order.index(owner['slot'])<order.index(palette['slot']),order
    if turn==0:c.shot(g,'owned-palette-remains-above-owner')
    p.logical(454,100,True);g.wait('M8_JOB_DONE',at);p.drain();assert 'M144_OWNER_LIFETIME_PASS'in output(g),output(g);assert len(t.records(g))==1 and t.records(g)[0]['token']==front['token'];assert ui.integer(g,'ui_resident144',True)==0;retained=f.stats(g)[0]-before;assert retained==0,retained
    report['cycles'].append({'cycle':turn+1,'retained_pages':retained,'explicit_visible_root_quota':True,'disabled_owner_close_blocked':True,'capture_outside_client':True,'owned_z_order_and_teardown':True,'disabled_click_preserves_desktop_state':True,'modal_keyboard_route':True})
   report['passed']=True;report['output']=output(g)
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps({k:v for k,v in report.items()if k!='cycles'},indent=2),flush=True)
if __name__=='__main__':main()
