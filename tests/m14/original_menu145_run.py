"""Reach the original unmodified 7-Zip About dialog through its real menus."""
import argparse,hashlib,json,os,struct,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
from window144_native import ui,c,f,t,clone,task,output
from original_window_trace4 import views,wait_for
def commands(g,handle,menu=False):
 pointers=struct.unpack('<32Q',ui.memory(g,ui.symbol('ui_windows144',installed=True)[0],256))
 for pointer in pointers:
  if not pointer:continue
  raw=ui.memory(g,pointer,912)
  if struct.unpack_from('<Q',raw)[0]!=handle:continue
  count=struct.unpack_from('<I',raw,892 if menu else 852)[0];assert count<=(64 if menu else 224)
  page=struct.unpack_from('<Q',raw,904 if menu else 864)[0];out=[];visited=set()
  while count:
   assert page and page not in visited;visited.add(page);data=ui.memory(g,page,3872)
   for at in range(min(count,7)):
    record=data[8+at*552:8+(at+1)*552];kind=struct.unpack_from('<I',record,32)[0]
    if kind==2:out.append(dict(bounds=list(struct.unpack_from('<4i',record)),text=record[40:].split(b'\0')[0].decode('utf-8')))
   count-=min(count,7);page=struct.unpack_from('<Q',data)[0]
  return out
 raise AssertionError('Missing owned native window')
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--profile',choices=['compact','4k'],default='compact');args=parser.parse_args()
 out=ROOT/'build/m14-native/stage5'/('original-menu-'+args.profile);out.mkdir(parents=True,exist_ok=True);c.OUT=out;meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage5'/('apps'if args.profile=='compact'else'apps-4k')/'results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/('EngineOS/Tests/M6/m145-window-apps'+(''if args.profile=='compact'else'-4k'))/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m145-original-menu-'+args.profile)
 original=ui.s.s.document(disk,'/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',8*1024**2);digest=hashlib.sha256(original).hexdigest();assert digest=='a12710799d5cb9b3076b86dd0f92d4a503b7062bc3efac62b7f4cb8a74e05931'
 report=dict(passed=False,profile=args.profile,build_id=meta['build_id'],original_sha256=digest,clone=cloned,scope='Original menu/About/callback/close development task; not full GUI archive/navigation or M14.5 acceptance')
 try:
  boot=ui.guest(work/'original-menu',disk,media='installed',ready='M7_DESKTOP_READY',resolution=(1280,800)if args.profile=='compact'else(3840,2160),ram=128 if args.profile=='compact'else 1024);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19);task(g,p,12005);before=f.stats(g)[0];at=len(g.log());p.desktop(12100,True,settle=False);g.wait('M8_CPL3_CREATED',at);root=wait_for(g,lambda:next((v for v in views(g)if v['class_name']=='7-Zip::FM'and v['visible']),None));p.drain();scale=c.flag(g,'scale73')/2
   def click(x,y):p.move(int(x*scale),int(y*scale));p.down(True);p.down(False);p.drain()
   bar=commands(g,root['handle'],True);report['original_bar_labels']=[v['text']for v in bar];help_=next(v for v in bar if v['text']=='Help');c.shot(g,'original-menu-bar');click(root['bounds'][0]+1+help_['bounds'][0]+4,root['bounds'][1]+52)
   popup=wait_for(g,lambda:next((v for v in views(g)if v['class_name']=='Engacer.Menu145'and v['visible']),None));p.drain();labels=commands(g,popup['handle']);report['original_popup_labels']=[v['text']for v in labels];about=next(v for v in labels if v['text'].startswith('About'));c.shot(g,'original-help-menu')
   px,py,_,_=popup['bounds'];click(root['bounds'][0]+1+px+1+about['bounds'][0]+4,root['bounds'][1]+40+root['menu_height']+py+1+about['bounds'][1]+8)
   modal=wait_for(g,lambda:next((v for v in views(g)if v['class_name']=='#32770'and v['visible']),None));p.drain();assert not next(v for v in views(g)if v['handle']==root['handle'])['enabled'];report['original_dialog_title']=modal['title'];report['original_dialog_controls']=views(g);c.shot(g,'original-about-dialog')
   button=next(v for v in views(g)if v['parent']==modal['handle']and v['class_name']=='Button'and v['title']=='OK');bx,by,bw,bh=button['bounds'];mx,my,_,_=modal['bounds'];click(mx+1+bx+bw//2,my+40+by+bh//2);wait_for(g,lambda:not any(v['class_name']=='#32770'for v in views(g)));assert next(v for v in views(g)if v['handle']==root['handle'])['enabled'];p.desktop(49002,True);g.wait('M8_JOB_DONE',at);p.drain();state,command,status=struct.unpack('<3I',ui.memory(g,ui.symbol('info8',installed=True)[0],12));assert state==2 and not status,(state,command,status,output(g));report['retained_pages']=f.stats(g)[0]-before;assert report['retained_pages']==1;assert len(t.records(g))==1 and t.records(g)[0]['token']==front['token'];report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
