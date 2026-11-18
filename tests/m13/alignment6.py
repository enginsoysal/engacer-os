"""Real per-user left/center launch surfaces and independent persisted boots."""
import hashlib,json,struct,traceback
import taskbar_native6 as t
c=t.c;f=t.f;s=t.s;ui=t.ui;ROOT=t.ROOT
out=ROOT/'build/m13/stage6/alignment';out.mkdir(parents=True,exist_ok=True);c.OUT=out
meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m136-alignment');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);report=dict(passed=False,stage='M13.6',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],checks=[],layouts=[])
def check(g,p,name,centered):
 start=c.control(g,0)
 # The model layout is observed through the actual controls; no memory is written.
 assert bool(s.prefs(g).centered)==bool(centered)
 groups=t.group_controls(g);assert len(groups)==3 and all(r[2]==104 for r in groups)
 assert all(groups[i][0]+groups[i][2]<=groups[i+1][0] for i in range(len(groups)-1))
 if centered:assert start[0]>16
 else:assert start[0]==16
 p.desktop(0,True);b=s.bounds(g);c.shot(g,name);report['observed_state']=dict(launcher=c.flag(g,'launcher'),guide=c.flag(g,'guide_open11'),context=c.flag(g,'context11'),bounds=b,controls=[list(r) for r in f.controls(g) if r[5]==0]);physical=ui.physical_boot(g,True);physical_width=struct.unpack_from('<I',physical,144)[0];logical_width=physical_width*2//c.flag(g,'scale73')
 assert b[0]==((logical_width-b[2])//2 if centered else 16),(b,logical_width)
 c.shot(g,name);c.key(g,'esc');report['layouts'].append(dict(name=name,centered=centered,start_button=list(start[:4]),start_panel=list(b),physical_width=physical_width,logical_width=logical_width))
try:
 with ui.guest(work/'install',disk) as g:
  p=ui.Pointer(g)
  for a in (2,2,100,2,2,2):c.wizard(g,p,a)
  at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain();t.close(g,p);before=f.stats(g);check(g,p,'left-default',0)
  for name,value in [('center-preview',1),('left-restored',0),('center-saved',1)]:
   p.desktop(0,True);p.desktop(42007,True);p.desktop(42030,True);p.desktop(42018,True);assert s.prefs(g).centered==value;p.desktop(42008,True);c.key(g,'esc');check(g,p,name,value)
  saved=bytes(s.prefs(g));assert ui.s.s.document(disk,'/System/Settings/start11-Owner.bin')==saved;f.same_pages(before,f.stats(g));c.idle(g);report['resources']=dict(before=list(before),after=list(f.stats(g)),retained_pages=0)
  (out/'native.log').write_text(g.log(),encoding='utf-8')
 report['checks'].append('Actual left/center/left/center customization moves both Start and real taskbar groups, preserves all targets and independently matches saved preference bytes')
 for n,resolution in [(1,(1920,1080)),(2,(3840,2160))]:
  boot=ui.guest(work/('disk-only-'+str(n)),disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution,ram=1024);ui.s.normal_boot(boot,work/'install/vars.fd')
  with boot as g:
   p=ui.Pointer(g);p.drain();assert bytes(s.prefs(g))==saved;check(g,p,'disk-only-'+str(n),1);c.idle(g);(out/('disk-only-'+str(n)+'.log')).write_text(g.log(),encoding='utf-8')
 report['checks'].append('Two ordinary no-ISO startups at physical 1080p and 4K preserve exact centered preferences and independently fit the real Start/taskbar controls')
 report['passed']=True
except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
