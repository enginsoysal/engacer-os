"""Ordinary original Notepad++ MSI lifecycle; optional owned French preference seed.

No original DLL or application executes on the host. The French variant changes
only the own worker to seed an existing preference through native registry APIs;
all installer effects and original deferred bodies run in the production service.
"""
import argparse,hashlib,json,os,struct,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 args=argparse.ArgumentParser();args.add_argument('--french',action='store_true');options=args.parse_args()
 import replay7
 loader=replay7.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  from window144_native import ui,c,f,t,clone,StoppedDisk,task
  from fixture1 import library
  tag='french' if options.french else 'default';out=ROOT/'build/m14-native/stage7'/('generic-native-'+tag);out.mkdir(parents=True,exist_ok=True);c.OUT=out
  meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage7/compact/results.json').read_text(encoding='utf-8'));assert base['passed'] and base['build_id']==meta['build_id']
  source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage7-compact'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m147-generic-'+tag)
  package=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/npp.8.9.9.1.Installer.x64.msi';download='/Users/Owner/Downloads/'+package.name;root='/Applications/Windows/{A23B657D-838B-4C9B-8F9D-386E50C1A76B}';reference=next(p for p in json.loads((ROOT/'evidence/M14/7/development/cab-host-initial.json').read_text(encoding='utf-8'))['originals'] if p['package_sha256']==hashlib.sha256(package.read_bytes()).hexdigest());report=dict(passed=False,scope=__doc__,profile=tag,build_id=meta['build_id'],source_commit=meta['source_commit'],observer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),clone=cloned,tasks=[])
  mounted=StoppedDisk(disk,library())
  try:
   mounted.put(download,package.read_bytes());mounted.put('/Users/Owner/Documents/Keep personal.txt',b'Independent personal document')
   if options.french:
    from french147_build import build
    fixture=build();mounted.put('/System/Windows/runtime8.elf',fixture.read_bytes());report['preference_fixture_receipt_sha256']=hashlib.sha256((fixture.parent/'routing-inputs.json').read_bytes()).hexdigest()
  finally:mounted.close()
  def document(path,limit=32*1024*1024):return ui.s.s.document(disk,path,limit)
  def snapshot(g):
   data=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384)
   return dict(state=struct.unpack_from('<I',data)[0],status=struct.unpack_from('<I',data,8)[0],peak_native_managed_pages=struct.unpack_from('<Q',data,24)[0],message=data[304:496].split(b'\0')[0].decode(),output=data[496:].split(b'\0')[0].decode())
  def choose_review(g,p):
   p.desktop(12013,True);assert c.flag(g,'picker12')==9;p.desktop(54019,True);c.key(g,'ctrl','a');c.type_text(g,'/Users/Owner/Downloads');c.key(g,'ret');p.drain();row=f.entries(g)[download]['index']
   for _ in range(128):
    if any(r[5]==55000+row for r in f.controls(g)):break
    p.desktop(54023,True)
   else:raise AssertionError('The original MSI is not reachable in its chooser')
   p.desktop(55000+row,True);p.desktop(54011,True);output=task(g,p,12000);assert'M147_NATIVE_MSI_READ_ONLY_PLAN_PASS'in output;assert any(r[5]==12001 for r in f.controls(g));c.shot(g,tag+'-reviewed-original')
  def verify_install(g):
   image=document(root+'/product.bin',512*1024);assert image[72:104]==hashlib.sha256(image[:72]+bytes(32)+image[104:]).digest();remaining=list(reference['all_file_sha256'].values());payloads=links=generated=registry=0;at=1024
   while at<len(image):
    kind,count=struct.unpack_from('<II',image,at)
    if kind in (1,3):
     path=image[at+8:at+264].split(b'\0')[0].decode();sha=image[at+264:at+296].hex();size,flags=struct.unpack_from('<QI',image,at+296);prefix=root if kind==1 else '/Data/Windows/Common/Programs' if flags else '/Users/Owner';data=document(prefix+'/'+path);assert len(data)==size and hashlib.sha256(data).hexdigest()==sha,(path,size)
     if kind==1 and flags==1:remaining.remove(sha);payloads+=1
     elif kind==1 and flags==2:generated+=1;assert path=='nativeLang.xml' and sha=='7bd00f2d43f7700524d2a11ba643909229d87255b8aa43b27a0a7bc6ca7e52ef'
     elif kind==3:links+=1
    elif kind==2:registry+=1
    at+=count
   assert not remaining and payloads==217 and links==1 and registry==(10 if options.french else 9) and generated==int(options.french)
   return dict(payloads=payloads,links=links,registry_ownerships=registry,generated_files=generated,journal_sha256=hashlib.sha256(image).hexdigest())
  try:
   boot=ui.guest(work/'install',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
   with boot as g:
    p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);choose_review(g,p);before=f.stats(g)[0];p.desktop(12001,True);task(g,p,12003);after=f.stats(g)[0];state=snapshot(g);assert state['state']==2 and state['status']==0;assert after-before in (0,4),(before,after)
    if options.french:assert'M147_ORIGINAL_DEFERRED_BODY CopyNativeLangAction result=0 continued=0'in state['output']
    report['tasks'].append(dict(operation='install',retained_managed_pages=0,first_activation_pages=after-before,**state,**verify_install(g)));c.shot(g,tag+'-installed');(out/'install-serial.log').write_bytes(g.log().encode())
   mounted=StoppedDisk(disk,library(['remove']))
   try:
    assert mounted.lib.v6_remove(__import__('ctypes').byref(mounted.volume),download.encode())==0
    if options.french:mounted.put(root+'/nativeLang.xml',b'Modified language file must survive removal')
   finally:mounted.close()
   boot=ui.guest(work/'remove',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
   with boot as g:
    p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);p.desktop(12208,True);c.shot(g,tag+'-installed-apps');p.desktop(12200,True);before=f.stats(g)[0];p.desktop(12002,True);c.shot(g,tag+'-remove-confirmation');task(g,p,12003);after=f.stats(g)[0];state=snapshot(g);assert state['state']==2 and state['status']==0;assert after-before in (0,4);assert not any(path==root or path.startswith(root+'/') for path in f.entries(g));assert download not in f.entries(g)
    if options.french:
     assert'M147_ORIGINAL_DEFERRED_BODY DeleteNativeLangAction result=0 continued=0'in state['output'];saved=[path for path in f.entries(g) if '/Recovered applications/' in path and path.endswith('-nativeLang.xml')];assert len(saved)==1 and document(saved[0])==b'Modified language file must survive removal';report['preserved_generated_file']=dict(path=saved[0],sha256=hashlib.sha256(document(saved[0])).hexdigest())
    assert document('/Users/Owner/Documents/Keep personal.txt')==b'Independent personal document';report['tasks'].append(dict(operation='remove without original download after independent restart',retained_managed_pages=0,first_activation_pages=after-before,**state));c.shot(g,tag+'-removed');(out/'remove-serial.log').write_bytes(g.log().encode())
   report['passed']=True
  except Exception:
   report['error']=ui.q.clean(traceback.format_exc())
   if'g'in locals():(out/'serial-failed.log').write_bytes(g.log().encode())
   raise
  finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
 finally:sys.meta_path.remove(loader)
if __name__=='__main__':main()
