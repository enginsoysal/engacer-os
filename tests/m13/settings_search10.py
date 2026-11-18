"""M13.10 installed Settings search, ownership, readable frames and disk boots."""
import argparse, hashlib, json, os, struct, sys, traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
os.environ['ENGACER12_IMAGE']='EngacerOS-M13STAGE10'
sys.path.insert(0,str(ROOT/'tests/m12'))
import settings_observe as h
import capture14, observe6, observer8
c=h.c; f=h.f; t=h.t; ui=h.ui
capture14.bind(ui); observe6.bind(ui); observer=observer8.bind(ui)


def query(g,slot=None):
    if slot is None:slot=f.model(g)[0]
    at,size=ui.symbol('settings_search18',installed=True)
    return ui.memory(g,at+slot*(size//8)+8,64).split(b'\0')[0].decode()


def search(g,p,value):
    c.key(g,'ctrl','f');c.key(g,'ctrl','a');c.type_text(g,value);p.drain()
    assert query(g)==value


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--profile',choices=['ordinary','compact','1024','150','4k'],default='ordinary');args=parser.parse_args()
    assert not (ROOT/'evidence/M13/10/publication-results.json').exists()
    resolution,ram,scale={'ordinary':((1920,1080),512,50011),'compact':((1280,800),128,50011),'1024':((1024,768),128,50011),'150':((1920,1200),512,50012),'4k':((3840,2160),1024,50013)}[args.profile]
    out=ROOT/'build/m13/stage10'/('search-'+args.profile);out.mkdir(parents=True,exist_ok=True);c.OUT=out
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m1310-search-'+args.profile);disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
    report=dict(passed=False,stage='M13.10',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],physical=list(resolution),configured_guest_mib=ram,owned_fixture=work.name,host_observer=observer,checks=[])
    try:
        with ui.guest(work/'install',disk,resolution=resolution,ram=ram) as g:
            p=ui.Pointer(g)
            for action in (2,scale,2,100,2,2,2):c.wizard(g,p,action)
            at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain();t.close_all(g,p);baseline=f.stats(g)
            first=t.launch(g,p,'settings',3);initial=h.colors(g);before=f.sha_file(disk);c.shot(g,'settings-common-frame')
            for term,page in [('dark',0),('dark mode',0),('scale',1),('double',2),('devices',3),('apps',3),('contrast',4)]:
                search(g,p,term);assert not f.has(g,47) and not f.has(g,59006), 'Appearance footer must not occupy search results';clear=next(r for r in f.current_controls(g) if r[5]==61201);assert clear[2]==120;matches=[r[5]-61210 for r in f.current_controls(g) if 61210<=r[5]<61215];assert matches==[page],(term,matches);c.shot(g,'search-'+term.replace(' ','-'));c.key(g,'ret');assert h.page(g)==page and query(g)==''
            assert f.sha_file(disk)==before and h.colors(g)==initial
            report['checks'].append('Readable semantic Clear search and result-only footer preserve actual Ctrl+F, text editing, supported category results and Enter navigate all five real categories without writing preferences or changing appearance')
            previous_scale=c.flag(g,'scale73');previous_disk=f.sha_file(disk);p.desktop(59001,True)
            if args.profile in ('compact','1024'):
                p.desktop(113,True);assert c.flag(g,'scale73')==previous_scale and 'too little room' in f.app(g)['notice'];c.shot(g,'refused-display-size')
            else:
                p.desktop(112 if args.profile=='ordinary' else 111,True);assert c.flag(g,'scale73')!=previous_scale and h.preview(g)[0]==first['token'];c.shot(g,'display-preview');p.desktop(59005,True);assert c.flag(g,'scale73')==previous_scale
            assert f.sha_file(disk)==previous_disk
            report['checks'].append('Actual display-size preview and Cancel restore the previous scale, or a too-small physical profile refuses 200% with recovery text; the complete disk is unchanged')
            search(g,p,'zz-no-setting');assert not any(61210<=r[5]<61215 for r in f.current_controls(g));c.shot(g,'no-results');p.desktop(61201,True);assert query(g)==''
            p.desktop(59000,True);p.desktop(43,True);assert h.preview(g)[0]==first['token'];search(g,p,'unknown');c.key(g,'esc');assert query(g)=='' and h.preview(g)[0]==first['token'];c.key(g,'esc');assert h.preview(g)[0]==first['token'];c.key(g,'esc');assert not h.preview(g)[0] and h.colors(g)==initial and f.sha_file(disk)==before
            report['checks'].append('No-results/Clear recover browsing; Escape clears search then leaves it before cancelling only the owning appearance preview, with an independently identical complete disk')
            search(g,p,'wallpaper');other=t.launch(g,p,'settings',3);assert query(g)=='';search(g,p,'keyboard');t.focus(g,p,first);assert query(g)=='wallpaper';t.focus(g,p,other);h.close(g,p);t.focus(g,p,first);assert query(g)=='wallpaper';p.desktop(61201,True)
            f.resize(g,p,700,600);c.shot(g,'minimum-settings');_,bounds=f.model(g);rows=f.current_controls(g)
            for action in (61200,59000,59004,47,59006):
                r=next(r for r in rows if r[5]==action);assert r[0]>=bounds[0] and r[1]>=bounds[1]+36 and r[0]+r[2]<=bounds[0]+bounds[2] and r[1]+r[3]<=bounds[1]+bounds[3],(action,r,bounds)
            search(g,p,'a');c.shot(g,'minimum-search-results');p.desktop(61201,True)
            report['checks'].append('Two live generations retain independent temporary queries; the actual minimum 700x600 window retains search, categories, matching results and Apply/Restore controls inside its bounds')
            for name,dark in [('dark',1),('light',0)]:
                p.desktop(59000,True);p.desktop(43 if dark else 44,True);h.save(g,p);saved=h.record(disk);assert struct.unpack_from('<I',saved,12)[0]==dark and h.colors(g)[1]==dark;c.shot(g,'applied-'+name)
            p.desktop(59004,True);p.desktop(60010,True);assert c.flag(g,'access_flags16')&1;search(g,p,'contrast');c.shot(g,'high-contrast-search');p.desktop(61201,True);p.desktop(60010,True);assert not(c.flag(g,'access_flags16')&1)
            report['checks'].append('Light/dark are actually applied and independently read from the saved appearance record; high-contrast search uses the real accessibility flag and remains reachable at the minimum window size')
            t.right_group(g,p,3);f.menu(g,p,42703);p.drain();assert 3 in h.s.prefs(g).task[:h.s.prefs(g).tasks];dismiss=next(r for r in f.controls(g) if r[5]==60002);toast=(dismiss[0]-372,dismiss[1]-8,480,116);raw=ui.memory(g,ui.symbol('model',installed=True)[0],224)
            for slot in range(8):
                x,y,w,hh,generation,app,live,minimized=struct.unpack_from('<4iII2B',raw,slot*28)
                if live and not minimized:assert not(toast[0]<x+w and toast[0]+toast[2]>x and toast[1]<y+40 and toast[1]+toast[3]>y),(toast,(x,y,w,hh))
            c.shot(g,'caption-safe-feedback');p.desktop(60002,True);h.close(g,p)
            report['checks'].append('A real saved taskbar-pin notification uses the lower caption-safe rectangle; every live caption remains outside it and actual Dismiss clears the message')
            saved=h.record(disk);f.same_pages(baseline,f.stats(g));c.idle(g);report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0);report['saved_appearance_sha256']=hashlib.sha256(saved).hexdigest();(out/'native.log').write_text(g.log(),encoding='utf-8')
        for n in (1,2):
            boot=ui.guest(work/('disk-only-'+str(n)),disk,resolution=resolution,ram=ram,media='installed',ready='M7_DESKTOP_READY');ui.s.normal_boot(boot,work/'install/vars.fd')
            with boot as g:
                p=ui.Pointer(g);p.drain();t.launch(g,p,'settings',3);assert query(g)=='' and ui.memory(g,ui.symbol('appearance11',352,True)[0],352)==saved;search(g,p,'display');c.key(g,'ret');assert h.page(g)==1;h.close(g,p);c.shot(g,'disk-only-'+str(n));c.idle(g);(out/('disk-only-'+str(n)+'.log')).write_text(g.log(),encoding='utf-8')
        report['checks'].append('Two ordinary no-ISO disk startups reload exact saved appearance and minimum bounds, clear temporary searches, navigate a real result and halt at idle')
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':main()
