"""Actual compact/HiDPI switcher and arrangement, never resized captures."""
import json,os,struct,traceback
from pathlib import Path
import multitask_native as m
t=m.t;s=m.s;c=m.c;f=m.f;ui=m.ui;ROOT=m.ROOT

def main():
    out=ROOT/'build/m12/stage11/multitask-profiles';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    native=json.loads((ROOT/'build/m12/stage11/multitask-native/results.json').read_text(encoding='utf-8'));meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));assert native['passed'] and not native['development_only'] and native['build_id']==meta['build_id']
    work=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage11-multitask'/native['owned_fixture'];disk=work/'owned.img'
    report=dict(passed=False,build_id=meta['build_id'],profiles=[],checks=[])
    try:
        for label,resolution,scale,dark in [('compact',(800,600),111,False),('compact-dark',(800,600),111,True),('150',(1920,1200),112,False),('4k',(3840,2160),113,False)]:
            with ui.guest(work/('profile-'+label),disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution) as g:
                p=ui.Pointer(g);p.drain();c.open_settings(g,p);p.desktop(scale,True);assert c.flag(g,'scale73')=={111:2,112:3,113:4}[scale];p.desktop(43 if dark else 44,True);s.close(g,p);before=f.stats(g)
                logical=struct.unpack('<II',ui.memory(g,ui.symbol('model',installed=True)[0]+240,8));first=t.records(g)[0];second=t.launch(g,p,'files',1);f.visit(g,p,'Documents');old=m.geometry(g);m.arrange(g,p);c.shot(g,'arrange-'+label);m.selected_contrast(g,out/f'arrange-{label}.png')
                fits=logical[0]//2>=500
                if fits:
                    p.desktop(44100,True);assert c.flag(g,'switch_open11')==3;c.shot(g,'assist-'+label);p.desktop(44100,True);assert m.geometry(g,second['slot'])==(0,0,logical[0]//2,logical[1]-60);assert m.geometry(g,first['slot'])==(logical[0]//2,0,logical[0]-logical[0]//2,logical[1]-60)
                    c.shot(g,'paired-'+label);c.key(g,'meta_l','down');t.focus(g,p,second);c.key(g,'meta_l','down');assert m.geometry(g)==old
                else:
                    assert not any(r[5] in (44100,44101) for r in f.controls(g));c.key(g,'up');c.shot(g,'minimum-'+label);c.key(g,'ret');assert m.geometry(g)==old and c.flag(g,'switch_open11')==2;c.key(g,'esc')
                editor=t.launch(g,p,'text editor',2);c.type_text(g,'Keep this note');t.launch(g,p,'text editor',2)
                while s.windows(g)<8:t.launch(g,p,'files',1)
                m.alt(g,True);c.key(g,'tab');assert c.flag(g,'switch_open11')==1 and len(m.tokens(g))==8
                rows=[r for r in f.controls(g) if 44100<=r[5]<44108];assert len(rows)==8
                for x,y,w,h,*_ in rows:assert x>=0 and y>=0 and x+w<=logical[0] and y+h<logical[1]-60
                c.shot(g,'switcher-'+label);m.selected_contrast(g,out/f'switcher-{label}.png');chosen=m.tokens(g)[c.flag(g,'switch_choice11')];c.key(g,'ret');m.alt(g,False);assert next(w for w in t.records(g) if w['slot']==f.model(g)[0])['token']==chosen
                t.focus(g,p,editor);assert bytes(t.app_view(g).text)==b'Keep this note';s.close(g,p);assert t.closing(g)==1;c.shot(g,'dirty-review-'+label);p.desktop(61,True);assert bytes(t.app_view(g).text)==b'Keep this note';t.close_all(g,p)
                p.desktop(43101,True);f.same_pages(before,f.stats(g));c.idle(g);stats=f.stats(g)
                report['profiles'].append(dict(name=label,physical=list(resolution),logical=list(logical),scale=c.flag(g,'scale73'),half_available=fits,theme='dark' if dark else 'light',managed_current_bytes=stats[0]*4096,managed_peak_bytes=stats[1]*4096,retained_pages=0));(out/(label+'.log')).write_bytes(g.log().encode())
        report['checks'].append('Actual compact light/dark and physical 150%/3840x2160/200% show all eight switch rows within the work area, preserve dirty work and exercise real selection without retained pages or idle painting')
        report['checks'].append('Compact 800x600 truthfully disables halves that cannot fit Files; real 1280/1920-logical desktops preview, pair and restore independently measured windows')
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
