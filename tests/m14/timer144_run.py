"""Execute our owned resource/image fixture only inside the native guest."""
import hashlib,json,os,struct,sys,traceback,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];os.environ['ENGACER12_IMAGE']='EngacerOS-M14STAGE4'
sys.path[:0]=[str(ROOT/'tests/m12'),str(ROOT/'tests/m13')]
import taskbar_observe as t
ui=t.ui;c=t.c;f=t.f
from apps_native4 import task
from access_fixtures16 import clone
from fixture1 import library,StoppedDisk
from timer144_build import build

def main():
 assert not(ROOT/'evidence/M14/4/publication-results.json').exists();out=ROOT/'build/m14-native/stage4/timer-native';out.mkdir(parents=True,exist_ok=True)
 fixture=build();meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage4/apps/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m144-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m144-timer');mounted=StoppedDisk(disk,library());product='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}'
 try:mounted.put(product+'/7z.exe',(fixture/'timer.exe').read_bytes())
 finally:mounted.close()
 report=dict(passed=False,stage='M14.4 development',scope='Owned native GUI deadlines, timer callbacks and teardown; not original GUI qualification',build_id=meta['build_id'],clone=cloned,fixtures={name:hashlib.sha256((fixture/name).read_bytes()).hexdigest()for name in ('timer.exe',)},cycles=[])
 try:
  boot=ui.guest(work/'controls',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);before=f.stats(g)[0]
   for turn in range(21):
    if turn==0:
     at=len(g.log());p.desktop(12005,True,settle=False);g.wait('M8_CPL3_CREATED',at);deadline=time.monotonic()+5
     while time.monotonic()<deadline:
      raw=ui.memory(g,ui.symbol('info8',installed=True)[0]+496,16384)
      if b'M144_TIMER_WAITING'in raw:break
      time.sleep(.01)
     else:raise AssertionError('Timer fixture did not reach its wait')
     halted=0;limit=time.monotonic()+.5
     while time.monotonic()<limit:
      halted=g.qmp('human-monitor-command',{'command-line':'info registers -a'}).count('HLT=1')
      if halted==2:break
      time.sleep(.01)
     assert halted==2,halted;report['halted_cpus_while_waiting_for_deadline']=halted;g.wait('M8_JOB_DONE',at);p.drain();value=ui.memory(g,ui.symbol('info8',installed=True)[0]+496,16384).split(b'\0')[0].decode(errors='replace')
    else:value=task(g,p,12005)
    assert 'M144_TIMER_LIFETIME_PASS'in value,value
    retained=f.stats(g)[0]-before;assert retained==(4 if turn==0 else 0),(turn,retained)
    if turn==0:before=f.stats(g)[0]
    report['cycles'].append(dict(cycle=turn+1,retained_pages=retained,deadline_timer_cycles=5))
   report['output']=value;(out/'serial.log').write_bytes(g.log().encode());report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps({k:v for k,v in report.items()if k!='cycles'},indent=2),flush=True)
if __name__=='__main__':main()
