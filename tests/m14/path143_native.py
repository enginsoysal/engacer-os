"""Native syscall path regression, distinct from complete M14.3 qualification."""
import hashlib,json,os,sys,traceback
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

def main():
 out=ROOT/'build/m14-native/stage3/path-native';out.mkdir(parents=True,exist_ok=True)
 meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'))
 base=json.loads((ROOT/'build/m14-native/stage3/apps/results.json').read_text(encoding='utf-8'))
 assert base['passed'] and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m143-path-apps'/base['owned_fixture']/'owned.img'
 work,disk,cloned=clone(ui,source,'m143-path-boundary')
 report=dict(passed=False,stage='M14.3 development',scope='Synthetic native path syscall and resource regression only',build_id=meta['build_id'],clone=cloned,owned_fixture=work.name)
 tools=pinned_tools();symbols=['GetFullPathNameW','GetFullPathNameA','GetCurrentDirectoryW','GetLastError','GetStdHandle','WriteFile','ExitProcess']
 definition=out/'kernel32.def';definition.write_text('LIBRARY kernel32.dll\nEXPORTS\n'+'\n'.join(symbols)+'\n',encoding='utf-8')
 command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/'kernel32.lib')])
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',ROOT/'tests/m14/path143_native.c','-o',out/'path.obj'])
 command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(out/'path.exe'),out/'path.obj',out/'kernel32.lib'])
 report['fixture_sha256']=hashlib.sha256((out/'path.exe').read_bytes()).hexdigest()
 mounted=StoppedDisk(disk,library())
 try:mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7z.exe',(out/'path.exe').read_bytes())
 finally:mounted.close()
 try:
  boot=ui.guest(work/'probe',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19)
   warm=task(g,p,12005);assert 'M143_NATIVE_PATH_BOUNDARY_PASS' in warm,warm
   report['warm_output']=warm;before=f.stats(g)[0];samples=[]
   for turn in range(20):
    output=task(g,p,12005);assert 'M143_NATIVE_PATH_BOUNDARY_PASS' in output,output
    retained=f.stats(g)[0]-before;assert retained==0,retained
    samples.append(dict(turn=turn+1,retained_pages=retained))
   report['samples']=samples;(out/'serial.log').write_text(g.log(),encoding='utf-8')
  report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:
  (out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
