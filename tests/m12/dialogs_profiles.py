"""Ordinary installed starts and physical display profiles for shared dialogs."""
import json,os,struct,traceback
from pathlib import Path
import dialogs_native as d
c=d.c;f=d.f;ui=d.ui;ROOT=d.ROOT

def main():
    out=ROOT/'build/m12/stage8/dialogs-profiles';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    native=json.loads((ROOT/'build/m12/stage8/dialogs-native/results.json').read_text())
    meta=json.loads(ui.manifest_path12().read_text());assert native['passed'] and native['build_id']==meta['build_id']
    work=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage8-dialogs'/native['owned_fixture'];disk=work/'owned.img'
    report=dict(passed=False,build_id=meta['build_id'],feature_journeys_passed=native['passed'],checks=[],profiles=[])
    try:
        for number in (1,2):
            boot=ui.guest(work/f'dialogs-boot-{number}',disk,media='installed',ready='M7_DESKTOP_READY');ui.s.normal_boot(boot,work/'install/vars.fd')
            with boot as g:
                p=ui.Pointer(g);p.drain();f.visit(g,p,'Documents');p.desktop(f.item(g,p,'Existing.txt'),True);c.key(g,'ret');p.desktop(54001,True)
                assert d.picker(g).path==b'/Users/Owner/Documents';c.shot(g,f'ordinary-{number}');p.desktop(54010,True);d.close_focused(g,p);c.idle(g)
                (out/f'ordinary-{number}.log').write_bytes(g.log().encode())
            report['checks'].append(f'Ordinary no-ISO start {number} retains files and successful remembered Save destination using the same firmware variables')
        for label,resolution,scale in [('minimum-height',(1280,1024),113),('compact',(800,600),111),('compact-dark',(800,600),111),('150',(1920,1200),112),('4k',(3840,2160),113)]:
            with ui.guest(work/('dialogs-'+label),disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution) as g:
                p=ui.Pointer(g);p.drain();c.open_settings(g,p);p.desktop(scale,True);p.desktop(43 if label=='compact-dark' else 44,True);p.close_app(3,True);p.drain();before=f.stats(g)
                f.visit(g,p,'Documents');p.desktop(f.item(g,p,'Existing.txt'),True);c.key(g,'ret');p.desktop(54001,True);assert c.flag(g,'file_dialog_state11')==10
                c.shot(g,'save-as-'+label);p.desktop(54024,True);c.shot(g,'new-folder-'+label);p.desktop(54026,True);p.desktop(54011,True);assert d.picker(g).phase==1;c.shot(g,'replace-'+label);p.desktop(54026,True);p.desktop(54010,True)
                p.desktop(54000,True);c.shot(g,'open-'+label);p.desktop(54010,True);c.key(g,'end');c.type_text(g,' ui');p.desktop(54000,True);p.desktop(54016,True);d.choose(g,p,'First.txt');c.key(g,'ret');assert d.picker(g).phase==2;c.shot(g,'dirty-'+label);p.desktop(54028,True);d.close_focused(g,p);f.same_pages(before,f.stats(g));c.idle(g)
                stats=f.stats(g);report['profiles'].append(dict(physical=list(resolution),logical=list(struct.unpack('<II',ui.memory(g,ui.symbol('model',installed=True)[0]+240,8))),theme='dark' if label=='compact-dark' else 'light',scale=c.flag(g,'scale73'),managed_current_bytes=stats[0]*4096,managed_peak_bytes=stats[1]*4096,retained_pages=0))
                (out/(label+'.log')).write_bytes(g.log().encode())
        report['checks'].append('Actual compact, 150% and 3840x2160/200% Open/Save/new-folder controls retain zero pages and halted idle CPUs')
        report['passed']=True
    except Exception:
        report['error']=ui.q.clean(traceback.format_exc());raise
    finally:
        (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
