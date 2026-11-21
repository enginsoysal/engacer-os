"""Confirmed native install through a routing fixture and the production MSI DLL."""
import hashlib,json,os,struct,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 import replay7
 loader=replay7.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  from window144_native import ui,c,f,t,clone,library,StoppedDisk,task
  from install147_build import build
  out=ROOT/'build/m14-native/stage7/install-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out
  fixture=build();meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage7/compact/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id']
  source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage7-compact'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m147-install-native');mounted=StoppedDisk(disk,library())
  try:mounted.put('/System/Windows/runtime8.elf',fixture.read_bytes())
  finally:mounted.close()
  report=dict(passed=False,build_id=meta['build_id'],clone=cloned,scope=__doc__,observer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
  try:
   root='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}';boot=ui.guest(work/'install',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
   with boot as g:
    p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);assert not any(path.startswith(root+'/')for path in f.entries(g));before=f.stats(g)[0];p.desktop(12001,True);output=task(g,p,12003);assert'M147_TEST_ROUTE_TO_PRODUCTION_MSI_SERVICE'in output
    raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384);message=raw[304:496].split(b'\0')[0].decode();assert'installed and verified'in message;report['message']=message;report['output']=output;report['first_activation_pages']=f.stats(g)[0]-before;assert report['first_activation_pages']==4
    entries=f.entries(g);assert root+'/product.bin'in entries and root+'/.EngacerMSI/transaction.bin'not in entries
    journal=ui.s.s.document(disk,root+'/product.bin',512*1024);assert journal[72:104]==hashlib.sha256(journal[:72]+bytes(32)+journal[104:]).digest();report['journal_sha256']=hashlib.sha256(journal).hexdigest();references=json.loads((ROOT/'evidence/M14/7/development/cab-host-initial.json').read_text(encoding='utf-8'))['originals'];expected=list(next(x for x in references if x['package_sha256']==journal[40:72].hex())['all_file_sha256'].values());at=1024;payloads=[];links=[];registry=0
    while at<len(journal):
     kind,n=struct.unpack_from('<II',journal,at)
     if kind in [1,3]:
      relative=journal[at+8:at+264].split(b'\0')[0].decode();sha=journal[at+264:at+296].hex();length,flags=struct.unpack_from('<QI',journal,at+296);native=(root if kind==1 else'/Data/Windows/Common/Programs'if flags else'/Users/Owner')+'/'+relative;data=ui.s.s.document(disk,native,32*1024*1024);assert len(data)==length and hashlib.sha256(data).hexdigest()==sha
      if kind==1 and flags==1:assert sha in expected;expected.remove(sha);payloads.append(dict(path=native,sha256=sha,bytes=length))
      elif kind==3:links.append(dict(path=native,sha256=sha,bytes=length))
     elif kind==2:registry+=1
     at+=n
    assert at==len(journal)and not expected and len(payloads)==106 and len(links)==2 and registry==16;report.update(payloads=payloads,shortcuts=links,registry_ownership_rows=registry,peak_native_managed_pages=struct.unpack_from('<Q',raw,24)[0]);c.shot(g,'native-msi-installed');(out/'serial.log').write_bytes(g.log().encode())
   mounted=StoppedDisk(disk,library())
   try:mounted.put('/System/Windows/runtime8.elf',(fixture.parent/'production-runtime8.elf').read_bytes())
   finally:mounted.close()
   boot=ui.guest(work/'independent',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
   with boot as g:
    assert ui.s.s.document(disk,root+'/product.bin',512*1024)==journal
    for row in payloads+links:assert hashlib.sha256(ui.s.s.document(disk,row['path'],32*1024*1024)).hexdigest()==row['sha256']
    p=ui.Pointer(g);p.drain();c.key(g,'esc');t.launch(g,p,'files',1);c.shot(g,'native-msi-independent-restart');report['independent_restart_preserves_registration_and_payloads']=True
   report['passed']=True
  except Exception:
   report['error']=ui.q.clean(traceback.format_exc())
   if'g'in locals():(out/'serial-failed.log').write_bytes(g.log().encode())
   raise
  finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
 finally:sys.meta_path.remove(loader)
if __name__=='__main__':main()
