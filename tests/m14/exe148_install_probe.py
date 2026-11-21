"""Observe a real original installer button click in a disposable diagnostic clone; never acceptance."""
import hashlib,json,os,struct,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
    from exe148_probe_build import build
    import replay8
    loader=replay8.ReplayLoader();sys.meta_path.insert(0,loader)
    try:
        from window144_native import ui,c,f,t,clone,StoppedDisk
        from fixture1 import library
        private,inputs=build()
        original=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/SumatraPDF-3.6.1-64-install.exe'
        data=original.read_bytes();digest=hashlib.sha256(data).hexdigest()
        assert len(data)==11075960 and digest=='1eee71cccd2ea6e94d5bcea54ee2f759844da3e1a0ee2f6045035b1d17b94381'
        base=json.loads((ROOT/'build/m14-native/stage8/compact/results.json').read_text(encoding='utf-8'))
        assert base['passed'] and base['build_id']==inputs['kernel_build_id']
        source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage8-compact'/base['owned_fixture']/'owned.img'
        work,disk,cloned=clone(ui,source,'m148-original-install-click')
        mounted=StoppedDisk(disk,library())
        try:
            mounted.put('/Users/Owner/Downloads/'+original.name,data)
            mounted.put('/System/Windows/runtime8.elf',private.read_bytes())
        finally:mounted.close()
        out=ROOT/'build/m14-native/stage8/install-click-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out
        report=dict(diagnostic_completed=False,original_installer_qualified=False,
            observer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            scope='Private native routing of the unchanged original installer on full M14.8 development media; not a shipped route or successful installation.',
            kernel_build_id=base['build_id'],original_sha256=digest,original_bytes=len(data),private_inputs=inputs,clone=cloned,owned_fixture=work.name)
        try:
            boot=ui.guest(work/'startup',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
            with boot as g:
                p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19)
                before=f.stats(g)[0];p.desktop(12001,True);at=len(g.log());p.desktop(12003,True,settle=False)
                g.wait('M8_CPL3_CREATED',at)
                deadline=time.monotonic()+5
                while time.monotonic()<deadline:
                    raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384)
                    if struct.unpack_from('<I',raw)[0]!=1:break
                    time.sleep(.05)
                p.drain();c.shot(g,'original-installer-before-click')
                live=t.records(g);others=[w for w in live if w['token']!=front['token']];original_window=others[0] if len(others)==1 else None
                if original_window:
                    t.focus(g,p,original_window);x,y,width,height=f.model(g)[1];scale=c.flag(g,'scale73');click_x,click_y=x+width-100,y+height-25
                    report['ordinary_original_button_click']=dict(window_token=original_window['token'],logical_x=click_x,logical_y=click_y,source='Original visible Install SumatraPDF button; ordinary guest pointer down/up')
                    p.click(click_x*scale//2,click_y*scale//2);p.drain()
                    deadline=time.monotonic()+30
                    while time.monotonic()<deadline:
                        raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384)
                        if struct.unpack_from('<I',raw)[0]!=1:break
                        time.sleep(.05)
                p.drain();c.shot(g,'original-installer-after-click')
                raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384)
                state,command,status=struct.unpack_from('<3I',raw)
                report.update(state=state,status=status,message=raw[304:496].split(b'\0')[0].decode(errors='replace'),
                    output=raw[496:].split(b'\0')[0].decode(errors='replace'),native_windows=t.records(g),
                    pages_before_cleanup=f.stats(g)[0]-before)
                report['original_install_callback_observed']='OnButtonInstall:' in report['output']
                report['installer_flag_observed']='flags.install: 1' in report['output']
                report['original_startup_name_observed']='Starting: \'"C:\\Users\\Owner\\Downloads\\SumatraPDF-3.6.1-64-install.exe" -install -d ' in report['output']
                report['command_context_scope']='Private startup command override before runtime initialization; kernel grants still belong to the diagnostic MSI frontend.'
                if 'flags.install:' in report['output']:
                    assert report['installer_flag_observed'],report['output']
                    assert report['original_startup_name_observed'],report['output']
                if state==1:
                    t.focus(g,p,front);p.desktop(12008,True);report['explicit_diagnostic_cancel']=True
                report['retained_pages_after_cleanup']=f.stats(g)[0]-before
                (out/'serial.log').write_bytes(g.log().encode())
            mounted=StoppedDisk(disk,library())
            try:
                keys=values=0
                for entry in mounted.volume.entries:
                    if entry.kind!=1 or b'/Registry/' not in entry.path:continue
                    mounted.file.seek(mounted.offset+entry.first*4096);magic=mounted.file.read(8)
                    keys+=magic==struct.pack('<Q',0x314b52454734314d);values+=magic==struct.pack('<Q',0x315652454734314d)
                report['diagnostic_persistent_registry_keys']=keys
                report['diagnostic_persistent_registry_values']=values
                target=b'/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/SumatraPDF.exe'
                copied=next((e for e in mounted.volume.entries if e.kind==1 and e.path==target),None)
                report['diagnostic_self_copy_present']=copied is not None
                if copied:
                    assert copied.size<=64*1024*1024
                    mounted.file.seek(mounted.offset+copied.first*4096);copied_bytes=mounted.file.read(copied.size)
                    report['diagnostic_self_copy_bytes']=len(copied_bytes)
                    report['diagnostic_self_copy_sha256']=hashlib.sha256(copied_bytes).hexdigest()
                    report['diagnostic_self_copy_matches_original']=len(copied_bytes)==len(data) and report['diagnostic_self_copy_sha256']==digest
                for entry in mounted.volume.entries:
                    if entry.kind!=1 or entry.size!=552:continue
                    mounted.file.seek(mounted.offset+entry.first*4096);metadata=mounted.file.read(552)
                    if struct.unpack_from('<Q',metadata)[0]!=0x314d464e4534314d or metadata[264:520].split(b'\0')[0]!=target:continue
                    report['diagnostic_self_copy_metadata_times']=list(struct.unpack_from('<3Q',metadata,520))
                    report['diagnostic_self_copy_metadata_attributes']=struct.unpack_from('<I',metadata,544)[0]
            finally:mounted.close()
            report['diagnostic_completed']=True
        except Exception:
            report['observer_error']=ui.q.clean(traceback.format_exc());raise
        finally:
            (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
    finally:sys.meta_path.remove(loader)

if __name__=='__main__':main()
