"""Native compact/light/dark/150%/4K grouped controls and menu capacity."""
import json,os,struct,traceback
from pathlib import Path
import taskbar_native as t
s=t.s;c=t.c;f=t.f;ui=t.ui;ROOT=t.ROOT
def main():
    out=ROOT/'build/m12/stage10/taskbar-profiles';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    native=json.loads((ROOT/'build/m12/stage10/taskbar-native/results.json').read_text(encoding='utf-8'));meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));assert native['passed'] and not native['development_only'] and native['build_id']==meta['build_id']
    work=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage10-taskbar'/native['owned_fixture'];disk=work/'owned.img'
    report=dict(passed=False,build_id=meta['build_id'],profiles=[],checks=[])
    try:
        for label,resolution,scale,dark in [('compact',(800,600),111,False),('compact-dark',(800,600),111,True),('150',(1920,1200),112,False),('4k',(3840,2160),113,False)]:
            with ui.guest(work/('profile-'+label),disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution) as g:
                p=ui.Pointer(g);p.drain();c.open_settings(g,p);p.desktop(scale,True);assert c.flag(g,'scale73')=={111:2,112:3,113:4}[scale];p.desktop(43 if dark else 44,True);s.close(g,p);before=f.stats(g)
                c.shot(g,'groups-'+label);logical=struct.unpack('<II',ui.memory(g,ui.symbol('model',installed=True)[0]+240,8));groups=t.group_controls(g)
                assert groups and len({r[5] for r in groups})==len(groups)
                for x,y,w,h,*_ in groups:assert x>=0 and x+w<=logical[0] and y>=logical[1]-60 and y+h<=logical[1]
                first=t.launch(g,p,'text editor',2);c.type_text(g,'Keep this note');second=t.launch(g,p,'text editor',2);p.desktop(43102,True);rows=t.menu_rows(g);assert len([r for r in rows if 43020<=r['command']<43028])==2 and any('[unsaved]' in r['label'] for r in rows);c.shot(g,'chooser-'+label);c.key(g,'esc')
                t.focus(g,p,first);s.close(g,p);assert t.closing(g)==1;c.shot(g,'dirty-review-'+label);p.desktop(61,True);s.close(g,p);p.desktop(60,True);t.focus(g,p,second);s.close(g,p)
                p.desktop(43001,True);assert len(t.menu_rows(g))<=12;c.shot(g,'overflow-'+label);c.key(g,'esc')
                if label=='compact':
                    s.close(g,p);assert s.windows(g)==0
                    for name,app in [('settings',3),('downloads',5),('monitor',6),('disk utility',10),('software',11),('recovery',12),('archive',13),('help',18)]:t.launch(g,p,name,app)
                    assert s.windows(g)==8 and len(t.group_controls(g))==3;p.desktop(43001,True);first_rows=t.menu_rows(g);assert len(first_rows)<=12 and any(r['command']==43200 for r in first_rows);c.shot(g,'max-overflow-first-page');f.menu(g,p,43200);last_rows=t.menu_rows(g);assert len(last_rows)<=12 and any(r['command']==43238 for r in last_rows) and any(r['command']==43201 for r in last_rows);c.shot(g,'max-overflow-second-page');f.menu(g,p,43238);assert next(w for w in t.records(g) if w['slot']==f.model(g)[0])['app']==18 and not next(w for w in t.records(g) if w['app']==18)['minimized'];c.shot(g,'active-hidden-app');t.close_all(g,p);p.desktop(43101,True)
                    report['checks'].append('Actual 800x600 with eight pins and eight distinct running apps paginates thirteen hidden apps without exceeding twelve menu items; choosing the already-active hidden Help window focuses it rather than minimizing it')
                f.same_pages(before,f.stats(g));c.idle(g);stats=f.stats(g);report['profiles'].append(dict(name=label,physical=list(resolution),logical=list(logical),scale=c.flag(g,'scale73'),theme='dark' if dark else 'light',managed_current_bytes=stats[0]*4096,managed_peak_bytes=stats[1]*4096,retained_pages=0));(out/(label+'.log')).write_bytes(g.log().encode('utf-8'))
        report['checks'].append('Actual compact light/dark, 150% and physical 3840x2160/200% taskbar/chooser/dirty review/overflow use ordinary input, retain zero pages and halt at idle')
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode('utf-8'));print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
