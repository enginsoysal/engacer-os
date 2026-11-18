"""Ordinary-input owned native baseline and M13 control journeys; no guest memory writes."""
import argparse, json, os, struct, sys, time, traceback
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--baseline',action='store_true');p.add_argument('--stage',type=int,default=1);p.add_argument('--profile',choices=['ordinary','compact','1024','150','4k'],default='ordinary');args=p.parse_args()
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE18' if args.baseline else f'EngacerOS-M13STAGE{args.stage}'
sys.path.insert(0,str(ROOT/'tests/m12'))
import ui

def key(g,*keys):
 g.qmp('send-key',{'keys':[{'type':'qcode','data':k} for k in keys],'hold-time':50});time.sleep(.12);ui.Pointer(g).drain()
def wizard(g,ptr,action):
 n=ui.integer(g,'controls');raw=ui.memory(g,ui.symbol('buttons',480)[0],n*20)
 rows=[struct.unpack_from('<5I',raw,i*20)for i in range(n)if struct.unpack_from('<I',raw,i*20+16)[0]==action];assert len(rows)==1,(action,n)
 x,y,w,h,_=rows[0];at=len(g.log());ptr.logical(x+w//2,y+h//2);return at
def shot(g,out,name,installed=False):
 ui.Pointer(g).drain();g.qmp('stop')
 try:ui.raw_shot(g,out,name,installed)
 finally:g.qmp('cont')
def main():
 label='baseline' if args.baseline else 'stage'+str(args.stage)
 out=ROOT/'build/m13'/label/args.profile;out.mkdir(parents=True,exist_ok=True)
 resolution,ram,scale={'ordinary':((1920,1080),512,50011),'compact':((1280,800),128,50011),'1024':((1024,768),128,50011),'150':((1920,1200),512,50012),'4k':((3840,2160),1024,50013)}[args.profile]
 meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m13-'+label+'-'+args.profile);disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
 report=dict(passed=False,baseline=args.baseline,stage='M12.18 baseline' if args.baseline else f'M13.{args.stage}',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],physical=list(resolution),configured_guest_mib=ram,owned_fixture=work.name,checks=[])
 try:
  with ui.guest(work/'install',disk,resolution=resolution,ram=ram)as g:
   ptr=ui.Pointer(g);ptr.drain();shot(g,out,'welcome');wizard(g,ptr,2);wizard(g,ptr,scale)
   for action in (2,100,2,2,2):wizard(g,ptr,action)
   shot(g,out,'review');at=wizard(g,ptr,2);g.wait('M6_INSTALL_PASS',at,240);at=wizard(g,ptr,84);g.wait('M7_DESKTOP_READY',at,180);ptr=ui.Pointer(g);ptr.drain();key(g,'esc');shot(g,out,'desktop',True)
   report['scale_units']=ui.integer(g,'scale73',True);assert report['scale_units']=={'ordinary':2,'compact':2,'1024':2,'150':3,'4k':4}[args.profile]
   pages_before=struct.unpack('<4Q',ui.memory(g,ui.symbol('stats',32,True)[0],32))[0]
   ptr.desktop(0,True);ptr.desktop(42004,True);key(g,'ctrl','a')
   for c in 'settings':key(g,c)
   key(g,'ret');shot(g,out,'settings',True)
   if not args.baseline:
    ptr.desktop(59003,True);ptr.desktop(59007,True);shot(g,out,'component-gallery',True)
    ptr.desktop(60100,True);ptr.desktop(60101,True);ptr.desktop(60102,True)
    for c in 'readable':key(g,c)
    key(g,'backspace');key(g,'shift','x');key(g,'shift','1');shot(g,out,'component-gallery-interactive',True)
    address,size=ui.symbol('apps',installed=True);assert b'readablX!\0' in ui.memory(g,address,size)
    semantic=struct.unpack('<QII',ui.memory(g,ui.symbol('access_focus16',96,True)[0],16));assert semantic[1:]==(60102,2),semantic
    key(g,'f1');assert ui.integer(g,'access_help16',True);shot(g,out,'text-field-focus-help',True);key(g,'esc')
    count=ui.integer(g,'control_count',True);controls=ui.memory(g,ui.symbol('controls',65536,True)[0],count*32);assert all(struct.unpack_from('<iiiiQI',controls,i*32)[5]!=60103 for i in range(count))
    for theme in ('dark','high-contrast','light'):
     if theme=='dark':ptr.desktop(59000,True);ptr.desktop(43,True)
     elif theme=='high-contrast':ptr.desktop(59004,True);ptr.desktop(60010,True)
     else:ptr.desktop(59004,True);ptr.desktop(60010,True);ptr.desktop(59000,True);ptr.desktop(44,True)
     ptr.desktop(59003,True);ptr.desktop(59007,True);shot(g,out,'component-gallery-'+theme,True)
    report['checks'].append('Light, dark and high-contrast native gallery frames; disabled action absent from the hit registry; edited text independently read back')
    report['checks'].append('Native gallery opens through System, activates a real button and selection, and accepts bounded editable text including shifted capitals and punctuation')
   report['resources']=dict(managed_stats=list(struct.unpack('<4Q',ui.memory(g,ui.symbol('stats',32,True)[0],32))),framebuffer_bytes=struct.unpack_from('<I',ui.physical_boot(g,True),136)[0]*struct.unpack_from('<I',ui.physical_boot(g,True),148)[0])
   key(g,'alt','f4');ptr.drain();pages_after=struct.unpack('<4Q',ui.memory(g,ui.symbol('stats',32,True)[0],32))[0];report['resources']['retained_task_delta_pages']=pages_after-pages_before;assert pages_after==pages_before
   before=int.from_bytes(ui.memory(g,ui.symbol('paints',8,True)[0],8),'little');time.sleep(.5);after=int.from_bytes(ui.memory(g,ui.symbol('paints',8,True)[0],8),'little');halted=g.qmp('human-monitor-command',{'command-line':'info registers -a'}).count('HLT=1');assert before==after and halted==2,(before,after,halted)
   report['checks'].append('Actual reference-size installation, retained-ISO restart, ordinary keyboard Settings launch, native physical captures and stable idle halt pass')
   (out/'install.log').write_text(g.log(),encoding='utf-8')
  for n in (1,2):
   boot=ui.guest(work/('disk-only-'+str(n)),disk,resolution=resolution,ram=ram,media='installed',ready='M7_DESKTOP_READY');ui.s.normal_boot(boot,work/'install/vars.fd')
   with boot as g:ui.Pointer(g).drain();shot(g,out,'disk-only-'+str(n),True);(out/('disk-only-'+str(n)+'.log')).write_text(g.log(),encoding='utf-8')
  report['checks'].append('Two independent no-ISO startups use ordinary firmware discovery');report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
