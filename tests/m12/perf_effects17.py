"""Reduced effects verified from real native pixels during held pointer input."""
import json,os,traceback
from pathlib import Path
from PIL import Image,ImageChops
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE17'
import access_observe16 as a
from access_fixtures16 import clone
c=a.c;f=a.f;ui=a.ui;ROOT=a.ROOT

def main():
 out=ROOT/'build/m12/stage17/access-effects';out.mkdir(parents=True,exist_ok=True);c.OUT=out;meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));native=json.loads((ROOT/'build/m12/stage17/access-native/results.json').read_text(encoding='utf-8'));assert native['passed'] and native['build_id']==meta['build_id'];source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage17-access'/native['owned_fixture']/'owned.img';original=f.sha_file(source);work,disk,cloned=clone(ui,source,'m12-stage17-access-effects');report=dict(passed=False,build_id=meta['build_id'],clone=cloned,checks=[],profiles=[])
 try:
  with ui.guest(work/'tasks',disk,media='installed',ready='M7_DESKTOP_READY') as g:
   p=ui.Pointer(g);p.drain();baseline=f.stats(g)
   for desired in (0,2,1,3):
    c.open_settings(g,p);p.desktop(59004,True)
    for bit,action in ((1,60010),(2,60011)):
     if bool(c.flag(g,'access_flags16')&bit)!=bool(desired&bit):p.desktop(action,True)
    a.h.close(g,p);assert c.flag(g,'access_flags16')==desired
    x,y,w,hh,owner,command=next(r for r in f.controls(g) if r[4]==0 and r[5]==0);assert c.flag(g,'scale73')==2;p.move(x+w-12,y+hh//2);p.drain();c.shot(g,'hover-'+str(desired));p.down(True);p.drain();assert int.from_bytes(ui.memory(g,ui.symbol('interaction11',installed=True)[0]+60,4),'little')==1;c.shot(g,'held-'+str(desired));p.move(x+w+30,y-30);p.drain();p.down(False);p.drain();assert not c.flag(g,'launcher')
    region=(x+7,y+5,x+34,y+31)
    with Image.open(out/('hover-'+str(desired)+'.png')) as before,Image.open(out/('held-'+str(desired)+'.png')) as after:changed=ImageChops.difference(before.crop(region).convert('RGB'),after.crop(region).convert('RGB')).getbbox() is not None
    assert changed==(not bool(desired&2)),(desired,changed);report['profiles'].append(dict(flags=desired,actual_held_capture=True,icon_pixels_changed=changed))
   f.same_pages(baseline,f.stats(g));c.idle(g);report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0);(out/'native.log').write_bytes(g.log().encode())
  assert f.sha_file(source)==original;report['checks']=['Ordinary and high-contrast native held-button input produces actual icon movement with effects enabled; reduced effects preserves exact icon pixels under the same real captured press, cancels release outside, adds no retained pages and halts at idle'];report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
