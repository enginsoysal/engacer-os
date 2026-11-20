"""Execute our owned resource/image fixture only inside the native guest."""
import hashlib,json,os,struct,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];os.environ['ENGACER12_IMAGE']='EngacerOS-M14STAGE4'
sys.path[:0]=[str(ROOT/'tests/m12'),str(ROOT/'tests/m13')]
import taskbar_observe as t
ui=t.ui;c=t.c;f=t.f
from apps_native4 import task
from access_fixtures16 import clone
from fixture1 import library,StoppedDisk
from controls144_build import build

def main():
 assert not(ROOT/'evidence/M14/4/publication-results.json').exists();out=ROOT/'build/m14-native/stage4/controls-native';out.mkdir(parents=True,exist_ok=True)
 fixture=build();meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage4/apps/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m144-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m144-controls');mounted=StoppedDisk(disk,library());product='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}'
 try:mounted.put(product+'/7z.exe',(fixture/'controls.exe').read_bytes())
 finally:mounted.close()
 report=dict(passed=False,stage='M14.4 development',scope='Owned native common-control registration, child geometry, edit/status state, display metrics and cursor fixture; not original GUI qualification',build_id=meta['build_id'],clone=cloned,fixtures={name:hashlib.sha256((fixture/name).read_bytes()).hexdigest()for name in ('controls.exe',)},cycles=[])
 try:
  boot=ui.guest(work/'controls',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);before=f.stats(g)[0]
   for turn in range(21):
    value=task(g,p,12005);assert 'M144_CONTROLS_GEOMETRY_PASS'in value,value
    retained=f.stats(g)[0]-before;assert retained==(4 if turn==0 else 0),(turn,retained)
    if turn==0:before=f.stats(g)[0]
    report['cycles'].append(dict(cycle=turn+1,retained_pages=retained,control_api_geometry=True))
   report['output']=value;(out/'serial.log').write_bytes(g.log().encode());report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps({k:v for k,v in report.items()if k!='cycles'},indent=2),flush=True)
if __name__=='__main__':main()
