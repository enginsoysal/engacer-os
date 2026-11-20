"""An owned GUI instruction fault must release GUI/timers and preserve the desktop."""
import hashlib,json,os,struct,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tests/m14'))
from window144_native import ui,c,f,t,clone,library,StoppedDisk,task,output,wait
from fault144_build import build

def main():
 out=ROOT/'build/m14-native/stage4/gui-fault-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out;fixture=build()/'fault.exe';meta=json.loads(ui.manifest_path12().read_text());base=json.loads((ROOT/'build/m14-native/stage4/apps/results.json').read_text());assert base['passed']and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m144-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m144-gui-fault');mounted=StoppedDisk(disk,library())
 try:mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())
 finally:mounted.close()
 report=dict(passed=False,scope='Owned CPL3 GUI instruction-fault containment, timers/GUI teardown and subsequent original console use; not app compatibility qualification',build_id=meta['build_id'],fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest(),clone=cloned,cycles=[])
 try:
  boot=ui.guest(work/'faults',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19);task(g,p,12005);before=f.stats(g)[0]
   for turn in range(21):
    at=len(g.log());p.desktop(12100,True);g.wait('M8_CPL3_CREATED',at);wait(g,'M144_FAULT_READY');p.drain();assert len(t.records(g))==2;c.key(g,'f');g.wait('M8_JOB_FAILED',at);p.drain();state,command,status=struct.unpack('<3I',ui.memory(g,ui.symbol('info8',installed=True)[0],12));assert state==3 and status,(state,status,output(g));assert len(t.records(g))==1 and t.records(g)[0]['token']==front['token'];assert ui.integer(g,'ui_resident144',True)==0;retained=f.stats(g)[0]-before;assert retained==0,retained
    if turn==0:c.shot(g,'contained-gui-fault')
    value=task(g,p,12005);assert 'Mapped original image: 7z.exe'in value and '7-Zip'in value,value;report['cycles'].append({'cycle':turn+1,'expected_fault_status':status,'retained_pages':retained,'subsequent_original_console_success':True})
   report['passed']=True;report['output']=output(g)
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps({k:v for k,v in report.items()if k!='cycles'},indent=2),flush=True)
if __name__=='__main__':main()
