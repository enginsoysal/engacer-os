"""Confirmed parent grants reach RUN helpers; production runtime is restored afterward."""
import hashlib,json,os,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 import replay7
 loader=replay7.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  from window144_native import ui,c,f,t,clone,library,StoppedDisk
  from apps_native4 import task
  from machine147_build import build as dispatcher
  out=ROOT/'build/m14-native/stage7/pipe-authority';out.mkdir(parents=True,exist_ok=True);c.OUT=out
  # Reuse the already compiled pipe fixture without rebuilding files another observer reads.
  files=ROOT/'build/m14-native/stage7/pipe-fixture';proof=json.loads((files/'compile-inputs.json').read_text());fixture=files/'authorized.exe';assert hashlib.sha256(fixture.read_bytes()).hexdigest()==proof['artifacts']['authorized']
  _,runtime=dispatcher();meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage7/apps/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id'];source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m147-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m147-pipe-authority');root='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}';original_runtime=(ROOT/'build/m14-native/WINDOWS8.ELF').read_bytes();mounted=StoppedDisk(disk,library())
  try:
   for path,data in [(root+'/machine147.exe',fixture.read_bytes()),(root+'/child147.exe',fixture.read_bytes()),('/System/Windows/runtime8.elf',runtime.read_bytes())]:mounted.put(path,data)
  finally:mounted.close()
  report=dict(passed=False,build_id=meta['build_id'],scope=__doc__,clone=cloned,fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest(),dispatcher_sha256=hashlib.sha256(runtime.read_bytes()).hexdigest(),cycles=[])
  try:
   boot=ui.guest(work/'authority',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
   with boot as g:
    p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);task(g,p,12005);before=f.stats(g)[0]
    for cycle in range(5):
     p.desktop(12002,True);value=task(g,p,12003);assert 'M147_NATIVE_PIPE_INHERITED_1M_SHA_EOF_QUOTA_PASS'in value,value;assert ui.integer(g,'pipe_resident147',True)==0 and f.stats(g)[0]==before;report['cycles'].append(dict(cycle=cycle+1,retained_pages=0))
    c.shot(g,'confirmed-helper');(out/'serial.log').write_bytes(g.log().encode())
   mounted=StoppedDisk(disk,library())
   try:mounted.put('/System/Windows/runtime8.elf',original_runtime)
   finally:mounted.close()
   boot=ui.guest(work/'restored',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
   with boot as g:
    p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);value=task(g,p,12005);assert 'Mapped original image: 7z.exe'in value and '7-Zip'in value;report['subsequent_original_console_success']=True
   report['passed']=True
  except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
  finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
 finally:
  sys.meta_path.remove(loader);out=ROOT/'build/m14-native/stage7/pipe-authority';out.mkdir(parents=True,exist_ok=True);(out/'dependencies.json').write_bytes((json.dumps(replay7.observed,indent=2)+'\n').encode())
if __name__=='__main__':main()
