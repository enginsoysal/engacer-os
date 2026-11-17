"""Exact archived M13 starter: headless VMware, guest input and independent boots."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import traceback
import uuid
import zipfile

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('shared_devices_vmware',ROOT/'tests/m10/vmware.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
v=m.v

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',type=int,required=True);stage=parser.parse_args().stage
    assert 1<=stage<=12
    image=f'EngacerOS-M13STAGE{stage}';archive=ROOT/'dist'/(image+'-VMware.zip')
    meta=json.loads((ROOT/f'dist/m13stage{stage}-build-manifest.json').read_text())
    work=ROOT/f'build/m13-native/stage{stage}/vmware'/uuid.uuid4().hex;work.mkdir(parents=True)
    out=ROOT/f'build/m13/stage{stage}/vmware-results';out.mkdir(parents=True,exist_ok=True)
    before=v.old.v.inventory()
    report=dict(passed=False,stage=f'M13.{stage}',build_id=meta['build_id'],iso_sha256=meta['artifacts'][image+'.iso']['sha256'],starter_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),checks=[])
    try:
        with zipfile.ZipFile(archive) as bundle:
            assert bundle.testzip() is None;bundle.extractall(work)
        folder=work/'EngacerOS';original=(folder/'EngacerOS.vmx').read_text()
        g=v.Guest(work/'same-vm',folder/'EngacerOS.vmdk','efi')
        observation='\n'.join(line for line in g.vmx.read_text().splitlines() if line.startswith(('serial0.','RemoteDisplay.')))+'\n'
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
            sx=(width-700)//2+24;sy=(height-60-550)//2+56
            # Appearance uses category tabs and an explicit Apply footer.
            m.guest_click10(g,sx+164,sy+304);m.guest_click10(g,sx+82,sy+396)
            g.wait('M11_APPEARANCE_SAVED');v.shot(g,out,'saved-appearance')
            (out/'install.log').write_bytes(g.read().encode())
        report['checks'].append('Exact blank-disk VMware ZIP installs through eight setup steps and restarts with ISO retained into the actual installed desktop, with all shipped devices enabled and DHCP')
        report['checks'].append('Guest mouse and keyboard exercise maximize/restore, Start search and shared native Settings controls without host desktop input')
        config=g.vmx.read_text();g.vmx.write_bytes(re.sub(r'(?im)^ide1:0.startConnected\s*=.*$','ide1:0.startConnected = "FALSE"',config).encode());g.installed=True
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
        report['existing_vm_inventory_unchanged']=before==v.old.v.inventory()
        report['passed']=report['passed'] and report['existing_vm_inventory_unchanged']
        (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
