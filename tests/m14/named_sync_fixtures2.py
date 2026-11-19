"""Build native Windows cross-process synchronization probes; no host execution."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command
def build():
 work=ROOT/'build/m14-native/stage2/named-sync-fixtures';work.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
 exports=['CreateProcessW','CreateEventW','OpenEventW','CreateSemaphoreW','OpenSemaphoreW','CreateWaitableTimerW','OpenWaitableTimerW','SetWaitableTimer','SetEvent','ResetEvent','ReleaseSemaphore','WaitForSingleObject','WaitForMultipleObjects','GetExitCodeProcess','CloseHandle','GetLastError','GetCommandLineW','ExitProcess','Sleep','GetStdHandle','WriteFile']
 (work/'kernel32.def').write_bytes(('LIBRARY kernel32.dll\nEXPORTS\n'+'\n'.join(exports)+'\n').encode());command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(work/'kernel32.def'),'/out:'+str(work/'kernel32.lib')])
 for mode,flags in [('named',[]),('survivor',['-DNAMED_PARENT_EXITS142']),('cancel',['-DNAMED_CANCEL142'])]:
  obj=work/(mode+'.obj');command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-funwind-tables','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe',*flags,'-c',ROOT/'tests/m14/named_sync2.c','-o',obj]);command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(work/(mode+'.exe')),obj,work/'kernel32.lib'])
 return work
if __name__=='__main__':build();print('Named-object Windows fixtures built; no host execution')
