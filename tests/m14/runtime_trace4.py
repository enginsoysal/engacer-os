"""Fast diagnostic: immutable owned kernel plus an explicitly identified new runtime.
These mixed development observations never qualify a stage or public ISO.
"""
import argparse,hashlib,json,os,struct,sys,time,traceback,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];os.environ['ENGACER12_IMAGE']='EngacerOS-M14STAGE4'
sys.path[:0]=[str(ROOT/'tests/m12'),str(ROOT/'tests/m13'),str(ROOT/'tools/build')]
import taskbar_observe as t
ui=t.ui;c=t.c;f=t.f
from fixture1 import library,StoppedDisk
from access_fixtures16 import clone
from m1 import pinned_tools
from m8 import runtime
from apps_native4 import task
import capture14
capture14.bind(ui)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--fixture',choices=['original','heap','controls','resources','com','menu'],default='original');parser.add_argument('--runtime');args=parser.parse_args()
 out=ROOT/'build/m14-native/stage4/runtime-traces'/uuid.uuid4().hex;out.mkdir(parents=True);c.OUT=out
 meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage4/apps/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id']
 # Reject a kernel/IPC edit under frozen maps. User-runtime-only tracing is separate.
 for path,want in meta['source_sha256'].items():
  if path.startswith(('kernel/','include/','boot/')):assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==want,('Rebuild the kernel before tracing this ABI change',path)
 if args.runtime:
  rt=Path(args.runtime).resolve();assert rt.is_relative_to((ROOT/'build/m14-native').resolve())and rt.is_file()
 else:
  work=out/'runtime';work.mkdir();common=['-std=c17','-O2','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-red-zone','-mgeneral-regs-only','-Wall','-Wextra','-Werror','-DENGINE_M10','-DENGINE_M14','-I',ROOT/'include'];runtime(work,pinned_tools(),common);rt=work/'WINDOWS8.ELF'
 report=dict(scope='Mixed kernel/user-runtime diagnostic only; NOT stage/ISO/original GUI qualification',kernel_build_id=meta['build_id'],runtime_sha256=hashlib.sha256(rt.read_bytes()).hexdigest(),runtime_path='build/m14-native/'+rt.resolve().relative_to((ROOT/'build/m14-native').resolve()).as_posix(),fixture=args.fixture,passed=False,original_gui_qualified=False,runtime_sources={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted((ROOT/'user/windows8').glob('*'))if p.is_file()})
 if args.runtime:
  prior=json.loads((rt.parent.parent/'results.json').read_text(encoding='utf-8'));assert prior['runtime_sha256']==report['runtime_sha256'];report['runtime_sources']=prior['runtime_sources']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m144-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m144-runtime-trace');report['clone']=cloned;mounted=StoppedDisk(disk,library());product='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}'
 try:
  mounted.put('/System/Windows/runtime8.elf',rt.read_bytes())
  if args.fixture!='original':
   module=__import__({'heap':'heap144_build','controls':'controls144_build','resources':'resource144_build','com':'com144_build','menu':'menu144_build'}[args.fixture]);fixture=module.build();filename={'heap':'heap.exe','controls':'controls.exe','resources':'resource.exe','com':'com.exe','menu':'menu.exe'}[args.fixture];mounted.put(product+'/7z.exe',(fixture/filename).read_bytes());report['fixture_sha256']=hashlib.sha256((fixture/filename).read_bytes()).hexdigest()
   if args.fixture=='menu':mounted.put(product+'/menus144.dll',(fixture/'menus144.dll').read_bytes())
   if args.fixture=='resources':mounted.put(product+'/resources144.dll',(fixture/'resources144.dll').read_bytes())
 finally:mounted.close()
 try:
  boot=ui.guest(work/'trace',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);before=f.stats(g)[0]
   if args.fixture=='original':
    original=ui.s.s.document(disk,product+'/7zFM.exe',8*1024**2);assert hashlib.sha256(original).hexdigest()=='a12710799d5cb9b3076b86dd0f92d4a503b7062bc3efac62b7f4cb8a74e05931'
    at=len(g.log());p.desktop(12100,True,settle=False);g.wait('M8_CPL3_CREATED',at);deadline=time.monotonic()+20
    while time.monotonic()<deadline:
     raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384)
     if struct.unpack_from('<I',raw)[0]!=1:break
     if len(t.records(g))>1 and g.qmp('human-monitor-command',{'command-line':'info registers -a'}).count('HLT=1')==2:break
     time.sleep(.05)
    raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384);state,command,status=struct.unpack_from('<3I',raw);report.update(state=state,status=status,message=raw[304:496].split(b'\0')[0].decode(errors='replace'),output=raw[496:].split(b'\0')[0].decode(errors='replace'),native_windows=t.records(g));c.shot(g,'original-startup-observation')
   else:
    value=task(g,p,12005);marker={'heap':'M144_HEAP_OVERHEAD_PASS','controls':'M144_CONTROLS_GEOMETRY_PASS','resources':'M144_RESOURCE_IMAGE_HEAP_PASS','com':'M144_COM_LIFETIME_PASS','menu':'M144_MENU_STATE_PASS'}[args.fixture];assert marker in value,value;report.update(output=value,retained_pages=f.stats(g)[0]-before,passed=True)
   (out/'serial.log').write_bytes(g.log().encode())
 except Exception:report['observer_error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps({k:v for k,v in report.items()if k not in ('runtime_sources','clone')},indent=2),flush=True)
if __name__=='__main__':main()
