"""An installed data-volume failure must offer only executable recovery actions."""
import hashlib,json,os,struct,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];os.environ['ENGACER12_IMAGE']='EngacerOS-M13STAGE4';sys.path.insert(0,str(ROOT/'tests/m12'))
import setup_observe as s
ui=s.ui
import capture14
capture14.bind(ui)

def main():
 assert not (ROOT/'evidence/M13/4/publication-results.json').exists(),'Accepted stage is immutable'
 out=ROOT/'build/m13/stage4/startup-failure';out.mkdir(parents=True,exist_ok=True);work=ui.q.new_work('m134-startup-failure');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));report=dict(passed=False,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],checks=[])
 try:
  with ui.guest(work/'install',disk) as g:
   p=ui.Pointer(g);s.go(g,p,2,2,100,2,2,2);at=s.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240)
  with disk.open('r+b') as f:
   f.seek(2*512+4*128+32);data=struct.unpack('<Q',f.read(8))[0]*512
   for bank in (0,1):
    f.seek(data+bank*71*4096);original=f.read(8);assert original==b'ENGINEV6';f.seek(-8,1);f.write(b'BROKENV6')
  before=ui.q.digest(disk)
  # The failure UI runs in the installed ELF; observe that image, not the live bundle.
  ui.MAPS74[False]=ui.MAPS74[True]
  boot=ui.guest(work/'failed-start',disk,media='installed',ready='M6_WIZARD_READY');ui.s.normal_boot(boot,work/'install/vars.fd')
  with boot as g:
   p=ui.Pointer(g);p.drain();report['failure_state']={k:s.flag(g,k) for k in ('failure','busy','installed','step')};report['failure_controls']=s.controls(g);s.shot(g,out,'observed-failure');(out/'boot.log').write_bytes(g.log().encode());assert s.flag(g,'failure') and not s.flag(g,'busy');assert s.has(g,86) and s.has(g,50);assert not any(s.has(g,a) for a in (80,81,82,63));s.shot(g,out,'installed-start-failure');s.key(g,'esc');assert s.has(g,86)
   s.go(g,p,50);assert not any(s.has(g,a) for a in (80,81,82));s.shot(g,out,'no-iso-repair-hidden');s.key(g,'esc');assert s.has(g,86)
   at=s.wizard(g,p,86);g.wait('M75_USER_RESTART',at,30);g.wait('M6_WIZARD_READY',at,180);p.drain();assert s.flag(g,'failure') and 'M7_DESKTOP_READY' not in g.log();s.shot(g,out,'failed-start-after-restart');(out/'boot.log').write_bytes(g.log().encode())
  assert ui.q.digest(disk)==before;report['checks']=['Deliberately corrupted owned data-volume banks produce a readable installed-start failure','Without matching live ISO, unavailable boot maintenance is absent; Details and Escape remain safe','Restart performs a real firmware reset and returns to truthful failure without claiming desktop success or modifying disk'];report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report),flush=True)
if __name__=='__main__':main()
