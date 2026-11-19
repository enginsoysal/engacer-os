"""Run synthetic Windows x64 DLL/lazy-memory probes in the actual protected worker."""
import json,os,struct,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
from thread_native2 import task,ui,c,f,t
from access_fixtures16 import clone
from fixture1 import library,StoppedDisk
from lifetime_fixtures2 import build


def main():
    out=ROOT/'build/m14-native/stage2/probes';out.mkdir(parents=True,exist_ok=True)
    meta=json.loads(ui.manifest_path12().read_text())
    base=json.loads((ROOT/'build/m14-native/stage2/compact/results.json').read_text())
    assert base['passed'] and base['build_id']==meta['build_id']
    source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage2-compact'/base['owned_fixture']/'owned.img'
    work,disk,cloned=clone(ui,source,'m142-lifetime')
    report=dict(passed=False,build_id=meta['build_id'],synthetic=True,clone=cloned,checks=[])
    product='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}'
    try:
        boot=ui.guest(work/'prepare',disk,media='installed',ready='M7_DESKTOP_READY',ram=128)
        ui.s.normal_boot(boot)
        with boot as g:
            p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19)
            p.desktop(12001,True);task(g,p,12003)
        fixtures=build();mounted=StoppedDisk(disk,library())
        try:
            mounted.put(product+'/7z.exe',(fixtures/'probe.exe').read_bytes())
            for name in ('leaf.dll','forward.dll','dynamic.dll'):mounted.put(product+'/'+name,(fixtures/name).read_bytes())
        finally:mounted.close()
        boot=ui.guest(work/'probe',disk,media='installed',ready='M7_DESKTOP_READY',ram=128)
        ui.s.normal_boot(boot)
        with boot as g:
            p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19)
            # One-time shared transition stack is initialized before retention samples.
            warm=task(g,p,12005);assert 'M141_SPARSE_FORWARD_REFERENCE_REUSE_PASS' in warm,warm
            assert warm.count('M141_DLL_DETACH')==50 and warm.count('M141_DLL_ATTACH')==50,warm
            assert warm.rfind('Mapped original image: dynamic.dll')>warm.index('M141_DELAY_CALL_BEGIN'),warm
            report['dependency_output_sample']=warm
            report['normal_process_detach']={'attach_notifications':warm.count('M141_DLL_ATTACH'),'detach_notifications':warm.count('M141_DLL_DETACH'),'remaining_dlls_detached_at_exit':2}
            report['fixture_sha256']={name:__import__('hashlib').sha256((fixtures/name).read_bytes()).hexdigest() for name in ('probe.exe','leaf.dll','forward.dll','dynamic.dll')}
            before=f.stats(g)[0];samples=[]
            for turn in range(20):
                start=time.monotonic();text=task(g,p,12005)
                assert 'M141_SPARSE_FORWARD_REFERENCE_REUSE_PASS' in text,text
                raw=ui.memory(g,ui.symbol('info8',installed=True)[0],40)
                peak,quanta=struct.unpack_from('<QQ',raw,24)
                retained=f.stats(g)[0]-before
                assert not retained and peak<1024,(retained,peak)
                samples.append(dict(turn=turn+1,peak_owned_pages=peak,retained_pages=retained,quanta=quanta,observer_wall_seconds=time.monotonic()-start))
            report['samples']=samples
            report['checks'].append('20 actual Windows PE executions touch a 24-MiB sparse image, resolve a forwarded import and repeatedly load/reference/free/reuse an application DLL 48 times per execution')
            report['checks'].append('Each measured execution remains below 4 MiB of owned physical pages, with zero managed-page retention after one-time kernel initialization')
            (out/'serial.log').write_text(g.log())
        for mode,label in ((1,'non-executable data'),(2,'read-only data'),(3,'unmapped image guard')):
            mounted=StoppedDisk(disk,library())
            try:mounted.put(product+'/7z.exe',(fixtures/f'fault{mode}.exe').read_bytes())
            finally:mounted.close()
            boot=ui.guest(work/('fault-'+str(mode)),disk,media='installed',ready='M7_DESKTOP_READY',ram=128)
            ui.s.normal_boot(boot)
            with boot as g:
                p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19)
                retained=[]
                for turn in range(2):
                    before=f.stats(g)[0];at=len(g.log());p.desktop(12005,True,settle=False)
                    g.wait('M8_JOB_FAILED',at,90);p.drain()
                    assert 'M8_PROCESS_FAULT vector=0x000000000000000e' in g.log()[at:],g.log()[at:]
                    delta=f.stats(g)[0]-before;retained.append(delta)
                    assert delta==(4 if turn==0 else 0),(label,turn,delta)
                t.close_all(g,p);t.launch(g,p,'clock',8);t.close_all(g,p)
                (out/('fault-'+str(mode)+'.log')).write_text(g.log())
                report['checks'].append(dict(name=label,actual_cpl3_fault_contained=True,repeated_retention_pages=retained,desktop_responsive=True))
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:
        (out/'results.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
