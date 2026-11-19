"""Build Windows process lifetime probes; no host execution."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command
def build():
 work=ROOT/'build/m14-native/stage2/exception-fixtures';work.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
 exports=['CreateThread','WaitForMultipleObjects','CloseHandle','AddVectoredExceptionHandler','AddVectoredContinueHandler','RemoveVectoredExceptionHandler','RemoveVectoredContinueHandler','GetStdHandle','WriteFile','ExitProcess']
 (work/'kernel32.def').write_bytes(('LIBRARY kernel32.dll\nEXPORTS\n'+'\n'.join(exports)+'\n').encode('utf-8'))
 command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(work/'kernel32.def'),'/out:'+str(work/'kernel32.lib')])
 for mode in ['exceptions','invalid-mxcsr','invalid-rip','nested','overflow']:
  obj=work/(mode+'.obj');command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe',*({'invalid-mxcsr':['-DINVALID_MXCSR142'],'invalid-rip':['-DINVALID_RIP142'],'overflow':['-DOVERFLOW142']}.get(mode,[])),'-c',ROOT/('tests/m14/exceptions_nested2.c' if mode in ['nested','overflow'] else 'tests/m14/exceptions2.c'),'-o',obj])
  command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(work/(mode+'.exe')),obj,work/'kernel32.lib'])
 return work
if __name__=='__main__':build();print('Exception fixtures built; no host execution')
