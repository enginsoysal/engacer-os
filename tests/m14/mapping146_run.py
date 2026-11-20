"""Native fixed/movable global memory, ownership, quotas and thread cleanup."""
import argparse,hashlib,json,os,struct,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
from window144_native import ui,c,f,t,clone,library,StoppedDisk,task,output
from mapping146_build import build

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--cycles',type=int,default=1);args=parser.parse_args();assert 1<=args.cycles<=21
 out=ROOT/'build/m14-native/stage6/mapping-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out;fixture=build();meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage6/apps/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m146-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m146-mapping-native');mounted=StoppedDisk(disk,library())
 try:mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())
 finally:mounted.close()
 report=dict(passed=False,build_id=meta['build_id'],scope='Owned shared mappings across actual private processes, read-only fault containment, source exit, alias/protection/handle/view/object limits; not original-app qualification',clone=cloned,fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest())
 try:
  boot=ui.guest(work/'mapping',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19);task(g,p,12005);before=f.stats(g)[0];samples=[]
   for cycle in range(args.cycles):
    text=task(g,p,12100);assert 'M146_SHARED_MAPPING_PRIVATE_PROCESSES_LIFETIMES_LIMITS_PASS' in text,text
    assert len(t.records(g))==1 and t.records(g)[0]['token']==front['token'];assert ui.integer(g,'ui_resident144',True)==0 and ui.integer(g,'mapping_resident146',True)==0
    retained=f.stats(g)[0]-before;assert retained==0,(cycle,retained);samples.append(dict(cycle=cycle+1,retained_pages=retained,actual_private_child_processes=3,readonly_child_fault_contained=True))
   c.shot(g,'shared-mapping-lifetimes');value=task(g,p,12005);assert 'Mapped original image: 7z.exe' in value and '7-Zip' in value
   report.update(passed=True,cycles=samples,subsequent_original_console_success=True,output=text);(out/'serial.log').write_bytes(g.log().encode())

 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
