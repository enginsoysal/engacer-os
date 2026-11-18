"""Measure actual installation progress repaint coalescing on frozen native media."""
import json,os,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];os.environ['ENGACER12_IMAGE']='EngacerOS-M13STAGE4';sys.path.insert(0,str(ROOT/'tests/m12'))
import setup_observe as s
ui=s.ui

def main():
 out=ROOT/'build/m13/stage4/progress-resources';out.mkdir(parents=True,exist_ok=True);work=ui.q.new_work('m134-progress-resources');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));report=dict(passed=False,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'])
 try:
  with ui.guest(work/'install',disk,resolution=(1024,768),ram=128) as g:
   p=ui.Pointer(g);s.go(g,p,2,2,100,2,2,2);before={n:ui.integer(g,n) for n in ('full_frames75','content_frames75')};at=s.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);p.drain();after={n:ui.integer(g,n) for n in before};report['before']=before;report['after']=after;report['progress_callbacks']=g.log()[at:].count('M6_PROGRESS ');report['content_transitions']=after['content_frames75']-before['content_frames75'];report['visible_frame_events']=g.log()[at:].count('M75_FRAME ');assert 0<report['visible_frame_events']<report['progress_callbacks'] and report['visible_frame_events']<=110;assert after['full_frames75']-before['full_frames75']<=1;assert s.flag(g,'step')==6 and not s.flag(g,'failure');report['checks']=['Actual verified installation emits more progress callbacks than visible frame events','At most 110 visible progress/result frame events and at most one full-frame repaint','Skipped duplicate visible progress never skips successful actual installation'];report['passed']=True;(out/'boot.log').write_bytes(g.log().encode())
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report),flush=True)
if __name__=='__main__':main()
