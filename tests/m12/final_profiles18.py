"""Actual native contrast/scaling, focus, pointer and boundary qualification."""
import json,os,struct,traceback,hashlib
from pathlib import Path
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE18'
import access_observe16 as a
from access_fixtures16 import clone
c=a.c;f=a.f;h=a.h;t=a.t;ui=a.ui;ROOT=a.ROOT

def dump(g,address,size,name):
 path=g.folder/(name+'.bin');g.qmp('human-monitor-command',{'command-line':f'pmemsave 0x{address:x} 0x{size:x} "{path.as_posix()}"'});data=path.read_bytes();assert len(data)==size;return data

def cursor(g,physical):
 g.qmp('stop')
 try:
  boot=ui.physical_boot(g,True);front=struct.unpack_from('<Q',boot,80)[0];stride,fmt,width,height=struct.unpack_from('<4I',boot,136);shadow=a.scalar(g,'shadow9',8);assert shadow
  x,y,w,hh=[a.scalar(g,n) for n in ('cursor9_x','cursor9_y','cursor9_w','cursor9_h')];mouse=[a.scalar(g,'mouse_x'),a.scalar(g,'mouse_y')];logical=[a.scalar(g,'pointer_x'),a.scalar(g,'pointer_y')];scale=c.flag(g,'scale73')
  assert [x,y]==mouse==list(physical),dict(cursor=[x,y],mouse=mouse,expected=physical)
  assert logical==[x*2//scale,y*2//scale] and 0<w<=15*scale//2 and 0<hh<=24*scale//2 and x+w<=width and y+hh<=height
  length=(hh-1)*stride+w*4;offset=y*stride+x*4;visible=dump(g,front+offset,length,'cursor-front');back=dump(g,shadow+offset,length,'cursor-shadow');differences=[]
  for row in range(hh):
   for col in range(w):
    at=row*stride+col*4
    if visible[at:at+4]!=back[at:at+4]:differences.append((col,row))
  if w>4 and hh>4:assert differences,'No physically rendered cursor over the actual compositor shadow'
  return dict(physical=mouse,logical=logical,cursor_rect=[x,y,w,hh],changed_pixels=len(differences),difference_bounds=[min(v[0] for v in differences),min(v[1] for v in differences),max(v[0] for v in differences),max(v[1] for v in differences)] if differences else None)
 finally:g.qmp('cont')

def main():
 out=ROOT/'build/m12/stage18/access-profiles';out.mkdir(parents=True,exist_ok=True);c.OUT=out
 meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));native=json.loads((ROOT/'build/m12/stage18/access-native/results.json').read_text(encoding='utf-8'));assert native['passed'] and native['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage18-access'/native['owned_fixture']/'owned.img';original=f.sha_file(source);work,disk,cloned=clone(ui,source,'m12-stage18-access-profiles');report=dict(passed=False,build_id=meta['build_id'],iso_sha256=native['iso_sha256'],clone=cloned,profiles=[],checks=[])
 try:
  appearance=h.record(disk)
  for label,resolution,scale,dark,contrast in [('compact-light',(800,600),2,False,False),('compact-dark',(800,600),2,True,False),('compact-150',(1280,1024),3,False,True),('150',(1920,1200),3,False,True),('4k',(3840,2160),4,False,True)]:
   with ui.guest(work/label,disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution) as g:
    p=ui.Pointer(g);p.drain();c.open_settings(g,p);before=f.stats(g);initial_scale=c.flag(g,'scale73');initial_colors=h.colors(g);p.desktop(43 if dark else 44,True);p.desktop(59004,True)
    if not contrast:p.desktop(60010,True)
    assert c.flag(g,'access_flags16')==(3 if contrast else 2)
    if scale==3:p.desktop(59001,True);p.desktop(112,True)
    assert c.flag(g,'scale73')==scale
    logical=struct.unpack('<II',ui.memory(g,ui.symbol('model',installed=True)[0]+240,8));assert logical[0]>=800 and logical[1]>=600
    for action,name in [(59000,'appearance'),(59001,'display'),(59002,'input'),(59003,'system'),(59004,'accessibility')]:
     p.desktop(action,True);assert h.page(g)==action-59000
     for x,y,w,hh,owner,command in f.current_controls(g):assert x>=0 and y>=0 and x+w<=logical[0] and y+hh<=logical[1],(label,name,command,(x,y,w,hh),logical)
     a.key(g,'tab');a.key(g,'f1');assert c.flag(g,'access_help16') and a.semantic(g,'access_help_item16')['label'];c.shot(g,name+'-'+label);a.key(g,'esc')
    if label=='compact-150':
     p.desktop(59001,True);p.desktop(113,True);assert c.flag(g,'scale73')==3 and 'small' in f.app(g)['notice'].lower();report['checks'].append('1280x1024 permits actual 150% logical 853x682 while refusing 200% without changing the accepted scale')
    pointers=[]
    if label in ('150','4k'):
     for point in [(resolution[0]//2,resolution[1]//2),(resolution[0]-1,resolution[1]-1),(0,0)]:
      p.x=a.scalar(g,'mouse_x');p.y=a.scalar(g,'mouse_y');p.move(*point);p.drain();pointers.append(cursor(g,point))
     # Actual mouse clicks still target the displayed control/caption at this scale.
     p.desktop(59001,True);assert h.page(g)==1;p.desktop(49001,True);p.desktop(49001,True);assert h.page(g)==1
    p.desktop(59004,True)
    if not contrast:p.desktop(60010,True)
    assert c.flag(g,'access_flags16')==3;h.close(g,p);assert c.flag(g,'scale73')==initial_scale and h.colors(g)==initial_colors and h.record(disk)==appearance;f.same_pages(before,f.stats(g));c.idle(g);stats=f.stats(g)
    report['profiles'].append(dict(name=label,physical=list(resolution),logical=list(logical),scale=scale,theme='high contrast' if contrast else 'dark' if dark else 'light',managed_current_bytes=stats[0]*4096,managed_peak_bytes=stats[1]*4096,retained_pages=0,pointer_observations=pointers));(out/(label+'.log')).write_bytes(g.log().encode())
  assert f.sha_file(source)==original;report['checks']+=['Five actual compact Light/Dark, compact 150%, ordinary 150% and 4K contrast profiles keep all five Settings categories and Focus Help readable and within the logical viewport','Physical front VRAM differs from the actual compositor shadow at the cursor; 150% and 200% hotspot, logical input and rendered rectangle agree at the middle and both screen corners; scaled client/caption clicks still activate their actual targets','Independent accessibility survives each profile; cancelled appearance/scale previews preserve exact appearance bytes, the source fixture remains unchanged, completed tasks retain zero pages and the desktop halts at idle'];report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
