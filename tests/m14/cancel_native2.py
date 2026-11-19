"""Cancel real all-sleeping Win64 threads using ordinary native UI input."""
import hashlib,json,os,struct,sys,time,traceback
from pathlib import Path
from thread_native2 import ui,c,f,t,task
from access_fixtures16 import clone
from fixture1 import library,StoppedDisk
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/build'))
from m1 import pinned_tools,command
ROOT=Path(__file__).resolve().parents[2]
def fixture():
 work=ROOT/'build/m14-native/stage2/cancel-fixtures';work.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
 (work/'kernel32.def').write_bytes(b'LIBRARY kernel32.dll\nEXPORTS\nCreateThread\nSleep\nExitProcess\n')
 command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(work/'kernel32.def'),'/out:'+str(work/'kernel32.lib')])
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',ROOT/'tests/m14/cancel2.c','-o',work/'cancel.obj'])
 command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(work/'cancel.exe'),work/'cancel.obj',work/'kernel32.lib'])
 return work/'cancel.exe'
def main():
 out=ROOT/'build/m14-native/stage2/cancel';out.mkdir(parents=True,exist_ok=True)
 meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));baseline=json.loads((ROOT/'build/m14-native/stage2/compact/results.json').read_text(encoding='utf-8'));assert baseline['passed'] and baseline['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage2-compact'/baseline['owned_fixture']/'owned.img';work,disk,_=clone(ui,source,'m142-cancel')
 report=dict(passed=False,build_id=meta['build_id'],synthetic=True,scope='Native cancellation of one Windows process with three secondary threads; not child-process qualification')
 try:
  boot=ui.guest(work/'prepare',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);p.desktop(12001,True);task(g,p,12003)
  binary=fixture();mounted=StoppedDisk(disk,library())
  try:mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7z.exe',binary.read_bytes())
  finally:mounted.close()
  boot=ui.guest(work/'cancel',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);before=f.stats(g)[0];samples=[]
   for n in range(21):
    at=len(g.log());p.desktop(12005,True,settle=False);g.wait('M8_CPL3_CREATED',at);time.sleep(.2);p.drain()
    raw=ui.memory(g,ui.symbol('info8',installed=True)[0],40);assert struct.unpack_from('<I',raw)[0]==1
    halted=g.qmp('human-monitor-command',{'command-line':'info registers -a'}).count('HLT=1');assert halted==2,halted
    p.desktop(12008,True);raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496)
    assert struct.unpack_from('<I',raw)[0]==3 and b'cancel' in raw[304:].lower(),raw[:40].hex()
    retained=f.stats(g)[0]-before;assert retained==(4 if n==0 else 0),(n,retained)
    if not n:before=f.stats(g)[0]
    samples.append(dict(turn=n+1,all_cpus_halted_while_blocked=halted,retained_pages=retained))
   report.update(passed=True,samples=samples,fixture_sha256=hashlib.sha256(binary.read_bytes()).hexdigest());t.close_all(g,p);t.launch(g,p,'clock',8);t.close_all(g,p);(out/'native.log').write_bytes(g.log().encode('utf-8'))
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode('utf-8'));print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
