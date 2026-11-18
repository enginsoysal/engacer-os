"""Native M13.4 actual progress, recovery and completion frames."""
import json,os,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];os.environ['ENGACER12_IMAGE']='EngacerOS-M13STAGE4';sys.path.insert(0,str(ROOT/'tests/m12'))
import setup_observe as s
ui=s.ui
import capture14
capture14.bind(ui)
def main():
 out=ROOT/'build/m13/stage4/progress-recovery';out.mkdir(parents=True,exist_ok=True);work=ui.q.new_work('m134-progress-recovery');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));report=dict(passed=False,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'])
 try:
  guest=ui.guest(work/'install',disk);at=next(i for i,a in enumerate(guest.args) if a.startswith('if=none,id=target,'));guest.args[at]+=',bps_wr=1048576'
  with guest as g:
   p=ui.Pointer(g);p.drain();s.go(g,p,50500,50);s.shot(g,out,'recovery');s.key(g,'esc');s.go(g,p,2,2,100,2,2,2);s.shot(g,out,'review');at=len(g.log());g.qmp('send-key',{'keys':[{'type':'qcode','data':'ret'}],'hold-time':50});g.wait('M6_PROGRESS 0x0000000000000005',at,180);g.qmp('stop')
   try:
    ui.raw_shot(g,out,'actual-progress');report['observed_percent']=s.flag(g,'percent');report['observed_step']=s.flag(g,'step');report['observed_busy']=s.flag(g,'busy');assert report['observed_step']==5 and s.flag(g,'busy')==1 and 0<report['observed_percent']<100,report
   finally:g.qmp('cont')
   g.wait('M6_INSTALL_PASS',at,300);p.drain();s.shot(g,out,'finish');report['passed']=True;(out/'boot.log').write_bytes(g.log().encode())
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report),flush=True)
if __name__=='__main__':main()
