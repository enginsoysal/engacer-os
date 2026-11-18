"""Actual installed app-frame scale/bounds checks in the applied Light theme."""
import argparse, hashlib, json, os, struct, sys, traceback
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
os.environ['ENGACER12_IMAGE'] = 'EngacerOS-M13STAGE12'
sys.path.insert(0, str(ROOT/'tests/m12'))
import settings_observe as h
import capture14, observe20, observer8
from access_fixtures16 import clone
c=h.c; f=h.f; t=h.t; ui=h.ui
capture14.bind(ui); barrier=observe20.bind(ui); observer8.bind(ui)

APPS = [('files',1), ('text editor',2), ('settings',3), ('calc',4),
        ('downloads',5), ('system monitor',6), ('terminal',7), ('clock',8),
        ('calendar',9), ('disk utility',10), ('software',11), ('recovery',12),
        ('archive manager',13), ('image viewer',14), ('screenshot',15),
        ('media player',16), ('browser',17), ('help',18), ('windows apps',19)]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--profile', choices=['ordinary','compact','1024','150','4k'], required=True)
    a=parser.parse_args();assert a.profile!='ordinary', 'Ordinary all-theme coverage uses apps_frames12.py'
    physical,ram={'ordinary':((1920,1080),512),'compact':((1280,800),128),
                  '1024':((1024,768),128),'150':((1920,1200),512),'4k':((3840,2160),1024)}[a.profile]
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'))
    native=json.loads((ROOT/'build/m13/stage12'/a.profile/'results.json').read_text(encoding='utf-8'))
    assert native['passed'] and native['build_id']==meta['build_id']
    source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6'/('m13-stage12-'+a.profile)/native['owned_fixture']/'owned.img'
    work,disk,cloned=clone(ui,source,'m1312-app-frames-'+a.profile)
    out=ROOT/'build/m13/stage12'/('apps-'+a.profile);out.mkdir(parents=True,exist_ok=True);c.OUT=out
    report=dict(passed=False,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],
                physical=list(physical),clone=cloned,host_observer=barrier,checks=[],frames=[])
    try:
        with ui.guest(work/'installed',disk,resolution=physical,ram=ram,media='installed',ready='M7_DESKTOP_READY') as g:
            p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p)
            for theme in ('light',):
                t.launch(g,p,'settings',3)
                p.desktop(59004,True)
                if bool(c.flag(g,'access_flags16')&1)!=(theme=='high-contrast'):p.desktop(60010,True)
                p.desktop(59000,True);p.desktop(43 if theme=='dark' else 44,True);h.save(g,p)
                saved=h.record(disk)
                assert struct.unpack_from('<I',saved,12)[0]==(theme=='dark')
                h.close(g,p);baseline=f.stats(g)
                for name,kind in APPS:
                    app=t.launch(g,p,name,kind)
                    bounds=struct.unpack('<4i',ui.memory(g,ui.symbol('model',installed=True)[0]+app['slot']*28,16))
                    rows=[r for r in f.controls(g) if r[4]==app['token'] and 49000<=r[5]<=49003]
                    assert {r[5] for r in rows}=={49000,49001,49002,49003}
                    assert all(r[2]>=32 and r[3]>=28 for r in rows)
                    owned=[r for r in f.controls(g) if r[4]==app['token']]
                    outside=[list(r) for r in owned if r[0]<bounds[0] or r[1]<bounds[1] or r[0]+r[2]>bounds[0]+bounds[2] or r[1]+r[3]>bounds[1]+bounds[3]]
                    assert not outside,(name,theme,bounds,outside)
                    label=theme+'-'+str(kind);c.shot(g,label)
                    report['frames'].append(dict(theme=theme,app=kind,name=name,bounds=list(bounds),capture=label+'.png'))
                    t.close_all(g,p);f.same_pages(baseline,f.stats(g))
                report['checks'].append(theme+': nineteen actual base/optional app frames open with owner-bound captions, close independently and retain zero managed pages')
            c.idle(g);report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0)
            report['scale_units']=c.flag(g,'scale73');(out/'native.log').write_bytes(g.log().encode('utf-8'))
        report['passed']=True
    except Exception:
        report['error']=ui.q.clean(traceback.format_exc())
        if 'g' in locals():(out/'failure.log').write_bytes(g.log().encode('utf-8'))
        raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode('utf-8'));print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':main()
