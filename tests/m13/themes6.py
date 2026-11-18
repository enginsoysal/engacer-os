"""Actual applied Start themes, independently observed after Settings closes."""
import argparse,json,os,struct,traceback
from pathlib import Path
import taskbar_native6 as t
import observe6
observe6.bind(t.ui)
c=t.c;f=t.f;s=t.s;ui=t.ui;ROOT=t.ROOT
p=argparse.ArgumentParser();p.add_argument('--profile',required=True,choices=['ordinary','compact','1024','150','4k']);args=p.parse_args()
meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));prior=json.loads((ROOT/('build/m13/stage6/start-'+args.profile)/'results.json').read_text(encoding='utf-8'));assert prior['passed'] and prior['build_id']==meta['build_id']
work=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6'/('m136-start-'+args.profile)/prior['owned_fixture'];disk=work/'owned.img';assert disk.is_file()
out=ROOT/('build/m13/stage6/themes-'+args.profile);out.mkdir(parents=True,exist_ok=True);c.OUT=out
resolution,ram={'ordinary':((1920,1080),512),'compact':((1280,800),128),'1024':((1024,768),128),'150':((1920,1200),512),'4k':((3840,2160),1024)}[args.profile]
report=dict(passed=False,stage='M13.6',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],profile=args.profile,physical=list(resolution),checks=[],themes=[])
def dark(g):return struct.unpack_from('<I',ui.memory(g,ui.symbol('preferences',24,True)[0],24),12)[0]
try:
 boot=ui.guest(work/('applied-themes-'+os.urandom(4).hex()),disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution,ram=ram);ui.s.normal_boot(boot,work/'install/vars.fd')
 with boot as g:
  ptr=ui.Pointer(g);ptr.drain();t.close_all(g,ptr);before=f.stats(g);start_bytes=bytes(s.prefs(g))
  for theme in ('dark','high-contrast','light'):
   t.launch(g,ptr,'settings',3)
   if theme=='high-contrast':
    ptr.desktop(59004,True)
    if not c.flag(g,'access_flags16')&1:ptr.desktop(60010,True)
   else:
    if c.flag(g,'access_flags16')&1:ptr.desktop(59004,True);ptr.desktop(60010,True)
    ptr.desktop(59000,True);ptr.desktop(43 if theme=='dark' else 44,True);ptr.desktop(47,True)
    assert dark(g)==(theme=='dark')
    record=ui.s.s.document(disk,'/System/Settings/appearance11-Owner.bin');assert struct.unpack_from('<I',record,12)[0]==dark(g)
   t.close(g,ptr);assert not t.records(g) and dark(g)==(theme!='light')
   ptr.desktop(0,True);ptr.desktop(42000,True)
   if not s.prefs(g).view:ptr.desktop(42003,True)
   b=s.bounds(g);c.shot(g,theme)
   pixel=c.pixel(g,b[0]+4,b[1]+50);components=((pixel>>16)&255,(pixel>>8)&255,pixel&255)
   if theme=='high-contrast':assert pixel==0 and c.flag(g,'access_flags16')&1
   elif theme=='dark':assert sum(components)<240 and not c.flag(g,'access_flags16')&1
   else:assert sum(components)>600 and not c.flag(g,'access_flags16')&1
   report['themes'].append(dict(theme=theme,dark=dark(g),high_contrast=bool(c.flag(g,'access_flags16')&1),actual_surface_rgb=hex(pixel),bounds=b,after_settings_close=True))
   c.key(g,'esc')
  assert bytes(s.prefs(g))==start_bytes;f.same_pages(before,f.stats(g));c.idle(g);report['resources']=dict(before=list(before),after=list(f.stats(g)),retained_pages=0);(out/'native.log').write_text(g.log(),encoding='utf-8')
 report['checks'].append('Actual Dark Apply, high contrast and Light Apply survive closing Settings; native Start surfaces, real flags and independently read appearance bytes agree at the named physical profile')
 report['passed']=True
except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
