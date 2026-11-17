"""Base tray/calendar/audio independence from removable optional applications."""
import json,os,time,traceback
from pathlib import Path
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE12'
import tray_observe as q
c=q.c;f=q.f;s=q.s;t=q.t;ui=q.ui;ROOT=q.ROOT

def close(g,p):
    target=next(w for w in t.records(g) if w['slot']==f.model(g)[0]);deadline=time.monotonic()+15
    while True:
        rows=[r for r in f.controls(g) if r[5]==49002 and r[4]==target['token']]
        if len(rows)==1:break
        if time.monotonic()>deadline:raise AssertionError(('Caption not painted for live owner',target,f.controls(g)))
        time.sleep(.05)
    x,y,w,h,*_=rows[0];p.logical(x+w//2,y+h//2,True);p.drain();assert not any(w['token']==target['token'] for w in t.records(g))

def ensure_installed(g,p,name,kind):
    s.search(g,p,name);present=(1,kind) in s.results(g);c.key(g,'esc');c.key(g,'esc')
    if not present:t.launch(g,p,'software',11);change(g,p,kind);close(g,p)

def change(g,p,kind):
    for _ in range(8):
        if q.has(g,10300+kind):break
        assert q.has(g,10002);p.desktop(10002,True)
    else:raise AssertionError(('Missing optional package control',kind))
    p.desktop(10300+kind,True)
    if q.has(g,10004):p.desktop(10004,True)

def main():
    out=ROOT/'build/m12/stage12/tray-optional';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    native=json.loads((ROOT/'build/m12/stage12/tray-native/results.json').read_text(encoding='utf-8'));meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));assert native['passed'] and native['build_id']==meta['build_id']
    work=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage12-tray'/native['owned_fixture'];report=dict(passed=False,build_id=meta['build_id'],checks=[])
    try:
        with ui.guest(work/'optional',work/'owned.img',media='installed',ready='M7_DESKTOP_READY') as g:
            p=ui.Pointer(g);p.drain();t.close_all(g,p)
            for name,kind in [('clock',8),('calendar',9),('media',16)]:ensure_installed(g,p,name,kind)
            baseline=f.stats(g)
            t.launch(g,p,'files',1);f.visit(g,p,'Music');p.desktop(f.item(g,p,'Chime.wav'),True);c.key(g,'ret');assert s.windows(g,16)==1;p.desktop(18001,True);assert q.audio(g)[0]==3
            q.open_quick(g);assert q.audio(g)[0]==3;c.shot(g,'real-playback-unavailable');c.key(g,'esc');s.close(g,p);t.close_all(g,p)
            report['checks'].append('Playing the included original WAV without an audio controller reaches the real provider failure state; Quick settings reports unavailable playback rather than invented hardware readiness')
            for name,kind in [('clock',8),('calendar',9),('media',16)]:
                t.launch(g,p,'software',11);change(g,p,kind);close(g,p);s.search(g,p,name);assert (1,kind) not in s.results(g);c.key(g,'esc');c.key(g,'esc')
            q.open_quick(g);p.desktop(58016,True);assert s.windows(g)==0 and 'install' in q.notice(g).lower();p.desktop(58003,True);assert 2000<=q.date(g)[0]<=2099;p.desktop(58023,True);assert s.windows(g)==0 and 'install' in q.notice(g).lower();c.shot(g,'optional-calendar-removed');c.key(g,'esc')
            for name,kind in [('clock',8),('calendar',9),('media',16)]:
                t.launch(g,p,'software',11);change(g,p,kind);close(g,p);t.launch(g,p,name,kind);close(g,p)
            for name,kind in [('clock',8),('calendar',9),('media',16)]:t.pin(g,p,name,kind)
            f.same_pages(baseline,f.stats(g));c.idle(g);report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0);(out/'native.log').write_bytes(g.log().encode())
        report['checks'].append('Actual Clock, Calendar and Media Player removal leaves the base flyout, real date and provider controls usable; missing optional launch targets explain installation, and all three apps reinstall and launch independently')
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
