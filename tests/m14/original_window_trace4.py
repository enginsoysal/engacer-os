"""Original GUI functional development trace; mixed runtime, never ISO acceptance."""
import hashlib,json,os,struct,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tests/m14'))
from window144_native import ui,c,f,t,clone,library,StoppedDisk,output,drag
import capture14
capture14.bind(ui)

def controls(g):
 count=ui.integer(g,'control_count',True);raw=ui.memory(g,ui.symbol('controls',65536,True)[0],count*32)
 return [struct.unpack_from('<iiiiQI',raw,n*32)for n in range(count)]

def views(g):
 pointers=struct.unpack('<32Q',ui.memory(g,ui.symbol('ui_windows144',installed=True)[0],256));out=[]
 for pointer in pointers:
  if not pointer:continue
  raw=ui.memory(g,pointer,840);h,parent,owner=struct.unpack_from('<3Q',raw);x,y,w,height=struct.unpack_from('<4i',raw,24);style,ex,visible,enabled=struct.unpack_from('<4I',raw,40)
  wide=lambda a,b:raw[a:b].decode('utf-16-le').split('\0')[0]
  out.append(dict(handle=h,parent=parent,owner=owner,bounds=[x,y,w,height],style=style,visible=visible,enabled=enabled,title=wide(56,312),class_name=wide(312,440)))
 return out

def wait_for(g,predicate,seconds=15):
 deadline=time.monotonic()+seconds
 while time.monotonic()<deadline:
  raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384);state=struct.unpack_from('<I',raw)[0]
  if state==3:raise AssertionError((raw[304:496].split(b'\0')[0],output(g)))
  value=predicate()
  if value:return value
  time.sleep(.03)
 raise TimeoutError((output(g),views(g),t.records(g)))

def main():
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--runtime',required=True);args=parser.parse_args();rt=Path(args.runtime).resolve();assert rt.is_relative_to((ROOT/'build/m14-native').resolve());prior=json.loads((rt.parent.parent/'results.json').read_text());assert hashlib.sha256(rt.read_bytes()).hexdigest()==prior['runtime_sha256']
 out=ROOT/'build/m14-native/stage4/original-window-trace';out.mkdir(parents=True,exist_ok=True);c.OUT=out;meta=json.loads(ui.manifest_path12().read_text());assert prior['kernel_build_id']==meta['build_id'];base=json.loads((ROOT/'build/m14-native/stage4/apps/results.json').read_text());assert base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m144-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m144-original-window-functional');mounted=StoppedDisk(disk,library())
 try:mounted.put('/System/Windows/runtime8.elf',rt.read_bytes())
 finally:mounted.close()
 original=ui.s.s.document(disk,'/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',8*1024**2);digest=hashlib.sha256(original).hexdigest();assert digest=='a12710799d5cb9b3076b86dd0f92d4a503b7062bc3efac62b7f4cb8a74e05931'
 report=dict(passed=False,original_gui_qualified=False,scope='Original GUI functional diagnostic with mixed identified runtime; NOT stage or ISO qualification',kernel_build_id=meta['build_id'],runtime_sha256=prior['runtime_sha256'],runtime_sources=prior['runtime_sources'],original_sha256=digest,clone=cloned,checks=[])
 try:
  boot=ui.guest(work/'original-functional',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19);before=f.stats(g)[0];at=len(g.log());p.desktop(12100,True,settle=False);g.wait('M8_CPL3_CREATED',at)
   wait_for(g,lambda:len(t.records(g))==2);p.drain();c.shot(g,'original-initial');report['checks'].append({'name':'original window visible','views':views(g)})
   edit=next(v for v in views(g)if v['class_name']=='Edit'and v['visible']);table={v['handle']:v for v in views(g)};x,y=0,0;node=edit
   while node['parent']:
    border=1 if node['style']&0x800000 else 0;x+=node['bounds'][0]+border;y+=node['bounds'][1]+border;node=table[node['parent']]
   x+=node['bounds'][0]+1;y+=node['bounds'][1]+40;scale=c.flag(g,'scale73')/2;p.move(int((x+8)*scale),int((y+8)*scale));p.down(True);p.down(False);p.drain();c.key(g,'z');changed=wait_for(g,lambda:next((v for v in views(g)if v['handle']==edit['handle']and 'z'in v['title']),None));c.key(g,'backspace');p.drain();report['checks'].append({'name':'actual original edit receives native input','after_character':changed['title']});c.shot(g,'original-input')
   x,y,w,h=f.model(g)[1];drag(g,p,x+200,y+20,x+230,y+40);moved=f.model(g)[1];assert moved[:2]!=(x,y);report['checks'].append({'name':'native movement','bounds':list(moved)})
   x,y,w,h=moved;drag(g,p,x+w-4,y+h-4,x+w+20,y+h+15);resized=f.model(g)[1];assert resized[2:]!=(w,h);report['checks'].append({'name':'original resize handling','bounds':list(resized)});c.shot(g,'original-resized')
   target=next(v for v in t.records(g)if v['slot']==f.model(g)[0]);owner=target['token'];minimum=next(r for r in controls(g)if r[5]==49000 and r[4]==owner)
   p.logical(minimum[0]+minimum[2]//2,minimum[1]+minimum[3]//2,True);p.drain();wait_for(g,lambda:next(v for v in t.records(g)if v['token']==owner)['minimized']);report['checks'].append({'name':'native minimize','window':owner})
   t.focus(g,p,target);p.drain();wait_for(g,lambda:not next(v for v in t.records(g)if v['token']==owner)['minimized']);report['checks'].append({'name':'exact grouped taskbar restore','window':owner})
   p.desktop(49001,True);p.drain();wait_for(g,lambda:len(t.records(g))==2);p.desktop(49001,True);p.drain();report['checks'].append({'name':'native maximize and restore'});c.shot(g,'original-restored')
   p.desktop(49002,True);g.wait('M8_JOB_DONE',at);p.drain();raw=ui.memory(g,ui.symbol('info8',installed=True)[0],12);assert struct.unpack('<3I',raw)[0]==2 and struct.unpack('<3I',raw)[2]==0,(raw,output(g));assert len(t.records(g))==1 and t.records(g)[0]['token']==front['token'];assert ui.integer(g,'ui_resident144',True)==0;report['checks'].append({'name':'original close returns success and releases GUI pages','retained_pages':f.stats(g)[0]-before});report['output']=output(g);report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps({k:v for k,v in report.items()if k!='runtime_sources'},indent=2),flush=True)
if __name__=='__main__':main()
