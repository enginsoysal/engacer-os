"""Real Settings/idle/wake transactions on owned media; no simulated uptime."""
import ctypes,hashlib,json,os,struct,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
os.environ['ENGACER12_IMAGE']='EngacerOS-M13STAGE11'
sys.path.insert(0,str(ROOT/'tests/m12'))
import settings_observe as h
import capture14,observe20,observer8
c=h.c;f=h.f;s=h.s;t=h.t;ui=h.ui
capture14.bind(ui);observe20.bind(ui);observer8.bind(ui)
PATH='/System/Settings/screensaver21-Owner.bin'


def phase(g):return c.flag(g,'saver_phase21',4)
def read_record(g,name):
    try:return struct.unpack('<5I',ui.memory(g,ui.symbol(name,20,True)[0],20))
    except AssertionError:return tuple(int.from_bytes(c.field(g,name,i,4),'little') for i in range(5))
def saved(g):return read_record(g,'saver_saved21')
def wait(g,value,seconds=10):
    end=time.monotonic()+seconds
    while phase(g)!=value:
        if time.monotonic()>end:raise AssertionError(('Screensaver phase',value,phase(g)))
        time.sleep(.05)
def raw_key(g,key,down):g.qmp('input-send-event',{'events':[{'type':'key','data':{'down':down,'key':{'type':'qcode','data':key}}}]})
def open_saver(g,p):
    if not any(w['app']==3 for w in t.records(g)):t.launch(g,p,'settings',3)
    p.desktop(59000,True);p.desktop(60200,True);assert h.page(g)==6
