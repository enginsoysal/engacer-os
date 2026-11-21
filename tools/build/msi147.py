"""Build Engacer's own lazy native Win64 MSI service; never execute it on host."""
import hashlib
import json
from pathlib import Path
from m1 import ROOT,command,pinned_tools

def build(work,tools=None):
    tools=tools or pinned_tools();out=Path(work)/'msi147';out.mkdir(parents=True,exist_ok=True)
    definition=out/'kernel32.def';definition.write_bytes(b'LIBRARY kernel32.dll\nEXPORTS\nGetProcessHeap\nHeapAlloc\nHeapFree\nHeapSize\nExitProcess\n')
    command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/'kernel32.lib')])
    sources=['user/windows8/msi-native147.c','user/windows8/msi-service147.c','user/windows8/msi_db.c','user/windows8/msi-plan147.c','user/windows8/msi-cost147.c','user/windows8/cab147.c','runtime/sha256.c','third_party/libmspack/lzxd.c'];objects=[]
    flags=['--target=x86_64-pc-windows-msvc','-O2','-std=c17','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-DMSPACK_NO_DEFAULT_SYSTEM','-DSIZEOF_OFF_T=8','-DDEBUG=0','-I',ROOT/'include','-I',ROOT/'third_party/libmspack-port','-I',ROOT/'third_party/libmspack']
    for source in sources:
        obj=out/(Path(source).stem+'.obj');command([tools['clang'],*flags,'-c',ROOT/source,'-o',obj]);objects.append(obj)
    dll=out/'msi.dll';command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/dynamicbase','/fixed:no','/out:'+str(dll),'/implib:'+str(out/'msi.lib'),*objects,out/'kernel32.lib'])
    entry=out/'msiexec147.obj';command([tools['clang'],*flags,'-c',ROOT/'user/windows8/msiexec147.c','-o',entry]);exe=out/'msiexec.exe';command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(exe),entry,out/'msi.lib',out/'kernel32.lib'])
    inputs=sources+['user/windows8/msiexec147.c','user/windows8/msi-plan147.h','user/windows8/msi-properties147.h','user/windows8/msi-condition147.h','user/windows8/cab147.h','user/windows8/msi_db.h','tools/build/msi147.py'];report=dict(scope='Engacer-authored native service build; execution/installation qualification is separate',sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in inputs},artifacts={p.name:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())for p in [exe,dll]});(out/'build-inputs.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());return {'msi':dll,'msiexec':exe}

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True);args=parser.parse_args();build(args.work)
