"""Use the real unmodified 7-Zip Info button and original resource/dialog procedure."""
import hashlib,json,os,struct,time,traceback
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
from window144_native import ui,c,f,t,clone,task,output
from original_window_trace4 import views

def wait_for(g,predicate,seconds=30):
 deadline=time.monotonic()+seconds
 while time.monotonic()<deadline:
  state,command,status=struct.unpack('<3I',ui.memory(g,ui.symbol('info8',installed=True)[0],12))
  if state==3 or(state==2 and status):raise AssertionError((state,command,status,output(g)))
  result=predicate()
  if result:return result
  time.sleep(.03)
 raise TimeoutError((output(g),views(g)))

def main():
 out=ROOT/'build/m14-native/stage5/original-about';out.mkdir(parents=True,exist_ok=True);c.OUT=out;meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage5/apps/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m145-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m145-original-about')
 original=ui.s.s.document(disk,'/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',8*1024**2);digest=hashlib.sha256(original).hexdigest();assert digest=='a12710799d5cb9b3076b86dd0f92d4a503b7062bc3efac62b7f4cb8a74e05931'
 report=dict(passed=False,stage='M14.5 development',build_id=meta['build_id'],original_sha256=digest,clone=cloned,scope='Original toolbar/Info dialog/callback/close development task; not complete M14.5 or archive/navigation qualification')
 try:
  boot=ui.guest(work/'about',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19);task(g,p,12005);before=f.stats(g)[0];at=len(g.log());p.desktop(12100,True,settle=False);g.wait('M8_CPL3_CREATED',at);root=wait_for(g,lambda:next((v for v in views(g)if v['class_name']=='7-Zip::FM'and v['visible']),None));p.drain();c.shot(g,'original-toolbar')
   # Locate the real yellow Info artwork in the actual physical toolbar pixels.
   image=Image.open(out/'original-toolbar.png').convert('RGB');x,y,w,h=root['bounds'];scale=c.flag(g,'scale73')/2;points=[]
   for yy in range(int((y+42)*scale),int((y+76)*scale)):
    for xx in range(int((x+1)*scale),int((x+w-1)*scale)):
     r,green,b=image.getpixel((xx,yy))
     if r>180 and green>180 and b<90:points.append((xx,yy))
   assert points,'Original Info image not visible';px=(min(v[0]for v in points)+max(v[0]for v in points))//2;py=(min(v[1]for v in points)+max(v[1]for v in points))//2
   p.move(px,py);p.down(True);p.down(False);p.drain();modal=wait_for(g,lambda:next((v for v in views(g)if v['class_name']=='#32770'and v['visible']),None));assert not next(v for v in views(g)if v['handle']==root['handle'])['enabled'];c.shot(g,'original-about-dialog');report['modal_title']=modal['title'];report['original_dialog_controls']=views(g)
   button=next(v for v in views(g)if v['parent']==modal['handle']and v['class_name']=='Button'and v['title']=='OK');bx,by,bw,bh=button['bounds'];mx,my,_,_=modal['bounds'];p.move(int((mx+1+bx+bw//2)*scale),int((my+40+by+bh//2)*scale));p.down(True);p.down(False);p.drain();wait_for(g,lambda:not any(v['class_name']=='#32770'for v in views(g)));assert next(v for v in views(g)if v['handle']==root['handle'])['enabled'];report['original_owner_restored']=True
   p.desktop(49002,True);g.wait('M8_JOB_DONE',at);p.drain();state,command,status=struct.unpack('<3I',ui.memory(g,ui.symbol('info8',installed=True)[0],12));assert state==2 and not status,(state,command,status,output(g));report['retained_pages']=f.stats(g)[0]-before;assert report['retained_pages']==1;assert len(t.records(g))==1 and t.records(g)[0]['token']==front['token'];report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());report['output']=output(g)if'g'in locals()else'';raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
