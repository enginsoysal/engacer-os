"""Run real Win64 process isolation, original child apps and surviving children."""
import hashlib,io,json,os,time,traceback,zipfile
from pathlib import Path
from thread_native2 import ui,c,f,t,task
from access_fixtures16 import clone
from fixture1 import library,StoppedDisk
from process_fixtures2 import build
ROOT=Path(__file__).resolve().parents[2]
def main():
 out=ROOT/'build/m14-native/stage2/processes';out.mkdir(parents=True,exist_ok=True);meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage2/compact/results.json').read_text(encoding='utf-8'));assert base['passed'] and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage2-compact'/base['owned_fixture']/'owned.img';work,disk,_=clone(ui,source,'m142-processes');report=dict(passed=False,build_id=meta['build_id'],scope='Synthetic Windows parent/isolation plus actual unmodified original 7-Zip children; not generic Win64 compatibility')
 product='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}';payload=b'Created by the native Windows process integration test.\n'
 try:
  boot=ui.guest(work/'prepare',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);p.desktop(12001,True);task(g,p,12003)
   dirs=[path for path,row in f.entries(g).items() if row['kind']==2 and path.startswith('/Users/') and path.endswith('/Documents')];assert len(dirs)==1,dirs;documents=dirs[0]
  original=ui.s.s.document(disk,product+'/7z.exe',8*1024**2);fixtures=build();mounted=StoppedDisk(disk,library())
  try:
   mounted.put(product+'/original7z.exe',original);mounted.put(product+'/child.exe',(fixtures/'parent.exe').read_bytes());mounted.put(product+'/7z.exe',(fixtures/'parent.exe').read_bytes());mounted.put(documents+'/child-input.txt',payload)
  finally:mounted.close()
  boot=ui.guest(work/'processes',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);text=task(g,p,12005);assert 'M142_PROCESSES_ISOLATION_ORIGINAL_CHILDREN_PASS' in text,text
   before=f.stats(g)[0];samples=[]
   for turn in range(20):
    text=task(g,p,12005);assert 'M142_PROCESSES_ISOLATION_ORIGINAL_CHILDREN_PASS' in text,text;delta=f.stats(g)[0]-before;assert not delta,(turn,delta);samples.append({'turn':turn+1,'retained_pages':delta})
   report['process_samples']=samples;report['parent_output']=text;(out/'processes.log').write_bytes(g.log().encode('utf-8'));t.close_all(g,p)
  archives={}
  for name in ['child-a.zip','child-b.zip']:
   data=ui.s.s.document(disk,documents+'/'+name,8*1024**2)
   with zipfile.ZipFile(io.BytesIO(data)) as archive:assert archive.read('child-input.txt')==payload
   archives[name]={'sha256':hashlib.sha256(data).hexdigest(),'original_child_output_matches':True}
  report['actual_original_archives']=archives;report['original_7zip_exe_sha256']=hashlib.sha256(original).hexdigest()
  mounted=StoppedDisk(disk,library())
  try:mounted.put(product+'/7z.exe',(fixtures/'survivor.exe').read_bytes())
  finally:mounted.close()
  boot=ui.guest(work/'survivor',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);before=f.stats(g)[0];samples=[]
   for turn in range(2):
    at=len(g.log());text=task(g,p,12005);part=g.log()[at:];assert 'M142_CHILD_SURVIVED_PARENT_PASS' in text and text.index('M142_PARENT_EXIT_BEGIN')<text.index('M142_CHILD_SURVIVED_PARENT_PASS'),text;assert part.index('M142_ROOT_EXIT')<part.index('M142_CHILD_EXIT'),part
    delta=f.stats(g)[0]-before;assert delta==(4 if turn==0 else 0),(turn,delta)
    if not turn:before=f.stats(g)[0]
    samples.append({'turn':turn+1,'retained_pages':delta,'root_exit_precedes_child_exit':True})
   report['survivor_samples']=samples;report['survivor_output']=text;(out/'survivor.log').write_bytes(g.log().encode('utf-8'));t.close_all(g,p);t.launch(g,p,'clock',8);t.close_all(g,p)
  saved=ui.s.s.document(disk,documents+'/child-survivor.txt',4096);assert saved==b'The child continued after its parent exited.\n';report['survivor_saved_sha256']=hashlib.sha256(saved).hexdigest();report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode('utf-8'));print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
