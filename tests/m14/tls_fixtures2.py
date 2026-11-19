"""Build real PE static TLS directory and compiler TLS instructions."""
import struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command
def build():
 work=ROOT/'build/m14-native/stage2/tls-fixtures';work.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
 names=['ExitThread','CreateThread','ResumeThread','WaitForMultipleObjects','Sleep','CloseHandle','ExitProcess','GetStdHandle','WriteFile','LoadLibraryA','GetProcAddress','FreeLibrary']
 (work/'kernel32.def').write_bytes(('LIBRARY kernel32.dll\nEXPORTS\n'+'\n'.join(names)+'\n').encode('utf-8'))
 command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(work/'kernel32.def'),'/out:'+str(work/'kernel32.lib')])
 flags=['--target=x86_64-pc-windows-msvc','-O2','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c']
 for mode in ['exe','dll']:
  command([tools['clang'],*flags,*(['-DTLS_DLL142'] if mode=='dll' else []),ROOT/'tests/m14/tls2.c','-o',work/(mode+'.obj')])
 for name in ['tlsaddon','tlsdynamic']:
  command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/dynamicbase','/fixed:no','/include:_tls_used','/out:'+str(work/(name+'.dll')),work/'dll.obj',work/'kernel32.lib'])
 command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/include:_tls_used','/out:'+str(work/'tls.exe'),work/'exe.obj',work/'kernel32.lib',work/'tlsaddon.lib'])
 command([tools['clang'],*flags,'-DTLS_LAST142',ROOT/'tests/m14/tls2.c','-o',work/'last.obj'])
 command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/include:_tls_used','/out:'+str(work/'last.exe'),work/'last.obj',work/'kernel32.lib',work/'tlsaddon.lib'])
 for name in ['tls.exe','last.exe','tlsaddon.dll','tlsdynamic.dll']:
  pe=(work/name).read_bytes();optional=struct.unpack_from('<I',pe,60)[0]+24;rva,size=struct.unpack_from('<II',pe,optional+184);assert rva and size>=40,(name,rva,size)
 return work
if __name__=='__main__':build();print('Compiler-generated PE static TLS fixtures built; no host execution')
