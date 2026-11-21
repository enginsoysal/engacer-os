"""Cancel an original generic MSI after durable staging, then recover without download."""
import ctypes as ct,hashlib,json,os,struct,subprocess,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 import replay7
 loader=replay7.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  from window144_native import ui,c,f,t,clone,StoppedDisk,task
  from fixture1 import library
  from runtime147_build import build
  from m14_integrity import verify_working_inputs
  commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();private=ROOT/'build/m14-native/stage7'/('runtime-cancel-'+commit[:8]);fixture=private/'WINDOWS8.ELF'
  if not(private/'compile-inputs.json').exists():build('cancel-'+commit[:8])
  recipe=json.loads((private/'compile-inputs.json').read_text(encoding='utf-8'));verify_working_inputs(ROOT,recipe['source_sha256'])
  out=ROOT/'build/m14-native/stage7/generic-cancel-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out;meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage7/compact/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id']==recipe['kernel_build_id'];source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage7-compact'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m147-generic-cancel');package=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/npp.8.9.9.1.Installer.x64.msi';download='/Users/Owner/Downloads/'+package.name;root='/Applications/Windows/{A23B657D-838B-4C9B-8F9D-386E50C1A76B}';pending=root+'/.EngacerMSI/transaction.bin';report=dict(passed=False,scope=__doc__,kernel_build_id=meta['build_id'],service_source_commit=json.loads((fixture.parent/'compile-inputs.json').read_text(encoding='utf-8'))['source_commit'],observer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),private_service_receipt_sha256=hashlib.sha256((fixture.parent/'compile-inputs.json').read_bytes()).hexdigest(),owned_fixture=work.name,clone=cloned)
  mounted=StoppedDisk(disk,library())
  try:
   for native,file in [('/System/Windows/runtime8.elf',fixture.parent/'WINDOWS8.ELF'),('/System/Windows/Installer/msi.dll',fixture.parent/'msi147/msi.dll'),('/System/Windows/Installer/msiexec.exe',fixture.parent/'msi147/msiexec.exe')]:mounted.put(native,file.read_bytes())
   mounted.put(download,package.read_bytes());mounted.put('/Users/Owner/Documents/Keep.txt',b'Independent personal data')
  finally:mounted.close()
  def job(g):
   raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384);return dict(state=struct.unpack_from('<I',raw)[0],status=struct.unpack_from('<I',raw,8)[0],message=raw[304:496].split(b'\0')[0].decode(),output=raw[496:].split(b'\0')[0].decode())
  try:
   boot=ui.guest(work/'cancel',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
   with boot as g:
    p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);p.desktop(12013,True);p.desktop(54019,True);c.key(g,'ctrl','a');c.type_text(g,'/Users/Owner/Downloads');c.key(g,'ret');p.drain();row=f.entries(g)[download]['index']
    for _ in range(128):
     if any(r[5]==55000+row for r in f.controls(g)):break
     p.desktop(54023,True)
    else:raise AssertionError('The original MSI cannot be selected')
    p.desktop(55000+row,True);p.desktop(54011,True);task(g,p,12000);before=f.stats(g)[0];p.desktop(12001,True);start=len(g.log());p.desktop(12003,True,settle=False);g.wait('M8_CPL3_CREATED',start);deadline=time.monotonic()+240
    while time.monotonic()<deadline:
     if pending in f.entries(g):break
     if'M8_JOB_DONE'in g.log()[start:]or'M8_JOB_FAILED'in g.log()[start:]:raise AssertionError('The selected durable cancellation point was not reached')
     time.sleep(.05)
    else:raise TimeoutError('No durable original MSI transaction appeared')
    p.desktop(12008,True);state=job(g);report['last_observed']=dict(job=state,managed_delta=f.stats(g)[0]-before);assert state['state']==3 and state['status']==1 and'kept'in state['message'],report['last_observed'];assert'M8_JOB_FAILED code=0x00000000000004c7'in g.log()[start:],report['last_observed'];assert f.stats(g)[0]==before,report['last_observed'];entries=f.entries(g);assert pending in entries and root+'/product.bin'not in entries;image=ui.s.s.document(disk,pending,512*1024);assert image[72:104]==hashlib.sha256(image[:72]+bytes(32)+image[104:]).digest();report['cancel']=dict(**state,retained_managed_pages=0,transaction_sha256=hashlib.sha256(image).hexdigest());c.shot(g,'generic-durable-cancel');(out/'cancel-serial.log').write_bytes(g.log().encode())
   mounted=StoppedDisk(disk,library(['remove']))
   try:assert mounted.lib.v6_remove(ct.byref(mounted.volume),download.encode())==0
   finally:mounted.close()
   boot=ui.guest(work/'recover',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
   with boot as g:
    p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);p.desktop(12208,True);p.desktop(12200,True);before=f.stats(g)[0];p.desktop(12002,True);c.shot(g,'generic-recovery-confirmation');task(g,p,12003);state=job(g);assert state['state']==2 and state['status']==0;assert f.stats(g)[0]-before==4;assert not any(path==root or path.startswith(root+'/')for path in f.entries(g));assert download not in f.entries(g);assert ui.s.s.document(disk,'/Users/Owner/Documents/Keep.txt',4096)==b'Independent personal data';report['recovery']=dict(**state,retained_managed_pages=0,first_activation_pages=4,original_download_absent=True);c.shot(g,'generic-recovered');(out/'recover-serial.log').write_bytes(g.log().encode())
   report['passed']=True
  except Exception:
   report['error']=ui.q.clean(traceback.format_exc())
   if'g'in locals():(out/'serial-failed.log').write_bytes(g.log().encode())
   raise
  finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
 finally:sys.meta_path.remove(loader)
if __name__=='__main__':main()
