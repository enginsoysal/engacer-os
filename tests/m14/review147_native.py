"""Native ordinary-input MSI chooser, cancellation and source-bound metadata review."""
import ctypes,hashlib,json,os,struct,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 import replay7
 loader=replay7.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  from window144_native import ui,c,f,t,clone,library,StoppedDisk,task
  out=ROOT/'build/m14-native/stage7/review-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out
  meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage7/compact/results.json').read_text(encoding='utf-8'));assert base['passed'] and base['build_id']==meta['build_id']
  source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage7-compact'/base['owned_fixture']/'owned.img'
  work,disk,cloned=clone(ui,source,'m147-review-native');mounted=StoppedDisk(disk,library())
  packages=[ROOT/'third_party/7zip/7z2606-x64.msi',Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/npp.8.9.9.1.Installer.x64.msi']
  try:
   for package in packages:mounted.put('/Users/Owner/Downloads/'+package.name,package.read_bytes())
   mounted.put('/Users/Owner/Downloads/Not-an-installer.txt',b'not an MSI')
  finally:mounted.close()
  report=dict(passed=False,build_id=meta['build_id'],clone=cloned,scope=__doc__,packages=[])
  try:
   boot=ui.guest(work/'review',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
   with boot as g:
    p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19)
    slot=front['slot'];address,size=ui.symbol('apps',installed=True);address+=slot*(size//8)
    def state():return struct.unpack('<9I',ui.memory(g,address,36))
    initial=state();p.desktop(12013,True);assert c.flag(g,'picker12')==9;p.desktop(54010,True);assert state()==initial
    entries=f.entries(g)
    for index,package in enumerate(packages):
     path='/Users/Owner/Downloads/'+package.name;p.desktop(12013,True);assert c.flag(g,'picker12')==9
     p.desktop(54019,True);c.key(g,'ctrl','a');c.type_text(g,'/Users/Owner/Downloads');c.key(g,'ret');p.drain()
     row=entries[path]['index'];bad=entries['/Users/Owner/Downloads/Not-an-installer.txt']['index'];assert not any(r[5]==55000+bad for r in f.controls(g))
     for _ in range(128):
      if any(r[5]==55000+row for r in f.controls(g)):break
      p.desktop(54023,True)
     else:raise AssertionError('MSI is not reachable in chooser')
     p.desktop(55000+row,True);p.desktop(54011,True);assert not c.flag(g,'file_dialog_state11');assert state()[0]==1 and state()[1]==0
     output=task(g,p,12000);assert 'M147_NATIVE_MSI_READ_ONLY_PLAN_PASS' in output;review=state();assert review[:3]==(1,1,0),review
     digest=ui.memory(g,address+68,32);expected=hashlib.sha256(package.read_bytes()).digest();assert digest==expected,(digest.hex(),expected.hex())
     assert review[4]==(3 if index==0 else 2),review
     raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496);assert ('7-Zip' if index==0 else 'Notepad++')in raw[40:136].split(b'\0')[0].decode()
     if index==1:
      assert not c.flag(g,'w8_active');assert any(r[5]==12001 for r in f.controls(g)) and not any(r[5]==12003 for r in f.controls(g));assert not any(k.startswith('/Applications/Windows/')for k in f.entries(g))
     c.shot(g,'review-'+str(index));report['packages'].append(dict(file=package.name,sha256=expected.hex(),profile=review[4],files=review[5],registry=review[6],shortcuts=review[7],features=review[8],output=output))
    report['checks']=['Chooser opens with MSI filter; cancel preserves previous selection','Both unchanged original MSI packages produce their independently computed source digest','Both original packages pass read-only generic admission without starting an install job or mutating a product'];report['passed']=True;(out/'serial.log').write_bytes(g.log().encode())
  except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
  finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
 finally:sys.meta_path.remove(loader)
if __name__=='__main__':main()
