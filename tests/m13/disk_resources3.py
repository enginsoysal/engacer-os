"""Measure actual disk-tool allocator state and repeated-format retention."""
import json,struct,traceback
import disk_profiles3 as d
ui=d.ui;s=d.s;ROOT=d.ROOT
def stats(g):return list(struct.unpack('<4Q',ui.memory(g,ui.symbol('stats',32)[0],32)))
def main():
 out=ROOT/'build/m13/stage3/disk-resources';out.mkdir(parents=True,exist_ok=True);work=ui.q.new_work('m133-disk-resources');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));report=dict(passed=False,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'])
 try:
  with ui.guest(work/'tools',disk,ram=128) as g:
   p=ui.Pointer(g);p.drain();before=stats(g);s.go(g,p,2,2,100,90,213);d.apply(g,p,2,False);s.go(g,p,300,210,223);d.apply(g,p,3,False);samples=[]
   for _ in range(3):s.go(g,p,300,212,225);d.apply(g,p,6,False);samples.append(stats(g))
   assert len({r[0] for r in samples})==1,samples;s.go(g,p,200);after=stats(g);halted=g.qmp('human-monitor-command',{'command-line':'info registers -a'}).count('HLT=1');assert halted==2
   report.update(passed=True,before=before,after=after,repeated_format=samples,retained_delta_pages=after[0]-before[0],both_cpus_halted=True,scope='Allocator current/peak page counts and allocation/free counters are distinct from fixed installer state and configured 128-MiB RAM');(out/'boot.log').write_bytes(g.log().encode())
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report),flush=True)
if __name__=='__main__':main()
