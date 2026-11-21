"""Native cached-source removal, cancellation, preserved data and reinstallation.

Private stopped-clone worker/service update over the frozen kernel, not public ISO qualification.
"""
import ctypes as ct,hashlib,json,os,struct,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 import replay7
 loader=replay7.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  from window144_native import ui,c,f,t,clone,StoppedDisk,task
  from fixture1 import library
  from remove147_build import build
  out=ROOT/'build/m14-native/stage7/remove-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out;fixture=build();meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));recipe=json.loads((fixture.parent/'routing-inputs.json').read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage7/compact/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id']==recipe['kernel_build_id']
  source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage7-compact'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m147-remove-native');root='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}';download='/Users/Owner/Downloads/7z2606-x64.msi';report=dict(passed=False,kernel_build_id=meta['build_id'],source_commit=recipe['source_commit'],clone=cloned,scope=__doc__,observer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),tasks=[])
  mounted=StoppedDisk(disk,library(['remove']))
  try:
   for native,file in [('/System/Windows/runtime8.elf',fixture),('/System/Windows/Installer/msi.dll',fixture.parent/'msi147/msi.dll'),('/System/Windows/Installer/msiexec.exe',fixture.parent/'msi147/msiexec.exe')]:mounted.put(native,file.read_bytes())
  finally:mounted.close()
  def document(path,limit=64*1024*1024):return ui.s.s.document(disk,path,limit)
  def snapshot_job(g):
   raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384);return dict(state=struct.unpack_from('<I',raw)[0],status=struct.unpack_from('<I',raw,8)[0],message=raw[304:496].split(b'\0')[0].decode(),peak_native_managed_pages=struct.unpack_from('<Q',raw,24)[0])
  def verify_saved(g,wanted):
   entries=f.entries(g);prefix='/Users/Owner/Documents/Recovered applications/'+root.rsplit('/',1)[1]+'/';found={};metadata={}
   for path,entry in entries.items():
    if path.startswith('/Data/Windows/')and'/Files/m'in path and entry['kind']==1:
     raw=document(path,4096)
     if len(raw)==552 and struct.unpack_from('<Q',raw)[0]==0x314d464e4534314d:metadata[raw[264:520].split(b'\0')[0].decode()]=struct.unpack_from('<I',raw,544)[0]
   for path,entry in entries.items():
    if not path.startswith(prefix)or entry['kind']!=1 or not path.endswith('.txt'):continue
    data=document(path,4096)
    if not data.startswith(b'Preserved application file\n'):continue
    original=data.split(b'Original path: ',1)[1].split(b'\n',1)[0].decode();value=wanted[original];backup=path[:-4];actual=document(backup);assert actual==value and hashlib.sha256(value).hexdigest().encode()in data;assert metadata[backup]==32;found[original]=dict(path=backup,sha256=hashlib.sha256(actual).hexdigest(),bytes=len(actual),native_metadata_attributes=metadata[backup])
   assert len(found)==len(wanted);assert document('/Users/Owner/Documents/Personal.txt')==b'Personal document outside the application';return found
  try:
   boot=ui.guest(work/'install',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
   with boot as g:
    p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);cold=f.stats(g)[0];task(g,p,12000);before=f.stats(g)[0];assert before-cold==4;p.desktop(12001,True);task(g,p,12003);assert f.stats(g)[0]==before;report['tasks'].append(dict(operation='install',retained_managed_pages=0,**snapshot_job(g)));journal=document(root+'/product.bin',512*1024);assert journal[72:104]==hashlib.sha256(journal[:72]+bytes(32)+journal[104:]).digest();paths=[];at=1024
    while at<len(journal):
     kind,n=struct.unpack_from('<II',journal,at)
     if kind in [1,3]:
      rel=journal[at+8:at+264].split(b'\0')[0].decode();sha=journal[at+264:at+296].hex();length,flags=struct.unpack_from('<QI',journal,at+296);path=(root if kind==1 else'/Data/Windows/Common/Programs'if flags else'/Users/Owner')+'/'+rel;actual=document(path);assert len(actual)==length and hashlib.sha256(actual).hexdigest()==sha;paths.append(dict(path=path,sha256=sha,bytes=length,kind=kind))
     at+=n
    c.shot(g,'native-new-controller-install');(out/'install-serial.log').write_bytes(g.log().encode())
   wanted={root+'/7zFM.exe':b'User-modified installed binary',root+'/User-\u00e9\U0001f680.txt':b'User-created Unicode-named document',next(row['path']for row in paths if row['kind']==3):b'User-customized shortcut',root+'/Large personal file.bin':bytes((n*17+5)&255 for n in range(256))*(33*1024*1024//256)}
   mounted=StoppedDisk(disk,library(['remove']))
   try:
    for path,value in wanted.items():mounted.put(path,value)
    mounted.put('/Users/Owner/Documents/Personal.txt',b'Personal document outside the application');assert mounted.lib.v6_remove(ct.byref(mounted.volume),download.encode())==0
   finally:mounted.close()
   boot=ui.guest(work/'remove',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
   with boot as g:
    p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);assert download not in f.entries(g);cold=f.stats(g)[0];p.desktop(12002,True);start=len(g.log());p.desktop(12003,True,settle=False);g.wait('M8_CPL3_CREATED',start);deadline=time.monotonic()+180;cancelled=False
    while time.monotonic()<deadline:
     log=g.log()[start:]
     if'M8_JOB_DONE'in log or'M8_JOB_FAILED'in log:break
     if root+'/.EngacerMSI/transaction.bin'in f.entries(g):p.desktop(12008,True,settle=False);cancelled=True;break
     time.sleep(.01)
    assert cancelled,'The native operation finished before cancellation could be delivered'
    g.wait('M8_JOB_FAILED',start);p.drain();state=snapshot_job(g);assert state['state']==3 and'transaction was kept'in state['message'];assert f.stats(g)[0]-cold==4;report['tasks'].append(dict(operation='cancel after durable removal journal',retained_managed_pages=0,first_activation_pages=4,**state));retained=document(root+'/.EngacerMSI/transaction.bin',512*1024);assert retained[72:104]==hashlib.sha256(retained[:72]+bytes(32)+retained[104:]).digest();c.shot(g,'native-removal-cancelled-with-journal');(out/'cancel-serial.log').write_bytes(g.log().encode())
   # Independent restart exercises a fresh worker and rereads the durable log/cache.
   boot=ui.guest(work/'recover',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
   with boot as g:
    p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);assert document(root+'/.EngacerMSI/transaction.bin',512*1024)==retained;before=f.stats(g)[0];p.desktop(12002,True);task(g,p,12003);assert f.stats(g)[0]-before==4;assert not any(path==root or path.startswith(root+'/')for path in f.entries(g));report['tasks'].append(dict(operation='recover removal after independent restart',retained_managed_pages=0,first_activation_pages=4,**snapshot_job(g)));report['preserved']=verify_saved(g,wanted);c.shot(g,'native-recovered-removal');(out/'recover-serial.log').write_bytes(g.log().encode())
   mounted=StoppedDisk(disk,library())
   try:mounted.put(download,(ROOT/'third_party/7zip/7z2606-x64.msi').read_bytes())
   finally:mounted.close()
   boot=ui.guest(work/'reinstall',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
   with boot as g:
    p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);cold=f.stats(g)[0];p.desktop(12001,True);task(g,p,12003);before=f.stats(g)[0];assert before-cold==4;report['tasks'].append(dict(operation='reinstall after saved modified files',retained_managed_pages=0,first_activation_pages=4,**snapshot_job(g)))
    for row in paths:assert hashlib.sha256(document(row['path'])).hexdigest()==row['sha256']
    p.desktop(12002,True);task(g,p,12003);assert f.stats(g)[0]==before;assert not any(path==root or path.startswith(root+'/')for path in f.entries(g));assert verify_saved(g,wanted)==report['preserved'];report['tasks'].append(dict(operation='remove reinstalled unchanged product',retained_managed_pages=0,**snapshot_job(g)));c.shot(g,'native-reinstall-and-remove');(out/'reinstall-serial.log').write_bytes(g.log().encode())
   mounted=StoppedDisk(disk,library())
   try:mounted.put('/System/Windows/runtime8.elf',(fixture.parent/'WINDOWS8.ELF').read_bytes())
   finally:mounted.close()
   boot=ui.guest(work/'final',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
   with boot as g:
    assert verify_saved(g,wanted)==report['preserved'];p=ui.Pointer(g);p.drain();c.key(g,'esc');t.launch(g,p,'files',1);c.shot(g,'native-preserved-data-final-restart');report['production_worker_restored_and_restart_preserves_saved_data']=True
   report['passed']=True
  except Exception:
   report['error']=ui.q.clean(traceback.format_exc())
   if'g'in locals():(out/'serial-failed.log').write_bytes(g.log().encode())
   raise
  finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
 finally:sys.meta_path.remove(loader)
if __name__=='__main__':main()
