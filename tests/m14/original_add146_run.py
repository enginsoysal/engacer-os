"""Read-only native diagnostic of original unmodified 7-Zip Add action."""
import argparse,ctypes,hashlib,json,os,struct,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
from window144_native import ui,c,f,t,clone,library,StoppedDisk,task,output
from original_window_trace4 import views,wait_for
from original_menu145_run import commands
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--profile',choices=['compact','ordinary','4k'],default='compact');profile=parser.parse_args().profile
 out=ROOT/'build/m14-native/stage6'/('original-add-probe'+(''if profile=='compact'else'-'+profile));out.mkdir(parents=True,exist_ok=True);c.OUT=out;meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage6'/('apps'+(''if profile=='compact'else'-'+profile))/'results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/('EngineOS/Tests/M6/m146-window-apps'+(''if profile=='compact'else'-'+profile))/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m146-original-add-probe');mounted=StoppedDisk(disk,library());folder='/Users/Owner/Documents';leaf='m146-é.txt';expected=leaf.encode('utf-8');payload=b'Original source file must remain unchanged.\n'
 invalid={
  'm146-invalid-overlong.txt':bytes.fromhex('c0af'),
  'm146-invalid-surrogate.txt':bytes.fromhex('eda080'),
  'm146-invalid-range.txt':bytes.fromhex('f4908080'),
  'm146-invalid-tail.txt':b'A'*4095+bytes.fromhex('f09f'),
  'm146-invalid-nul.txt':b'valid'+bytes([0])+b'tail',
  'm146-invalid-control.txt':b'valid'+bytes([1])+b'tail'}
 try:
  mounted.put(folder+'/'+leaf,payload)
  for name,data in invalid.items():mounted.put(folder+'/'+name,data)
 finally:mounted.close()
 original=ui.s.s.document(disk,'/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',8*1024**2);digest=hashlib.sha256(original).hexdigest();assert digest=='a12710799d5cb9b3076b86dd0f92d4a503b7062bc3efac62b7f4cb8a74e05931'
 helper=ui.s.s.document(disk,'/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zG.exe',8*1024**2);helper_digest=hashlib.sha256(helper).hexdigest();assert helper_digest=='5eb5d21003927be4d53401b9b6bbe8a787caabb38eaafaf0d429a136d7031621'
 report=dict(passed=False,original_helper_sha256=helper_digest,build_id=meta['build_id'],original_sha256=digest,fixture_sha256=hashlib.sha256(payload).hexdigest(),clone=cloned,profile=profile,scope='Original 7-Zip Add-action diagnostic only; no complete archive/common-dialog task qualification')
 try:
  boot=ui.guest(work/'browse',disk,media='installed',ready='M7_DESKTOP_READY',ram=1024 if profile=='4k'else 512 if profile=='ordinary'else 128,resolution=(3840,2160)if profile=='4k'else(1920,1080)if profile=='ordinary'else(1280,800));ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p)
   def choose_path(path):
    index=f.entries(g)[path]['index']
    for _ in range(128):
     if any(row[5]==55000+index for row in f.controls(g)):break
     p.desktop(54023,True)
    else:raise AssertionError(('Picker entry unavailable',path))
    p.desktop(55000+index,True)
   editor=t.launch(g,p,'text editor',2);assert t.app_view(g).length==0;saved_path=f.app(g,editor['slot'])['path'];front=t.launch(g,p,'windows apps',19);task(g,p,12005);before=f.stats(g)[0];at=len(g.log());p.desktop(12100,True,settle=False);g.wait('M8_CPL3_CREATED',at);wait_for(g,lambda:any(v['class_name']=='7-Zip::FM'and v['visible']for v in views(g)));p.drain();scale=c.flag(g,'scale73')/2
   def list_():return next(v for v in views(g)if v['class_name']=='SysListView32'and v['visible'])
   def labels():return [v['text']for v in commands(g,list_()['handle'])]
   def point(label):
    table={v['handle']:v for v in views(g)};node=list_();draw=next(v for v in commands(g,node['handle'])if v['text']==label);border=1 if node['style']&0x800000 else 0;x=node['bounds'][0]+border+draw['bounds'][0]+4;y=node['bounds'][1]+border+draw['bounds'][1]+8
    while node['parent']:
     node=table[node['parent']];border=1 if node['style']&0x800000 else 0;x+=node['bounds'][0]+border;y+=node['bounds'][1]+(border if node['parent']else 40+node['menu_height'])
    p.move(int(x*scale),int(y*scale))
   point('Documents');p.down(True);p.down(False);p.drain();time.sleep(.6);point('Documents');p.down(True);p.down(False);p.down(True);p.down(False);p.drain();wait_for(g,lambda:leaf in labels());report['documents_labels']=labels()
   time.sleep(.6);point(leaf);p.down(True);p.down(False);p.drain();c.shot(g,'original-add-selected')
   table={v['handle']:v for v in views(g)};node=next(v for v in table.values()if v['class_name']=='ToolbarWindow32'and v['visible']);draw=next(v for v in commands(g,node['handle'])if v['text']=='Add');border=1 if node['style']&0x800000 else 0;x=node['bounds'][0]+border+draw['bounds'][0]+4;y=node['bounds'][1]+border+draw['bounds'][1]+8
   while node['parent']:
    node=table[node['parent']];border=1 if node['style']&0x800000 else 0;x+=node['bounds'][0]+border;y+=node['bounds'][1]+(border if node['parent']else 40+node['menu_height'])
   p.move(int(x*scale),int(y*scale));p.down(True);p.down(False);p.drain();deadline=time.monotonic()+20
   while time.monotonic()<deadline:
    state,command,status=struct.unpack('<3I',ui.memory(g,ui.symbol('info8',installed=True)[0],12));report['worker_state']=[state,command,status];report['output']=output(g);report['views']=views(g);report['maximum_observed_windows']=max(report.get('maximum_observed_windows',0),len(report['views']))
    if state==3 or 'Not implemented:'in report['output']or any('Add to Archive'in v['title']for v in report['views']):break
    time.sleep(.1)
   c.shot(g,'original-add-result');report['scope']='Read-only native diagnostic of the actual original 7-Zip Add action; no archive/common-dialog compatibility qualification';report['diagnostic_completed']=True;report['passed']=False
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
