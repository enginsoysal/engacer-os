"""Verify own CPL3 primitives using actual guest framebuffer pixels and teardown."""
import hashlib,json,os,sys,traceback
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tests/m14'))
from window144_native import ui,c,f,t,clone,library,StoppedDisk,task,output,wait
from deep144_build import build

def main():
 out=ROOT/'build/m14-native/stage4/deep-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out
 fixture=build()/'deep.exe';meta=json.loads(ui.manifest_path12().read_text());base=json.loads((ROOT/'build/m14-native/stage4/apps/results.json').read_text());assert base['passed']and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m144-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m144-native-deep');mounted=StoppedDisk(disk,library())
 try:mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())
 finally:mounted.close()
 report=dict(passed=False,scope='Own maximum-depth native HWND rendering, initial visibility, quota refusal and teardown; not original app qualification',build_id=meta['build_id'],fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest(),clone=cloned,cycles=[])
 try:
  boot=ui.guest(work/'deep',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);task(g,p,12005);before=f.stats(g)[0]
   for turn in range(21):
    at=len(g.log());p.desktop(12100,True);g.wait('M8_CPL3_CREATED',at);wait(g,'M144_DEEP_READY');wait(g,'M144_DEEP_PAINTED');p.drain();assert len(t.records(g))==2
    if turn==0:
     c.shot(g,'maximum-depth-painted-window');image=Image.open(out/'maximum-depth-painted-window.png');scale=c.flag(g,'scale73')/2;x,y,w,h=f.model(g)[1]
     rgb=image.getpixel((int((x+31)*scale),int((y+70)*scale)));assert rgb==(0,120,199),rgb;report['physical_framebuffer']={'deepest_child_rgb':list(rgb),'depth':32,'physical_width':image.width,'physical_height':image.height}
    p.desktop(49002,True);g.wait('M8_JOB_DONE',at);p.drain();assert 'M144_DEEP_LIFETIME_PASS'in output(g),output(g)
    assert ui.integer(g,'ui_resident144',True)==0 and ui.integer(g,'ui_draw_pages144',True)==0
    retained=f.stats(g)[0]-before;assert retained==0,retained;report['cycles'].append({'cycle':turn+1,'legal_nesting_depth':32,'retained_pages':retained})
   report['passed']=True;report['output']=output(g)
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps({k:v for k,v in report.items()if k!='cycles'},indent=2),flush=True)
if __name__=='__main__':main()
