"""Original unmodified 7-Zip copies a Unicode filename into the native editor."""
import argparse,ctypes,hashlib,json,os,struct,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
from window144_native import ui,c,f,t,clone,library,StoppedDisk,task,output
from original_window_trace4 import views,wait_for
from original_menu145_run import commands
import dialogs_native as dialogs
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--profile',choices=['compact','ordinary','4k'],default='compact');profile=parser.parse_args().profile
 out=ROOT/'build/m14-native/stage6'/('original-clipboard'+(''if profile=='compact'else'-'+profile));out.mkdir(parents=True,exist_ok=True);c.OUT=out;meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage6'/('apps'+(''if profile=='compact'else'-'+profile))/'results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/('EngineOS/Tests/M6/m146-window-apps'+(''if profile=='compact'else'-'+profile))/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m146-original-clipboard');mounted=StoppedDisk(disk,library());folder='/Users/Owner/Documents';leaf='m146-é.txt';expected=leaf.encode('utf-8');payload=b'Original source file must remain unchanged.\n'
 try:mounted.put(folder+'/'+leaf,payload)
 finally:mounted.close()
 original=ui.s.s.document(disk,'/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',8*1024**2);digest=hashlib.sha256(original).hexdigest();assert digest=='a12710799d5cb9b3076b86dd0f92d4a503b7062bc3efac62b7f4cb8a74e05931'
 report=dict(passed=False,build_id=meta['build_id'],original_sha256=digest,fixture_sha256=hashlib.sha256(payload).hexdigest(),clone=cloned,profile=profile,scope='Actual original 7-Zip Unicode filename copy, source exit and native-editor paste/save with independent byte verification; not complete original archive/document tasks')
 try:
  boot=ui.guest(work/'browse',disk,media='installed',ready='M7_DESKTOP_READY',ram=1024 if profile=='4k'else 512 if profile=='ordinary'else 128,resolution=(3840,2160)if profile=='4k'else(1920,1080)if profile=='ordinary'else(1280,800));ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);editor=t.launch(g,p,'text editor',2);assert t.app_view(g).length==0;saved_path=f.app(g,editor['slot'])['path'];front=t.launch(g,p,'windows apps',19);task(g,p,12005);before=f.stats(g)[0];at=len(g.log());p.desktop(12100,True,settle=False);g.wait('M8_CPL3_CREATED',at);wait_for(g,lambda:any(v['class_name']=='7-Zip::FM'and v['visible']for v in views(g)));p.drain();scale=c.flag(g,'scale73')/2
   def list_():return next(v for v in views(g)if v['class_name']=='SysListView32'and v['visible'])
   def labels():return [v['text']for v in commands(g,list_()['handle'])]
   def point(label):
    table={v['handle']:v for v in views(g)};node=list_();draw=next(v for v in commands(g,node['handle'])if v['text']==label);border=1 if node['style']&0x800000 else 0;x=node['bounds'][0]+border+draw['bounds'][0]+4;y=node['bounds'][1]+border+draw['bounds'][1]+8
    while node['parent']:
     node=table[node['parent']];border=1 if node['style']&0x800000 else 0;x+=node['bounds'][0]+border;y+=node['bounds'][1]+(border if node['parent']else 40+node['menu_height'])
    p.move(int(x*scale),int(y*scale))
   point('Documents');p.down(True);p.down(False);p.drain();time.sleep(.6);point('Documents');p.down(True);p.down(False);p.down(True);p.down(False);p.drain();wait_for(g,lambda:leaf in labels());report['documents_labels']=labels()
   time.sleep(.6);point(leaf);p.down(True);p.down(False);p.drain();c.shot(g,'original-leaf-selection');c.key(g,'ctrl','c')
   def copied():
    size=ui.integer(g,'clipboard_length',True)
    report['copy_state']=dict(bytes=size,kind=ui.integer(g,'clipboard_kind11',True),open=ui.memory(g,ui.symbol('clip_open146',1,True)[0],1)[0],revision=struct.unpack('<Q',ui.memory(g,ui.symbol('clipboard_revision146',installed=True)[0],8))[0],focus=list(struct.unpack('<4Q',ui.memory(g,ui.symbol('ui_focus144',installed=True)[0],32))))
    return size==len(expected) and ui.memory(g,ui.symbol('clipboard',installed=True)[0],size)==expected
   wait_for(g,copied);assert ui.integer(g,'clipboard_kind11',True)==1;report['original_copied_utf8_hex']=expected.hex();c.shot(g,'original-unicode-copy')
   p.desktop(49002,True);g.wait('M8_JOB_DONE',at);p.drain();state,command,status=struct.unpack('<3I',ui.memory(g,ui.symbol('info8',installed=True)[0],12));assert state==2 and not status,(state,command,status,output(g));assert copied();report['source_exit_keeps_text']=True
   report['declared_shared_format_pages']=ui.integer(g,'clipboard_resident144',True);assert report['declared_shared_format_pages']==1
   report['retained_original_process_pages']=f.stats(g)[0]-before-report['declared_shared_format_pages'];assert report['retained_original_process_pages']==0
   t.focus(g,p,editor);p.desktop(23,True);wait_for(g,lambda:bytes(t.app_view(g).text)==expected);assert t.app_view(g).length==len(expected);c.shot(g,'native-editor-received-original-copy')
   p.desktop(20,True);wait_for(g,lambda:t.app_view(g).dirty==0);report['saved_native_path']=saved_path;assert saved_path.startswith('/Users/Owner/Documents/') and saved_path!=folder+'/'+leaf
   p.desktop(49002,True);editor=t.launch(g,p,'text editor',2);p.desktop(54000,True);p.desktop(54016,True);dialogs.choose(g,p,saved_path.rsplit('/',1)[1]);c.key(g,'ret');wait_for(g,lambda:bytes(t.app_view(g).text)==expected);assert not t.app_view(g).dirty;report['native_reopened_unicode_bytes']=True;c.shot(g,'native-editor-reopened-original-copy')
   c.key(g,'home')
   for _ in range(6):c.key(g,'right')
   assert t.app_view(g).cursor==7;c.key(g,'left');assert t.app_view(g).cursor==5;c.key(g,'right');assert t.app_view(g).cursor==7;c.key(g,'backspace');assert bytes(t.app_view(g).text)==b'm146-.txt'
   c.key(g,'ctrl','a');c.key(g,'ctrl','v');assert bytes(t.app_view(g).text)==expected;c.key(g,'home')
   for _ in range(5):c.key(g,'right')
   assert t.app_view(g).cursor==5;c.key(g,'delete');assert bytes(t.app_view(g).text)==b'm146-.txt';c.key(g,'ctrl','a');c.key(g,'ctrl','v');assert bytes(t.app_view(g).text)==expected;p.desktop(20,True);assert not t.app_view(g).dirty;report['scalar_cursor_backspace_delete_preserve_utf8']=True
   p.desktop(49002,True);t.focus(g,p,front);value=task(g,p,12005);assert 'Mapped original image: 7z.exe' in value and '7-Zip' in value;report['subsequent_original_console_success']=True
  assert ui.s.s.document(disk,saved_path,8192)==expected;assert ui.s.s.document(disk,folder+'/'+leaf,4096)==payload;report['native_saved_bytes_verified']=True;report['source_file_unchanged']=True;report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
