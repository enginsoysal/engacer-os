"""Compile our owned unavailable-import fixture, never execute it on the host."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools

def build():
 out=ROOT/'build/m14-native/stage5/guard-fixture';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
 for provider,names in [('kernel32',['GetModuleHandleW','GetProcAddress','GetLastError','GetStdHandle','WriteFile','ExitProcess']),('shlwapi',['PathIsRelativeW'])]:
  definition=out/(provider+'.def');definition.write_bytes(('LIBRARY '+provider+'.dll\nEXPORTS\n'+'\n'.join(names)+'\n').encode());command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/(provider+'.lib'))])
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',ROOT/'tests/m14/guard145_native.c','-o',out/'guard.obj'])
 command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(out/'guard.exe'),out/'guard.obj',out/'kernel32.lib',out/'shlwapi.lib']);return out/'guard.exe'

if __name__=='__main__':build()
