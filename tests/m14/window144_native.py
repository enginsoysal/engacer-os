"""Run our own GUI PE through actual native CPL3 and ordinary desktop input."""
import hashlib,json,os,struct,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
os.environ['ENGACER12_IMAGE']='EngacerOS-M14STAGE4'
sys.path[:0]=[str(ROOT/'tests/m12'),str(ROOT/'tests/m13')]
import taskbar_observe as t
ui=t.ui;c=t.c;f=t.f
import capture14
capture14.bind(ui)
from access_fixtures16 import clone
from fixture1 import library,StoppedDisk
from window144_build import build
from apps_native4 import task

def output(g):return ui.memory(g,ui.symbol('info8',installed=True)[0]+496,16384).split(b'\0')[0].decode(errors='replace')
def wait(g,text,timeout=30):
 deadline=time.monotonic()+timeout
 while time.monotonic()<deadline:
  value=output(g)
  if text in value:return value
  if 'M144_FAIL' in value:raise AssertionError(value)
  if not ui.integer(g,'w8_active',True) and struct.unpack_from('<I',ui.memory(g,ui.symbol('info8',installed=True)[0],4))[0]==3:raise AssertionError(ui.memory(g,ui.symbol('info8',installed=True)[0]+304,192).split(b'\0')[0])
  time.sleep(.03)
 raise TimeoutError((text,output(g)))
def geometry(g):return f.model(g)[1]
def drag(g,p,x,y,xx,yy):
 scale=c.flag(g,'scale73');p.move(x*scale//2,y*scale//2);p.drain();p.down(True);p.drain();p.move(xx*scale//2,yy*scale//2);p.drain();p.down(False);p.drain()
def main():
 assert not(ROOT/'evidence/M14/4/publication-results.json').exists()
 out=ROOT/'build/m14-native/stage4/window-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out
 fixture=build();base=json.loads((ROOT/'build/m14-native/stage4/apps/results.json').read_text(encoding='utf-8'));meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));assert base['passed'] and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m144-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m144-own-window');mounted=StoppedDisk(disk,library())
 try:mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())
 finally:mounted.close()
 report=dict(passed=False,stage='M14.4 development',scope='Owned synthetic AMD64 GUI fixture; not original 7-Zip GUI qualification',build_id=meta['build_id'],fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest(),clone=cloned)
 try:
  boot=ui.guest(work/'window',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19)
   cold=f.stats(g)[0];task(g,p,12005);before=f.stats(g)[0];report['existing_transition_warmup_pages']=before-cold;assert before-cold==4
   report['cycles']=[]
   for turn in range(21):
    at=len(g.log());p.desktop(12100,True);g.wait('M8_CPL3_CREATED',at);wait(g,'M144_NATIVE_WINDOW_WAITING');p.drain();assert len(t.records(g))==2,t.records(g)
    sample=dict(cycle=turn+1,initial_bounds=list(geometry(g)));assert f.model(g)[0]!=front['slot']
    if turn==0:c.shot(g,'real-cpl3-window')
    halted=g.qmp('human-monitor-command',{'command-line':'info registers -a'}).count('HLT=1');assert halted==2,halted;sample['halted_cpus_while_message_waiting']=halted
    c.key(g,'a');wait(g,'M144_CHARACTER_RECEIVED');p.drain()
    if turn==0:c.shot(g,'original-procedure-changed-title')
    x,y,w,h=geometry(g);drag(g,p,x+180,y+20,x+220,y+50);wait(g,'M144_MOVE_RECEIVED');sample['moved_bounds']=list(geometry(g))
    x,y,w,h=geometry(g);drag(g,p,x+w-4,y+h-4,x+w+20,y+h+20);wait(g,'M144_SIZE_RECEIVED');sample['resized_bounds']=list(geometry(g))
    if turn==0:c.shot(g,'native-window-resized')
    p.desktop(49002,True);g.wait('M8_JOB_DONE',at);p.drain();assert 'M144_WINDOW_LIFETIME_PASS' in output(g),output(g)
    assert len(t.records(g))==1 and t.records(g)[0]['token']==front['token'];assert ui.integer(g,'ui_resident144',True)==0
    sample['retained_pages']=f.stats(g)[0]-before;assert sample['retained_pages']==0,sample;report['cycles'].append(sample)
   report['output']=output(g);(out/'serial.log').write_bytes(g.log().encode());report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
