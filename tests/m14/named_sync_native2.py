"""Actual Windows named event/semaphore/timer sharing and creator lifetime."""
import hashlib,json,os,traceback
from pathlib import Path
from thread_native2 import ui,c,f,t,task
from access_fixtures16 import clone
from fixture1 import library,StoppedDisk
from named_sync_fixtures2 import build
ROOT=Path(__file__).resolve().parents[2]
def main():
 out=ROOT/'build/m14-native/stage2/named-sync';out.mkdir(parents=True,exist_ok=True);meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage2/compact/results.json').read_text(encoding='utf-8'));assert base['passed'] and base['build_id']==meta['build_id'];source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage2-compact'/base['owned_fixture']/'owned.img';work,disk,_=clone(ui,source,'m142-named-sync');report=dict(passed=False,build_id=meta['build_id'],owned_fixture=work.name,scope='Synthetic Windows parent/child using actual shared event/semaphore/timer objects, atomic mixed waits and access grants')
 product='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}'
 try:
  boot=ui.guest(work/'prepare',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);p.desktop(12001,True);task(g,p,12003)
  fixtures=build();binary=(fixtures/'named.exe').read_bytes();mounted=StoppedDisk(disk,library())
  try:
   mounted.put(product+'/7z.exe',binary);mounted.put(product+'/child.exe',binary)
  finally:mounted.close()
  boot=ui.guest(work/'named',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);text=task(g,p,12005);assert 'M142_NAMED_SYNC_CHILD_AND_ATOMIC_WAIT_PASS' in text,text;assert ui.integer(g,'sync_resident142',True)==0;before=f.stats(g)[0];samples=[]
   for n in range(20):
    text=task(g,p,12005);assert 'M142_NAMED_SYNC_CHILD_AND_ATOMIC_WAIT_PASS' in text,text;delta=f.stats(g)[0]-before;assert not delta,(n,delta);resident=ui.integer(g,'sync_resident142',True);assert resident==0; samples.append(dict(turn=n+1,retained_pages=delta,shared_registry_pages_after_close=resident))
   report.update(samples=samples,quota_object_limit=32,quota_grant_limit=64,quota_and_stale_refusal_checked=True,output=text,fixture_sha256=hashlib.sha256(binary).hexdigest());(out/'named.log').write_bytes(g.log().encode('utf-8'));t.close_all(g,p)
  mounted=StoppedDisk(disk,library())
  try:mounted.put(product+'/7z.exe',(fixtures/'survivor.exe').read_bytes())
  finally:mounted.close()
  boot=ui.guest(work/'survivor',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);before=f.stats(g)[0];samples=[]
   for n in range(2):
    at=len(g.log());text=task(g,p,12005);part=g.log()[at:];assert 'M142_NAMED_OBJECT_SURVIVED_CREATOR_PASS' in text and text.index('M142_NAMED_CREATOR_EXIT_BEGIN')<text.index('M142_NAMED_OBJECT_SURVIVED_CREATOR_PASS'),text;assert part.index('M142_ROOT_EXIT')<part.index('M142_CHILD_EXIT'),part;delta=f.stats(g)[0]-before;assert delta==(4 if not n else 0),(n,delta)
    if not n:before=f.stats(g)[0]
    resident=ui.integer(g,'sync_resident142',True);assert resident==0;samples.append(dict(turn=n+1,retained_pages=delta,shared_registry_pages_after_close=resident,object_survives_creator_exit=True))
   report.update(passed=True,survivor_samples=samples,survivor_output=text);(out/'survivor.log').write_bytes(g.log().encode('utf-8'));t.close_all(g,p);t.launch(g,p,'clock',8);t.close_all(g,p)
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode('utf-8'));print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
