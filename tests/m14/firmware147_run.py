"""Exact stage-seven boot bundle through ordinary BIOS/UEFI installation and disk boots."""
import argparse,hashlib,json,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--firmware',choices=['bios','uefi'],default='bios');parser.add_argument('--media',choices=['iso','usb'],default='iso');args=parser.parse_args();sys.argv=[str(__file__),'--stage','7','--profile','compact']
 import native1 as n
 ui=n.ui;out=ROOT/'build/m14-native/stage7'/('firmware-'+args.firmware+'-'+args.media);out.mkdir(parents=True,exist_ok=True);meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m147-firmware-'+args.firmware+'-'+args.media);disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
 report=dict(passed=False,build_id=meta['build_id'],firmware=args.firmware,media=args.media,owned_fixture=work.name,scope=__doc__,media_sha256=meta['artifacts']['EngacerOS-M14STAGE7'+('.iso'if args.media=='iso'else '-usb.img')]['sha256'],checks=[])
 try:
  with ui.guest(work/'install',disk,firmware=args.firmware,media=args.media,resolution=(1280,800),ram=128)as g:
   p=ui.Pointer(g);p.drain();assert 'M147_BOOT_SERVICE_DIGESTS_OK' in g.log();n.shot(g,out,'welcome');n.wizard(g,p,2);n.wizard(g,p,50011)
   for action in [2,100,2,2,2]:n.wizard(g,p,action)
   start=n.wizard(g,p,2);g.wait('M6_INSTALL_PASS',start,240);start=n.wizard(g,p,84);g.wait('M7_DESKTOP_READY',start,180);n.shot(g,out,'desktop',True);(out/'install.log').write_bytes(g.log().encode());report['checks'].append('Ordinary wizard installs and Finish reaches the persistent desktop on the exact live module.')
  runtime=ui.s.s.document(disk,'/System/Windows/runtime8.elf',1024**2);assert runtime==(ROOT/'build/m14-native/WINDOWS8.ELF').read_bytes();report['installed_runtime_sha256']=hashlib.sha256(runtime).hexdigest()
  for turn in [1,2]:
   boot=ui.guest(work/('disk-only-'+str(turn)),disk,firmware=args.firmware,media='installed',ready='M7_DESKTOP_READY',resolution=(1280,800),ram=128);ui.s.normal_boot(boot)
   with boot as g:
    assert 'ENGINE_OS_KERNEL_ENTRY build='+meta['build_id'] in g.log();ui.Pointer(g).drain();n.shot(g,out,'disk-only-'+str(turn),True);(out/('disk-only-'+str(turn)+'.log')).write_bytes(g.log().encode())
  report['checks'].append('Two independent no-media starts use ordinary firmware discovery without forced boot order.');report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
