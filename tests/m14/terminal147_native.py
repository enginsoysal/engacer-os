"""Labelled native DELETE faults after semantic undo, followed by source-free recovery.

Fault DLL changes only the native remove8 adapter; recovery restores the production DLL.
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
  from terminal147_build import build
  out=ROOT/'build/m14-native/stage7/terminal-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out;fixture,fault=build();meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));recipe=json.loads((fixture.parent/'routing-inputs.json').read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage7/compact/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id']==recipe['kernel_build_id'];source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage7-compact'/base['owned_fixture']/'owned.img';root='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}';done='/Data/Windows/Transactions/{23170F69-40C1-2702-2606-000001000000}.done';download='/Users/Owner/Downloads/7z2606-x64.msi';report=dict(passed=False,kernel_build_id=meta['build_id'],source_commit=recipe['source_commit'],scope=__doc__,observer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=[])
  def job(g):
   raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384);return dict(state=struct.unpack_from('<I',raw)[0],status=struct.unpack_from('<I',raw,8)[0],message=raw[304:496].split(b'\0')[0].decode(),output=raw[496:].split(b'\0')[0].decode(),peak_native_managed_pages=struct.unpack_from('<Q',raw,24)[0])
  try:
   for mode in ['pending','done']:
    work,disk,cloned=clone(ui,source,'m147-terminal-'+mode);mounted=StoppedDisk(disk,library())
    try:
     for native,file in [('/System/Windows/runtime8.elf',fixture),('/System/Windows/Installer/msi.dll',fault),('/System/Windows/Installer/msiexec.exe',fixture.parent/'msi147/msiexec.exe')]:mounted.put(native,file.read_bytes())
     mounted.put('/Users/Owner/Documents/cleanup-mode147.txt',mode.encode());mounted.put('/Users/Owner/Documents/Personal.txt',b'Personal data remains intact')
    finally:mounted.close()
    boot=ui.guest(work/'install',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
    with boot as g:
     p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);p.desktop(12001,True);task(g,p,12003);assert root+'/product.bin'in f.entries(g);(out/(mode+'-install.log')).write_bytes(g.log().encode())
    mounted=StoppedDisk(disk,library(['remove']))
    try:assert mounted.lib.v6_remove(ct.byref(mounted.volume),download.encode())==0
    finally:mounted.close()
    boot=ui.guest(work/'fault',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
    with boot as g:
     p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);before=f.stats(g)[0];p.desktop(12002,True);start=len(g.log());p.desktop(12003,True,settle=False);g.wait('M8_CPL3_CREATED',start);deadline=time.monotonic()+180
     while time.monotonic()<deadline:
      log=g.log()[start:]
      if'M8_JOB_FAILED'in log or'M8_JOB_DONE'in log:break
      time.sleep(.05)
     else:raise TimeoutError('The labelled native delete-fault task did not finish')
     p.drain();state=job(g);assert state['state']==3 and state['status']!=0 and'M147_TEST_IO_DELETE_REFUSAL '+mode in state['output'];assert'transaction was kept'in state['message'];assert f.stats(g)[0]-before==4
     entries=f.entries(g);assert done in entries and root+'/.EngacerMSI/source.msi'not in entries and download not in entries;image=ui.s.s.document(disk,done,512*1024);assert image[72:104]==hashlib.sha256(image[:72]+bytes(32)+image[104:]).digest()
     if mode=='pending':assert root+'/.EngacerMSI/transaction.bin'in entries
     else:assert not any(path==root or path.startswith(root+'/')for path in entries)
     c.shot(g,'native-tail-'+mode+'-retained');(out/(mode+'-fault.log')).write_bytes(g.log().encode());row=dict(mode=mode,clone=cloned,fault=state,fault_retained_managed_pages=0,first_activation_pages=4,completion_sha256=hashlib.sha256(image).hexdigest())
    # Remove the test I/O adapter. The next boot runs ordinary production cleanup.
    mounted=StoppedDisk(disk,library())
    try:mounted.put('/System/Windows/Installer/msi.dll',(fixture.parent/'msi147/msi.dll').read_bytes())
    finally:mounted.close()
    boot=ui.guest(work/'recover',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
    with boot as g:
     p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);assert ui.s.s.document(disk,done,512*1024)==image;before=f.stats(g)[0];p.desktop(12002,True);c.shot(g,'native-tail-'+mode+'-recovery-confirmation');task(g,p,12003);assert f.stats(g)[0]-before==4;state=job(g);assert state['state']==2 and state['status']==0 and'Removal finished'in state['message'];entries=f.entries(g);assert done not in entries and not any(path==root or path.startswith(root+'/')for path in entries);assert ui.s.s.document(disk,'/Users/Owner/Documents/Personal.txt',4096)==b'Personal data remains intact';row.update(recovery=state,recovery_retained_managed_pages=0,original_download_absent=True,source_cache_absent=True,independent_restart_source_free_recovery=True);c.shot(g,'native-tail-'+mode+'-recovered');(out/(mode+'-recover.log')).write_bytes(g.log().encode())
    report['cases'].append(row)
   report['passed']=True
  except Exception:
   report['error']=ui.q.clean(traceback.format_exc())
   if'g'in locals():(out/'serial-failed.log').write_bytes(g.log().encode())
   raise
  finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
 finally:sys.meta_path.remove(loader)
if __name__=='__main__':main()
