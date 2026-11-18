"""Actual native personalization/saver scale, theme and contrast frames."""
import argparse,hashlib,json,os,struct,time,traceback
from pathlib import Path
import saver_native12 as n
from access_fixtures16 import clone
c=n.c;f=n.f;h=n.h;t=n.t;ui=n.ui;ROOT=n.ROOT


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--profile',choices=['ordinary','compact','1024','150','4k'],required=True);a=parser.parse_args()
    physical,ram={'ordinary':((1920,1080),512),'compact':((1280,800),128),'1024':((1024,768),128),'150':((1920,1200),512),'4k':((3840,2160),1024)}[a.profile]
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m13/stage12'/a.profile/'results.json').read_text(encoding='utf-8'));assert base['passed'] and base['build_id']==meta['build_id']
    source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6'/('m13-stage12-'+a.profile)/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m1312-personalization-'+a.profile)
    out=ROOT/'build/m13/stage12'/('personalization-'+a.profile);out.mkdir(parents=True,exist_ok=True);c.OUT=out
    report=dict(passed=False,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],physical=list(physical),clone=cloned,themes=[],checks=[])
    try:
        with ui.guest(work/'installed',disk,resolution=physical,ram=ram,media='installed',ready='M7_DESKTOP_READY') as g:
            p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);baseline=f.stats(g)
            for theme in ('light','dark','high-contrast'):
                t.launch(g,p,'settings',3);p.desktop(59004,True)
                if bool(c.flag(g,'access_flags16')&1)!=(theme=='high-contrast'):p.desktop(60010,True)
                p.desktop(59000,True);p.desktop(43 if theme=='dark' else 44,True);h.save(g,p)
                # Actual minimum owner geometry through the native resize/move tools.
                f.resize(g,p,700,600)
                p.desktop(60200,True);assert h.page(g)==6
                owner=next(w for w in t.records(g) if w['slot']==f.model(g)[0]);_,bounds=f.model(g)
                for x,y,w,hh,token,command in f.current_controls(g):
                    assert bounds[0]<=x and bounds[1]<=y and x+w<=bounds[0]+bounds[2] and y+hh<=bounds[1]+bounds[3],(a.profile,theme,command,bounds,(x,y,w,hh))
                required={60201,60202,60203,60204,60205,60206,60207,60208,60209,60212,60213}
                assert required<={r[5] for r in f.current_controls(g)}
                c.shot(g,theme+'-screensaver-settings');before=f.sha_file(disk);n.preview(g,p);c.shot(g,theme+'-logo-preview');n.wake(g);assert f.sha_file(disk)==before
                p.desktop(59004,True)
                if not c.flag(g,'access_flags16')&2:p.desktop(60011,True)
                p.desktop(59000,True);p.desktop(60200,True);n.preview(g,p)
                c.shot(g,theme+'-reduced-motion-before');time.sleep(1.15);c.shot(g,theme+'-reduced-motion');assert (out/(theme+'-reduced-motion-before.png')).read_bytes()==(out/(theme+'-reduced-motion.png')).read_bytes(),'Reduced-motion visible logo changed without user input';n.wake(g);h.close(g,p)
                t.launch(g,p,'files',1);f.visit(g,p,'Documents');c.shot(g,theme+'-current-place')
                if theme=='high-contrast':
                    row=next(r for r in f.current_controls(g) if r[5]==94);assert c.pixel(g,row[0],row[1]+row[3]//2)==0xffffff
                h.close(g,p);p.desktop(0,True);c.shot(g,theme+'-start-outline')
                if theme=='high-contrast':
                    b=n.s.bounds(g);assert c.pixel(g,b[0]+b[2]//2,b[1])==0xffffff
                c.key(g,'esc');f.same_pages(baseline,f.stats(g));report['themes'].append(theme)
            report['checks']=['All actual saver controls stay inside their owner at the named scale in Light, Dark and High contrast','Preview and wake preserve the independently identical complete disk; reduced motion retains an independently identical visible logo frame','Current-place and Start captures retain real navigation; the High-contrast Start perimeter has independently read white pixels']
            c.idle(g);report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0);(out/'native.log').write_bytes(g.log().encode())
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':main()
