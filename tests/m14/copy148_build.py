"""Compile owned software-raise and compiler-generated x64 C exception metadata; never host-execute."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command
def build():
 work=ROOT/'build/m14-native/stage8/copy-fixtures';work.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
 for dll,exports in [('kernel32',['ExitProcess','GetStdHandle','WriteFile','ReadFile','CreateFileW','GetTempPathW','CopyFileW','CloseHandle','GetLastError','DeleteFileW','SetFileAttributesW','GetFileAttributesW','GetFileAttributesExW','SetFileTime','FormatMessageA','LocalFree'])]:
  (work/(dll+'.def')).write_bytes(('LIBRARY '+dll+'.dll\nEXPORTS\n'+'\n'.join(exports)+'\n').encode());command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(work/(dll+'.def')),'/out:'+str(work/(dll+'.lib'))])
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-funwind-tables','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',ROOT/'tests/m14/copy148_native.c','-o',work/'unwind.obj'])
 command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(work/'unwind.exe'),work/'unwind.obj',work/'kernel32.lib'])
 (work/'large-source.bin').write_bytes(bytes((i*37+11)&255 for i in range(256))*(11*1024*1024//256))
 return work
if __name__=='__main__':build();print('C SEH fixture built; runtime qualification remains pending')
