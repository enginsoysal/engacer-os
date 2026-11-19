"""Build a synthetic x64 threading probe with the pinned toolchain."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command
def build():
 work=ROOT/'build/m14-native/stage2/fixtures';work.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
 exports=['CreateEventW','OpenEventW','SetEvent','CreateSemaphoreW','ReleaseSemaphore','WaitForSingleObject','CreateWaitableTimerW','SetWaitableTimer','CancelWaitableTimer','CreateThread','ResumeThread','ExitProcess','WaitForMultipleObjects','GetExitCodeThread','GetCurrentThreadId','GetLastError','TlsAlloc','TlsSetValue','TlsGetValue','TlsFree','Sleep','CloseHandle','InitializeCriticalSection','EnterCriticalSection','LeaveCriticalSection','GetStdHandle','WriteFile']
 (work/'kernel32.def').write_text('LIBRARY kernel32.dll\nEXPORTS\n'+'\n'.join(exports)+'\n',encoding='utf-8')
 command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(work/'kernel32.def'),'/out:'+str(work/'kernel32.lib')])
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',ROOT/'tests/m14/threads2.c','-o',work/'threads.obj'])
 command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(work/'threads.exe'),work/'threads.obj',work/'kernel32.lib'])
 return work
if __name__=='__main__':build();print('Synthetic fixture built; no host execution')
