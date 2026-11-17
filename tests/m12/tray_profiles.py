"""Actual compact/light/dark/150%/4K system flyout layout and bounded idle state."""
import json,os,struct,traceback
from pathlib import Path
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE12'
import tray_observe as q
c=q.c;f=q.f;s=q.s;t=q.t;ui=q.ui;ROOT=q.ROOT

def main():
    out=ROOT/'build/m12/stage12/tray-profiles';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    native=json.loads((ROOT/'build/m12/stage12/tray-native/results.json').read_text(encoding='utf-8'));meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));assert native['passed'] and native['build_id']==meta['build_id']
    work=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage12-tray'/native['owned_fixture'];disk=work/'owned.img';report=dict(passed=False,build_id=meta['build_id'],profiles=[],checks=[])
    try:
        for label,resolution,scale,dark in [('compact',(800,600),111,False),('compact-dark',(800,600),111,True),('150',(1920,1200),112,False),('4k',(3840,2160),113,False)]:
            with ui.guest(work/('profile-'+label),disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution) as g:
                p=ui.Pointer(g);p.drain();c.open_settings(g,p);p.desktop(scale,True);assert c.flag(g,'scale73')=={111:2,112:3,113:4}[scale];p.desktop(43 if dark else 44,True);s.close(g,p);before=f.stats(g)
                logical=struct.unpack('<II',ui.memory(g,ui.symbol('model',installed=True)[0]+240,8));reserve=64 if logical[0]<1000 else 180
                for x,y,w,h,*_ in t.group_controls(g):assert 0<=x and x+w<=logical[0]-reserve and logical[1]-60<=y and y+h<=logical[1]
                action=58000 if logical[0]<1000 else 58005;assert q.has(g,action);p.desktop(action,True);assert c.flag(g,'tray_open12')==1
                c.shot(g,'quick-'+label);c.idle(g)
                for action,mode,name in [(58002,2,'usb-'),(58003,3,'calendar-')]:
                    p.desktop(action,True);assert c.flag(g,'tray_open12')==mode
                    for x,y,w,h,_,command in f.controls(g):
                        if 58000<=command<58300:assert x>=0 and y>=0 and x+w<=logical[0] and y+h<=logical[1],(label,command,x,y,w,h,logical)
                    c.key(g,'tab');assert c.flag(g,'control_active') and 58000<=c.flag(g,'focused_action')<58300;c.shot(g,name+label)
                c.key(g,'esc');assert not c.flag(g,'tray_open12');f.same_pages(before,f.stats(g));c.idle(g);stats=f.stats(g)
                report['profiles'].append(dict(name=label,physical=list(resolution),logical=list(logical),scale=c.flag(g,'scale73'),theme='dark' if dark else 'light',managed_current_bytes=stats[0]*4096,managed_peak_bytes=stats[1]*4096,retained_pages=0));(out/(label+'.log')).write_bytes(g.log().encode())
        report['checks'].append('Actual 800x600 light/dark, 1920x1200/150% and 3840x2160/200% keep taskbar groups outside the system area and all three flyouts reachable, keyboard focus visible and memory stable at idle')
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
