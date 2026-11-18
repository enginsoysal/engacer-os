"""M13.7 actual installed Files input, filter ownership and persistence."""
import argparse,hashlib,json,os,struct,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
os.environ['ENGACER12_IMAGE']='EngacerOS-M13STAGE7'
sys.path.insert(0,str(ROOT/'tests/m12'))
import taskbar_observe as t
f=t.f;c=t.c;ui=t.ui
import capture14,observe6
capture14.bind(ui);observe6.bind(ui)

def query(g,slot=None):
 if slot is None:slot=f.model(g)[0]
 address,size=ui.symbol('file_filters17',installed=True);stride=size//8
 return ui.memory(g,address+slot*stride+8,64).split(b'\0')[0].decode()

def close(g,p):
 if any(r[5]==60002 for r in f.controls(g)):p.desktop(60002,True)
 t.s.close(g,p)

def filter_name(g,p,value):
 c.key(g,'ctrl','f');c.key(g,'ctrl','a');c.type_text(g,value);p.drain();assert query(g)==value

def finish_job(g,p):
 deadline=time.monotonic()+90
 while c.flag(g,'file_job_state11'):
  if time.monotonic()>deadline:raise TimeoutError('Owned file task')
  time.sleep(.05)
 p.drain();assert not c.flag(g,'file_job_error11')

