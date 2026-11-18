"""M13.12 ordinary-input window tasks at every reference display and scale."""
import argparse,json,os,struct,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];os.environ['ENGACER12_IMAGE']='EngacerOS-M13STAGE12';sys.path.insert(0,str(ROOT/'tests/m12'))
import taskbar_observe as t
c=t.c;f=t.f;ui=t.ui
import capture14
capture14.bind(ui)
import observer8
observer8.bind(ui)

def geometry(g,slot=None):
 if slot is None:slot=f.model(g)[0]
 return struct.unpack('<4i',ui.memory(g,ui.symbol('model',installed=True)[0]+slot*28,16))
def move(g,p,x,y):
 scale=c.flag(g,'scale73');p.move(x*scale//2,y*scale//2);p.drain()
def drag(g,p,x,y,xx,yy,release=True):
 move(g,p,x,y);p.down(True);p.drain();move(g,p,xx,yy)
 if release:p.down(False);p.drain()
def idle(g):
 observations=[]
 for _ in range(20):
  ui.Pointer(g).drain();before=int.from_bytes(ui.memory(g,ui.symbol('paints',8,True)[0],8),'little');time.sleep(.5);after=int.from_bytes(ui.memory(g,ui.symbol('paints',8,True)[0],8),'little');halted=g.qmp('human-monitor-command',{'command-line':'info registers -a'}).count('HLT=1');observations.append(dict(before=before,after=after,halted=halted))
  if len(observations)>=3 and all(r['before']==r['after'] and r['halted']==2 for r in observations[-3:]):return observations
 raise AssertionError(observations)
def main():
 assert not (ROOT/'evidence/M13/12/publication-results.json').exists(),'Accepted stage is immutable'
 parser=argparse.ArgumentParser();parser.add_argument('--fixture',action='store_true');parser.add_argument('--profile',choices=['ordinary','compact','1024','150','4k'],required=True);a=parser.parse_args();resolution,ram,scale={'ordinary':((1920,1080),512,50011),'compact':((1280,800),128,50011),'1024':((1024,768),128,50011),'150':((1920,1200),512,50012),'4k':((3840,2160),1024,50013)}[a.profile]
 out=ROOT/'build/m13/stage12'/('windows-'+a.profile);out.mkdir(parents=True,exist_ok=True);c.OUT=out;meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m1312-windows-'+a.profile);disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);report=dict(passed=False,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],physical=list(resolution),checks=[])
 if a.fixture:
  from access_fixtures16 import clone
  native=json.loads((ROOT/'build/m13/stage12'/a.profile/'results.json').read_text());assert native['passed'] and native['build_id']==meta['build_id']
  source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6'/('m13-stage12-'+a.profile)/native['owned_fixture']/'owned.img'
  work,disk,report['clone']=clone(ui,source,'m1312-windows-clone-'+a.profile)
 try:
  with ui.guest(work/'install',disk,resolution=resolution,ram=ram,**(dict(media='installed',ready='M7_DESKTOP_READY') if a.fixture else {})) as g:
   p=ui.Pointer(g)
   if not a.fixture:
    for action in (2,scale,2,100,2,2,2):c.wizard(g,p,action)
    at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180)
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);baseline=f.stats(g);c.shot(g,'desktop');first=t.launch(g,p,'files',1);normal_first=geometry(g);second=t.launch(g,p,'files',1);normal=geometry(g);width,height=struct.unpack('<II',ui.memory(g,ui.symbol('model',installed=True)[0]+240,8));report['logical']=[width,height];report['scale_units']=c.flag(g,'scale73');c.shot(g,'active-inactive')
   p.desktop(49000,True);assert next(w for w in t.records(g) if w['token']==second['token'])['minimized'];t.focus(g,p,second);assert geometry(g)==normal;c.key(g,'meta_l','up');assert geometry(g)==(0,0,width,height-60);c.key(g,'meta_l','down');assert geometry(g)==normal
   x,y,w,h=normal;drag(g,p,x+180,y+18,x+224,y+42,False);assert geometry(g)!=normal;c.key(g,'esc');p.down(False);p.drain();assert geometry(g)==normal
   drag(g,p,x+w-2,y+h-2,x+w+6,y+h+6,False);assert geometry(g)[2:]!=normal[2:];c.key(g,'esc');p.down(False);p.drain();assert geometry(g)==normal
   report['checks'].append('Minimize/exact-owner restore, maximize/normal restore, pointer move and resize cancellation preserve real bounds')
   drag(g,p,x+180,y+18,2,160,False);assert c.flag(g,'window_snap_preview11')==2;c.shot(g,'edge-preview');c.key(g,'esc');p.down(False);p.drain();assert geometry(g)==normal
   drag(g,p,x+180,y+18,2,160);assert geometry(g)==(0,0,width//2,height-60) and c.flag(g,'switch_open11')==3;raw=ui.memory(g,ui.symbol('switch_tokens11',installed=True)[0],64);tokens=list(struct.unpack('<8Q',raw));choice=tokens.index(first['token']);p.desktop(44100+choice,True);assert geometry(g,first['slot'])==(width//2,0,width-width//2,height-60);c.shot(g,'two-real-windows');c.key(g,'meta_l','down');assert geometry(g)==normal_first;t.focus(g,p,second);c.key(g,'meta_l','down');assert geometry(g)==normal
   report['checks'].append('Actual edge preview cancels safely; release and complementary-window choice place exact left/right halves and restore each independent normal rectangle')
   editor=t.launch(g,p,'text editor',2);c.type_text(g,'M13.12 unsaved work');assert bytes(t.app_view(g).text)==b'M13.12 unsaved work';p.desktop(49000,True);t.focus(g,p,first);t.focus(g,p,editor);assert bytes(t.app_view(g).text)==b'M13.12 unsaved work';c.key(g,'meta_l','left');c.key(g,'esc');c.key(g,'meta_l','down');assert bytes(t.app_view(g).text)==b'M13.12 unsaved work';c.shot(g,'unsaved-work-survives')
   t.focus(g,p,second);x,y,w,h=geometry(g);drag(g,p,x+180,y+18,50,160);assert geometry(g)[0]<0;offscreen=geometry(g);c.key(g,'alt','spc');assert c.flag(g,'context11') and 0<=c.flag(g,'context_x11')<width;f.menu(g,p,44004)
   for _ in range(10):c.key(g,'right')
   c.key(g,'ret');assert geometry(g)==(offscreen[0]+160,offscreen[1],offscreen[2],offscreen[3]) and not c.flag(g,'switch_open11') and not c.flag(g,'window_snap_preview11');c.shot(g,'offscreen-recovered');report['checks'].append('Dirty editor text survives minimizing, switching and snapping; a partially off-screen window retains a reachable real Move menu and returns on screen')
   report['before_close']=dict(windows=t.records(g),focused=int.from_bytes(ui.memory(g,ui.symbol('model',installed=True)[0]+236,4),'little'),context=c.flag(g,'context11'),keyboard_move=c.flag(g,'window_keyboard_move11'));c.shot(g,'before-close-all')
   try:t.close_all(g,p)
   except Exception:
    report['close_failure']=dict(windows=t.records(g),focused=int.from_bytes(ui.memory(g,ui.symbol('model',installed=True)[0]+236,4),'little'),context=c.flag(g,'context11'),menu=t.menu_rows(g) if c.flag(g,'context11') else []);c.shot(g,'close-all-failure');raise
   f.same_pages(baseline,f.stats(g));report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0);report['idle_observations']=idle(g);(out/'install.log').write_bytes(g.log().encode())
  for n in (1,2):
   boot=ui.guest(work/('disk-'+str(n)),disk,resolution=resolution,ram=ram,media='installed',ready='M7_DESKTOP_READY');ui.s.normal_boot(boot,work/'install/vars.fd')
   with boot as g:
    p=ui.Pointer(g);p.drain();assert not c.flag(g,'switch_open11') and not c.flag(g,'window_snap_preview11');c.shot(g,'disk-only-'+str(n));(out/('disk-'+str(n)+'.log')).write_bytes(g.log().encode())
  report['checks'].append('Tasks retain zero managed pages and stable idle halt; two ordinary no-ISO boots start without persisting transient snap overlays');report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report),flush=True)
if __name__=='__main__':main()
