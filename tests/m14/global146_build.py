"""Build an owned Windows x64 ABI fixture; never execute it on the host."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools

def build():
 out=ROOT/'build/m14-native/stage6/global-fixture';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
 names=['GlobalAlloc','GlobalFree','GlobalLock','GlobalUnlock','GlobalSize','GlobalFlags','GlobalHandle','LocalAlloc','LocalFree','GetLastError','SetLastError','CreateThread','WaitForMultipleObjects','GetExitCodeThread','CloseHandle','GetStdHandle','WriteFile','ExitProcess']
 definition=out/'kernel32.def';definition.write_bytes(('LIBRARY kernel32.dll\nEXPORTS\n'+'\n'.join(names)+'\n').encode())
 command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/'kernel32.lib')])
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',ROOT/'tests/m14/global146_native.c','-o',out/'global.obj'])
 command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(out/'global.exe'),out/'global.obj',out/'kernel32.lib'])
 return out/'global.exe'

if __name__=='__main__':build()
