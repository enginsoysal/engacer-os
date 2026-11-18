"""Keep the known QEMU PVSCSI refusal separate from supported transport passes."""
import json,os,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];os.environ['ENGACER12_IMAGE']='EngacerOS-M13STAGE3';sys.path.insert(0,str(ROOT/'tests/m12'))
import setup_observe as s
ui=s.ui
def main():
 out=ROOT/'build/m13/stage3/qemu-pvscsi-refusal';out.mkdir(parents=True,exist_ok=True);work=ui.q.new_work('m133-pvscsi-refusal');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);before=ui.q.digest(disk);meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));report=dict(passed=False,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],scope='Expected refusal only; QEMU PVSCSI is not qualified for disk operations or installation')
 try:
  with ui.guest(work/'refusal',disk,controller='pvscsi',ram=256) as g:
   p=ui.Pointer(g);p.drain();s.go(g,p,2,2);ids=[r[4] for r in s.controls(g)];assert 100 not in ids and 2 not in ids and ui.integer(g,'disk_count92')==0
   assert 'M92_SCSI_STATS' in g.log() and 'M92_SCSI_DISK_READY' not in g.log();s.shot(g,out,'no-admitted-disk');assert ui.q.digest(disk)==before
   report['passed']=True;report['checks']=['Adapter is observed but no inconsistent disk is admitted','Readable no-disk state retains navigation and no active Next','Complete owned disk remains byte-identical'];(out/'boot.log').write_bytes(g.log().encode())
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report),flush=True)
if __name__=='__main__':main()
