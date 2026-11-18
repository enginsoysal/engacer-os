"""Observe the new native boot/welcome without guest memory writes."""
import os,sys,json,time,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];os.environ['ENGACER12_IMAGE']='EngacerOS-M13STAGE2';sys.path.insert(0,str(ROOT/'tests/m12'));import ui

def click(g,p,action):
 n=ui.integer(g,'controls');raw=ui.memory(g,ui.symbol('buttons',480)[0],n*20);rows=[struct.unpack_from('<5I',raw,i*20)for i in range(n)if struct.unpack_from('<I',raw,i*20+16)[0]==action];assert len(rows)==1,(action,n);x,y,w,h,_=rows[0];p.logical(x+w//2,y+h//2)
def shot(g,out,name):
 g.qmp('stop')
 try:ui.raw_shot(g,out,name)
 finally:g.qmp('cont')

def main():
 out=ROOT/'build/m13/stage2/candidate3-smoke';out.mkdir(parents=True,exist_ok=True);work=ui.q.new_work('m13-stage2-smoke');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));report=dict(passed=False,build_id=meta['build_id'])
 try:
  with ui.guest(work/'boot',disk,resolution=(1920,1080),ram=512,ready='M13_STARTUP_PHASE value=0x0000000000000001')as g:
   g.qmp('stop')
   try:
    phase=ui.integer(g,'startup_phase13');assert phase in (1,2,3) and ui.integer(g,'controls')==0,phase;ui.raw_shot(g,out,'actual-startup');report['observed_startup_phase']=phase
   finally:g.qmp('cont')
   g.wait('M6_WIZARD_READY',timeout=180);p=ui.Pointer(g);p.drain();shot(g,out,'welcome');full=ui.integer(g,'full_frames75');click(g,p,50500);shot(g,out,'startup-options');assert ui.integer(g,'full_frames75')==full;click(g,p,50500);assert ui.integer(g,'full_frames75')==full;(out/'boot.log').write_text(g.log(),encoding='utf-8');report['passed']=True
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report))
if __name__=='__main__':main()
