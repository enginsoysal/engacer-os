"""Ordinary mouse-first Settings search tasks on compact and physical 4K media."""
import hashlib,json,os,struct,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
os.environ['ENGACER12_IMAGE']='EngacerOS-M13STAGE8'
sys.path.insert(0,str(ROOT/'tests/m12'))
import settings_observe as h
import capture14,observe6,observer8
c=h.c;f=h.f;t=h.t;ui=h.ui
capture14.bind(ui);observe6.bind(ui);observer8.bind(ui)


def main():
    for name,resolution,ram,scale in [('compact',(1280,800),128,50011),('4k',(3840,2160),1024,50013)]:
        out=ROOT/'build/m13/stage8'/('mouse-'+name);out.mkdir(parents=True,exist_ok=True);c.OUT=out
        meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m138-settings-mouse-'+name);disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
        report=dict(passed=False,stage='M13.8',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],physical=list(resolution),configured_guest_mib=ram,owned_fixture=work.name,checks=[])
        try:
            with ui.guest(work/'install',disk,resolution=resolution,ram=ram) as g:
                p=ui.Pointer(g)
                for action in (2,scale,2,100,2,2,2):c.wizard(g,p,action)
                at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain();t.close_all(g,p);baseline=f.stats(g)
                t.launch(g,p,'settings',3);p.desktop(61200,True);c.type_text(g,'dark mode');c.shot(g,'mouse-result');p.desktop(61210,True);assert h.page(g)==0
                p.desktop(43,True);h.save(g,p);saved=h.record(disk);assert struct.unpack_from('<I',saved,12)[0]==1;c.shot(g,'mouse-applied-dark')
                p.desktop(61200,True);c.type_text(g,'keyboard');p.desktop(61212,True);assert h.page(g)==2;p.desktop(59020,True)
                assert h.click_interval(g)==200 and ui.s.s.document(disk,'/System/Settings/input11.bin')==struct.pack('<2I',0x31314955,200)
                p.desktop(61200,True);c.type_text(g,'DISPLAY');p.desktop(61211,True);assert h.page(g)==1
                p.desktop(61200,True);c.type_text(g,'no-such-setting');p.desktop(61201,True);assert h.page(g)==1;c.shot(g,'mouse-cleared-search')
                h.close(g,p);f.same_pages(baseline,f.stats(g));c.idle(g);report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0)
                report['saved_appearance_sha256']=hashlib.sha256(saved).hexdigest();(out/'native.log').write_text(g.log(),encoding='utf-8')
            report['checks'].append('Mouse focuses the real search field and chooses real dark-mode, keyboard and uppercase DISPLAY results; Apply and an immediate input choice produce independently verified appearance/input bytes')
            report['checks'].append('Mouse Clear recovers from an unavailable query to the same category; close retains no managed pages and idle CPUs halt')
            report['passed']=True
        except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
        finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':main()
