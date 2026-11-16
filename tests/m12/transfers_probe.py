"""Development-only reproduction of cancellation using an explicitly owned fixture."""
import argparse,json,os,shutil,uuid,traceback
from pathlib import Path
import transfers_native as t
f=t.f;c=t.c;ui=t.ui;ROOT=t.ROOT

def main():
    p=argparse.ArgumentParser();p.add_argument('--fixture',required=True);a=p.parse_args()
    assert len(a.fixture)==32 and all(ch in '0123456789abcdef' for ch in a.fixture)
    family=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage7-transfers';work=family/a.fixture
    assert work.resolve().is_relative_to(family.resolve()) and (work/'owned.img').is_file()
    out=ROOT/'build/m12/stage7/diagnostics';out.mkdir(exist_ok=True)
    for name in ('results.json','failure.log','usb-transfer-progress.png'):
        source=t.OUT/name
        if source.exists():shutil.copyfile(source,out/('control-snapshot-observer-'+name.replace('.log','.txt')))
    t.OUT=out;c.OUT=out;source=work/'owned-usb.img';before=f.sha_file(source);report=dict(passed=False,development_only=True,fixture=a.fixture,build_id=json.loads(ui.manifest_path12().read_text())['build_id'])
    try:
        guest=ui.guest(work/('cancel-probe-'+uuid.uuid4().hex),work/'owned.img',media='installed',ready='M7_DESKTOP_READY',extra=['-drive',f'if=none,id=probe-source,format=raw,file={source}'])
        ui.s.normal_boot(guest,work/'install/vars.fd')
        with guest as g:
            assert 'M7_DESKTOP_READY build='+report['build_id'] in g.log(),'A probe requires a fixture installed from the matching current media'
            pointer=ui.Pointer(g);pointer.drain();pointer.desktop(21000,True);f.attach(g,pointer,'probe-source','probe-usb');pointer.desktop(f.drive(g),True);c.key(g,'ret');pointer.desktop(f.row(g,'Large.bin'),True)
            t.start(g,pointer,21004);t.busy_frame(g);t.capture_active(g,'cancel-probe-active');c.key(g,'esc');t.wait(g,pointer)
            assert '/Users/Owner/Downloads/Large.bin' not in f.entries(g)
            assert 'cancelled=0x0000000000000001' in g.log();report['cancelled_job']=t.job(g);c.shot(g,'cancel-probe-result')
            pointer.desktop(f.row(g,'Large.bin'),True);c.key(g,'ctrl','c');f.visit(g,pointer,'Pictures');t.start(g,pointer,40002);t.busy_frame(g)
            g.qmp('device_del',{'id':'probe-usb'});t.wait(g,pointer,error=(3,9))
            assert '/Users/Owner/Pictures/Large.bin' not in f.entries(g);report['removed_source_job']=t.job(g);report['removed_source_error']=c.flag(g,'file_job_error11');c.shot(g,'removed-source-probe-result')
            (out/'cancel-probe-log.txt').write_text(ui.q.clean(g.log()),encoding='utf-8')
        assert f.sha_file(source)==before;report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'cancel-probe-results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
