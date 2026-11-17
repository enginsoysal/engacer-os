"""Actual compact/light/dark/150%/4K Start and keyboard result layouts."""
import json,os,struct,traceback
from pathlib import Path
import start_native as s
c=s.c;f=s.f;ui=s.ui;ROOT=s.ROOT
def main():
    out=ROOT/'build/m12/stage9/start-profiles';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    native=json.loads((ROOT/'build/m12/stage9/start-native/results.json').read_text());meta=json.loads(ui.manifest_path12().read_text());assert native['passed'] and native['build_id']==meta['build_id']
    work=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage9-start'/native['owned_fixture'];disk=work/'owned.img'
    report=dict(passed=False,build_id=meta['build_id'],profiles=[],checks=[])
    try:
        for label,resolution,scale,dark in [('compact',(800,600),111,False),('compact-dark',(800,600),111,True),('150',(1920,1200),112,False),('4k',(3840,2160),113,False)]:
            with ui.guest(work/('profile-'+label),disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution) as g:
                p=ui.Pointer(g);p.drain();c.open_settings(g,p);p.desktop(scale,True);assert c.flag(g,'scale73')=={111:2,112:3,113:4}[scale];p.desktop(43 if dark else 44,True);s.close(g,p);before=f.stats(g)
                p.desktop(0,True);p.desktop(42000,True);c.shot(g,'pinned-'+label)
                x,y,w,h=s.bounds(g);assert x>=0 and y>=0
                model=ui.symbol('model',installed=True)[0];logical=struct.unpack('<II',ui.memory(g,model+240,8));assert x+w<=logical[0] and y+h<=logical[1]-60
                for _ in range(6):
                    c.key(g,'tab');assert c.flag(g,'control_active') and 42000<=c.flag(g,'focused_action')<43400
                p.desktop(42001,True)
                if not s.prefs(g).view:p.desktop(42003,True)
                c.shot(g,'all-apps-'+label)
                s.search(g,p,'calc');rows=[r for r in f.controls(g) if 42200<=r[5]<42252];assert len(rows)==1 and rows[0][2]>w-60;c.shot(g,'search-'+label)
                c.key(g,'down');c.key(g,'shift','f10');assert c.flag(g,'context11');c.shot(g,'context-'+label);c.key(g,'esc');c.key(g,'ret');assert s.windows(g,4)==1;s.close(g,p)
                p.desktop(0,True);p.desktop(42007,True);p.desktop(42010,True);c.shot(g,'category-dialog-'+label);c.key(g,'esc');p.desktop(42008,True);c.key(g,'esc');f.same_pages(before,f.stats(g));c.idle(g)
                stats=f.stats(g);report['profiles'].append(dict(name=label,physical=list(resolution),logical=list(logical),scale=c.flag(g,'scale73'),theme='dark' if dark else 'light',managed_current_bytes=stats[0]*4096,managed_peak_bytes=stats[1]*4096,retained_pages=0));(out/(label+'.log')).write_bytes(g.log().encode())
        report['checks'].append('Actual compact light/dark, 150% and physical 3840x2160/200% Start, apps, local search, context and category review use real input, retain zero pages and halt when idle')
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
