"""Development-only M12.16 accessibility provider and focus smoke."""
import json,os,traceback
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE16'
import setup_observe as z
ui=z.ui;ROOT=z.ROOT

def main():
 out=ROOT/'build/m12/stage16/access-smoke';out.mkdir(parents=True,exist_ok=True);z.c.OUT=out
 meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m12-stage16-access-smoke');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);report=dict(passed=False,development_only=True,build_id=meta['build_id'],owned_fixture=work.name,checks=[])
 try:
  with ui.guest(work/'install',disk) as g:
   p=ui.Pointer(g)
   z.go(g,p,2,2,100,2,2,2);at=z.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);at=z.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain();z.c.shot(g,'first-guide');assert z.c.flag(g,'guide_open11');z.key(g,'f1');assert z.c.flag(g,'access_help16');z.c.shot(g,'guide-focus-help');z.key(g,'esc');assert not z.c.flag(g,'access_help16') and z.c.flag(g,'guide_open11');z.key(g,'esc');assert not z.c.flag(g,'guide_open11');z.h.close(g,p)
   z.c.open_settings(g,p);p.desktop(59004,True);assert z.h.page(g)==4;z.c.shot(g,'accessibility');p.desktop(60010,True);assert z.c.flag(g,'access_flags16')==1;z.c.shot(g,'high-contrast');p.desktop(60011,True);assert z.c.flag(g,'access_flags16')==3;z.c.shot(g,'reduced-motion');z.key(g,'tab');z.key(g,'f1');assert z.c.flag(g,'access_help16');z.c.shot(g,'focus-help');z.key(g,'esc');assert not z.c.flag(g,'access_help16');p.desktop(60012,True);assert not z.c.flag(g,'access_flags16');z.h.close(g,p);z.key(g,'f6');assert z.c.flag(g,'access_region16')==1 and z.c.flag(g,'control_active');z.key(g,'f1');z.c.shot(g,'taskbar-focus-help');z.key(g,'esc');z.c.idle(g);(out/'native.log').write_bytes(g.log().encode())
  report['checks']=['Actual installation, guide help, settings contrast/reduced effects/reset and keyboard taskbar focus are exercised in the native guest'];report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
