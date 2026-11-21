"""Exercise the new native read-only service with both unchanged original MSIs.

The legacy chooser filename is reused only in a private offline clone. This is
not qualification of a Notepad++ chooser, custom actions or installation.
"""
import hashlib,json,os,struct,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 import replay7
 loader=replay7.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  from window144_native import ui,c,f,t,clone,library,StoppedDisk,task
  out=ROOT/'build/m14-native/stage7/preview-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out
  meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage7/compact/results.json').read_text(encoding='utf-8'));assert base['passed'] and base['build_id']==meta['build_id']
  source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage7-compact'/base['owned_fixture']/'owned.img'
  packages=[ROOT/'third_party/7zip/7z2606-x64.msi',Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/npp.8.9.9.1.Installer.x64.msi']
  inventory=json.loads((ROOT/'evidence/M14/0/msi-inventory.json').read_text(encoding='utf-8-sig'));report=dict(passed=False,build_id=meta['build_id'],scope=__doc__,packages=[])
  try:
   for index,package in enumerate(packages):
    data=package.read_bytes();pin=next(x for x in inventory['packages'] if x['file']==package.name);assert hashlib.sha256(data).hexdigest()==pin['sha256']
    work,disk,cloned=clone(ui,source,'m147-preview-'+str(index));mounted=StoppedDisk(disk,library())
    try:mounted.put('/Users/Owner/Downloads/7z2606-x64.msi',data)
    finally:mounted.close()
    boot=ui.guest(work/'preview',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
    with boot as g:
     p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19);samples=[]
     # First invocation may populate normal UI state. Subsequent service lifetimes must retain no pages.
     task(g,p,12000);before=f.stats(g)[0]
     for cycle in range(5):
      output=task(g,p,12000);assert 'M147_NATIVE_MSI_READ_ONLY_PLAN_PASS' in output,output
      raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496)
      product=raw[40:136].split(b'\0')[0].decode();code=raw[264:304].split(b'\0')[0].decode();assert ('7-Zip' in product if index==0 else 'Notepad++' in product),(product,code)
      assert f.stats(g)[0]==before and ui.integer(g,'ui_resident144',True)==0
      assert len(t.records(g))==1 and t.records(g)[0]['token']==front['token'];samples.append(dict(cycle=cycle+1,retained_pages=0))
     c.shot(g,'preview-'+str(index));(out/('serial-'+str(index)+'.log')).write_bytes(g.log().encode())
     report['packages'].append(dict(file=package.name,sha256=hashlib.sha256(data).hexdigest(),product=product,code=code,clone=cloned,cycles=samples,output=output))
   report['passed']=True
  except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
  finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
 finally:
  sys.meta_path.remove(loader)
  out=ROOT/'build/m14-native/stage7/preview-native';out.mkdir(parents=True,exist_ok=True);(out/'dependencies.json').write_bytes((json.dumps(replay7.observed,indent=2)+'\n').encode())
if __name__=='__main__':main()
