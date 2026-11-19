"""Build explicitly synthetic Windows PE fixtures with the pinned compiler."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command

def build():
    work=ROOT/'build/m14-native/fixtures';work.mkdir(parents=True,exist_ok=True)
    tools=pinned_tools()
    kernel=work/'kernel32.def'
    kernel.write_text('LIBRARY kernel32.dll\nEXPORTS\nGetStdHandle\nWriteFile\nExitProcess\nLoadLibraryA\nGetProcAddress\nFreeLibrary\n')
    command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(kernel),'/out:'+str(work/'kernel32.lib')])
    flags=['--target=x86_64-pc-windows-msvc','-O2','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c']
    for name in ['leaf1','probe1','forward1']:
        command([tools['clang'],*flags,ROOT/f'tests/m14/{name}.c','-o',work/(name+'.obj')])
    for name in ['leaf','dynamic']:
        command([tools['lld-link'],'/dll','/entry:dllentry','/nodefaultlib','/timestamp:0','/dynamicbase','/fixed:no',
                 '/export:value,@7','/out:'+str(work/(name+'.dll')),work/'leaf1.obj',work/'kernel32.lib'])
    forward=work/'forward.def';forward.write_text('LIBRARY forward.dll\nEXPORTS\nforwarded=leaf.value\nforwardedOrdinal=leaf.#7\n')
    command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/def:'+str(forward),
             '/out:'+str(work/'forward.dll'),work/'forward1.obj'])
    command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no',
             '/delayload:dynamic.dll','/out:'+str(work/'probe.exe'),work/'probe1.obj',work/'kernel32.lib',work/'forward.lib',work/'dynamic.lib'])
    import struct
    pe=(work/'probe.exe').read_bytes()
    optional=struct.unpack_from('<I',pe,60)[0]+24
    assert struct.unpack_from('<II',pe,optional+216)[0]!=0,'The fixture must contain a real delay-import directory'
    for mode in (1,2,3):
        obj=work/f'fault{mode}.obj'
        command([tools['clang'],*flags,'-DFAULT141='+str(mode),ROOT/'tests/m14/fault1.c','-o',obj])
        command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no',
                 '/out:'+str(work/f'fault{mode}.exe'),obj,work/'kernel32.lib'])
    return work

if __name__=='__main__':
    folder=build()
    print(json.dumps(dict(files=[p.name for p in folder.glob('*.exe')]+[p.name for p in folder.glob('*.dll')],synthetic=True)))
