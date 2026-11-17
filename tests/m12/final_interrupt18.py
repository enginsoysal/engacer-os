"""Actual Escape interruption restores cached window pixels without timers or retention."""
import json,os,struct,traceback
from pathlib import Path
from PIL import Image,ImageChops
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE18'
import access_observe16 as a
c=a.c;f=a.f;h=a.h;t=a.t;ui=a.ui;ROOT=a.ROOT

def main():
 out=ROOT/'build/m12/stage18/performance-interrupt';out.mkdir(parents=True,exist_ok=True);c.OUT=out;meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));native=json.loads((ROOT/'build/m12/stage18/performance-native/results.json').read_text(encoding='utf-8'));assert native['passed'] and native['build_id']==meta['build_id'];work=ui.q.new_work('m12-stage18-interrupt');disk=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage18-performance'/native['owned_fixture']/'owned.img';original=f.sha_file(disk);report=dict(passed=False,build_id=meta['build_id'],profiles=[],checks=[])
 try:
  for label,resolution,scale in [('ordinary',(1280,800),2),('150',(1920,1200),3),('4k',(3840,2160),4)]:
   with ui.guest(work/label,disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution) as g:
    p=ui.Pointer(g);p.drain();assert not c.flag(g,'access_flags16')
    if scale==3:c.open_settings(g,p);p.desktop(59001,True);p.desktop(112,True);p.desktop(49000,True)
    assert c.flag(g,'scale73')==scale;before=f.stats(g);files=next(w for w in t.records(g) if w['app']==1);assert f.model(g)[0]==files['slot'];bounds=f.model(g)[1];p.move(5,5);p.drain();c.shot(g,'before-'+label)
    x,y,w,hh=bounds;p.move((x+180)*scale//2,(y+18)*scale//2);p.drain();p.down(True);p.drain();p.move((x+260)*scale//2,(y+58)*scale//2);p.drain();assert c.flag(g,'dragging') and f.model(g)[1]!=bounds;c.shot(g,'moving-'+label);a.key(g,'esc');assert not c.flag(g,'dragging') and f.model(g)[1]==bounds;p.down(False);p.move(5,5);p.drain();c.shot(g,'cancelled-'+label)
    with Image.open(out/('before-'+label+'.png')) as left,Image.open(out/('cancelled-'+label+'.png')) as right:
     crop=(0,0,resolution[0],resolution[1]-60*scale//2);assert ImageChops.difference(left.crop(crop).convert('RGB'),right.crop(crop).convert('RGB')).getbbox() is None,(label,'Cancelled viewport differs')
    f.same_pages(before,f.stats(g));c.idle(g);stats=f.stats(g);report['profiles'].append(dict(name=label,physical=list(resolution),scale=scale,exact_restored_bounds=list(bounds),viewport_pixels_restored=True,managed_current_bytes=stats[0]*4096,managed_peak_bytes=stats[1]*4096,retained_pages=0));(out/(label+'.log')).write_bytes(g.log().encode())
  assert f.sha_file(disk)==original;report['checks']=['Actual default-effect title-bar drags are interrupted by Escape at 100%, 150% and physical 4K/200%; the prior rectangle and full native viewport above the clock/taskbar restore pixel for pixel after pointer release','Cancelled moves leave exact persistent disk bytes, retain zero managed pages, add no idle paint loop and halt all CPUs at idle'];report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
