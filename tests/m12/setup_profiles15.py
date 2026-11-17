"""Actual M12.15 setup pages on ordinary, explicit 150% and physical 4K."""
import json,os,traceback
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE15'
import setup_observe as z
ui=z.ui;ROOT=z.ROOT

def main():
 out=ROOT/'build/m12/stage15/setup-profiles';out.mkdir(parents=True,exist_ok=True)
 meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));report=dict(passed=False,build_id=meta['build_id'],profiles=[],checks=[])
 try:
  for name,resolution,choice,expected in [('ordinary',(1280,800),50010,2),('150',(1920,1200),50012,3),('4k',(3840,2160),50013,4)]:
   work=ui.q.new_work('m12-stage15-setup-p-'+name);disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
   with ui.guest(work/'install',disk,resolution=resolution) as g:
    p=ui.Pointer(g);p.drain();before=z.f.sha_file(disk);z.shot(g,out,'welcome-'+name);z.wizard(g,p,2);z.wizard(g,p,choice);assert z.flag(g,'scale73')==expected;z.shot(g,out,'keyboard-'+name);frames=z.flag(g,'full_frames75')
    z.go(g,p,2,100);z.shot(g,out,'disk-'+name);z.go(g,p,2);z.shot(g,out,'apps-'+name);z.go(g,p,2);z.shot(g,out,'style-'+name);z.go(g,p,2);z.shot(g,out,'review-'+name);assert z.f.sha_file(disk)==before and z.flag(g,'full_frames75')==frames
    at=z.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);p.drain();z.shot(g,out,'ready-'+name);at=z.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain();assert z.c.flag(g,'scale73')==expected and z.c.flag(g,'guide_open11');z.shot(g,out,'first-use-'+name,True);z.key(g,'esc');z.t.close_all(g,p);z.c.idle(g);stats=z.f.stats(g);report['profiles'].append(dict(name=name,physical=list(resolution),scale=expected,managed_current_bytes=stats[0]*4096,managed_peak_bytes=stats[1]*4096,owned_fixture=work.name));(out/(name+'.log')).write_bytes(g.log().encode())
  report['checks']=['All ordinary setup pages have bounded non-overlapping hit targets on actual ordinary, explicit 150% and physical 3840x2160/200% displays','Next preserves the outer frame after scaling, the complete disk is unchanged before Install, and each profile really installs and restarts into its correctly scaled first-use guide'];report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
