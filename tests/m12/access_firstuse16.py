"""Actual Dark first-use card boundary and retained guide keyboard ownership."""
import json,os,struct,traceback
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE16'
import access_observe16 as a
z=a.z;c=a.c;ui=a.ui;ROOT=a.ROOT

def main():
 out=ROOT/'build/m12/stage16/access-firstuse';out.mkdir(parents=True,exist_ok=True);c.OUT=out;meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m12-stage16-firstuse');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);report=dict(passed=False,build_id=meta['build_id'],checks=[])
 try:
  with ui.guest(work/'install',disk) as g:
   p=ui.Pointer(g);p.drain();z.go(g,p,2,2,100,2,2,50301,2);at=z.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);at=z.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);ui.Pointer(g).drain();assert c.flag(g,'guide_open11') and a.h.colors(g)[1]==1;c.shot(g,'dark-first-use');rows=[r for r in a.f.controls(g) if 46000<=r[5]<=46003];assert len(rows)==4 and all(r[0]>=0 and r[1]>=0 for r in rows);a.key(g,'f6');assert c.flag(g,'guide_open11') and a.focus(g)==(1,0,46000);a.key(g,'f1');assert a.semantic(g,'access_help_item16')['action']==46000;c.shot(g,'dark-guide-help');a.key(g,'esc');assert c.flag(g,'guide_open11') and a.focus(g)==(1,0,46000);a.key(g,'esc');assert not c.flag(g,'guide_open11');a.close(g);assert not a.t.records(g);c.idle(g);report['managed_current_bytes']=a.f.stats(g)[0]*4096;(out/'native.log').write_bytes(g.log().encode())
  report['checks']=['A real Dark-style installation starts with an explicit contrasting first-guide boundary; F6 retains guide ownership and F1/Escape restores the actual guide action before explicit dismissal, with the base desktop still usable'];report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
