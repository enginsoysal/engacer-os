"""Minimal native installation and optional-package independence."""
import json,os,traceback
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE15'
import setup_observe as z
ui=z.ui;ROOT=z.ROOT

def main():
 out=ROOT/'build/m12/stage15/setup-minimal';out.mkdir(parents=True,exist_ok=True);z.c.OUT=out
 meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m12-stage15-setup-minimal');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);report=dict(passed=False,build_id=meta['build_id'],owned_fixture=work.name,checks=[])
 try:
  with ui.guest(work/'install',disk) as g:
   p=ui.Pointer(g);p.drain();z.go(g,p,2,2,100,2,50102);z.shot(g,out,'no-optional-apps');z.go(g,p,2,2);z.shot(g,out,'minimal-review');at=z.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);at=z.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain();assert z.c.flag(g,'guide_open11');z.shot(g,out,'base-first-use',True);p.desktop(46003,True);assert not z.c.flag(g,'guide_open11') and sum(w["app"]==3 for w in z.t.records(g))==1;z.h.close(g,p);z.t.close_all(g,p)
   assert '/Applications/Calculator/program.elf' not in z.f.rows(g) and '/Applications/Editor/program.elf' not in z.f.rows(g);before=z.f.stats(g);z.c.open_settings(g,p);p.desktop(59003,True);p.desktop(10000,True);z.h.software_change(g,p,4);assert ui.s.s.document(disk,'/Applications/Calculator/program.elf').startswith(b'\x7fELF');p.desktop(10204,True);assert sum(w["app"]==4 for w in z.t.records(g))==1;z.c.shot(g,'offline-calculator');z.h.close(g,p);z.h.software_change(g,p,4);assert '/Applications/Calculator/program.elf' not in z.f.rows(g);z.h.close(g,p);z.t.close_all(g,p);z.f.same_pages(before,z.f.stats(g));z.c.idle(g);report['resources']=dict(before=list(before),after=list(z.f.stats(g)),retained_pages=0);(out/'native.log').write_bytes(g.log().encode())
  report['checks']=['A real No optional apps installation reaches its base-owned first-use card; Appearance opens actual required Settings without Calculator or Editor','Offline installation starts the real Calculator worker and reviewed removal preserves the base desktop with zero completed-task page retention'];report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
