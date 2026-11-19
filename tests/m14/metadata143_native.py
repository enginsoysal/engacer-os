"""File-owned metadata across private processes, rename, uninstall and restart."""
import hashlib,json,os,re,struct,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
os.environ['ENGACER12_IMAGE']='EngacerOS-M14STAGE3'
sys.path[:0]=[str(ROOT/'tests/m12'),str(ROOT/'tests/m13'),str(ROOT/'tools/build')]
import taskbar_observe as t
from apps_native3 import task
from access_fixtures16 import clone
from fixture1 import library,StoppedDisk
from m1 import pinned_tools,command
ui=t.ui;c=t.c;f=t.f

def build(out):
 tools=pinned_tools();exports=['CreateFileW','WriteFile','CloseHandle','SetFileTime','GetFileInformationByHandle','SetFileAttributesW','GetFileAttributesW','DeleteFileW','MoveFileExW','GetLastError','CreateProcessW','GetExitCodeProcess','WaitForSingleObject','GetCommandLineW','GetStdHandle','ExitProcess']
 definition=out/'kernel32.def';definition.write_text('LIBRARY kernel32.dll\nEXPORTS\n'+'\n'.join(exports)+'\n',encoding='utf-8')
 command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/'kernel32.lib')])
 for name in ['probe','read']:
  command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe',*(['-DREAD143']if name=='read'else[]),'-c',ROOT/'tests/m14/metadata143_native.c','-o',out/(name+'.obj')])
  command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(out/(name+'.exe')),out/(name+'.obj'),out/'kernel32.lib'])

def main():
 out=ROOT/'build/m14-native/stage3/file-metadata-native';out.mkdir(parents=True,exist_ok=True);build(out)
 meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage3/apps/results.json').read_text(encoding='utf-8'));assert base['passed'] and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m143-path-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m143-file-metadata')
 product='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}';original=ui.s.s.document(disk,product+'/7z.exe',32*1024**2)
 report=dict(passed=False,stage='M14.3 development',scope='Synthetic file-owned timestamps/attributes and identity, including independent restart after original application removal/reinstallation',build_id=meta['build_id'],clone=cloned,owned_fixture=work.name,fixture_sha256={name:hashlib.sha256((out/name).read_bytes()).hexdigest()for name in ['probe.exe','read.exe']})
 mounted=StoppedDisk(disk,library())
 try:
  mounted.put(product+'/7z.exe',(out/'probe.exe').read_bytes());mounted.put('/Users/Owner/Documents/m143-metadata-child.exe',(out/'probe.exe').read_bytes())
 finally:mounted.close()
 try:
  boot=ui.guest(work/'probe',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);warm=task(g,p,12005);assert 'M143_NATIVE_FILE_METADATA_PASS' in warm,warm;report['warm_output']=warm;identities=re.findall(r'M143_FILE_ID_([0-9a-f]{16})',warm);assert len(identities)==3 and len(set(identities))==1 and int(identities[0],16)>0,identities;report['initial_file_identity']=identities[0];report['live_file_identity']=identities[0]
   before=f.stats(g)[0];samples=[]
   for turn in range(20):
    started=time.monotonic();output=task(g,p,12005);assert 'M143_NATIVE_FILE_METADATA_PASS' in output,output;retained=f.stats(g)[0]-before;assert not retained,(turn,retained)
    live_identities=re.findall(r'M143_FILE_ID_([0-9a-f]{16})',output);assert len(live_identities)==3 and len(set(live_identities))==1,live_identities;report['live_file_identity']=live_identities[0]
    peak,quanta=struct.unpack_from('<QQ',ui.memory(g,ui.symbol('info8',installed=True)[0],40),24);samples.append(dict(turn=turn+1,retained_pages=retained,peak_group_owned_pages=peak,worker_quanta=quanta,observer_wall_seconds=time.monotonic()-started))
   report['samples']=samples;(out/'serial.log').write_text(g.log(),encoding='utf-8')
  saved=ui.s.s.document(disk,'/Users/Owner/Documents/m143-metadata-renamed.bin',4096);assert saved==b'metadata survives\n';report['document_sha256']=hashlib.sha256(saved).hexdigest()
  mounted=StoppedDisk(disk,library())
  try:mounted.put(product+'/7z.exe',original)
  finally:mounted.close()
  boot=ui.guest(work/'remove-reinstall',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);p.desktop(12002,True);task(g,p,12003);assert product+'/7z.exe' not in f.entries(g)
   p.desktop(12001,True);task(g,p,12003);output=task(g,p,12005);assert '7-Zip' in output,output;report['original_removal_and_reinstallation']=True
  mounted=StoppedDisk(disk,library())
  try:mounted.put(product+'/7z.exe',(out/'read.exe').read_bytes())
  finally:mounted.close()
  boot=ui.guest(work/'independent',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);output=task(g,p,12005);assert 'M143_METADATA_RESTART_AND_REMOVE_PASS' in output,output;report['independent_start_output']=output;restart_identities=re.findall(r'M143_FILE_ID_([0-9a-f]{16})',output);assert restart_identities==[report['live_file_identity']],restart_identities;report['same_identity_after_restart_and_removal']=True
  assert ui.s.s.document(disk,'/Users/Owner/Documents/m143-metadata-renamed.bin',4096)==saved;report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:
  (out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
