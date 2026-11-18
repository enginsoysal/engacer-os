"""Observe the owner's M13.8 freeze report on untouched exact release media.

Warm resets after an independently observed freeze; a full power cycle is separate. New owned fixture/output paths only. Ordinary guest dragging, visible frames
and serial output are independent observations; this is not a stability pass.
"""
import argparse,hashlib,json,re,shutil,struct,time,traceback,uuid,zipfile
from pathlib import Path
import vmware_stage8 as observer
from stability9 import changed_pixels
ROOT=observer.ROOT;v=observer.v


def main():
    p=argparse.ArgumentParser();p.add_argument('--steps',type=int,default=128);args=p.parse_args();assert 16<=args.steps<=512
    accepted=json.loads((ROOT/'evidence/M13/8/acceptance-results.json').read_text(encoding='utf-8'))
    meta=json.loads((ROOT/'dist/m13stage8-build-manifest.json').read_text(encoding='utf-8'))
    archive=ROOT/'dist/EngacerOS-M13STAGE8-VMware.zip'
    assert meta['build_id']==accepted['build_id'] and hashlib.sha256(archive.read_bytes()).hexdigest()==accepted['vmware_zip_sha256']
    stamp=uuid.uuid4().hex;work=ROOT/'build/m13-native/baseline8-reset'/stamp;out=ROOT/'build/m13/baseline8-reset'/stamp
    work.mkdir(parents=True);out.mkdir(parents=True)
    report=dict(passed=False,diagnostic_only=True,observed_version='M13.8',build_id=meta['build_id'],iso_sha256=accepted['iso_sha256'],starter_sha256=accepted['vmware_zip_sha256'],owned_fixture=stamp,requested_positions=args.steps,completed_positions=0,frames=[],scope='Untouched exact M13.8 starter, all shipped devices enabled. Ordinary held-pointer movement with independent large central-frame changes. This does not qualify long-duration stability or speed.')
    def save():(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    before=v.old.v.inventory();save()
    try:
        with zipfile.ZipFile(archive) as z:assert z.testzip() is None;z.extractall(work)
        folder=work/'EngacerOS';original=(folder/'EngacerOS.vmx').read_text(encoding='utf-8');g=v.Guest(work/'same-vm',folder/'EngacerOS.vmdk','efi')
        g.rfb_port,report['observation_port_policy']=observer.observer_port8()
        cfg=re.sub(r'(?m)^RemoteDisplay\.vnc\.port\s*=.*$','RemoteDisplay.vnc.port = '+json.dumps(str(g.rfb_port)),g.vmx.read_text(encoding='utf-8'))
        observation='\n'.join(x for x in cfg.splitlines() if x.startswith(('serial0.','RemoteDisplay.')))+'\n'
        for file in folder.iterdir():shutil.copyfile(file,g.folder/file.name)
        g.vmx=g.folder/'EngacerOS.vmx';g.vmx.write_bytes((original+observation).encode('utf-8'))
        assert 'bios.bootOrder' not in original and all(x in original for x in ('ethernet0.present = "TRUE"','sound.present = "TRUE"','usb_xhci.present = "TRUE"'))
        with g:
            v.enter(g);v.enter(g);v.enter(g);v.tab(g,3);v.enter(g);v.enter(g);v.enter(g);v.enter(g);g.wait('M6_INSTALL_PASS',timeout=240)
            at=len(g.read());v.enter(g);g.wait('M7_DESKTOP_READY build='+meta['build_id'],offset=at,timeout=180);g.rfb.close();g.rfb=None;v.key(g,0xff1b)
            display=g.connect_display();width,height=display.width,display.height
            fw=1080 if width>1200 else width-112;fh=720 if height>900 else height-100
            x=(width-fw)//2+230;y=(height-60-fh)//2+18
            v.shot(g,out,'before-movement');previous=out/'before-movement.png'
            display.socket.sendall(struct.pack('!BBHH',5,0,x,y));time.sleep(.15);display.socket.sendall(struct.pack('!BBHH',5,1,x,y));time.sleep(.15)
            for number in range(args.steps):
                dx,dy=(24,20) if number%2==0 else (0,0)
                began=time.monotonic();display.socket.sendall(struct.pack('!BBHH',5,1,x+dx,y+dy))
                name='position-'+str(number);target=out/(name+'.png');deadline=time.monotonic()+2
                while True:
                    v.shot(g,out,name);pixels=changed_pixels(previous,target)
                    if pixels>=1000:break
                    if time.monotonic()>deadline:
                        report['failed_position']=number;report['changed_central_pixels']=pixels
                        report['natural_visible_freeze']=True;save();break
                if report.get('natural_visible_freeze'):break
                report['frames'].append(dict(png=target.name,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),changed_central_pixels=pixels,observed_seconds=time.monotonic()-began))
                report['completed_positions']=number+1;save();previous=target;g.read()
                if number%16==15:print('M13.8 baseline visible positions '+str(number+1),flush=True)
                time.sleep(.1)
            display.socket.sendall(struct.pack('!BBHH',5,0,x,y));g.read()
            report['warm_resets']=[]
            if report.get('natural_visible_freeze'):
                (out/'before-reset-native.log').write_text(g.output,encoding='utf-8')
                for number in range(3):
                    row=dict(number=number+1,after_observed_freeze=True,full_power_cycle=False,visible_response=False)
                    try:
                        assert g.owned and str(g.vmx) in v.old.v.inventory()
                        assert g.vmx.resolve().is_relative_to(work.resolve())
                        at=len(g.read());g.rfb.close();g.rfb=None
                        reset=v.old.v.run('reset',g.vmx,'hard');assert reset.returncode==0
                        g.wait('M7_DESKTOP_READY build='+meta['build_id'],offset=at,timeout=90)
                        assert 'ENGINE_OS_KERNEL_ENTRY' in g.read()[at:]
                        row['fresh_boot']=True;v.key(g,0xff1b)
                        v.shot(g,out,'reset-'+str(number)+'-before');before_image=out/('reset-'+str(number)+'-before.png')
                        at=len(g.read());v.key(g,0xffeb)
                        for char in 'calculator':v.key(g,ord(char))
                        v.enter(g);g.wait('M7_WINDOW_OPEN app=0x0000000000000004',offset=at,timeout=20)
                        v.shot(g,out,'reset-'+str(number)+'-after');pixels=changed_pixels(before_image,out/('reset-'+str(number)+'-after.png'))
                        row.update(changed_central_pixels=pixels,visible_response=pixels>=10000)
                    except Exception:
                        row['error']=v.old.v.redact(traceback.format_exc())
                    report['warm_resets'].append(row);save()
            else:report['reset_not_exercised_reason']='No natural freeze reproduced; do not substitute a simulated freeze'
            report['passed']=True
        # Full power-off/start is recorded separately from powered-on resets.
        if report.get('natural_visible_freeze'):
            (out/'post-resets-native.log').write_text(g.output,encoding='utf-8')
            g.output='';g.pipe=None;g.rfb=None;g.installed=True
            try:
                with g:
                    g.wait('M7_DESKTOP_READY build='+meta['build_id'],timeout=90)
                    v.key(g,0xff1b);v.shot(g,out,'cold-power-cycle')
                    report['cold_power_cycle']=dict(fresh_boot=True,scope='Desktop startup frame only; not a stability pass')
            except Exception:report['cold_power_cycle']=dict(error=v.old.v.redact(traceback.format_exc()))
    except Exception:
        report['error']=v.old.v.redact(traceback.format_exc());raise
    finally:
        if 'g' in locals():
            (out/'native.log').write_text(g.output,encoding='utf-8');report['fifo_quarantines']=g.output.count('M9_SVGA_QUARANTINED')
            report['quarantine_count_scope']='Final COM1 session; pre-reset and post-reset logs are separate and may overlap'
            report['fifo_quarantines_by_phase']={name:(out/name).read_text(encoding='utf-8').count('M9_SVGA_QUARANTINED') for name in ('before-reset-native.log','post-resets-native.log','native.log') if (out/name).exists()}
        after=v.old.v.inventory();deadline=time.monotonic()+20
        while 'g' in locals() and str(g.vmx) in after and time.monotonic()<deadline:time.sleep(.2);after=v.old.v.inventory()
        report['existing_vm_inventory_unchanged']=before==after;report['passed']=report['passed'] and before==after;save()
        print(json.dumps({k:report.get(k) for k in ('passed','diagnostic_only','owned_fixture','completed_positions','fifo_quarantines','error')},indent=2),flush=True)


if __name__=='__main__':main()
