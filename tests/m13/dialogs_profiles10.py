"""Actual secondary-surface themes/scales, ordinary input and independent bytes."""
import argparse,hashlib,json,os,struct,traceback
from pathlib import Path
import dialogs_native10 as d
import settings_observe as h
import observe20
from access_fixtures16 import clone
c=d.c;f=d.f;ui=d.ui;ROOT=d.ROOT;t=d.t
# Select the original pointer beneath the imported barrier; never nest barriers.
assert ui.Pointer.__qualname__=='bind.<locals>.Pointer'
barrier=observe20.bind(ui,ui.Pointer.__bases__[0])


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--profile',choices=['ordinary','compact','1024','150','4k'],required=True);a=parser.parse_args()
    physical,ram,scale={'ordinary':((1920,1080),512,111),'compact':((1280,800),128,111),
                        '1024':((1024,768),128,111),'150':((1920,1200),512,112),'4k':((3840,2160),1024,113)}[a.profile]
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'))
    native=json.loads((ROOT/'build/m13/stage10/dialogs-native/results.json').read_text(encoding='utf-8'))
    assert native['passed'] and not native['development_only'] and native['build_id']==meta['build_id']
    source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m1310-dialogs'/native['owned_fixture']/'owned.img'
    work,disk,cloned=clone(ui,source,'m1310-secondary-'+a.profile)
    out=ROOT/'build/m13/stage10'/('secondary-'+a.profile);out.mkdir(parents=True,exist_ok=True);c.OUT=out
    report=dict(passed=False,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],
                physical=list(physical),clone=cloned,host_observer=barrier,checks=[],themes=[])
    documents=['/Users/Owner/Documents/First.txt','/Users/Owner/Documents/Existing.txt','/Users/Owner/Downloads/Saved.txt']
    expected={path:ui.s.s.document(disk,path) for path in documents}
    try:
        with ui.guest(work/'installed',disk,resolution=physical,ram=ram,media='installed',ready='M7_DESKTOP_READY') as g:
            p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p)
            t.launch(g,p,'settings',3);p.desktop(59001,True);p.desktop(scale,True);h.save(g,p);h.close(g,p)
            assert c.flag(g,'scale73')=={'ordinary':2,'compact':2,'1024':2,'150':3,'4k':4}[a.profile]
            t.launch(g,p,'files',1);f.visit(g,p,'Documents')
            long_name='A clearly named document with a long description for review.txt'
            assert len(long_name)<=63
            d.create_text(g,p,long_name,'M13.10 metadata')
            t.close_all(g,p)
            for theme in ('light','dark','high-contrast'):
                t.launch(g,p,'settings',3);p.desktop(59004,True)
                if bool(c.flag(g,'access_flags16')&1)!=(theme=='high-contrast'):p.desktop(60010,True)
                p.desktop(59000,True);p.desktop(43 if theme=='dark' else 44,True);h.save(g,p);h.close(g,p)
                baseline=f.stats(g)
                t.launch(g,p,'files',1);f.visit(g,p,'Documents');p.desktop(f.item(g,p,long_name),True)
                p.desktop(52000,True);f.menu(g,p,40008);assert c.flag(g,'file_dialog_state11')==3;c.shot(g,theme+'-properties-long-location')
                if theme=='high-contrast':
                    width,height=struct.unpack('<II',ui.memory(g,ui.symbol('model',installed=True)[0]+240,8))
                    dialog_width=660 if width>720 else width-40
                    assert c.pixel(g,width//2,(height-60-420)//2)==0xffffff
                p.desktop(40021,True)
                assert f.entries(g)['/Users/Owner/Documents/'+long_name]['size']==len(b'M13.10 metadata')
                p.desktop(f.item(g,p,'Existing.txt'),True);c.key(g,'ret');p.desktop(54001,True);assert d.picker(g).purpose==2;c.shot(g,theme+'-save-as')
                p.desktop(54024,True);d.field(g,p,54020,'Bad/Name');p.desktop(54011,True);assert d.picker(g).phase==3 and d.picker(g).error;c.shot(g,theme+'-folder-name-error');p.desktop(54026,True)
                original=bytes(d.picker(g).path);d.location(g,p,'/Users/Owner/DoesNotExist');assert bytes(d.picker(g).path)==original and d.picker(g).error;c.shot(g,theme+'-unavailable-location')
                d.location(g,p,'/Users/Owner/Music');assert not d.picker(g).count;c.shot(g,theme+'-empty-location')
                d.location(g,p,'/Users/Owner/Documents');d.field(g,p,54020,'Existing.txt');p.desktop(54011,True);assert d.picker(g).phase==1;c.shot(g,theme+'-replace-review');p.desktop(54026,True);p.desktop(54010,True)
                c.key(g,'end');c.type_text(g,' unsaved');dirty=bytes(d.appview(g).text);assert d.appview(g).dirty
                p.desktop(54000,True);p.desktop(54016,True);d.choose(g,p,'First.txt');c.key(g,'ret');assert d.picker(g).phase==2;c.shot(g,theme+'-dirty-review')
                p.desktop(54026,True);assert d.appview(g).dirty and bytes(d.appview(g).text)==dirty
                d.choose(g,p,'First.txt');c.key(g,'ret');p.desktop(54028,True);assert not c.flag(g,'file_dialog_state11') and not d.appview(g).dirty
                t.close_all(g,p);f.same_pages(baseline,f.stats(g))
                report['themes'].append(theme)
                report['checks'].append(theme+': real long-name Properties, Save as, invalid folder, unavailable and empty locations, explicit replacement and owner-bound dirty review remain readable and preserve all original files')
            c.idle(g);report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0)
            report['scale_units']=c.flag(g,'scale73');(out/'native.log').write_bytes(g.log().encode('utf-8'))
        for path,value in expected.items():assert ui.s.s.document(disk,path)==value
        assert ui.s.s.document(disk,'/Users/Owner/Documents/'+long_name)==b'M13.10 metadata'
        report['independent_file_sha256']={path:hashlib.sha256(value).hexdigest() for path,value in expected.items()}
        report['passed']=True
    except Exception:
        report['error']=ui.q.clean(traceback.format_exc())
        if 'g' in locals():(out/'failure.log').write_bytes(g.log().encode('utf-8'))
        raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode('utf-8'));print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':main()
