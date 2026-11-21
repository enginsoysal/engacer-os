"""Build Engacer's own lazy native Win64 MSI service; never execute it on host."""
import hashlib
import json
import re
from pathlib import Path
from m1 import ROOT,command,pinned_tools

# Stable Windows MSI ordinals for implemented exports only. Missing services
# stay absent; never map an unimplemented ordinal to a success stub.
ORDINALS147={8:'MsiCloseHandle',17:'MsiCreateRecord',47:'MsiEvaluateConditionW',49:'MsiGetActiveDatabase',64:'MsiGetMode',73:'MsiGetPropertyA',74:'MsiGetPropertyW',80:'MsiGetTargetPathW',103:'MsiProcessMessage',116:'MsiRecordGetInteger',118:'MsiRecordGetStringW',119:'MsiRecordIsNull',121:'MsiRecordSetInteger',124:'MsiRecordSetStringA',125:'MsiRecordSetStringW',143:'MsiSetMode',145:'MsiSetPropertyW',171:'MsiFormatRecordW'}

def build(work,tools=None):
    tools=tools or pinned_tools();out=Path(work)/'msi147';out.mkdir(parents=True,exist_ok=True)
    definition=out/'kernel32.def';definition.write_bytes(b'LIBRARY kernel32.dll\nEXPORTS\nGetProcessHeap\nHeapAlloc\nHeapFree\nHeapSize\nExitProcess\nInitializeCriticalSection\nEnterCriticalSection\nLeaveCriticalSection\nDeleteCriticalSection\nLoadLibraryW\nGetProcAddress\nFreeLibrary\nCreateThread\nWaitForSingleObject\nGetExitCodeThread\nCloseHandle\nGetLastError\n')
    command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/'kernel32.lib')])
    sources=['user/windows8/msi-native147.c','user/windows8/msi-service147.c','user/windows8/msi-api147.c','user/windows8/msi-custom147.c','user/windows8/msi-journal147.c','user/windows8/msi-files147.c','user/windows8/msi-registry147.c','user/windows8/msi-shortcuts147.c','user/windows8/msi_db.c','user/windows8/msi-plan147.c','user/windows8/msi-cost147.c','user/windows8/cab147.c','runtime/sha256.c','third_party/libmspack/lzxd.c'];objects=[]
    flags=['--target=x86_64-pc-windows-msvc','-O2','-std=c17','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-DMSPACK_NO_DEFAULT_SYSTEM','-DSIZEOF_OFF_T=8','-DDEBUG=0','-I',ROOT/'include','-I',ROOT/'third_party/libmspack-port','-I',ROOT/'third_party/libmspack']
    for source in sources:
        obj=out/(Path(source).stem+'.obj');command([tools['clang'],*flags,'-c',ROOT/source,'-o',obj]);objects.append(obj)
    # Give every other own export an explicit private ordinal. Automatic linker
    # numbering could otherwise alias a missing Windows ordinal to a wrong API.
    public=[]
    for source in ['user/windows8/msi-api147.c','user/windows8/msi-service147.c']:
        public+=re.findall(r'(?m)^(?:MSI_EXPORT147|__declspec\(dllexport\))\s+(?:unsigned|int|int32_t)\s+(\w+)\s*\(', (ROOT/source).read_text())
    known=set(ORDINALS147.values());private={0x7000+i:name for i,name in enumerate(sorted(set(public)-known))};assigned={**ORDINALS147,**private}
    exports=out/'msi.def';exports.write_bytes(('LIBRARY msi.dll\nEXPORTS\n'+'\n'.join(name+' @'+str(ordinal)for ordinal,name in sorted(assigned.items()))+'\n').encode())
    dll=out/'msi.dll';command([tools['lld-link'],'/def:'+str(exports),'/dll','/entry:EngacerMsiDllEntry147','/nodefaultlib','/timestamp:0','/dynamicbase','/fixed:no','/out:'+str(dll),'/implib:'+str(out/'msi.lib'),*objects,out/'kernel32.lib'])
    entry=out/'msiexec147.obj';command([tools['clang'],*flags,'-c',ROOT/'user/windows8/msiexec147.c','-o',entry]);exe=out/'msiexec.exe';command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(exe),entry,out/'msi.lib',out/'kernel32.lib'])
    inputs=sources+['user/windows8/msiexec147.c','user/windows8/msi-plan147.h','user/windows8/msi-properties147.h','user/windows8/msi-condition147.h','user/windows8/cab147.h','user/windows8/msi_db.h','user/windows8/msi-record147.h','user/windows8/msi-text147.h','user/windows8/msi-custom147.h','user/windows8/msi-journal147.h','user/windows8/msi-files147.h','user/windows8/msi-registry147.h','user/windows8/msi-shortcuts147.h','user/windows8/msi-link147.h','include/engine/wintxn147.h','tools/build/msi147.py','include/engine/winproduct147.h'];report=dict(scope='Engacer-authored native service build; execution/installation qualification is separate',sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in inputs},artifacts={p.name:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())for p in [exe,dll]});(out/'build-inputs.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());return {'msi':dll,'msiexec':exe}

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True);args=parser.parse_args();build(args.work)
