"""Package a fresh, isolated M13 stage VM; never opens an existing user VM."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import uuid
import zipfile

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/build'))
from m8 import privacy_input
spec=importlib.util.spec_from_file_location('starter11',ROOT/'tools/release/vmware_starter11.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',type=int,required=True,choices=range(1,13));args=parser.parse_args()
    assert not (ROOT/f'evidence/M13/{args.stage}/publication-results.json').exists(),'Published media are immutable'
    image=f'EngacerOS-M13STAGE{args.stage}'
    meta=json.loads((ROOT/f'dist/m13stage{args.stage}-build-manifest.json').read_text())
    assert meta['qualification_scope']==f'M13-STAGE{args.stage}-VM-v1'
    iso=ROOT/'dist'/(image+'.iso');assert hashlib.sha256(iso.read_bytes()).hexdigest()==meta['artifacts'][iso.name]['sha256']
    folder=ROOT/f'build/m13-native/starter/stage{args.stage}'/uuid.uuid4().hex;folder.mkdir(parents=True)
    tool=Path('C:/Program Files/VMware/VMware Workstation/vmware-vdiskmanager.exe')
    subprocess.run([str(tool),'-c','-s','20GB','-a','ide','-t','0',str(folder/'EngacerOS.vmdk')],capture_output=True,check=True,timeout=60,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    (folder/'EngacerOS.vmx').write_bytes(base.configuration(image).encode())
    shutil.copyfile(iso,folder/iso.name)
    for source,dest in [('LICENSE','LICENSE'),('third_party/inter/OFL.txt','Inter-OFL.txt'),('third_party/7zip/7z2606-src.tar.xz','7z2606-src.tar.xz'),('third_party/libmspack/COPYING.LIB','libmspack-LGPL-2.1.txt')]:shutil.copyfile(ROOT/source,folder/dest)
    with zipfile.ZipFile(ROOT/'dist/EngacerOS-M11FINAL-VMware.zip') as old:
        notices=old.read('EngacerOS/THIRD-PARTY-NOTICES.txt').decode().replace('Engacer OS M11 third-party notices','Engacer OS M13 third-party notices',1)
    (folder/'THIRD-PARTY-NOTICES.txt').write_bytes(notices.encode())
    text=(f'ENGACER OS M13.{args.stage}\n\nExtract the complete ZIP into an ordinary local folder. Open EngacerOS.vmx.\nChoose I Copied It if asked. Start and follow the graphical installer.\nSelect the disk row, review erasure and install, then choose Restart to Engacer OS.\nThe matching ISO may remain connected. Keep the installed disk attached.\n\nA new blank growable 20-GiB SATA disk is included; it is not preinstalled.\n128 MiB RAM, two CPUs, UEFI, Secure Boot off. All shipped devices remain enabled.\nThe matching release guide states the exact tested stage scope and limitations.\nhttps://engaceros.brixcanvas.com/blog/documentation\nhttps://github.com/enginsoysal/engacer-os\n')
    (folder/'START-HERE.txt').write_bytes(text.encode())
    archive=ROOT/'dist'/(image+'-VMware.zip')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as out:
        for file in sorted(folder.iterdir()):
            data=privacy_input(file.read_bytes());assert b'C:\\Users\\' not in data and b'C:/Users/' not in data
            out.write(file,'EngacerOS/'+file.name)
    with zipfile.ZipFile(archive) as check:
        assert check.testzip() is None
        assert check.read('EngacerOS/EngacerOS.vmx').decode()==base.configuration(image)
        assert hashlib.sha256(check.read('EngacerOS/'+iso.name)).hexdigest()==meta['artifacts'][iso.name]['sha256']
    report=dict(passed=True,archive=archive.name,sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),size=archive.stat().st_size,image=image,build_id=meta['build_id'],members=[p.name for p in sorted(folder.iterdir())],disk='new growable 20-GiB SATA; not preinstalled',firmware='UEFI, Secure Boot off',boot_order_forced=False,all_shipped_devices_enabled=True)
    (ROOT/f'dist/m13stage{args.stage}-starter-manifest.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
