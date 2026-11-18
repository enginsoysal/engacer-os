"""Keep the known QEMU PVSCSI refusal separate from supported transport passes."""
import json,os,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];os.environ['ENGACER12_IMAGE']='EngacerOS-M13STAGE12';sys.path.insert(0,str(ROOT/'tests/m12'))
import setup_observe as s
ui=s.ui
import capture14
capture14.bind(ui)
def main():
 assert not (ROOT/'evidence/M13/12/publication-results.json').exists(),'Accepted stage is immutable'
 out=ROOT/'build/m13/stage12/4kn-refusal';out.mkdir(parents=True,exist_ok=True);work=ui.q.new_work('m1312-4kn-refusal');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);before=ui.q.digest(disk);meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));report=dict(passed=False,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],scope='Correct observed 4Kn NVMe capacity; installer writes remain unsupported')
 try:
  guest=ui.guest(work/'refusal',disk,controller='nvme',ram=256);at=next(i for i,a in enumerate(guest.args) if a.startswith('nvme,serial='));guest.args[at]+=',logical_block_size=4096,physical_block_size=4096'
  with guest as g:
   p=ui.Pointer(g);p.drain();s.go(g,p,2,2);ids=[r[4] for r in s.controls(g)];assert 100 in ids and 2 not in ids;s.go(g,p,100);assert not s.has(g,2)
   assert 'M92_NVME' in g.log() or 'NVME' in g.log();s.shot(g,out,'no-admitted-disk');assert ui.q.digest(disk)==before
   report['passed']=True;report['checks']=['Actual 4096-byte-sector NVMe disk remains inspectable with correct 2-GiB capacity','Unsupported installer sector width cannot enable Next','Complete owned disk remains byte-identical'];(out/'boot.log').write_bytes(g.log().encode())
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report),flush=True)
if __name__=='__main__':main()
