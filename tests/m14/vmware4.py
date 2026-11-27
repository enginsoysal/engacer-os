"""Exact archived M14 starter: headless VMware, guest input and independent boots."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import socket
import struct
import subprocess
import traceback
import time
import uuid
import zipfile

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('shared_devices_vmware',ROOT/'tests/m10/vmware.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
v=m.v

def observer_port8():
    # Keep observation listeners outside the host's actual outbound TCP range.
    text=subprocess.check_output(['netsh','int','ipv4','show','dynamicport','tcp']).decode('utf-8',errors='replace')
    values=[int(v) for v in re.findall(r':\s*(\d+)',text)];assert len(values)==2 and 1<=values[0]<65536 and 1<=values[1]<=65536-values[0]
    first,count=values
    for _ in range(128):
        port=40000+uuid.uuid4().int%8000
        if first<=port<first+count:continue
        try:
            with socket.socket() as probe:
                if hasattr(socket,'SO_EXCLUSIVEADDRUSE'):probe.setsockopt(socket.SOL_SOCKET,socket.SO_EXCLUSIVEADDRUSE,1)
                probe.bind(('127.0.0.1',port))
            return port,dict(outbound_start=first,outbound_count=count,listener_outside_outbound_range=True,loopback_only=True)
        except OSError:continue
    raise RuntimeError('No free owned loopback observation port outside the outbound range')

def original_window_tasks(g,out):
    # Real guest RFB only. No host application execution or desktop input.
    display=g.connect_display();display.key(0xffe9,True);display.press(0xffc1);display.key(0xffe9,False);time.sleep(.3)
    v.key(g,0xffeb)
    for char in 'windows apps':v.key(g,ord(char))
    at=len(g.read());v.enter(g);g.wait('M7_WINDOW_OPEN app=0x0000000000000013',offset=at)
    width=display.width;left=(width-min(width-80,940))//2;x=left+24;y=35+62
    at=len(g.read());m.guest_click10(g,x+80,y+226+20);m.guest_click10(g,x+166+95,y+340+20)
    g.wait('M8_CPL3_CREATED',offset=at);g.wait('M8_JOB_DONE code=0x0000000000000000',offset=at,timeout=240);assert 'M8_JOB_FAILED' not in g.read()[at:]
    v.shot(g,out,'original-msi-installed')
    at=len(g.read());m.guest_click10(g,x+418+105,y+194+20);g.wait('M8_CPL3_CREATED command=0x0000000000000003',offset=at);time.sleep(1)
    assert 'M8_JOB_FAILED' not in g.read()[at:];v.shot(g,out,'original-file-manager')
    # Original first-run placement is the documented 80,70,760,500 rectangle.
    # Move the real caption through the virtual mouse, then close that moved frame.
    for buttons,px,py in ((0,260,90),(1,260,90),(1,300,120),(0,300,120)):
        display.socket.sendall(struct.pack('!BBHH',5,buttons,px,py));g.read();time.sleep(.15)
    v.shot(g,out,'original-file-manager-moved')
    m.guest_click10(g,854,120);g.wait('M8_JOB_DONE code=0x0000000000000000',offset=at,timeout=90);assert 'M8_JOB_FAILED' not in g.read()[at:]
    v.shot(g,out,'original-file-manager-closed')
    return {'passed':True,'scope':'Original supported MSI installation and original file-manager window launch/move/normal close in exact enabled-device VMware starter; not complete GUI app tasks','expected_original_sha256':'a12710799d5cb9b3076b86dd0f92d4a503b7062bc3efac62b7f4cb8a74e05931','original_identity_basis':'Pinned bundled MSI verification; full installed payload SHA-256 independently checked in native QEMU profiles','input':'Authenticated loopback RFB of this new owned headless guest'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',type=int,required=True);parser.add_argument('--inspect-input',action='store_true');args=parser.parse_args();stage=args.stage
    assert stage in (4, 10)
    image=f'EngacerOS-M14STAGE{stage}';archive=ROOT/'dist'/(image+'-VMware.zip')
    meta=json.loads((ROOT/f'dist/m14stage{stage}-build-manifest.json').read_text(encoding='utf-8'))
    work=ROOT/f'build/m14-native/stage{stage}/vmware'/uuid.uuid4().hex;work.mkdir(parents=True)
    out=ROOT/f'build/m14-native/stage{stage}/vmware-results';out.mkdir(parents=True,exist_ok=True)
    before=v.old.v.inventory()
    report=dict(passed=False,stage=f'M14.{stage}',build_id=meta['build_id'],iso_sha256=meta['artifacts'][image+'.iso']['sha256'],starter_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),checks=[])
    try:
        with zipfile.ZipFile(archive) as bundle:
            assert bundle.testzip() is None;bundle.extractall(work)
        folder=work/'EngacerOS';original=(folder/'EngacerOS.vmx').read_text(encoding='utf-8')
        g=v.Guest(work/'same-vm',folder/'EngacerOS.vmdk','efi')
        g.rfb_port,report['observation_port_policy']=observer_port8()
        cfg=g.vmx.read_text(encoding='utf-8');cfg=re.sub(r'(?m)^RemoteDisplay\.vnc\.port\s*=.*$', 'RemoteDisplay.vnc.port = '+json.dumps(str(g.rfb_port)),cfg);g.vmx.write_text(cfg,encoding='utf-8')
        observation='\n'.join(line for line in g.vmx.read_text(encoding='utf-8').splitlines() if line.startswith(('serial0.','RemoteDisplay.')))+'\n'
        for file in folder.iterdir():shutil.copyfile(file,g.folder/file.name)
        g.vmx=g.folder/'EngacerOS.vmx';g.vmx.write_bytes((original+observation).encode())
        assert all(s in original for s in ('ethernet0.present = "TRUE"','pciBridge4.virtualDev = "pcieRootPort"','sound.present = "TRUE"','usb_xhci.present = "TRUE"'))
        assert 'bios.bootOrder' not in original
        with g:
            v.shot(g,out,'welcome');v.enter(g);v.shot(g,out,'keyboard');v.enter(g);v.enter(g);v.tab(g,3);v.enter(g)
            v.shot(g,out,'apps');v.enter(g);v.shot(g,out,'style');v.enter(g);v.shot(g,out,'review');v.enter(g)
            g.wait('M6_INSTALL_PASS',timeout=240);v.shot(g,out,'finish')
            start=len(g.read());v.enter(g);g.wait('M75_USER_RESTART',offset=start);g.wait('M7_DESKTOP_READY',offset=start,timeout=180)
            assert 'M6_INSTALLED_VOLUME' in g.read()[start:] and 'M6_WIZARD_READY' not in g.read()[start:]
            g.wait('M7_DHCP_CONFIGURED',offset=start,timeout=90)
            g.rfb.close();g.rfb=None
            v.shot(g,out,'first-start-guide');v.key(g,0xff1b);v.shot(g,out,'installed-desktop')
            display=g.connect_display();width,height=display.width,display.height
            fw=1080 if width>1200 else width-112;fh=720 if height>900 else height-100
            left=(width-fw)//2;top=(height-60-fh)//2
            m.guest_click10(g,left+fw-76,top+18);v.shot(g,out,'maximized-files')
            m.guest_click10(g,width-76,18);v.shot(g,out,'restored-files')
            v.key(g,0xffeb)
            v.shot(g,out,'icons-start')
            for char in 'settings':v.key(g,ord(char))
            at=len(g.read());v.enter(g);g.wait('M7_WINDOW_OPEN app=0x0000000000000003',offset=at)
            v.shot(g,out,'shared-components')
            sx=(width-800)//2+24;sy=(height-60-650)//2+56
            # Appearance uses category tabs and an explicit Apply footer.
            m.guest_click10(g,sx+234,sy+270);m.guest_click10(g,sx+82,sy+496)
            g.wait('M11_APPEARANCE_SAVED');v.shot(g,out,'saved-appearance')
            # Ordinary visible RFB input: open Screensaver and return to the same Settings frame.
            m.guest_click10(g,sx+660,sy+12);v.shot(g,out,'screensaver-settings')
            from PIL import Image,ImageChops
            with Image.open(out/'screensaver-settings.png') as original_frame:original_frame=original_frame.convert('RGB').copy()
            observations=[]
            m.guest_click10(g,sx+76,sy+144+250)
            deadline=time.monotonic()+10
            while True:
                v.shot(g,out,'screensaver-preview')
                with Image.open(out/'screensaver-preview.png') as frame:ratio=frame.convert('L').histogram()[0]/(frame.width*frame.height)
                observations.append(dict(phase='preview',black_fraction=ratio))
                if ratio>.9:break
                if time.monotonic()>deadline:
                    if args.inspect_input:
                        # Owned fresh test guest only: a stopped physical-memory read,
                        # never guest writes or a user VM, to explain this new Preview failure.
                        result=v.old.v.run('suspend',g.vmx,'hard');assert result.returncode==0,'Owned diagnostic suspend failed';g.owned=False
                        memories=list(g.folder.glob('*.vmem'));assert len(memories)==1
                        mapping=(ROOT/f'dist/EngacerOS-M14STAGE{stage}-installed-kernel.map').read_text(encoding='utf-8')
                        values={}
                        with memories[0].open('rb') as ram:
                            for name in ['saver_saved21','saver_phase21','activity21','legacy_held21','usb_held21','pointer_held21','legacy_pressed21','pause21','prefix21','control_modifier','shift','usb_modifiers11']:
                                found=re.findall(r'^\s*([0-9a-f]+)\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+'+re.escape(name)+r'$',mapping,re.M);assert len(found)==1,name
                                address,size=[int(x,16) for x in found[0]];ram.seek(address);raw=ram.read(size);assert len(raw)==size;values[name]=raw.hex() if size>8 else int.from_bytes(raw,'little')
                        assert values['saver_saved21'].startswith('4553323101000000'),'Physical memory layout was not independently anchored'
                        (out/'preview-input.json').write_text(json.dumps(dict(build_id=meta['build_id'],scope='Read-only stopped owned test RAM for a functional Preview failure; not stability qualification',fields=values),indent=2)+'\n',encoding='utf-8')
                    raise AssertionError('Preview did not visibly replace the desktop in fresh owned RFB observations')
                time.sleep(.15)
            m.guest_click10(g,sx+76,sy+144+250)
            deadline=time.monotonic()+10
            while True:
                v.shot(g,out,'screensaver-wake')
                with Image.open(out/'screensaver-wake.png') as awake:
                    point=awake.getpixel((sx+400,sy+200))[:3];expected=original_frame.getpixel((sx+400,sy+200))[:3]
                    box=(sx,sy,sx+740,sy+550);diff=ImageChops.difference(original_frame.crop(box),awake.convert('RGB').crop(box)).convert('L');same=diff.histogram()[0]/(diff.width*diff.height)
                observations.append(dict(phase='wake',body_restored=point==expected and point!=(0,0,0),unchanged_settings_fraction=same))
                if point==expected and point!=(0,0,0) and same>.95:break
                if time.monotonic()>deadline:raise AssertionError('Wake did not visibly restore and retain the Settings frame')
                time.sleep(.15)
            report['visible_preview_wake_observations']=observations
            report['checks'].append('Actual RFB mouse opens Screensaver settings, shows native preview and returns without operating the underlying Preview control')
            report['original_window']=original_window_tasks(g,out)
            (out/'install.log').write_bytes(g.read().encode())
        report['checks'].append('Exact blank-disk VMware ZIP installs through eight setup steps and restarts with ISO retained into the actual installed desktop, with all shipped devices enabled and DHCP')
        report['checks'].append('Guest mouse and keyboard exercise maximize/restore, Start search and shared native Settings controls without host desktop input')
        config=g.vmx.read_text(encoding='utf-8');g.vmx.write_bytes(re.sub(r'(?im)^ide1:0.startConnected\s*=.*$','ide1:0.startConnected = "FALSE"',config).encode());g.installed=True
        for number in (1,2):
            g.output='';g.pipe=None;g.rfb=None
            with g:
                g.wait('M7_DESKTOP_READY build='+meta['build_id']);assert 'M6_INSTALLED_VOLUME' in g.read()
                v.shot(g,out,f'disk-only-{number}');(out/f'disk-only-{number}.log').write_bytes(g.read().encode())
        report['checks'].append('Two independent boots retain the same disk, VMware configuration and firmware variables with only the ISO disconnected; no forced boot order')
        report['passed']=True
    except Exception:
        report['error']=v.old.v.redact(traceback.format_exc());raise
    finally:
        after=v.old.v.inventory();observations=[];deadline=time.monotonic()+20;owned_path=str(g.vmx) if 'g' in locals() else None
        while True:
            observations.append(dict(count=len(after),owned_test_still_listed=bool(owned_path and owned_path in after),matches_before=before==after))
            if not owned_path or owned_path not in after or time.monotonic()>=deadline:break
            time.sleep(.2);after=v.old.v.inventory()
        report['inventory_cleanup_observations']=observations
        report['before_inventory_sha256']=sorted(hashlib.sha256(p.encode('utf-8')).hexdigest() for p in before)
        report['after_inventory_sha256']=sorted(hashlib.sha256(p.encode('utf-8')).hexdigest() for p in after)
        report['existing_vm_inventory_unchanged']=before==after
        report['passed']=report['passed'] and report['existing_vm_inventory_unchanged']
        (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
    assert report['passed'],'The exact starter or existing VM inventory was not qualified'

if __name__=='__main__':main()
