"""Actual CPL3 vectored hardware-fault continuation; not structured unwind qualification."""
import hashlib,json,os,traceback
from pathlib import Path
from thread_native2 import ui,c,f,t,task
from access_fixtures16 import clone
from fixture1 import library,StoppedDisk
from exception_fixtures2 import build
ROOT=Path(__file__).resolve().parents[2]
def main():
 out=ROOT/'build/m14-native/stage2/exceptions';out.mkdir(parents=True,exist_ok=True)
 meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));baseline=json.loads((ROOT/'build/m14-native/stage2/compact/results.json').read_text(encoding='utf-8'));assert baseline['passed'] and baseline['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage2-compact'/baseline['owned_fixture']/'owned.img';work,disk,_=clone(ui,source,'m142-exceptions');report=dict(passed=False,build_id=meta['build_id'],scope='Native AMD64 vectored access-violation/illegal-instruction continuation; structured unwind remains unqualified')
 product='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}'
 try:
  boot=ui.guest(work/'prepare',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);p.desktop(12001,True);task(g,p,12003)
  fixtures=build();binary=(fixtures/'exceptions.exe').read_bytes();mounted=StoppedDisk(disk,library())
  try:mounted.put(product+'/7z.exe',binary)
  finally:mounted.close()
  boot=ui.guest(work/'probe',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);text=task(g,p,12005);assert 'M142_VECTORED_HARDWARE_FAULTS_RESUME_PASS' in text,text;before=f.stats(g)[0];samples=[]
   for n in range(20):
    text=task(g,p,12005);assert 'M142_VECTORED_HARDWARE_FAULTS_RESUME_PASS' in text,text;delta=f.stats(g)[0]-before;assert delta==0,(n,delta);samples.append(dict(turn=n+1,retained_pages=delta))
   report.update(passed=True,samples=samples,output=text,fixture_sha256=hashlib.sha256(binary).hexdigest(),handled_faults_per_execution=48);t.close_all(g,p);t.launch(g,p,'clock',8);t.close_all(g,p);(out/'native.log').write_bytes(g.log().encode('utf-8'))
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode('utf-8'));print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