def documents(g,p):
 if f.has(g,94):p.desktop(94,True)
 else:p.desktop(40016,True);f.menu(g,p,40202)
 assert f.app(g)['path']=='/Users/Owner/Documents'

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--profile',choices=['ordinary','compact','1024','150','4k'],default='ordinary');a=parser.parse_args()
 assert not (ROOT/'evidence/M13/7/publication-results.json').exists()
 resolution,ram,scale={'ordinary':((1920,1080),512,50011),'compact':((1280,800),128,50011),'1024':((1024,768),128,50011),'150':((1920,1200),512,50012),'4k':((3840,2160),1024,50013)}[a.profile]
 out=ROOT/'build/m13/stage7'/('files-'+a.profile);out.mkdir(parents=True,exist_ok=True);c.OUT=out
 meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m137-files-'+a.profile);disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
 report=dict(passed=False,stage='M13.7',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],physical=list(resolution),owned_fixture=work.name,checks=[])
 try:
  with ui.guest(work/'install',disk,resolution=resolution,ram=ram) as g:
   p=ui.Pointer(g)
   for action in (2,scale,2,100,2,2,2):c.wizard(g,p,action)
   at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain();t.close_all(g,p);baseline=f.stats(g)
   first=t.launch(g,p,'files',1);documents(g,p);assert f.app(g)['path'].endswith('/Documents');original=f.app(g)['path'];assert query(g)==''
   for name in ('Alpha','ALPINE','Beta'):f.create(g,p,name,True)
   assert set(f.names(g))>={'Alpha','ALPINE','Beta'};c.shot(g,'common-frame')
   p.desktop(f.item(g,p,'Beta'),True);assert f.selected(g)==[original+'/Beta']
   filter_name(g,p,'alp');assert set(f.names(g))=={'Alpha','ALPINE'} and not f.selected(g) and f.app(g)['offset']==0;c.shot(g,'filtered-names')
   p.desktop(40013,True);f.menu(g,p,40031);assert query(g)=='alp' and set(f.names(g))=={'Alpha','ALPINE'};p.desktop(40012,True);assert f.view(g)[0]==1 and query(g)=='alp';c.shot(g,'filtered-icons');p.desktop(40012,True);filter_name(g,p,'alp')
   c.key(g,'ret');assert len(f.selected(g))==1 and f.app(g)['path']==original
   c.key(g,'ctrl','a');assert set(f.selected(g))=={original+'/Alpha',original+'/ALPINE'}
   p.desktop(50000,True);assert query(g)=='alp' and set(f.names(g))=={'Alpha','ALPINE'}
   filter_name(g,p,'notfound');assert not f.names(g) and not f.selected(g),(f.names(g),f.selected(g),query(g));c.shot(g,'no-matching-names');c.key(g,'esc');assert query(g)=='' and set(f.names(g))>={'Alpha','ALPINE','Beta'};c.key(g,'esc')
   report['checks'].append('Actual current-folder case-insensitive filtering, hidden-selection reset, filtered Ctrl+A, retained sort/view, non-launching Enter, Refresh retention and recoverable empty state')
   filter_name(g,p,'Beta');p.desktop(61001,True);assert query(g)=='' and not f.selected(g)
   filter_name(g,p,'Alpha');c.key(g,'esc');c.key(g,'esc');filter_name(g,p,'Beta');c.key(g,'ret');c.key(g,'ret');p.drain();assert f.app(g)['path']==original+'/Beta' and query(g)=='' and f.model(g)[0]==first['slot']
   p.desktop(90,True);assert f.app(g)['path']==original and query(g)=='',('Back',f.app(g),query(g),f.history(g));p.desktop(91,True);assert f.app(g)['path']==original+'/Beta',('Forward',f.app(g),f.history(g));p.desktop(24,True);assert f.app(g)['path']==original,('Up',f.app(g),f.history(g))
   filter_name(g,p,'Alpha');c.key(g,'tab');p.desktop(26,True);assert c.flag(g,'file_dialog_state11')==7;c.key(g,'ctrl','f');assert query(g)=='Alpha' and c.flag(g,'file_dialog_state11')==7;c.key(g,'esc');assert query(g)=='Alpha';f.create(g,p,'Gamma',True);assert query(g)=='' and 'Gamma' in f.names(g)
   report['checks'].append('Clear, child/Back/Forward/Up navigation and successful create preserve reachable unfiltered names and actual path history')
   if a.profile=='ordinary':
    filter_name(g,p,'Alpha');c.key(g,'ret');c.key(g,'ctrl','c');f.visit(g,p,'Beta');filter_name(g,p,'missing');c.key(g,'ret');c.key(g,'ctrl','v');finish_job(g,p);assert query(g)=='' and 'Alpha' in f.names(g)
    p.desktop(f.item(g,p,'Alpha'),True);c.key(g,'ctrl','x');p.desktop(24,True);f.visit(g,p,'Gamma');filter_name(g,p,'missing');c.key(g,'ret');c.key(g,'ctrl','v');finish_job(g,p);assert query(g)=='' and 'Alpha' in f.names(g) and original+'/Beta/Alpha' not in f.entries(g) and original+'/Gamma/Alpha' in f.entries(g)
    documents(g,p);report['checks'].append('Real filtered selection copy and move clear only the completed destination query, reveal the resulting name and independently expose the correct native paths')
   filter_name(g,p,'alp');second=t.launch(g,p,'files',1);documents(g,p);assert query(g)=='';filter_name(g,p,'Beta');t.focus(g,p,first);assert query(g)=='alp';t.focus(g,p,second);close(g,p);replacement=t.launch(g,p,'files',1);assert replacement['slot']==second['slot'] and replacement['token']!=second['token'] and query(g)==''
   report['checks'].append('Two real Files windows keep independent queries; closing and reusing a generation clears the old query and cached listing')
   p.desktop(21000,True);assert f.app(g)['mode']==1 and not f.has(g,61000) and f.has(g,90);c.key(g,'ctrl','f');assert 'system folders' in f.app(g)['notice'];c.shot(g,'usb-no-device');p.desktop(90,True);assert not f.app(g)['mode'] and query(g)==''
   if a.profile=='ordinary':
    f.resize(g,p,500,420);c.shot(g,'minimum-frame');rows=f.current_controls(g);toolbar=[r for r in rows if r[1]==f.model(g)[1][1]+86];assert all(a[0]+a[2]<=b[0] for a,b in zip(sorted(toolbar),sorted(toolbar)[1:])),toolbar
   report['checks'].append('USB no-device frame retains real Back and truthful unavailable filter; compact command targets remain separate')
   for theme in ('dark','high-contrast','light'):
    t.launch(g,p,'settings',3)
    if theme=='high-contrast':
     p.desktop(59004,True)
     if not c.flag(g,'access_flags16')&1:p.desktop(60010,True)
    else:
     if c.flag(g,'access_flags16')&1:p.desktop(59004,True);p.desktop(60010,True)
     p.desktop(59000,True);p.desktop(43 if theme=='dark' else 44,True);p.desktop(47,True)
     assert struct.unpack_from('<I',ui.s.s.document(disk,'/System/Settings/appearance11-Owner.bin'),12)[0]==(theme=='dark')
    close(g,p);assert struct.unpack_from('<I',ui.memory(g,ui.symbol('preferences',24,True)[0],24),12)[0]==(theme!='light');c.shot(g,theme)
   report['checks'].append('Actual Files dark/high-contrast/light surfaces follow applied settings after the settings window closes; saved light/dark appearance bytes are independently read')
   t.close_all(g,p);f.same_pages(baseline,f.stats(g));c.idle(g);report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0);(out/'native.log').write_bytes(g.log().encode())
  for n in (1,2):
   boot=ui.guest(work/f'disk-{n}',disk,resolution=resolution,ram=ram,media='installed',ready='M7_DESKTOP_READY');ui.s.normal_boot(boot,work/'install/vars.fd')
   with boot as g:
    p=ui.Pointer(g);p.drain();t.close_all(g,p);t.launch(g,p,'files',1);documents(g,p);assert query(g)=='' and set(f.names(g))>={'Alpha','ALPINE','Beta','Gamma'};c.shot(g,f'disk-only-{n}');c.idle(g);(out/f'disk-{n}.log').write_bytes(g.log().encode())
  report['checks'].append('Completed tasks retain zero managed pages and idle CPUs halt; two independent no-ISO boots retain actual created folders and clear transient filters');report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report),flush=True)
if __name__=='__main__':main()
