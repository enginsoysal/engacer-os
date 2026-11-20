"""Observe pinned original application entry in an owned native test disk.

This diagnostic replaces only the launch target in a stopped disposable clone.
It is not installer, complete portable-package, app-task or release acceptance.
"""
import argparse,hashlib,json,os,struct,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
from window144_native import ui,c,f,t,clone,library,StoppedDisk,output
from original_window_trace4 import views

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--app',choices=['notepadpp','sumatra'],required=True);args=parser.parse_args()
 meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage5/apps/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id']
 research=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0';original=research/('notepadpp/notepad++.exe'if args.app=='notepadpp'else'sumatra/SumatraPDF-3.6.1-64.exe');body=original.read_bytes()
 targets=json.loads((ROOT/'docs/roadmap/m14-targets.json').read_text(encoding='utf-8'))['targets'];target=next(v for v in targets if v['id']==args.app);assert hashlib.sha256(body).hexdigest()==target['payload']['sha256']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m145-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m145-entry-'+args.app)
 mounted=StoppedDisk(disk,library());folder='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/'
 try:
  mounted.put(folder+'7zFM.exe',body)
  if args.app=='notepadpp':
   for p in original.parent.iterdir():
    if p.is_file()and p!=original and p.suffix.lower()in('.dll','.xml'):mounted.put(folder+p.name,p.read_bytes())
 finally:mounted.close()
 out=ROOT/'build/m14-native/stage5'/('entry-'+args.app);out.mkdir(parents=True,exist_ok=True);c.OUT=out
 report=dict(stage='M14.5 development diagnostic',build_id=meta['build_id'],app=args.app,original_sha256=hashlib.sha256(body).hexdigest(),original_bytes=len(body),clone=cloned,qualified=False,scope='Original entry through the current supported launch slot; not installation or complete package/task qualification')
 try:
  boot=ui.guest(work/'entry',disk,media='installed',ready='M7_DESKTOP_READY',ram=512);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);at=len(g.log());p.desktop(12100,True,settle=False)
   deadline=time.monotonic()+30
   while time.monotonic()<deadline:
    state,command,status=struct.unpack('<3I',ui.memory(g,ui.symbol('info8',installed=True)[0],12))
    if state in(2,3):break
    time.sleep(.1)
   p.drain();raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384)
   report.update(state=state,command=command,exit_status=status,detail=raw[304:496].split(b'\0')[0].decode(errors='replace'),output=output(g),windows=views(g),protected_worker_started='M8_CPL3_CREATED'in g.log()[at:],original_app_entry_qualified=False)
   c.shot(g,'original-entry');(out/'serial.log').write_bytes(g.log().encode())
 except Exception:report['observer_error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
