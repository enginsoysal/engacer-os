"""Real-duration owned VMware stability: visible output AND serial input.

The M13.7 serial-only baseline missed a presentation freeze. This test retains
every sampled frame and requires a large central native image change after an
ordinary app launch, independently of the matching serial event. It never sends
input during the named uninterrupted idle interval.
"""
import argparse, hashlib, json, re, shutil, time, traceback, uuid, zipfile
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageChops
import vmware_stage8 as observer

ROOT=observer.ROOT
v=observer.v


def changed_pixels(left, right):
    with Image.open(left) as a, Image.open(right) as b:
        assert a.size==b.size
        # Exclude the pointer/clock/taskbar and outer desktop. A changed clock
        # alone cannot make a newly opened native window visibly responsive.
        crop=(100,70,a.width-100,a.height-100)
        difference=ImageChops.difference(a.convert('RGB').crop(crop),b.convert('RGB').crop(crop))
        return sum(1 for pixel in difference.getdata() if pixel!=(0,0,0))


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--seconds',type=int,default=3600)
    p.add_argument('--cycles',type=int,default=3)
    p.add_argument('--cycle-seconds',type=int,default=300)
    args=p.parse_args()
    assert 60<=args.seconds<=86400 and 0<=args.cycles<=12 and 10<=args.cycle_seconds<=3600
    assert not (ROOT/'evidence/M13/9/publication-results.json').exists()
    meta=json.loads((ROOT/'dist/m13stage9-build-manifest.json').read_text(encoding='utf-8'))
    starter=json.loads((ROOT/'dist/m13stage9-starter-manifest.json').read_text(encoding='utf-8'))
    archive=ROOT/'dist/EngacerOS-M13STAGE9-VMware.zip'
    assert meta['build_id']==starter['build_id'] and hashlib.sha256(archive.read_bytes()).hexdigest()==starter['sha256']
    stamp=uuid.uuid4().hex
    work=ROOT/'build/m13-native/stage9/stability'/stamp
    out=ROOT/'build/m13/stage9/stability'/stamp
    work.mkdir(parents=True);out.mkdir(parents=True)
    report=dict(passed=False,status='starting',stage='M13.9',build_id=meta['build_id'],iso_sha256=meta['artifacts']['EngacerOS-M13STAGE9.iso']['sha256'],starter_sha256=starter['sha256'],owned_fixture=stamp,frames=[],visible_launches=[],requested_idle_seconds=args.seconds,requested_cycles=args.cycles,cycle_idle_seconds=args.cycle_seconds,scope='Real elapsed uninterrupted idle followed by ordinary-input/idle cycles on a new exact enabled-device starter. Serial liveness alone never passes visible recovery.')

    def save():
        (out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        (out.parent/'current.json').write_text(json.dumps({'owned_fixture':stamp,'report':(out/'results.json').relative_to(ROOT).as_posix()},indent=2)+'\n',encoding='utf-8')

    def frame(g,name):
        v.shot(g,out,name)
        return out/(name+'.png')

    def launch(g,query,app,label):
        before=frame(g,label+'-before')
        v.key(g,0xffeb)
        for char in query:v.key(g,ord(char))
        at=len(g.read());v.enter(g)
        g.wait('M7_WINDOW_OPEN app='+f'0x{app:016x}',offset=at,timeout=90)
        deadline=time.monotonic()+10
        while True:
            after=frame(g,label+'-after')
            pixels=changed_pixels(before,after)
            if pixels>=10000:break
            if time.monotonic()>=deadline:raise AssertionError('Serial app launch did not produce a changed native window: '+label)
            time.sleep(.1)
        report['visible_launches'].append(dict(name=label,app=app,changed_central_pixels=pixels,serial_event=True,visible_frame=True))
        save()

    before=v.old.v.inventory();save()
    try:
        with zipfile.ZipFile(archive) as z:assert z.testzip() is None;z.extractall(work)
        folder=work/'EngacerOS';original=(folder/'EngacerOS.vmx').read_text(encoding='utf-8')
        g=v.Guest(work/'same-vm',folder/'EngacerOS.vmdk','efi')
        g.rfb_port,report['observation_port_policy']=observer.observer_port8()
        cfg=g.vmx.read_text(encoding='utf-8')
        cfg=re.sub(r'(?m)^RemoteDisplay\.vnc\.port\s*=.*$','RemoteDisplay.vnc.port = '+json.dumps(str(g.rfb_port)),cfg)
        observation='\n'.join(line for line in cfg.splitlines() if line.startswith(('serial0.','RemoteDisplay.')))+'\n'
        for file in folder.iterdir():shutil.copyfile(file,g.folder/file.name)
        g.vmx=g.folder/'EngacerOS.vmx';g.vmx.write_bytes((original+observation).encode('utf-8'))
        assert 'bios.bootOrder' not in original and all(x in original for x in ('ethernet0.present = "TRUE"','sound.present = "TRUE"','usb_xhci.present = "TRUE"'))
        with g:
            v.enter(g);v.enter(g);v.enter(g);v.tab(g,3);v.enter(g);v.enter(g);v.enter(g);v.enter(g)
            g.wait('M6_INSTALL_PASS',timeout=240)
            at=len(g.read());v.enter(g);g.wait('M7_DESKTOP_READY build='+meta['build_id'],offset=at,timeout=180)
            g.rfb.close();g.rfb=None;v.key(g,0xff1b)
            frame(g,'idle-start')
            began=time.monotonic();report.update(status='uninterrupted-idle',idle_started_at=datetime.now(timezone.utc).isoformat());save();next_sample=began+60
            while time.monotonic()-began<args.seconds:
                log=g.read()
                if any(s in log for s in ('KERNEL_PANIC','KERNEL_REJECT:')):raise RuntimeError('Native failure during real idle')
                if time.monotonic()>=next_sample:
                    elapsed=time.monotonic()-began;name='idle-'+str(int(elapsed));png=frame(g,name)
                    report['frames'].append(dict(elapsed_seconds=elapsed,png=png.name,sha256=hashlib.sha256(png.read_bytes()).hexdigest()))
                    report['idle_elapsed_seconds']=time.monotonic()-began;save();next_sample=time.monotonic()+60
                time.sleep(1)
            report.update(status='visible-recovery',idle_elapsed_seconds=time.monotonic()-began,idle_finished_at=datetime.now(timezone.utc).isoformat());save()
            launch(g,'calculator',4,'after-uninterrupted-idle')
            # Close only the just-opened foreground test app, retaining Files.
            display=g.connect_display();display.key(0xffe9,True);display.press(0xffc1);display.key(0xffe9,False)
            for cycle in range(args.cycles):
                began_cycle=time.monotonic();report.update(status='active-idle-cycle',active_cycle=cycle);save()
                while time.monotonic()-began_cycle<args.cycle_seconds:g.read();time.sleep(1)
                launch(g,'calculator',4,'cycle-'+str(cycle))
                # Use a normal shortcut chord through the authenticated guest.
                display=g.connect_display();display.key(0xffe9,True);display.press(0xffc1);display.key(0xffe9,False)
            report.update(passed=True,status='completed',visible_responsiveness=True)
    except Exception:
        report.update(status='failed',error=v.old.v.redact(traceback.format_exc()))
        raise
    finally:
        if 'g' in locals():
            (out/'native.log').write_text(g.read(),encoding='utf-8')
            report['fifo_quarantines']=g.read().count('M9_SVGA_QUARANTINED')
            report['framebuffer_recoveries']=g.read().count('M139_SVGA_FRAMEBUFFER_RECOVERY')
        after=v.old.v.inventory();report['existing_vm_inventory_unchanged']=before==after
        report['passed']=report['passed'] and before==after
        report['completed_at']=datetime.now(timezone.utc).isoformat();save()
        print(json.dumps({k:report.get(k) for k in ('status','passed','owned_fixture','idle_elapsed_seconds','visible_responsiveness','fifo_quarantines','framebuffer_recoveries','error')},indent=2),flush=True)


if __name__=='__main__':main()
