"""Reject privileged/noncanonical continuation and invalid MXCSR in the native guest."""
import json,os,struct,traceback
from pathlib import Path
from thread_native2 import ui,c,f,t,task
from access_fixtures16 import clone
from fixture1 import library,StoppedDisk
from unwind_variants2 import variants as build
ROOT=Path(__file__).resolve().parents[2]
def main():
 out=ROOT/'build/m14-native/stage2/unwind-invalid';out.mkdir(parents=True,exist_ok=True);meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage2/compact/results.json').read_text(encoding='utf-8'));assert base['passed'] and base['build_id']==meta['build_id'];source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage2-compact'/base['owned_fixture']/'owned.img';work,disk,_=clone(ui,source,'m142-unwind-invalid');report=dict(passed=False,build_id=meta['build_id'],scope='Native malformed cyclic/opcode/scope/directory metadata refuses safely with responsive desktop',cases=[])
 product='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}'
 try:
  boot=ui.guest(work/'prepare',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);p.desktop(12001,True);task(g,p,12003)
  fixtures=build()
  for mode in ['cycle','opcode','scope','directory']:
   mounted=StoppedDisk(disk,library())
   try:mounted.put(product+'/7z.exe',(fixtures/('unwind-'+mode+'.exe')).read_bytes())
   finally:mounted.close()
   boot=ui.guest(work/mode,disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
   with boot as g:
    p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);before=f.stats(g)[0];samples=[]
    for n in range(2):
     at=len(g.log());p.desktop(12005,True,settle=False);g.wait('M8_JOB_FAILED',at);p.drain();raw=ui.memory(g,ui.symbol('info8',installed=True)[0],40);state,_,status=struct.unpack_from('<3I',raw);assert state==3 and status==(1 if mode=='directory' else 0xc0000027),(state,status,g.log()[at:]);delta=f.stats(g)[0]-before;assert delta==(4 if not n else 0),(mode,n,delta)
     if not n:before=f.stats(g)[0]
     samples.append(dict(turn=n+1,status=status,retained_pages=delta))
    t.close_all(g,p);t.launch(g,p,'clock',8);t.close_all(g,p);(out/(mode+'.log')).write_bytes(g.log().encode('utf-8'));report['cases'].append(dict(name=mode,samples=samples,desktop_responsive=True))
  report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode('utf-8'));print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
