"""M11.5 real setup choices, readback, reset and disk-only native desktop."""
import argparse,hashlib,json,struct,time,traceback
import files as f
ui=f.ui;ROOT=ui.ROOT

def flag(g,name,installed=False):
 address,size=ui.symbol(name,4 if name=='controls' else None,installed=installed);return int.from_bytes(ui.memory(g,address,min(size,4)),'little')

def key(g,name):ui.h.key(g,name);ui.Pointer(g).drain()

def text(g,value):
 for c in value:
  if c.isupper():g.qmp('send-key',{'keys':[{'type':'qcode','data':'shift'},{'type':'qcode','data':c.lower()}],'hold-time':35});time.sleep(.12);ui.Pointer(g).drain()
  else:key(g,{' ':'spc','-':'minus'}.get(c,c))

def shot(g,out,name,installed=False):
 print('Capture',name,flush=True)
 if not installed:
  width=flag(g,'width');height=flag(g,'height');left=flag(g,'left');top=flag(g,'top');n=flag(g,'controls')
  assert n<=24;raw=ui.memory(g,ui.symbol('buttons',480)[0],n*20)
  for i in range(n):
   x,y,w,h,action=struct.unpack_from('<5I',raw,i*20);assert w>=36 and h>=36 and x>=left and y>=top and x+w<=left+width and y+h<=top+height,(name,action,x,y,w,h)
 g.qmp('stop')
 try:ui.raw_shot(g,out,name,installed)
 finally:g.qmp('cont')

def wizard(g,p,command):return f.s.wizard(g,p,command)

def options(g):return struct.unpack('<6I',ui.memory(g,ui.symbol('setup11',24)[0],24))

def document(disk,path):return ui.s.s.document(disk,path)

