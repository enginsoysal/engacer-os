"""Measure the actual original GUI's bounded ownership; not a whole-OS speed claim."""
import hashlib,json,os,struct,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tests/m14'))
from window144_native import ui,c,f,t,clone,task,output
from original_window_trace4 import views,wait_for

def main():
 out=ROOT/'build/m14-native/stage4/original-resources';out.mkdir(parents=True,exist_ok=True);c.OUT=out
 meta=json.loads(ui.manifest_path12().read_text());base=json.loads((ROOT/'build/m14-native/stage4/apps/results.json').read_text());assert base['passed']and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m144-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m144-original-resources')
 original=ui.s.s.document(disk,'/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',8*1024**2);digest=hashlib.sha256(original).hexdigest();assert digest=='a12710799d5cb9b3076b86dd0f92d4a503b7062bc3efac62b7f4cb8a74e05931'
 report=dict(passed=False,build_id=meta['build_id'],original_sha256=digest,clone=cloned,cycles=[],limits=['Original window ownership measurements, not complete original-app work or whole-OS optimization','Dispatch quanta are not measured CPU time','Configured guest RAM is not measured OS consumption','M14.15 remains the whole-system CPU/RAM/storage optimization gate'])
 try:
  boot=ui.guest(work/'resources',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);task(g,p,12005);baseline=f.stats(g)[0];report['managed_pages_before_original']=baseline
   physical=ui.physical_boot(g,True);stride=struct.unpack_from('<I',physical,136)[0];height=struct.unpack_from('<I',physical,148)[0];report['separate_framebuffer_bytes']=stride*height
   for turn in range(3):
    at=len(g.log());p.desktop(12100,True,settle=False);g.wait('M8_CPL3_CREATED',at);wait_for(g,lambda:any(not v['parent']and v['class_name']=='7-Zip::FM'for v in views(g)));p.drain();wait_for(g,lambda:len(views(g))==10 and g.qmp('human-monitor-command',{'command-line':'info registers -a'}).count('HLT=1')==2)
    resident=ui.integer(g,'ui_resident144',True);draw=ui.integer(g,'ui_draw_pages144',True);cache=ui.integer(g,'clipboard_resident144',True);assert 0<draw<=128 and draw<resident and cache==1
    sample=dict(cycle=turn+1,live_windows=len(views(g)),gui_owned_pages=resident,drawing_pages_included=draw,shared_registered_format_cache_pages=cache,managed_pages_while_original_open=f.stats(g)[0])
    halted=[];q0=struct.unpack_from('<Q',ui.memory(g,ui.symbol('info8',installed=True)[0],40),32)[0]
    for n in range(6):
     time.sleep(.1);halted.append(g.qmp('human-monitor-command',{'command-line':'info registers -a'}).count('HLT=1'))
    q1=struct.unpack_from('<Q',ui.memory(g,ui.symbol('info8',installed=True)[0],40),32)[0];assert 2 in halted,halted;sample['idle_halted_cpu_observations']=halted;sample['dispatch_quanta_during_observed_idle']=q1-q0
    p.desktop(49002,True);g.wait('M8_JOB_DONE',at);p.drain();raw=ui.memory(g,ui.symbol('info8',installed=True)[0],40);state,command,status=struct.unpack_from('<3I',raw);peak,quanta=struct.unpack_from('<QQ',raw,24);assert state==2 and status==0 and peak<10500,(state,status,peak)
    assert ui.integer(g,'ui_resident144',True)==0 and ui.integer(g,'ui_draw_pages144',True)==0
    retained=f.stats(g)[0]-baseline;assert retained==(1 if turn==0 else 0),(turn,retained)
    sample.update(peak_group_owned_pages=peak,total_dispatch_quanta=quanta,retained_pages=retained);report['cycles'].append(sample)
    if turn==0:baseline=f.stats(g)[0]
   report['passed']=True;report['declared_persistent_pages']={'worker_transition_stack_after_console_warmup':4,'session_registered_format_cache_after_first_gui':1}
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
