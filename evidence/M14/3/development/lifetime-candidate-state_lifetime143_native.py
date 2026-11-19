"""Check live file/lock/key ownership on native exit, cancellation and faults."""
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
 tools=pinned_tools();exports=['CreateFileW','WriteFile','ReadFile','LockFileEx','GetStdHandle','Sleep','ExitProcess']
 definition=out/'kernel32.def';definition.write_bytes(('LIBRARY kernel32.dll\nEXPORTS\n'+'\n'.join(exports)+'\n').encode('utf-8'))
 command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/'kernel32.lib')])
 for provider in ('advapi32',):
  definition=out/(provider+'.def');definition.write_bytes(('LIBRARY '+provider+'.dll\nEXPORTS\nRegCreateKeyExW\nRegSetValueExW\nRegOpenKeyExW\nRegQueryValueExW\n').encode('utf-8'))
  command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/(provider+'.lib'))])
 for mode in range(4):
  name=str(mode)
  command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-DMODE143='+name,'-c',ROOT/'tests/m14/state_lifetime143.c','-o',out/(name+'.obj')])
  command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(out/(name+'.exe')),out/(name+'.obj'),out/'kernel32.lib',out/'advapi32.lib'])

def main():
 out=ROOT/'build/m14-native/stage3/state-lifetime';out.mkdir(parents=True,exist_ok=True);build(out)
 meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage3/apps/results.json').read_text(encoding='utf-8'));assert base['passed'] and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m143-path-apps'/base['owned_fixture']/'owned.img';product='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}'
 report=dict(passed=False,stage='M14.3 development',build_id=meta['build_id'],scope='Synthetic real CPL3 file/lock/registry ownership, acknowledged settings versus unflushed file data; no original GUI claim',cases=[])
 try:
  for mode,name in enumerate(('normal-exit','cancel','unhandled-fault')):
   work,disk,cloned=clone(ui,source,'m143-state-'+name);mounted=StoppedDisk(disk,library())
   try:
    mounted.put(product+'/7z.exe',(out/(str(mode)+'.exe')).read_bytes());mounted.put('/Users/Owner/Documents/m143-lifecycle.bin',b'original\n')
   finally:mounted.close()
   case=dict(name=name,clone=cloned,fixture_sha256=hashlib.sha256((out/(str(mode)+'.exe')).read_bytes()).hexdigest(),samples=[])
   boot=ui.guest(work/'probe',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
   with boot as g:
    p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);before=f.stats(g)[0]
    for turn in range(21):
     at=len(g.log());p.desktop(12005,True,settle=False);g.wait('M8_CPL3_CREATED',at)
     deadline=time.monotonic()+30
     while time.monotonic()<deadline:
      raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384);state=struct.unpack_from('<I',raw)[0]
      if mode==1 and b'M143_STATE_HELD_READY' in raw[496:]:break
      if mode!=1 and state!=1:break
      time.sleep(.03)
     else:raise TimeoutError('Native state fixture did not reach its terminal or blocked state')
     if mode==1:
      p.drain();assert ui.integer(g,'file_resident143',True)>0 and ui.integer(g,'registry_resident143',True)>0
      halted=g.qmp('human-monitor-command',{'command-line':'info registers -a'}).count('HLT=1');assert halted==2,halted
      p.desktop(12008,True)
     else:halted=None
     g.wait('M8_JOB_DONE' if mode==0 else 'M8_JOB_FAILED',at)
     p.drain();raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384);state,_,status=struct.unpack_from('<3I',raw)
     if mode==0:assert state==2 and status==0 and b'M143_STATE_EXIT_PASS' in raw[496:],(state,status,raw[496:].split(b'\0')[0])
     elif mode==1:assert state==3 and b'cancel' in raw[304:496].lower(),(state,status)
     else:assert state==3 and status==0xc0000005,(state,status,raw[496:].split(b'\0')[0])
     assert b'M143_STATE_HELD_READY' in raw[496:]
     resident={kind:ui.integer(g,kind+'_resident143',True)for kind in ('file','registry')};assert resident==dict(file=0,registry=0),resident
     assert '/Users/Owner/Documents/m143-lifecycle-temp.bin' not in f.entries(g)
     retained=f.stats(g)[0]-before;assert retained==(4 if turn==0 else 0),(name,turn,retained)
     if turn==0:before=f.stats(g)[0]
     case['samples'].append(dict(turn=turn+1,retained_pages=retained,shared_resident_pages=resident,halted_cpus_while_blocked=halted,status=status))
    t.close_all(g,p);t.launch(g,p,'clock',8);t.close_all(g,p);case['desktop_responsive']=True;(out/(name+'.log')).write_bytes(g.log().encode('utf-8'))
   expected=b'changed \n' if mode==0 else b'original\n';actual=ui.s.s.document(disk,'/Users/Owner/Documents/m143-lifecycle.bin',4096);assert actual==expected,(name,actual);case['saved_bytes_sha256']=hashlib.sha256(actual).hexdigest();case['unflushed_data_committed']=mode==0
   mounted=StoppedDisk(disk,library())
   try:mounted.put(product+'/7z.exe',(out/'3.exe').read_bytes())
   finally:mounted.close()
   boot=ui.guest(work/'independent',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
   with boot as g:
    p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19);output=task(g,p,12005);assert 'M143_STATE_RESTART_REGISTRY_PASS' in output,output;case['acknowledged_registry_survives_restart']=True
   assert ui.s.s.document(disk,'/Users/Owner/Documents/m143-lifecycle.bin',4096)==expected;report['cases'].append(case)
  report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode('utf-8'));print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
