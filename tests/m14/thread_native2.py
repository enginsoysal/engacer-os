"""Execute synthetic Windows threading code in the actual CPL3 runtime."""
import hashlib,json,os,struct,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
os.environ['ENGACER12_IMAGE']='EngacerOS-M14STAGE2'
sys.path[:0]=[str(ROOT/'tests/m12'),str(ROOT/'tests/m13')]
import taskbar_observe as t
ui=t.ui;c=t.c;f=t.f
import capture14,observer8
capture14.bind(ui);observer8.bind(ui)
from access_fixtures16 import clone
from fixture1 import library,StoppedDisk
from build_fixtures2 import build

sleep_observations=[]

def task(g,p,action):
 at=len(g.log());p.desktop(action,True,settle=False);g.wait('M8_CPL3_CREATED',at)
 deadline=time.monotonic()+180
 while time.monotonic()<deadline:
  if 'M8_JOB_DONE' in g.log()[at:] or 'M8_JOB_FAILED' in g.log()[at:]:break
  if action==12005:
   raw=ui.memory(g,ui.symbol('info8',installed=True)[0]+496,1024)
   if b'M142_SLEEP_IDLE_BEGIN' in raw:
    halted=g.qmp('human-monitor-command',{'command-line':'info registers -a'}).count('HLT=1')
    sleep_observations.append(halted)
  time.sleep(.03)
 else:raise TimeoutError('Windows threading probe did not finish')
 p.drain();raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384)
 text=raw[496:].split(b'\0')[0].decode(errors='replace')
 assert struct.unpack_from('<I',raw)[0]==2,(raw[:40].hex(),raw[304:496].split(b'\0')[0].decode(errors='replace'),text,g.log()[at:])
 return text

def main():
 out=ROOT/'build/m14-native/stage2/threads';out.mkdir(parents=True,exist_ok=True)
 meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'))
 baseline=json.loads((ROOT/'build/m14-native/stage2/compact/results.json').read_text(encoding='utf-8'))
 assert baseline['passed'] and baseline['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage2-compact'/baseline['owned_fixture']/'owned.img'
 work,disk,cloned=clone(ui,source,'m142-threads');report=dict(passed=False,stage='M14.2 development',build_id=meta['build_id'],synthetic=True,checks=[])
 product='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}'
 try:
  boot=ui.guest(work/'prepare',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);p.desktop(12001,True);task(g,p,12003)
  fixtures=build();mounted=StoppedDisk(disk,library())
  try:mounted.put(product+'/7z.exe',(fixtures/'threads.exe').read_bytes())
  finally:mounted.close()
  boot=ui.guest(work/'probe',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19)
   text=task(g,p,12005);assert 'M142_THREADS_TLS_WAIT_SLEEP_LOCK_PASS' in text,text
   before=f.stats(g)[0];samples=[]
   for n in range(20):
    text=task(g,p,12005);assert 'M142_THREADS_TLS_WAIT_SLEEP_LOCK_PASS' in text,text
    delta=f.stats(g)[0]-before;assert delta==0,(n,delta)
    samples.append(dict(turn=n+1,retained_pages=delta))
   assert 2 in sleep_observations,sleep_observations
   report.update(passed=True,samples=samples,sleep_cpu_halt_observations=sleep_observations,output=text,fixture_sha256=hashlib.sha256((fixtures/'threads.exe').read_bytes()).hexdigest())
   report['checks']=['4 genuine Windows threads per process','suspended start and resume','real timed sleeps','wait-all joins and zero-timeout','distinct thread IDs','recursive contended critical sections','per-thread dynamic TLS isolation','real thread return codes','24 sequential thread-close/reuse cycles within each process','wait-all preserves unsatisfied object states','named event independent handles','auto/manual reset and event producer wake','semaphore limit and consumption','one-shot/periodic timers and cancellation','20 repeated process closes retain zero pages']
   t.close_all(g,p);t.launch(g,p,'clock',8);t.close_all(g,p);(out/'native.log').write_text(g.log(),encoding='utf-8')
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:
  (out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
