"""Open original MSIs through Files: select once, open, then review before install."""
import hashlib,json,os,struct,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 import replay7
 loader=replay7.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  from window144_native import ui,c,f,t,clone,StoppedDisk,task
  from fixture1 import library
  out=ROOT/'build/m14-native/stage7/msi-entry-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out;meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage7/compact/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id'];source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage7-compact'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m147-msi-file-entry');packages=[Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/npp.8.9.9.1.Installer.x64.msi',ROOT/'third_party/7zip/7z2606-x64.msi'];mounted=StoppedDisk(disk,library())
  try:
   for p in packages:mounted.put('/Users/Owner/Downloads/'+p.name,p.read_bytes())
  finally:mounted.close()
  report=dict(passed=False,scope=__doc__,build_id=meta['build_id'],observer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),owned_fixture=work.name,clone=cloned,cases=[])
  try:
   boot=ui.guest(work/'entry',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
   with boot as g:
    p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p)
    for index,package in enumerate(packages):
     t.launch(g,p,'files',1);f.visit(g,p,'/Users/Owner/Downloads');row=f.item(g,p,package.name);p.desktop(row,True);assert not any(w['app']==19 for w in t.records(g));c.key(g,'ret');p.drain();front=next(w for w in t.records(g)if w['app']==19);assert f.model(g)[0]==front['slot'];address,size=ui.symbol('apps',installed=True);address+=front['slot']*(size//8);state=struct.unpack('<9I',ui.memory(g,address,36));assert state[:3]==(1,0,0),state;assert not any(r[5]in(12001,12003)for r in f.current_controls(g));assert any(r[5]==12000 for r in f.current_controls(g));c.shot(g,'msi-entry-unreviewed-'+str(index));before=f.stats(g)[0];output=task(g,p,12000);state=struct.unpack('<9I',ui.memory(g,address,36));assert state[:3]==(1,1,0) and state[4]==(2 if index==0 else 3);assert f.stats(g)[0]-before==(4 if index==0 else 0);assert any(r[5]==12001 for r in f.current_controls(g));assert not any(path.startswith('/Applications/Windows/')for path in f.entries(g));assert ui.memory(g,address+68,32)==hashlib.sha256(package.read_bytes()).digest();report['cases'].append(dict(file=package.name,single_click_selects=True,supplied_source_requires_review=True,reviewed_profile=state[4],no_product_mutation=True,retained_task_pages=0,first_activation_pages=4 if index==0 else 0,output=output));c.shot(g,'msi-entry-reviewed-'+str(index));t.close_all(g,p)
    (out/'serial.log').write_bytes(g.log().encode());report['passed']=True
  except Exception:
   report['error']=ui.q.clean(traceback.format_exc())
   if'g'in locals():(out/'serial-failed.log').write_bytes(g.log().encode())
   raise
  finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
 finally:sys.meta_path.remove(loader)
if __name__=='__main__':main()
