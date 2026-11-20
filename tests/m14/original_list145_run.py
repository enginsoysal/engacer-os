"""Unmodified original 7-Zip selects and browses real granted document folders."""
import ctypes,hashlib,json,os,struct,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
from window144_native import ui,c,f,t,clone,library,StoppedDisk,task,output
from original_window_trace4 import views,wait_for
from original_menu145_run import commands
def main():
 out=ROOT/'build/m14-native/stage5/original-list';out.mkdir(parents=True,exist_ok=True);c.OUT=out;meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage5/apps/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m145-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m145-original-list');mounted=StoppedDisk(disk,library());folder='/Users/Owner/Documents/M145-navigation';payload=b'Original application enumeration must preserve these bytes.\n'
 try:assert mounted.lib.v6_mkdir(ctypes.byref(mounted.volume),folder.encode())==0;mounted.put(folder+'/notes.txt',payload)
 finally:mounted.close()
 original=ui.s.s.document(disk,'/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',8*1024**2);digest=hashlib.sha256(original).hexdigest();assert digest=='a12710799d5cb9b3076b86dd0f92d4a503b7062bc3efac62b7f4cb8a74e05931'
 report=dict(passed=False,build_id=meta['build_id'],original_sha256=digest,fixture_sha256=hashlib.sha256(payload).hexdigest(),clone=cloned,scope='Original granted Documents folder selection/browse/back task; not complete archive tasks or M14.5 acceptance')
 try:
  boot=ui.guest(work/'browse',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19);task(g,p,12005);before=f.stats(g)[0];at=len(g.log());p.desktop(12100,True,settle=False);g.wait('M8_CPL3_CREATED',at);wait_for(g,lambda:any(v['class_name']=='7-Zip::FM'and v['visible']for v in views(g)));p.drain();scale=c.flag(g,'scale73')/2
   def list_():return next(v for v in views(g)if v['class_name']=='SysListView32'and v['visible'])
   def labels():return [v['text']for v in commands(g,list_()['handle'])]
   def point(label):
    table={v['handle']:v for v in views(g)};node=list_();draw=next(v for v in commands(g,node['handle'])if v['text']==label);border=1 if node['style']&0x800000 else 0;x=node['bounds'][0]+border+draw['bounds'][0]+4;y=node['bounds'][1]+border+draw['bounds'][1]+8
    while node['parent']:
     node=table[node['parent']];border=1 if node['style']&0x800000 else 0;x+=node['bounds'][0]+border;y+=node['bounds'][1]+(border if node['parent']else 40+node['menu_height'])
    p.move(int(x*scale),int(y*scale))
   point('Documents');p.down(True);p.down(False);p.drain();assert 'Documents'in labels();report['single_click_keeps_root']=True;c.shot(g,'original-single-selection')
   time.sleep(.6);point('Documents');p.down(True);p.down(False);p.down(True);p.down(False);p.drain();wait_for(g,lambda:'M145-navigation'in labels());report['documents_labels']=labels();c.shot(g,'original-documents')
   time.sleep(.6);point('M145-navigation');p.down(True);p.down(False);p.down(True);p.down(False);p.drain();wait_for(g,lambda:'notes.txt'in labels());report['nested_labels']=labels();assert str(len(payload))in labels(),('Actual file size missing',len(payload),labels());report['actual_size_visible']=True;c.shot(g,'original-real-folder');c.key(g,'backspace');wait_for(g,lambda:'M145-navigation'in labels());report['back_to_parent']=True
   p.desktop(49002,True);g.wait('M8_JOB_DONE',at);p.drain();state,command,status=struct.unpack('<3I',ui.memory(g,ui.symbol('info8',installed=True)[0],12));assert state==2 and not status,(state,command,status,output(g));report['retained_pages']=f.stats(g)[0]-before;assert report['retained_pages']==1;assert len(t.records(g))==1 and t.records(g)[0]['token']==front['token']
  assert ui.s.s.document(disk,folder+'/notes.txt',4096)==payload;report['native_fixture_bytes_unchanged']=True;report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
