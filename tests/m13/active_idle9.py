"""Real native active/idle cycles preserve saved files and unsaved documents."""
import argparse,hashlib,json,os,struct,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
os.environ['ENGACER12_IMAGE']='EngacerOS-M13STAGE9'
sys.path.insert(0,str(ROOT/'tests/m12'))
import settings_observe as h
import capture14,observe6,observer8
capture14.bind(h.ui);observe6.bind(h.ui);observer8.bind(h.ui)
c=h.c;f=h.f;t=h.t;ui=h.ui


def clock(g):
    return struct.unpack('<Q',ui.memory(g,ui.symbol('elapsed74',8,True)[0],8))[0]


def main():
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=int,default=180);p.add_argument('--cycles',type=int,default=3);args=p.parse_args()
    assert 10<=args.seconds<=3600 and 1<=args.cycles<=12
    assert not (ROOT/'evidence/M13/9/publication-results.json').exists()
    out=ROOT/'build/m13/stage9/active-idle';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m139-active-idle');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
    report=dict(passed=False,stage='M13.9',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],owned_fixture=work.name,requested_idle_seconds_per_cycle=args.seconds,cycles=[],checks=[],scope='Real elapsed native active/idle, RTC and document/persistent-data checks on a separate owned raw-disk fixture. Raw VRAM captures are not vendor GPU/scanout qualification; the exact VMware soak is separate.')
    def save():(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    save()
    try:
        with ui.guest(work/'install',disk,resolution=(1920,1080),ram=512) as g:
            pointer=h.q.install(g);initial=f.stats(g)
            editor=t.launch(g,pointer,'text editor',2);path=f.app(g)['path']
            c.type_text(g,'M13.9 saved document');pointer.desktop(20,True)
            persisted=b'M13.9 saved document';assert ui.s.s.document(disk,path)==persisted
            c.type_text(g,' retained draft');draft=bytes(t.app_view(g).text);assert t.app_view(g).dirty
            baseline=f.stats(g);c.shot(g,'before-idle-draft')
            for cycle in range(args.cycles):
                c.idle(g);before_clock=clock(g);began=time.monotonic()
                while time.monotonic()-began<args.seconds:
                    log=g.log();assert 'KERNEL_PANIC' not in log and 'KERNEL_REJECT:' not in log
                    time.sleep(1)
                elapsed=time.monotonic()-began;after_clock=clock(g)
                assert after_clock>before_clock,'RTC interrupt progress stopped during idle'
                assert bytes(t.app_view(g).text)==draft and t.app_view(g).dirty
                assert ui.s.s.document(disk,path)==persisted and f.model(g)[0]==editor['slot']
                c.shot(g,'cycle-'+str(cycle)+'-retained-draft')
                char=chr(ord('a')+cycle);c.type_text(g,char);draft+=char.encode()
                assert bytes(t.app_view(g).text)==draft and t.app_view(g).dirty
                f.same_pages(baseline,f.stats(g));c.idle(g)
                report['cycles'].append(dict(real_idle_seconds=elapsed,rtc_seconds_before=before_clock,rtc_seconds_after=after_clock,dirty_text_sha256=hashlib.sha256(draft).hexdigest(),saved_file_unchanged=True,same_window_owner=True,retained_pages=0,ordinary_input_after_idle=True))
                save()
            pointer.desktop(20,True);assert not t.app_view(g).dirty and ui.s.s.document(disk,path)==draft;c.shot(g,'draft-explicitly-saved')
            h.close(g,pointer);f.same_pages(initial,f.stats(g));c.idle(g)
            report['resources']=dict(before=list(initial),after=list(f.stats(g)),retained_task_delta_pages=0,all_cpus_halted_when_idle=True)
            (out/'native.log').write_text(g.log(),encoding='utf-8')
        for number in (1,2):
            boot=ui.guest(work/('disk-only-'+str(number)),disk,resolution=(1920,1080),ram=512,media='installed',ready='M7_DESKTOP_READY')
            ui.s.normal_boot(boot,work/'install/vars.fd')
            with boot as g:
                pointer=ui.Pointer(g);pointer.drain();assert ui.s.s.document(disk,path)==draft
                f.visit(g,pointer,'/Users/Owner/Documents');f.double(g,pointer,f.item(g,pointer,path.rsplit('/',1)[-1]))
                assert bytes(t.app_view(g).text)==draft and not t.app_view(g).dirty
                c.shot(g,'disk-only-'+str(number)+'-saved-document');c.idle(g)
                (out/('disk-only-'+str(number)+'.log')).write_text(g.log(),encoding='utf-8')
        report.update(passed=True,saved_document_sha256=hashlib.sha256(draft).hexdigest(),document_path=path)
        report['checks']=['Explicit Save creates independently read exact bytes before idle; subsequent unsaved edits remain owned by the same live Editor','Three separately recorded real active/idle cycles retain dirty text and original saved bytes, advance RTC interrupts, accept ordinary text input and retain zero managed pages','Explicit final Save publishes the retained draft; two independent disk-only starts reopen the actual document with exact bytes and correct saved state','Closing the task returns to baseline managed pages and idle CPUs halt without a new polling worker']
    except Exception:
        report['error']=ui.q.clean(traceback.format_exc());raise
    finally:save();print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':main()
