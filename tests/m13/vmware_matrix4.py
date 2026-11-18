"""M13.4 installation and startup enabled-device VMware controller matrix; ordinary guest input only."""
import argparse,ctypes,hashlib,importlib.util,io,json,msvcrt,re,shutil,subprocess,time,traceback,uuid,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
legacy=module('vmware10final',ROOT/'tests/m10/vmware.py');v=legacy.v
builder=module('starter11final',ROOT/'tools/release/vmware_starter11.py')
IMAGE='EngacerOS-M13STAGE4'
def sparse(path):
 assert path.resolve().is_relative_to((ROOT/'build/m13-native/stage4/matrix').resolve()) and not path.exists()
 with path.open('xb'):pass
 subprocess.run(['fsutil','sparse','setflag',str(path)],capture_output=True,check=True,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
 with path.open('r+b',buffering=0) as stream:
  handle=ctypes.wintypes.HANDLE(msvcrt.get_osfhandle(stream.fileno()))
  assert v.workspace.api.SetFilePointerEx(handle,20*1024**3,None,0) and v.workspace.api.SetEndOfFile(handle)
 assert v.workspace.allocated(path)<1024**2;return path
def click(g,x,y):legacy.guest_click10(g,x,y)
def launch(g,name,kind):
 v.key(g,0xffeb)
 for c in name:v.key(g,ord(c))
 start=len(g.read());v.enter(g);g.wait('M7_WINDOW_OPEN app=0x'+format(kind,'016x'),offset=start)
def chord(g,modifier,key):
 display=g.connect_display();display.key(modifier,True);time.sleep(.12);display.press(key);display.key(modifier,False);g.read();time.sleep(.2)
def windows(g,out):
 launch(g,'windows apps',19);v.shot(g,out,'windows-apps')
 for command in (12001,12005,12006,12007,12002,12001,12005):
  start=len(g.read());display=g.connect_display();left=(display.width-min(display.width-80,940))//2+24;top=35+62
  installed=command not in (12001,)
  if command==12001:click(g,left+80,top+226+18);click(g,left+166+95,top+340+18)
  elif command==12002:click(g,left+174+85,top+140+18);click(g,left+166+95,top+340+18)
  elif command==12005:click(g,left+80,top+140+18)
  elif command==12006:click(g,left+97,top+194+18)
  else:click(g,left+209+97,top+194+18)
  g.wait('M8_CPL3_CREATED',offset=start)
  for _ in range(48):
   g.connect_display().key(0xffe1,True);time.sleep(.01);g.connect_display().key(0xffe1,False);g.read();time.sleep(.01)
  g.wait('M8_JOB_DONE code=0x0000000000000000',offset=start,timeout=240)
  assert 'M8_JOB_FAILED' not in g.read()[start:];time.sleep(.8)
 assert 'M92_INPUT_IRQ_CPL3_SERVICED' in g.read();v.shot(g,out,'original-msi-reinstalled');v.key(g,0xff1b)
def folders(g,out):
 display=g.connect_display();fw=1080 if display.width>1200 else display.width-112;fh=720 if display.height>900 else display.height-100
 fx=(display.width-fw)//2;fy=(display.height-60-fh)//2
 chord(g,0xffe9,ord('d'));chord(g,0xffe3,ord('a'))
 for char in '/Users/Owner/Documents':
  if char.isupper():
   display=g.connect_display();display.key(0xffe1,True);v.key(g,ord(char.lower()));display.key(0xffe1,False)
  else:v.key(g,ord(char))
 start=len(g.read());v.enter(g);g.wait('M125_LOCATION native /Users/Owner/Documents',offset=start)
 v.shot(g,out,'documents-before-create')
 display=g.connect_display();display.key(0xffe3,True);display.key(0xffe1,True);v.key(g,ord('n'));display.key(0xffe1,False);display.key(0xffe3,False);g.read();time.sleep(.3)
 v.shot(g,out,'new-folder-dialog');chord(g,0xffe3,ord('a'))
 for c in 'vmware-folders':v.key(g,ord(c))
 v.shot(g,out,'folder-name-entered');v.enter(g);g.read();time.sleep(.3)
 # The M11 dialog stores through v6_mkdir and does not emit the old M72 create marker.
 # Navigate by ordinary address entry; visit72 logs only after validating a real folder.
 chord(g,0xffe9,ord('d'));chord(g,0xffe3,ord('a'))
 for c in 'vmware-folders':
  if c.isupper():
   display=g.connect_display();display.key(0xffe1,True);v.key(g,ord(c.lower()));display.key(0xffe1,False)
  else:v.key(g,ord(c))
 start=len(g.read());v.enter(g)
 try:g.wait('M125_LOCATION native /Users/Owner/Documents/vmware-folders',offset=start)
 except Exception:
  v.shot(g,out,'folder-failure');(out/'folder-failure.log').write_bytes(g.read().encode());raise
 v.shot(g,out,'real-folder')

def main():
 p=argparse.ArgumentParser();p.add_argument('--controller',choices=['sata','ide','lsilogic','lsisas1068','pvscsi','buslogic','nvme'],default='sata');p.add_argument('--firmware',choices=['efi','bios'],default='efi');p.add_argument('--starter',action='store_true');a=p.parse_args()
 assert not(a.controller=='buslogic' and a.firmware=='efi');assert not a.starter or (a.controller,a.firmware)==('sata','efi')
 assert not (ROOT/'evidence/M13/4/publication-results.json').exists(),'Final published evidence is immutable'
 label=a.controller+'-'+a.firmware+('-starter' if a.starter else '');out=ROOT/'build/m13/stage4/matrix-results'/label;out.mkdir(parents=True,exist_ok=True)
 work=ROOT/'build/m13-native/stage4/matrix'/label/uuid.uuid4().hex;work.mkdir(parents=True)
 meta=json.loads((ROOT/'dist/m13stage4-build-manifest.json').read_text(encoding='utf-8'));iso=ROOT/'dist'/(IMAGE+'.iso');iso_sha=hashlib.sha256(iso.read_bytes()).hexdigest();assert iso_sha==meta['artifacts'][iso.name]['sha256']
 before=v.old.v.inventory();harness_sha=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();report={'harness_sha256':harness_sha,'passed':False,'build_id':meta['build_id'],'iso_sha256':iso_sha,'controller':a.controller,'firmware':a.firmware,'exact_starter':a.starter,'checks':[]}
 try:
  if a.starter:
   archive=ROOT/'dist'/(IMAGE+'-VMware.zip')
   with zipfile.ZipFile(archive) as z:assert z.testzip() is None;z.extractall(work)
   source=work/'EngacerOS';descriptor=source/'EngacerOS.vmdk';original=(source/'EngacerOS.vmx').read_text(encoding='utf-8');report['starter_sha256']=hashlib.sha256(archive.read_bytes()).hexdigest()
  else:
   disk=sparse(work/'owned-flat.img');descriptor=work/'owned.vmdk';adapter='buslogic' if a.controller=='buslogic' else 'lsilogic' if a.controller in ('lsilogic','lsisas1068','pvscsi') else 'ide'
   descriptor.write_bytes(('version=1\nencoding="UTF-8"\nCID=fffffffe\nparentCID=ffffffff\ncreateType="monolithicFlat"\nRW 41943040 FLAT "owned-flat.img" 0\nddb.adapterType = "'+adapter+'"\n').encode())
  g=v.Guest(work/'same-vm',descriptor,a.firmware)
  observation='\n'.join(line for line in g.vmx.read_text(encoding='utf-8').splitlines() if line.startswith(('serial0.','RemoteDisplay.')))+'\n'
  if a.starter:
   for file in source.iterdir():shutil.copyfile(file,g.folder/file.name)
   g.vmx=g.folder/'EngacerOS.vmx';cfg=original+observation
  else:cfg=builder.configuration(IMAGE,a.controller,a.firmware).replace('EngacerOS.vmdk',descriptor.as_posix()).replace(IMAGE+'.iso',iso.as_posix())+observation
  for required in ['ethernet0.present = "TRUE"','sound.present = "TRUE"','usb_xhci.present = "TRUE"','pciBridge4.virtualDev = "pcieRootPort"']:assert required in cfg
  assert 'bios.bootOrder' not in cfg;g.vmx.write_bytes(cfg.encode())
  with g:
   v.shot(g,out,'welcome');v.enter(g);v.enter(g);v.enter(g);v.tab(g,3);v.enter(g);v.enter(g);v.enter(g);v.shot(g,out,'review');v.enter(g);g.wait('M6_INSTALL_PASS',timeout=240)
   start=len(g.read());v.enter(g);g.wait('M75_USER_RESTART',offset=start);g.wait('M7_DESKTOP_READY build='+meta['build_id'],offset=start,timeout=180);assert 'M6_INSTALLED_VOLUME' in g.read()[start:] and 'M6_WIZARD_READY' not in g.read()[start:]
   g.wait('M7_DHCP_CONFIGURED',offset=start,timeout=90);g.rfb.close();g.rfb=None;v.shot(g,out,'first-start');v.key(g,0xff1b);g.wait('M115_GUIDE_DISMISSED',offset=start)
   if a.starter:windows(g,out)
   folders(g,out);(out/'install.log').write_bytes(g.read().encode())
  report['checks'].append('All shipped devices enabled: real eight-step 20-GiB installation, retained-ISO reset into the actual installed kernel, DHCP and persistent graphical folder creation')
  cfg=g.vmx.read_text(encoding='utf-8');cfg=re.sub(r'(?im)^ide1:0.startConnected\s*=.*$','ide1:0.startConnected = "FALSE"',cfg);assert 'bios.bootOrder' not in cfg;g.vmx.write_bytes(cfg.encode());g.installed=True
  for turn in range(2):
   g.output='';g.pipe=None;g.rfb=None
   with g:
    g.wait('M7_DESKTOP_READY build='+meta['build_id']);assert 'M6_INSTALLED_VOLUME' in g.read();v.shot(g,out,'disk-only-'+str(turn));(out/('restart-'+str(turn)+'.log')).write_bytes(g.read().encode())
   if not a.starter:assert '/Users/Owner/Documents/vmware-folders' in legacy.s.directories(disk)
  report['checks'].append('Same VMX, disk and firmware variables: two disk-only starts with CD disconnected and no forced firmware boot order; independently verified persistent folder')
  if a.starter:
   inspection=sparse(work/'independent-starter.img');tool=Path('C:/Program Files/qemu/qemu-img.exe');subprocess.run([str(tool),'convert','-n','--target-is-zero','-f','vmdk','-O','raw','-S','4k',str(g.folder/'EngacerOS.vmdk'),str(inspection)],capture_output=True,check=True,timeout=120,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
  else:inspection=disk
  assert '/Users/Owner/Documents/vmware-folders' in legacy.s.directories(inspection)
  persisted={}
  for entry in meta['distribution']['resolved_files']:
   target=re.sub(r'^/Users/[^/]+/','/Users/Owner/',entry['target']);raw=legacy.s.s.document(inspection,target,8*1024**2);sha=hashlib.sha256(raw).hexdigest();assert sha==hashlib.sha256((ROOT/entry['source']).read_bytes()).hexdigest();persisted[target]=sha
  report['persisted_distribution_sha256']=persisted;report['checks'].append('Every distribution guide and binary sample independently matches its exact stored bytes')
  if a.starter:
   import sys;sys.path.insert(0,str(ROOT/'tests/m9'));from lifecycle import payloads
   report['original_payload_sha256']=payloads(inspection)
   document=legacy.s.s.document(inspection,'/Users/Owner/Documents/EngineOS-Windows.txt');extracted=legacy.s.s.document(inspection,'/Users/Owner/Documents/EngineOS-Windows-Extracted/EngineOS-Windows.txt');assert document==extracted
   archive=legacy.s.s.document(inspection,'/Users/Owner/Documents/EngineOS-Windows.zip',8*1024**2)
   with zipfile.ZipFile(io.BytesIO(archive)) as z:assert z.testzip() is None and z.read('EngineOS-Windows.txt')==document
   report['checks'].append('Original 7-Zip MSI install/run/archive/extract/remove/reinstall, protected-worker hardware input, 106 payload hashes and exact archived/extracted document bytes')
  report.update(passed=True,boot_order_forced=False,same_vm_reused=True,all_shipped_devices_enabled=True)
 except Exception:report['error']=v.old.v.redact(traceback.format_exc());raise
 finally:
  assert hashlib.sha256(Path(__file__).read_bytes()).hexdigest()==harness_sha,'Harness changed during native qualification';report['existing_vm_inventory_unchanged']=before==v.old.v.inventory();report['passed']=report['passed'] and report['existing_vm_inventory_unchanged'];assert hashlib.sha256(iso.read_bytes()).hexdigest()==iso_sha
  (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
