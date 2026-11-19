"""Build Windows process lifetime probes; no host execution."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command
def build():
 work=ROOT/'build/m14-native/stage2/process-fixtures';work.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
 exports=['CreateThread','ExitThread','DeleteFileW','GetLastError','GetTickCount','CreateProcessW','GetCurrentProcessId','GetCurrentProcess','GetProcessId','GetThreadId','GetExitCodeProcess','GetExitCodeThread','WaitForSingleObject','WaitForMultipleObjects','ResumeThread','TerminateProcess','CloseHandle','ExitProcess','Sleep','GetStdHandle','WriteFile','CreateFileW','GetCommandLineW','TlsAlloc','TlsSetValue','TlsGetValue']
 (work/'kernel32.def').write_bytes(('LIBRARY kernel32.dll\nEXPORTS\n'+'\n'.join(exports)+'\n').encode('utf-8'))
 command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(work/'kernel32.def'),'/out:'+str(work/'kernel32.lib')])
 for mode in ['parent','survivor']:
  obj=work/(mode+'.obj');command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-I',ROOT/'include',*(['-DPARENT_EXITS142'] if mode=='survivor' else []),'-c',ROOT/'tests/m14/processes2.c','-o',obj])
  command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(work/(mode+'.exe')),obj,work/'kernel32.lib'])
 return work
if __name__=='__main__':build();print('Process fixtures built; no host execution')
