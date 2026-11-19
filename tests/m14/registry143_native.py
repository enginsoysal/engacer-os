"""Actual Windows registry calls on a stopped owned clone, including independent restart."""
import hashlib,json,os,struct,sys,time,traceback
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
 tools=pinned_tools()
 exports={'kernel32':['CreateProcessW','GetExitCodeProcess','WaitForSingleObject','CloseHandle','GetStdHandle','WriteFile','GetCommandLineW','ExitProcess','GetLastError','SetLastError'],
          'advapi32':['RegCreateKeyExW','RegOpenKeyExW','RegQueryValueExW','RegSetValueExW','RegCloseKey','RegDeleteValueW','RegDeleteKeyW','RegEnumValueW','RegEnumKeyExW','RegFlushKey']}
 libraries=[]
 for name,symbols in exports.items():
  definition=out/(name+'.def');definition.write_text('LIBRARY '+name+'.dll\nEXPORTS\n'+'\n'.join(symbols)+'\n',encoding='utf-8')
  lib=out/(name+'.lib');command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(lib)]);libraries.append(lib)
 for name in ['probe','read']:
  command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe',*(['-DREAD143']if name=='read'else[]),'-c',ROOT/'tests/m14/registry143_native.c','-o',out/(name+'.obj')])
  command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(out/(name+'.exe')),out/(name+'.obj'),*libraries])

def main():
 out=ROOT/'build/m14-native/stage3/registry-native';out.mkdir(parents=True,exist_ok=True);build(out)
 meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage3/apps/results.json').read_text(encoding='utf-8'))
 assert base['passed'] and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m143-path-apps'/base['owned_fixture']/'owned.img'
 work,disk,cloned=clone(ui,source,'m143-registry');product='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}'
 report=dict(passed=False,stage='M14.3 development',scope='Synthetic native persistent user registry, rights, sizes, enumeration and private parent/child grants',build_id=meta['build_id'],clone=cloned,owned_fixture=work.name,fixture_sha256={name:hashlib.sha256((out/name).read_bytes()).hexdigest()for name in ['probe.exe','read.exe']})
 mounted=StoppedDisk(disk,library())
 try:
  for name in ['7z.exe','child.exe']:mounted.put(product+'/'+name,(out/'probe.exe').read_bytes())
 finally:mounted.close()
 try:
  boot=ui.guest(work/'probe',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19)
   warm=task(g,p,12005);assert 'M143_NATIVE_REGISTRY_PASS' in warm,warm;report['warm_output']=warm
   before=f.stats(g)[0];samples=[]
   for turn in range(20):
    started=time.monotonic();output=task(g,p,12005);assert 'M143_NATIVE_REGISTRY_PASS' in output,output;retained=f.stats(g)[0]-before;assert not retained,(turn,retained)
    peak,quanta=struct.unpack_from('<QQ',ui.memory(g,ui.symbol('info8',installed=True)[0],40),24);samples.append(dict(turn=turn+1,retained_pages=retained,peak_group_owned_pages=peak,worker_quanta=quanta,observer_wall_seconds=time.monotonic()-started))
   report['samples']=samples;(out/'serial.log').write_text(g.log(),encoding='utf-8')
  mounted=StoppedDisk(disk,library())
  try:mounted.put(product+'/7z.exe',(out/'read.exe').read_bytes())
  finally:mounted.close()
  boot=ui.guest(work/'independent',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);output=task(g,p,12005)
   assert 'M143_REGISTRY_RESTART_PASS' in output,output;report['independent_start_output']=output;(out/'restart.log').write_text(g.log(),encoding='utf-8')
  report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:
  (out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
