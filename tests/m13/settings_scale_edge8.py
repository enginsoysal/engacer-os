"""A display choice must leave room for the complete new Settings frame."""
import json,os,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
os.environ['ENGACER12_IMAGE']='EngacerOS-M13STAGE8'
sys.path.insert(0,str(ROOT/'tests/m12'))
import settings_observe as h
import capture14,observe6,observer8
c=h.c;f=h.f;t=h.t;ui=h.ui
capture14.bind(ui);observe6.bind(ui);observer8.bind(ui)


def main():
    out=ROOT/'build/m13/stage8/scale-edge';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m138-scale-edge');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
    report=dict(passed=False,stage='M13.8',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],physical=[1920,1200],owned_fixture=work.name,checks=[])
    try:
        with ui.guest(work/'install',disk,resolution=(1920,1200),ram=512) as g:
            p=ui.Pointer(g)
            for action in (2,50012,2,100,2,2,2):c.wizard(g,p,action)
            at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain();t.close_all(g,p);baseline=f.stats(g)
            t.launch(g,p,'settings',3);h.save(g,p);saved=h.record(disk);assert c.flag(g,'scale73')==3
            p.desktop(59001,True);p.desktop(113,True);report['observed_scale_units']=c.flag(g,'scale73');report['bounds']=list(f.model(g)[1]);c.shot(g,'200-percent-admission')
            assert c.flag(g,'scale73')==3,'200% would leave only 960x600 logical pixels and a 540-high workspace'
            assert 'room' in f.app(g)['notice'].lower() and not h.preview(g)[0] and h.record(disk)==saved
            p.desktop(59000,True);p.desktop(59003,True);p.desktop(59007,True);c.shot(g,'complete-preview-after-refusal');h.close(g,p);f.same_pages(baseline,f.stats(g));c.idle(g)
            report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0);(out/'native.log').write_text(g.log(),encoding='utf-8')
        report['checks'].append('On the actual 1920x1200 display, 200% is refused before changing the 150% session because the complete Settings frame needs a 660-high desktop; preferences remain byte-identical and every category stays reachable')
        report['checks'].append('Appearance and the complete Interface preview remain reachable after refusal; close retains no managed pages and idle CPUs halt')
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':main()
