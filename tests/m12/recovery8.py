"""Replay the compressed real installed slot, then boot its repaired BIOS files."""
import os,json,traceback
from pathlib import Path
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE8'
import components as c
ui=c.ui;ROOT=ui.ROOT

def main():
    out=ROOT/'build/m12/stage8/recovery';out.mkdir(exist_ok=True);c.OUT=out
    meta=json.loads(ui.manifest_path12().read_text());native=json.loads((ROOT/'build/m12/stage8/dialogs-native/results.json').read_text())
    assert native['passed'] and native['build_id']==meta['build_id']
    work=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage8-dialogs'/native['owned_fixture'];disk=work/'owned.img'
    report=dict(passed=False,build_id=meta['build_id'],iso_sha256=meta['artifacts']['EngacerOS-M12STAGE8.iso']['sha256'],checks=[])
    try:
        before=ui.q.digest(disk,2112*512,4096)
        with disk.open('r+b') as stream:
            stream.seek(2112*512+511);value=stream.read(1);stream.seek(-1,1);stream.write(bytes([value[0]^255]))
        repair=ui.guest(work/'compressed-repair',disk);original=repair.wait
        def recovery_wait(text,after=0,timeout=90):
            if text==repair.ready:
                original('M115_RECOVERY_WINDOW',after,timeout);ui.h.key(repair,'esc');original('M75_SETUP_OVERRIDE',after,10)
            return original(text,after,timeout)
        repair.wait=recovery_wait
        with repair as g:
            p=ui.Pointer(g)
            for action in (50,80,100,2):c.wizard(g,p,action)
            start=c.wizard(g,p,2);g.wait('M6_MAINTENANCE_PASS',start,240)
            g.qmp('stop')
            try:ui.raw_shot(g,out,'recovery-complete',False)
            finally:g.qmp('cont')
            (out/'recovery.log').write_bytes(g.log().encode())
        assert ui.q.digest(disk,2112*512,4096)==before
        report['checks'].append('Actual ISO recovery validates and decodes its on-disk compressed slot, restoring deliberately corrupted owned BIOS bytes exactly')
        with ui.guest(work/'compressed-repaired-bios',disk,firmware='bios',media='installed',ready='M7_DESKTOP_READY') as g:
            assert 'M7_DESKTOP_READY build='+meta['build_id'] in g.log();ui.Pointer(g).drain();c.shot(g,'repaired-disk-desktop');c.idle(g);(out/'repaired-boot.log').write_bytes(g.log().encode())
        assert ui.s.s.document(disk,'/Users/Owner/Downloads/Saved.txt')==b'Original native text edited'
        report['checks'].append('Repaired BIOS disk starts without ISO and independently stored user data remains unchanged')
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
