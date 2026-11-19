"""Download the real Mozilla installer through native ordinary browser controls."""
import hashlib,json,os,re,struct,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
os.environ['ENGACER12_IMAGE']='EngacerOS-M14STAGE2'
sys.path[:0]=[str(ROOT/'tests/m12'),str(ROOT/'tests/m13')]
import taskbar_observe as t
ui=t.ui;c=t.c;f=t.f
import capture14,observer8
capture14.bind(ui);observer8.bind(ui)
from access_fixtures16 import clone

def main():
    out=ROOT/'build/m14-native/stage2/browser-download';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'))
    base=json.loads((ROOT/'build/m14-native/stage2/ordinary/results.json').read_text(encoding='utf-8'))
    assert base['passed'] and base['build_id']==meta['build_id']
    source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage2-ordinary'/base['owned_fixture']/'owned.img'
    work,disk,cloned=clone(ui,source,'m142-browser-download')
    report=dict(passed=False,build_id=meta['build_id'],clone=cloned,checks=[])
    mapping=ui.MAPS74[True].split('kernel_network_download-kernel.o:(.bss)',1)[1]
    match=re.search(r'^\s*([0-9a-f]+)\s+[0-9a-f]+\s+[0-9a-f]+\s+\d+\s+info$',mapping,re.M)
    assert match;address=int(match[1],16)
    extra=['-cpu','max,x2apic=off','-rtc','base=utc,clock=host','-netdev','user,id=m141net','-device','e1000,netdev=m141net,mac=52:54:00:14:01:01','-object','filter-dump,id=m141capture,netdev=m141net,file='+str(work/'download.pcap')]
    try:
        boot=ui.guest(work/'download',disk,media='installed',ready='M7_DESKTOP_READY',resolution=(1920,1080),ram=512,extra=extra)
        ui.s.normal_boot(boot)
        with boot as g:
            p=ui.Pointer(g);p.drain();c.key(g,'esc');g.wait('M7_DHCP_CONFIGURED',timeout=90);t.close_all(g,p)
            browser_window=t.launch(g,p,'browser',17);p.desktop(15009,True);c.shot(g,'browser-choices')
            start=len(g.log());p.desktop(15010,True,settle=False)
            cancel_deadline=time.monotonic()+90
            while time.monotonic()<cancel_deadline:
                raw=ui.memory(g,address,288);cancel_state=struct.unpack_from('<I',raw)[0];cancel_bytes=struct.unpack_from('<Q',raw,16)[0]
                if cancel_bytes>=65536 or cancel_state>=4:break
                time.sleep(.05)
            assert cancel_state==3 and cancel_bytes>=65536,(cancel_state,cancel_bytes)
            cancelled_path=raw[32:288].split(b'\0')[0].decode()
            p.desktop(69,True,settle=False);p.drain()
            cancelled=ui.memory(g,address,288)
            assert struct.unpack_from('<I',cancelled)[0]==6
            assert cancelled_path not in f.entries(g)
            report['checks'].append(dict(name='Real in-progress HTTPS cancellation leaves no published partial installer',bytes_before_cancel=cancel_bytes,path=cancelled_path))
            t.focus(g,p,browser_window);p.desktop(15010,True,settle=False)
            deadline=time.monotonic()+300;observations=[];last=None
            while time.monotonic()<deadline:
                raw=ui.memory(g,address,288);state,revision,error=struct.unpack_from('<III',raw);received=struct.unpack_from('<Q',raw,16)[0]
                if last!=(state,received//(8*1024**2)):
                    observations.append(dict(state=state,bytes=received,tls_error=error));last=(state,received//(8*1024**2))
                if state>=4:break
                time.sleep(.1)
            report['download_observations']=observations
            pointer=struct.unpack_from('<Q',raw,24)[0]
            message=ui.memory(g,pointer,180).split(b'\0')[0].decode(errors='replace') if pointer else ''
            assert state==4,(state,error,received,message,g.log()[start:][-2000:])
            path=raw[32:288].split(b'\0')[0].decode();assert path.endswith('.msi')
            c.shot(g,'firefox-downloaded')
            (out/'serial.log').write_text(g.log(),encoding='utf-8')
        stored=ui.s.s.document(disk,path,128*1024**2)
        assert len(stored)==95924224
        digest=hashlib.sha256(stored).hexdigest()
        assert digest=='6dc28633cbd77cb1d044f339185cd467dda39397e4bcca942bfb0ddb2360c681'
        report['checks'].append(dict(name='Actual native HTTPS transfer from Mozilla and independent stopped-disk hash',path=path,bytes=len(stored),sha256=digest,installer_executed=False))
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:
        (out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