def main():
 a=argparse.ArgumentParser();a.add_argument('--profile',choices=['ordinary','150','4k'],default='ordinary');args=a.parse_args()
 resolution={'ordinary':(1280,800),'150':(1920,1200),'4k':(3840,2160)}[args.profile]
 out=ROOT/'build/m11/setup'/args.profile;out.mkdir(parents=True,exist_ok=True)
 work=ui.q.new_work('m115-setup-'+args.profile);disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
 meta=json.loads((ui.manifest_path11()).read_text());report={'passed':False,'build_id':meta['build_id'],'iso_sha256':meta['artifacts'][ui.IMAGE11+'.iso']['sha256'],'profile':args.profile,'checks':[]}
 user='Alex' if args.profile=='ordinary' else 'Owner';minimal=args.profile=='150'
 try:
  before=ui.q.digest(disk)
  live=ui.guest(work/'install',disk,resolution=resolution)
  with live as g:
   p=ui.Pointer(g);p.drain();shot(g,out,'01-welcome');frames=flag(g,'full_frames75')
   wizard(g,p,2);assert flag(g,'keyboard_page11')==1;shot(g,out,'02-keyboard')
   wizard(g,p,50001);wizard(g,p,50002);key(g,'q');assert ui.memory(g,ui.symbol('keyboard_test11',32)[0],2)==b"'\0"
   wizard(g,p,50003);wizard(g,p,50000);wizard(g,p,50002);text(g,'ready');assert ui.memory(g,ui.symbol('keyboard_test11',32)[0],6)==b'ready\0'
   if args.profile=='150':wizard(g,p,50012);assert flag(g,'scale73')==3
   if args.profile=='ordinary':
    previous=options(g);wizard(g,p,50013);assert options(g)==previous
    assert flag(g,'validation')!=0;shot(g,out,'size-refused-with-explanation')
   wizard(g,p,2);assert flag(g,'step')==1;shot(g,out,'03-disks-unselected')
   # Next is disabled until a full-row disk selection is made.
   n=flag(g,'controls');raw=ui.memory(g,ui.symbol('buttons',480)[0],n*20)
   assert all(struct.unpack_from('<I',raw,i*20+16)[0]!=2 for i in range(n))
   wizard(g,p,100);shot(g,out,'03-disk-selected');wizard(g,p,1);assert flag(g,'keyboard_page11')==1
   assert options(g)[0]==0
   if args.profile=='150':wizard(g,p,50001)
   wizard(g,p,2);assert flag(g,'chosen')==0;wizard(g,p,2)
   assert flag(g,'step')==2;shot(g,out,'04-apps')
   if minimal:wizard(g,p,50102);assert options(g)[5]==0;wizard(g,p,20)
   else:
    wizard(g,p,50101);assert options(g)[5]!=0;wizard(g,p,50104);shot(g,out,'04-more-apps');wizard(g,p,50100)
   selected=options(g)[5];wizard(g,p,2);assert flag(g,'step')==3
   if user!='Owner':
    wizard(g,p,30);text(g,'LongName');key(g,'home');key(g,'delete');key(g,'end');key(g,'backspace')
    assert ui.memory(g,ui.symbol('preferences',40)[0],8).split(b'\0')[0]==b'ongNam'
    g.qmp('send-key',{'keys':[{'type':'qcode','data':'ctrl'},{'type':'qcode','data':'a'}],'hold-time':40});time.sleep(.15);p.drain();text(g,user)
   wizard(g,p,32);wizard(g,p,50301);wizard(g,p,50311);shot(g,out,'05-your-style')
   wizard(g,p,2);assert flag(g,'step')==4;shot(g,out,'06-review')
   wizard(g,p,1);assert options(g)[1]==1 and options(g)[2]==0x182039 and options(g)[5]==selected
   wizard(g,p,2);assert ui.q.digest(disk)==before
   report['checks'].append('Eight-step native setup retains keyboard, app, user/style and disk choices on Back; no disk bytes change before Install')
   assert flag(g,'full_frames75')==frames+(1 if args.profile=='150' else 0)
   report['checks'].append('Next/Back preserve the outer frame; only a real display-size change recreates it')
   start=wizard(g,p,2);g.wait('M6_INSTALL_PASS',start,240);p.drain();shot(g,out,'07-installed-verified')
   settings=document(disk,'/System/Settings/setup.bin');assert settings[:32].split(b'\0')[0]==user.encode();assert struct.unpack_from('<II',settings,32)==(0x9caeff,int(not minimal))
   appearance=document(disk,'/System/Settings/appearance11-'+user+'.bin');assert len(appearance)==352
   assert struct.unpack_from('<8I',appearance)==(0x41313145,1,0x9caeff,1,3 if args.profile=='150' else 0,0x182039,0,0)
   assert document(disk,'/System/Settings/keyboard10.bin')==struct.pack('<II',0x30314c4b,int(args.profile=='150'))
   guidepath='/System/Settings/firstboot11-'+user+'.bin';assert document(disk,guidepath)==struct.pack('<III',0x47313145,1,int(minimal))
   report['checks'].append('Independent GPT/native metadata and payload CRC inspection verifies account, keyboard, appearance and first-start settings before installed startup')
   start=wizard(g,p,84);g.wait('M75_USER_RESTART',start);g.wait('M7_DESKTOP_READY build='+meta['build_id'],start,180);p=ui.Pointer(g);p.drain()
   assert 'M6_INSTALLED_VOLUME' in g.log()[start:] and 'M6_WIZARD_READY' not in g.log()[start:]
   assert flag(g,'guide_open11',True)==int(not minimal);shot(g,out,'08-first-desktop',True)
   if not minimal:

    if args.profile=='4k':p.desktop(46001,True)
    else:key(g,'esc')
    assert flag(g,'guide_open11',True)==0
    assert document(disk,guidepath)==struct.pack('<III',0x47313145,1,1)
   if minimal:
    rows=f.rows(g)
    for path in rows:
     assert not (path.startswith('/Applications/') and rows[path][1]==1),path
    assert any(path.startswith('/System/Packages/') for path in rows)
    p.desktop(0,True);assert flag(g,'launcher',True);shot(g,out,'no-optional-apps-start',True);key(g,'esc')
    p.logical(60,335,True);key(g,'ret');assert f.s.count(g,3)==1
   else:
    f.out=out;p.desktop(94,True);f.create(g,p,'SavedFolder',26);assert '/Users/'+user+'/Documents/SavedFolder' in ui.s.directories(disk)
   shot(g,out,'09-installed-desktop',True)
   # Initial DHCP/clock notifications are legitimate startup paints, not idle polling.
   idle=[]
   for attempt in range(20):
    p.drain();before_paint=ui.memory(g,ui.symbol('paints',8,True)[0],8);time.sleep(.5);after_paint=ui.memory(g,ui.symbol('paints',8,True)[0],8);idle.append(before_paint==after_paint)
    if len(idle)>=3 and all(idle[-3:]):break
   assert len(idle)>=3 and all(idle[-3:]),idle
   report['idle_observations']=idle
   assert g.qmp('human-monitor-command',{'command-line':'info registers -a'}).count('HLT=1')==len(g.qmp('query-cpus-fast'))
   report['checks'].append('Actual retained-ISO reset loads the installed volume; optional guide dismisses durably, saved appearance is active and idle CPUs halt without repaint')
   (out/'install.log').write_bytes(g.log().encode())
  for turn in range(2):
   guest=ui.guest(work/('disk-only-'+str(turn)),disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution);ui.s.normal_boot(guest,live.folder/'vars.fd')
   with guest as g:
    p=ui.Pointer(g);p.drain();assert flag(g,'guide_open11',True)==0
    assert 'M7_DESKTOP_READY build='+meta['build_id'] in g.log();assert 'M6_INSTALLED_VOLUME' in g.log()
    shot(g,out,'disk-only-'+str(turn),True);(out/('disk-only-'+str(turn)+'.log')).write_bytes(g.log().encode())
  report['checks'].append('Two independent disk-only firmware boots reuse installation NVRAM without forced disk priority and retain saved choices and guide dismissal')
  report['passed']=True
 except Exception:
  report['error']=ui.q.clean(traceback.format_exc());raise
 finally:
  (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
