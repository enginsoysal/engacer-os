"""Owned real-duration VMware M13.7 idle baseline for the owner's freeze report.

No accepted media/evidence is modified. Frame reads and COM1 draining inject no
guest input during the idle interval. This diagnostic is not a freeze fix, a
native performance measurement or qualification of a newer milestone.
"""
import argparse,hashlib,json,re,shutil,time,traceback,uuid,zipfile
from datetime import datetime,timezone
from pathlib import Path
import vmware_stage8 as observer
ROOT=observer.ROOT;v=observer.v


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--seconds',type=int,default=3600);args=parser.parse_args();assert 60<=args.seconds<=86400
    meta=json.loads((ROOT/'dist/m13stage7-build-manifest.json').read_text(encoding='utf-8'));accepted=json.loads((ROOT/'evidence/M13/7/acceptance-results.json').read_text(encoding='utf-8'));archive=ROOT/'dist/EngacerOS-M13STAGE7-VMware.zip'
    assert meta['build_id']==accepted['build_id'] and hashlib.sha256(archive.read_bytes()).hexdigest()==accepted['vmware_zip_sha256']
    stamp=uuid.uuid4().hex;work=ROOT/'build/m13-native/idle-baseline7'/stamp;work.mkdir(parents=True);out=ROOT/'build/m13/idle-baseline7'/stamp;out.mkdir(parents=True)
    report=dict(status='starting',passed=False,diagnostic_only=True,observed_version='M13.7',build_id=meta['build_id'],iso_sha256=accepted['iso_sha256'],starter_sha256=accepted['vmware_zip_sha256'],requested_idle_seconds=args.seconds,owned_fixture=stamp,frames=[],scope='Real elapsed idle on a new exact-starter VMware fixture, then ordinary guest keyboard launch. No accelerated uptime, host desktop input or claim that a freeze is fixed.')

    def save():
        (out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        pointer=ROOT/'build/m13/idle-baseline7/current.json';pointer.write_text(json.dumps(dict(owned_fixture=stamp,report=str((out/'results.json').relative_to(ROOT)).replace('\\','/')),indent=2)+'\n',encoding='utf-8')

    before=v.old.v.inventory();save()
    try:
        with zipfile.ZipFile(archive) as bundle:assert bundle.testzip() is None;bundle.extractall(work)
        folder=work/'EngacerOS';original=(folder/'EngacerOS.vmx').read_text(encoding='utf-8');g=v.Guest(work/'same-vm',folder/'EngacerOS.vmdk','efi')
        g.rfb_port,report['observation_port_policy']=observer.observer_port8();cfg=g.vmx.read_text(encoding='utf-8');cfg=re.sub(r'(?m)^RemoteDisplay\.vnc\.port\s*=.*$','RemoteDisplay.vnc.port = '+json.dumps(str(g.rfb_port)),cfg)
        observation='\n'.join(line for line in cfg.splitlines() if line.startswith(('serial0.','RemoteDisplay.')))+'\n'
        for file in folder.iterdir():shutil.copyfile(file,g.folder/file.name)
        g.vmx=g.folder/'EngacerOS.vmx';g.vmx.write_bytes((original+observation).encode('utf-8'))
        assert 'bios.bootOrder' not in original and all(x in original for x in ('ethernet0.present = "TRUE"','sound.present = "TRUE"','usb_xhci.present = "TRUE"'))
        with g:
            v.enter(g);v.enter(g);v.enter(g);v.tab(g,3);v.enter(g);v.enter(g);v.enter(g);v.enter(g);g.wait('M6_INSTALL_PASS',timeout=240)
            at=len(g.read());v.enter(g);g.wait('M7_DESKTOP_READY build='+meta['build_id'],offset=at,timeout=180);g.rfb.close();g.rfb=None;v.key(g,0xff1b);v.shot(g,out,'idle-start')
            began=time.monotonic();report.update(status='idle',idle_started_at=datetime.now(timezone.utc).isoformat());save();next_sample=began+60
            while time.monotonic()-began<args.seconds:
                text=g.read()
                if any(word in text for word in ('KERNEL_PANIC','KERNEL_REJECT:')):raise RuntimeError('Native failure during the real idle interval')
                if time.monotonic()>=next_sample:
                    elapsed=time.monotonic()-began;name='idle-'+str(int(elapsed));v.shot(g,out,name);report['frames'].append(dict(elapsed_seconds=elapsed,png=name+'.png',sha256=hashlib.sha256((out/(name+'.png')).read_bytes()).hexdigest()));report['idle_elapsed_seconds']=time.monotonic()-began;save();next_sample=time.monotonic()+60
                time.sleep(1)
            report.update(status='checking-input',idle_elapsed_seconds=time.monotonic()-began,idle_finished_at=datetime.now(timezone.utc).isoformat());save()
            v.key(g,0xffeb)
            for char in 'calculator':v.key(g,ord(char))
            at=len(g.read());v.enter(g);g.wait('M7_WINDOW_OPEN app=0x0000000000000004',offset=at,timeout=90);v.shot(g,out,'responsive-after-idle');(out/'native.log').write_text(g.read(),encoding='utf-8')
            report.update(passed=True,status='completed',ordinary_input_after_idle=True,interpretation='No freeze observed in this named real-duration idle baseline; this does not disprove the owner report or qualify active/idle transitions or a correction.')
    except Exception:report.update(status='failed',error=v.old.v.redact(traceback.format_exc()));raise
    finally:
        after=v.old.v.inventory();report['before_inventory_sha256']=sorted(hashlib.sha256(p.encode()).hexdigest() for p in before);report['after_inventory_sha256']=sorted(hashlib.sha256(p.encode()).hexdigest() for p in after);report['existing_vm_inventory_unchanged']=before==after;report['completed_at']=datetime.now(timezone.utc).isoformat();save();print(json.dumps({k:report.get(k) for k in ('status','passed','owned_fixture','idle_elapsed_seconds','ordinary_input_after_idle','error')},indent=2),flush=True)


if __name__=='__main__':main()
