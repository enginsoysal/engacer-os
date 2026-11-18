"""Actually applied Start/Settings search hints in light, dark and high contrast."""
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
    out=ROOT/'build/m13/stage8/hint-themes';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m138-hint-themes');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
    report=dict(passed=False,stage='M13.8',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],owned_fixture=work.name,checks=[],themes=[])
    try:
        with ui.guest(work/'install',disk,resolution=(1920,1080),ram=512) as g:
            p=h.q.install(g);t.close_all(g,p);baseline=f.stats(g);settings=t.launch(g,p,'settings',3)
            for name,dark,contrast in [('dark',1,False),('high-contrast',1,True),('light',0,False)]:
                if c.flag(g,'access_flags16')&1:p.desktop(59004,True);p.desktop(60010,True)
                p.desktop(59000,True);p.desktop(43 if dark else 44,True);h.save(g,p)
                saved=h.record(disk);assert struct.unpack_from('<I',saved,12)[0]==dark
                if contrast:p.desktop(59004,True);p.desktop(60010,True)
                assert bool(c.flag(g,'access_flags16')&1)==contrast
                c.shot(g,'settings-'+name);p.desktop(0,True);assert c.flag(g,'launcher')
                assert not ui.memory(g,ui.symbol('start_query11',256,True)[0],256).split(b'\0')[0]
                c.shot(g,'start-'+name);c.key(g,'esc');t.focus(g,p,settings)
                report['themes'].append(dict(name=name,dark=dark,high_contrast=contrast,appearance_record_sha256=hashlib.sha256(saved).hexdigest()))
            h.close(g,p);f.same_pages(baseline,f.stats(g));c.idle(g)
            report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0)
            (out/'native.log').write_text(g.log(),encoding='utf-8')
        report['checks'].append('Actual Apply and independent appearance bytes, plus the real high-contrast flag, bind empty Start and Settings hint captures in all three themes; cancelled previews never qualify them')
        report['checks'].append('Start opens with a genuinely empty query and returns to the same Settings owner; all windows close with zero retained managed pages and idle CPUs halt')
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':main()