def preview(g,p):p.desktop(60209,True);wait(g,2)
def wake(g,key='esc'):c.key(g,key);wait(g,0)
def editor_view(g,slot):
    from focus_ownership import View
    address,size=ui.symbol('apps',installed=True)
    return View.from_buffer_copy(ui.memory(g,address+slot*(size//8),ctypes.sizeof(View)))


def main():
    out=ROOT/'build/m13/stage11/screensaver-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m1311-saver');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
    report=dict(passed=False,stage='M13.11',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],owned_fixture=work.name,checks=[],scope='One-minute idle activation is a functional feature task; natural freezes and duration/reset-chain qualification remain exclusively M13.13')
    try:
        with ui.guest(work/'install',disk,resolution=(1920,1080),ram=512) as g:
            p=h.q.install(g);t.close_all(g,p);baseline=f.stats(g);welcome=ui.s.s.document(disk,'/Users/Owner/Documents/Welcome.txt');before=f.sha_file(disk)
            assert saved(g)==(0x31325345,1,0,60,0) and not c.flag(g,'saver_invalid21')
            open_saver(g,p);c.shot(g,'default-off');preview(g,p);c.shot(g,'logo-preview');wake(g)
            assert f.sha_file(disk)==before and h.page(g)==6
            for action,style in [(60207,1),(60208,2),(60206,0)]:
                p.desktop(action,True);preview(g,p);c.shot(g,'preview-'+str(style));wake(g)
            assert f.sha_file(disk)==before
            p.desktop(60211,True);assert not c.flag(g,'saver_owner21',8) and saved(g)[2:]==(0,60,0)
            report['checks'].append('Off defaults and all three actual previews work without writing the complete disk; Cancel restores the saved state and wake returns to the same Settings page without click-through')
            p.desktop(60202,True);p.desktop(60204,True);p.desktop(60207,True)
            first=next(w for w in t.records(g) if w['slot']==f.model(g)[0]);other=t.launch(g,p,'settings',3);p.desktop(60200,True)
            assert not f.has(g,60202) and not f.has(g,60210);c.shot(g,'competing-owner');h.close(g,p);t.focus(g,p,first);assert read_record(g,'saver_draft21')[2:]==(1,300,1)
            c.key(g,'esc');assert not c.flag(g,'saver_owner21',8);p.desktop(60202,True);p.desktop(60204,True);p.desktop(60207,True);p.desktop(60210,True)
            expected=struct.pack('<5I',0x31325345,1,1,300,1);assert ui.s.s.document(disk,PATH)==expected
            p.desktop(60208,True);p.desktop(59001,True);assert not c.flag(g,'saver_owner21',8) and saved(g)[2:]==(1,300,1);p.desktop(59000,True);p.desktop(60200,True)
            p.desktop(60212,True);assert read_record(g,'saver_draft21')[2:]==(0,60,0);p.desktop(60211,True);assert ui.s.s.document(disk,PATH)==expected
            report['checks'].append('Only the draft owner can edit or Apply; Escape, leaving the page and Restore defaults/Cancel preserve the exact independently read twenty-byte saved record')
            # A held activation key cannot immediately dismiss its own preview.
            preview(g,p);wake(g)
            for _ in range(64):
                if c.flag(g,'control_active') and c.flag(g,'focused_action')==60209:break
                c.key(g,'tab')
            else:raise AssertionError('Preview could not be reached through real keyboard focus')
            raw_key(g,'ret',True);wait(g,1);time.sleep(.25);assert phase(g)==1;raw_key(g,'ret',False);wait(g,2);c.shot(g,'held-enter-preview')
            raw_key(g,'ctrl',True);wait(g,3);time.sleep(.1);assert phase(g)==3;raw_key(g,'ctrl',False);wait(g,0)
            assert not c.flag(g,'control_modifier') and not c.flag(g,'usb_modifiers11')
            preview(g,p);g.qmp('input-send-event',{'events':[{'type':'btn','data':{'down':True,'button':'wheel-up'}},{'type':'btn','data':{'down':False,'button':'wheel-up'}}]});wait(g,0)
            report['checks'].append('A genuinely held Enter activation arms until release; a held Ctrl wake remains consumed until release, leaves no modifier state and wheel input also returns without scrolling the Settings behind the saver')
            # Keep dirty work and the complete eight-window model through Preview.
            h.close(g,p);editor=t.launch(g,p,'text editor',2);c.type_text(g,'Keep this unsaved document');dirty=bytes(t.app_view(g).text);assert t.app_view(g).dirty
            settings=t.launch(g,p,'settings',3);open_saver(g,p)
            for _ in range(6):t.launch(g,p,'files',1)
            assert len(t.records(g))==8;t.focus(g,p,settings);tokens=t.records(g);preview(g,p);c.shot(g,'eight-window-preview');wake(g,'a');assert t.records(g)==tokens
            assert bytes(editor_view(g,editor['slot']).text)==dirty and editor_view(g,editor['slot']).dirty
            t.close_all(g,p);assert ui.s.s.document(disk,'/Users/Owner/Documents/Welcome.txt')==welcome
            report['checks'].append('Eight actual window generations and exact unsaved Editor text survive a consumed letter wake; explicit later Discard closes the work and the original personal document remains independently unchanged')
            # Native base Settings can remove Clock independently of this feature.
            open_saver(g,p);p.desktop(59003,True);p.desktop(10000,True);h.software_change(g,p,8);p.desktop(10005,True);open_saver(g,p);p.desktop(60207,True);preview(g,p);c.shot(g,'clock-with-clock-app-removed');wake(g)
            p.desktop(59003,True);p.desktop(10000,True);h.software_change(g,p,8);p.desktop(10005,True);open_saver(g,p)
            report['checks'].append('Removing and reinstalling the optional Clock through base Settings does not break the actual Clock screensaver, Files or Settings; the saver uses the shared native clock service')
            # Actual elapsed idle feature test: no timer counter or guest state writes.
            p.desktop(60202,True);p.desktop(60203,True);p.desktop(60206,True);p.desktop(60210,True);h.close(g,p)
            start=time.monotonic();start_ticks=int.from_bytes(ui.memory(g,ui.symbol('ticks',8,True)[0],8),'little')
            wait(g,2,70);elapsed=time.monotonic()-start;assert elapsed>=58,elapsed;c.shot(g,'actual-one-minute-idle');wake(g)
            report['actual_idle_feature_seconds']=elapsed;report['start_ticks']=start_ticks
            report['checks'].append('The enabled one-minute choice activates after actual elapsed keyboard/mouse inactivity and wakes to the retained desktop; this is a functional timeout check, not a stability soak')
            open_saver(g,p);p.desktop(60201,True);p.desktop(60205,True);p.desktop(60208,True);p.desktop(60210,True);final=struct.pack('<5I',0x31325345,1,0,600,2);assert ui.s.s.document(disk,PATH)==final;h.close(g,p);t.close_all(g,p);f.same_pages(baseline,f.stats(g));c.idle(g)
            report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0);report['saved_record_hex']=final.hex();(out/'native.log').write_bytes(g.log().encode())
        for label,ps2 in [('usb',False),('ps2',True)]:
            boot=ui.guest(work/('disk-only-'+label),disk,resolution=(1920,1080),ram=512,media='installed',ready='M7_DESKTOP_READY',ps2_only=ps2);ui.s.normal_boot(boot,work/'install/vars.fd')
            with boot as g:
                p=ui.Pointer(g);p.drain();assert saved(g)==struct.unpack('<5I',final) and not c.flag(g,'saver_invalid21');open_saver(g,p);preview(g,p);wake(g);h.close(g,p);c.idle(g);(out/('disk-only-'+label+'.log')).write_bytes(g.log().encode())
        assert ui.s.s.document(disk,'/Users/Owner/Documents/Welcome.txt')==welcome
        report['checks'].append('Two ordinary no-ISO USB/PS2 starts load exact saved Off/ten-minute/Blank choices, preview/wake with real input, preserve personal bytes and halt at idle')
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2),flush=True)


if __name__=='__main__':main()
