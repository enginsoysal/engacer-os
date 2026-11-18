"""Observe setup state through ordinary guest input; never write guest memory."""
import argparse,hashlib,json,os,struct,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
os.environ['ENGACER12_IMAGE']='EngacerOS-M13STAGE2'
sys.path.insert(0,str(ROOT/'tests/m12'))
import ui
def key(g,*keys):
 g.qmp('send-key',{'keys':[{'type':'qcode','data':k} for k in keys],'hold-time':50});time.sleep(.12);ui.Pointer(g).drain()
def wizard(g,p,action):
 n=ui.integer(g,'controls');raw=ui.memory(g,ui.symbol('buttons',480)[0],n*20)
 rows=[struct.unpack_from('<5I',raw,i*20)for i in range(n)if struct.unpack_from('<I',raw,i*20+16)[0]==action];assert len(rows)==1,(action,n)
 x,y,w,h,_=rows[0];p.logical(x+w//2,y+h//2)
def shot(g,out,name,installed=False):
 ui.Pointer(g).drain();g.qmp('stop')
 try:ui.raw_shot(g,out,name,installed)
 finally:g.qmp('cont')

def value(g,name,size=4):return int.from_bytes(ui.memory(g,ui.symbol(name,24 if name=='setup11' else size)[0],size),'little')
def sample(g):return ui.memory(g,ui.symbol('keyboard_test11',32)[0],32).split(b'\0')[0]
def actions(g):
 n=ui.integer(g,'controls');raw=ui.memory(g,ui.symbol('buttons',480)[0],n*20)
 return [struct.unpack_from('<I',raw,i*20+16)[0] for i in range(n)]
def activate(g,p,action,keyboard):
 if not keyboard:return wizard(g,p,action)
 for _ in range(25):
  ids=actions(g);focus=ui.integer(g,'focus')
  if focus<len(ids) and ids[focus]==action:
   if action!=50002:key(g,'ret')
   return
  key(g,'tab')
 raise AssertionError(('Unreachable keyboard action',action,ids))
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(1024**2),b''):h.update(chunk)
 return h.hexdigest()
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--keyboard',action='store_true');parser.add_argument('--compact',action='store_true');args=parser.parse_args()
 label=('keyboard' if args.keyboard else 'pointer')+('-compact' if args.compact else '')
 out=ROOT/'build/m13/stage2'/('journey-'+label);out.mkdir(parents=True,exist_ok=True)
 work=ui.q.new_work('m132-'+label);disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);before=digest(disk)
 meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));report=dict(passed=False,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],input='keyboard only' if args.keyboard else 'pointer navigation with typing',checks=[])
 try:
  with ui.guest(work/'setup',disk,resolution=(1024,768) if args.compact else (1920,1080),ram=128 if args.compact else 512) as g:
   p=ui.Pointer(g);p.drain();go=lambda a:activate(g,p,a,args.keyboard)
   assert 50 not in actions(g) and 83 not in actions(g)
   go(50500);assert 50 in actions(g) and 83 in actions(g);shot(g,out,'advanced')
   key(g,'esc');assert 50 not in actions(g) and value(g,'startup_options13')==0
   go(50500);go(83);assert value(g,'step')==0 and value(g,'validation',8)!=0
   go(50500);go(2);assert value(g,'keyboard_page11')==1
   go(50001);assert value(g,'setup11')==1;go(50000);assert value(g,'setup11')==0
   if args.compact:
    go(50012);assert value(g,'validation',8)!=0 and ui.integer(g,'scale73')==2
    go(50013);assert value(g,'validation',8)!=0 and ui.integer(g,'scale73')==2
   go(50002)
   for c in 'hello':key(g,c)
   key(g,'shift','1');key(g,'backspace');key(g,'shift','x');assert sample(g)==b'helloX'
   key(g,'ctrl','a');assert sample(g)==b'helloX'
   shot(g,out,'keyboard-preview');full=value(g,'full_frames75');go(2);go(1)
   assert sample(g)==b'helloX' and value(g,'full_frames75')==full
   go(50003);assert sample(g)==b'';go(50002);key(g,'a');key(g,'ret');assert value(g,'step')==1
   go(100);go(2);go(50102);assert ui.memory(g,ui.symbol('setup11',24)[0]+20,4)==b'\0'*4
   shot(g,out,'apps');go(2);go(50301);go(50311);go(32);shot(g,out,'appearance');go(2);shot(g,out,'review')
   expected=ui.memory(g,ui.symbol('setup11',24)[0],24);assert struct.unpack('<6I',expected)[1:3]==(1,0x182039)
   go(1);assert ui.memory(g,ui.symbol('setup11',24)[0],24)==expected;go(2)
   assert value(g,'full_frames75')==full
   assert digest(disk)==before,'Setup wrote the disk before final Install'
   report['checks']=['Advanced options disclose, Escape closes and blank installed-start fails safely','Real keyboard layout, shifted text, modifiers, Clear and Enter; Back retains sample','Unsupported compact scales refuse and retain readable viewport' if args.compact else 'Ordinary viewport retains its size','No-optional-app, dark wallpaper/accent choices survive Back/Next','Every ordinary page keeps the outer frame; complete disk SHA unchanged before Install']
   at=len(g.log());go(2);g.wait('M6_INSTALL_PASS',at,240);p.drain()
   appearance=ui.s.s.document(disk,'/System/Settings/appearance11-Owner.bin')
   assert len(appearance)==352 and struct.unpack_from('<8I',appearance)==(0x41313145,1,0x9caeff,1,0,0x182039,0,0)
   assert ui.s.s.document(disk,'/System/Settings/keyboard10.bin')==struct.pack('<II',0x30314c4b,0)
   at=len(g.log());go(84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain();key(g,'esc');shot(g,out,'customized-installed',True)
   assert 'M6_INSTALLED_VOLUME' in g.log()[at:] and 'M6_WIZARD_READY' not in g.log()[at:]
   report['checks'].append('Custom no-optional-app installation independently verifies saved keyboard/appearance bytes and retained-ISO installed startup')
   (out/'boot.log').write_text(g.log(),encoding='utf-8');report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report),flush=True)
if __name__=='__main__':main()
