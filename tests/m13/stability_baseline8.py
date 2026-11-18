"""Observe the owner's M13.8 freeze report on untouched exact release media.

New owned fixture/output paths only. Ordinary guest dragging, visible frames
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
    stamp=uuid.uuid4().hex;work=ROOT/'build/m13-native/baseline8'/stamp;out=ROOT/'build/m13/baseline8'/stamp
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
                        raise AssertionError('Ordinary drag did not produce a changed visible window')
                report['frames'].append(dict(png=target.name,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),changed_central_pixels=pixels,observed_seconds=time.monotonic()-began))
                report['completed_positions']=number+1;save();previous=target;g.read()
                if number%16==15:print('M13.8 baseline visible positions '+str(number+1),flush=True)
                time.sleep(.1)
            display.socket.sendall(struct.pack('!BBHH',5,0,x,y));g.read();report['passed']=True
    except Exception:
        report['error']=v.old.v.redact(traceback.format_exc());raise
    finally:
        if 'g' in locals():
            (out/'native.log').write_text(g.output,encoding='utf-8');report['fifo_quarantines']=g.output.count('M9_SVGA_QUARANTINED')
        after=v.old.v.inventory();deadline=time.monotonic()+20
        while 'g' in locals() and str(g.vmx) in after and time.monotonic()<deadline:time.sleep(.2);after=v.old.v.inventory()
        report['existing_vm_inventory_unchanged']=before==after;report['passed']=report['passed'] and before==after;save()
        print(json.dumps({k:report.get(k) for k in ('passed','diagnostic_only','owned_fixture','completed_positions','fifo_quarantines','error')},indent=2),flush=True)


if __name__=='__main__':main()
