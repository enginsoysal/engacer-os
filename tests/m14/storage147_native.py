"""Ordinary confirmed INSTALL input exercises streaming, cancellation and retained journals."""
import hashlib,json,os,struct,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 import replay7
 loader=replay7.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  from window144_native import ui,c,f,t,clone,library,StoppedDisk
  from storage147_build import build
  out=ROOT/'build/m14-native/stage7/storage-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out;meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));fixture=ROOT/'build/m14-native/stage7/storage-fixture/fixture-runtime8.elf';receipt_path=fixture.parent/'compile-inputs.json'
  receipt=json.loads(receipt_path.read_text(encoding='utf-8'))if receipt_path.exists()else{}
  if receipt.get('kernel_build_id')!=meta['build_id']or any(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=digest for p,digest in receipt.get('test_sources',{}).items()):fixture=build();receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
  assert fixture.exists()and hashlib.sha256(fixture.read_bytes()).hexdigest()==receipt['artifacts'][fixture.name]['sha256']
  base=json.loads((ROOT/'build/m14-native/stage7/compact/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id'];source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage7-compact'/base['owned_fixture']/'owned.img'
  root='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}';size=9*1024*1024+17;period=bytes((i*37+19)&255 for i in range(256));expected=hashlib.sha256(period*(size//256)+period[:size%256]).hexdigest();report=dict(passed=False,build_id=meta['build_id'],observer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest(),scope='Test-only native worker over the production kernel; confirmed INSTALL, actual 9-MiB streaming, extent promotion, cancellation and recovery-record retention. Not authored original MSI installation or complete rollback qualification.',cases=[])
  try:
   for mode in ['success','cancel','journal-fail','corrupt-journal']:
    work,disk,cloned=clone(ui,source,'m147-storage-'+mode);mounted=StoppedDisk(disk,library())
    try:mounted.put('/System/Windows/runtime8.elf',fixture.read_bytes());mounted.put('/Users/Owner/Documents/storage-mode147.txt',mode.encode())
    finally:mounted.close()
    boot=ui.guest(work/'storage',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
    with boot as g:
     p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);initial_pages=f.stats(g)[0];assert ui.memory(g,ui.symbol('ready8',1,True)[0],1)[0]==0
     warm_start=len(g.log());p.desktop(12000,True,settle=False);g.wait('M8_JOB_FAILED',warm_start);p.drain();before=f.stats(g)[0];activation=before-initial_pages;assert ui.memory(g,ui.symbol('ready8',1,True)[0],1)[0]==1 and activation==4,activation
     assert not any(k.startswith(root+'/')for k in f.entries(g));p.desktop(12001,True);start=len(g.log());p.desktop(12003,True,settle=False);g.wait('M8_CPL3_CREATED',start);samples=[];deadline=time.monotonic()+180;cancelled=False
     while time.monotonic()<deadline:
      log=g.log()[start:];owner=ui.integer(g,'stream_owner147',True)
      if owner:
       dirty=ui.integer(g,'file_dirty_pages143',True)
       if ui.integer(g,'stream_owner147',True):assert dirty==0,(mode,dirty);samples.append(dirty)
      if mode=='cancel'and'M147_STREAM_CANCEL_READY'in log and not cancelled:p.drain();p.desktop(12008,True,settle=False);cancelled=True
      if 'M8_JOB_DONE'in log or'M8_JOB_FAILED'in log:break
      time.sleep(.05)
     else:raise TimeoutError('Native storage fixture did not finish')
     p.drain();raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384);state,command,status=struct.unpack_from('<III',raw);message=raw[304:496].split(b'\0')[0].decode();output=raw[496:].split(b'\0')[0].decode();owner=ui.integer(g,'stream_owner147',True);dirty=ui.integer(g,'file_dirty_pages143',True);retained=f.stats(g)[0]-before
     report['last_observed']=dict(mode=mode,state=state,status=status,message=message,output=output,stream_owner=owner,dirty_pages=dirty,retained_managed_pages=retained,before_managed_pages=before,after_managed_pages=f.stats(g)[0]);(out/(mode+'-serial.log')).write_bytes(g.log().encode());assert owner==0 and dirty==0,(owner,dirty);assert retained==0,retained
     entries=f.entries(g)
     if mode=='success':assert state==2 and status==0 and'M147_NATIVE_STREAM_JOURNAL_PROMOTION_PASS'in output and not any(k==root or k.startswith(root+'/')for k in entries)
     elif mode=='cancel':assert cancelled and state==3 and not any(k==root or k.startswith(root+'/')for k in entries)
     else:
      assert state==3 and status==1 and'M147_EXPECTED_FAILURE_AFTER_JOURNAL'in output
      payload=ui.s.s.document(disk,root+'/.EngacerMSI/stage/payload147.bin',16*1024*1024);assert len(payload)==size and hashlib.sha256(payload).hexdigest()==expected
      journal=ui.s.s.document(disk,root+'/.EngacerMSI/transaction.bin',4096);assert len(journal)==1336;valid=journal[72:104]==hashlib.sha256(journal[:72]+bytes(32)+journal[104:]).digest();assert valid==(mode=='journal-fail');assert ('transaction was kept'in message if valid else'record needs inspection'in message)
     t.close_all(g,p);t.launch(g,p,'files',1);c.shot(g,'storage-'+mode);(out/(mode+'-serial.log')).write_bytes(g.log().encode());report['cases'].append(dict(mode=mode,clone=cloned,first_activation_pages=activation,state=state,status=status,message=message,output=output,stream_samples=len(samples),whole_file_dirty_pages=0,retained_managed_pages=retained,peak_native_managed_pages=struct.unpack_from('<Q',raw,24)[0]))
    if mode in ['journal-fail','corrupt-journal']:
     # Restore only the explicit fixture worker on an owned stopped clone.
     mounted=StoppedDisk(disk,library())
     try:mounted.put('/System/Windows/runtime8.elf',(fixture.parent/'production-runtime8.elf').read_bytes())
     finally:mounted.close()
     again=ui.guest(work/'independent',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(again)
     with again as g:
      assert ui.s.s.document(disk,root+'/.EngacerMSI/transaction.bin',4096)==journal;assert hashlib.sha256(ui.s.s.document(disk,root+'/.EngacerMSI/stage/payload147.bin',16*1024*1024)).hexdigest()==expected;p=ui.Pointer(g);p.drain();c.key(g,'esc');t.launch(g,p,'files',1);c.shot(g,'storage-restart-'+mode);report['cases'][-1]['independent_restart_preserves_journal_and_payload']=True
   report['passed']=True
  except Exception:
   report['error']=ui.q.clean(traceback.format_exc())
   if 'g'in locals():(out/'serial-failed.log').write_bytes(g.log().encode())
   raise
  finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
 finally:sys.meta_path.remove(loader)
if __name__=='__main__':main()
