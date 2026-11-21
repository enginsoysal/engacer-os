"""Observe original Sumatra installer startup; diagnostic only, never acceptance."""
import hashlib,json,os,struct,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
    import replay8
    loader=replay8.ReplayLoader();sys.meta_path.insert(0,loader)
    try:
        from window144_native import ui,c,f,t,clone,StoppedDisk
        from fixture1 import library
        from exe148_probe_build import build
        private,inputs=build()
        original=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/SumatraPDF-3.6.1-64-install.exe'
        data=original.read_bytes();digest=hashlib.sha256(data).hexdigest()
        assert len(data)==11075960 and digest=='1eee71cccd2ea6e94d5bcea54ee2f759844da3e1a0ee2f6045035b1d17b94381'
        base=json.loads((ROOT/'build/m14-native/stage8/compact/results.json').read_text(encoding='utf-8'))
        assert base['passed'] and base['build_id']==inputs['kernel_build_id']
        source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage8-compact'/base['owned_fixture']/'owned.img'
        work,disk,cloned=clone(ui,source,'m148-original-installer-startup')
        mounted=StoppedDisk(disk,library())
        try:
            mounted.put('/Users/Owner/Downloads/'+original.name,data)
            mounted.put('/System/Windows/runtime8.elf',private.read_bytes())
        finally:mounted.close()
        out=ROOT/'build/m14-native/stage8/startup-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out
        report=dict(diagnostic_completed=False,original_installer_qualified=False,
            scope='Private native routing of the unchanged original installer on full M14.8 development media; not a shipped route or successful installation.',
            kernel_build_id=base['build_id'],original_sha256=digest,original_bytes=len(data),private_inputs=inputs,clone=cloned,owned_fixture=work.name)
        try:
            boot=ui.guest(work/'startup',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
            with boot as g:
                p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19)
                before=f.stats(g)[0];p.desktop(12001,True);at=len(g.log());p.desktop(12003,True,settle=False)
                g.wait('M8_CPL3_CREATED',at)
                deadline=time.monotonic()+45
                while time.monotonic()<deadline:
                    raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384)
                    if struct.unpack_from('<I',raw)[0]!=1:break
                    time.sleep(.05)
                p.drain();c.shot(g,'original-installer-startup')
                raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384)
                state,command,status=struct.unpack_from('<3I',raw)
                report.update(state=state,status=status,message=raw[304:496].split(b'\0')[0].decode(errors='replace'),
                    output=raw[496:].split(b'\0')[0].decode(errors='replace'),native_windows=t.records(g),
                    pages_before_cleanup=f.stats(g)[0]-before)
                if state==1:
                    p.desktop(12008,True);report['explicit_diagnostic_cancel']=True
                report['retained_pages_after_cleanup']=f.stats(g)[0]-before
                (out/'serial.log').write_bytes(g.log().encode())
            report['diagnostic_completed']=True
        except Exception:
            report['observer_error']=ui.q.clean(traceback.format_exc());raise
        finally:
            (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
    finally:sys.meta_path.remove(loader)

if __name__=='__main__':main()
