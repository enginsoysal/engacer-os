"""Build an owned native streaming probe with independent original-file hashes."""
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command

def build():
    out=ROOT/'build/m14-native/stage7/cab-fixture';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
    report_path=ROOT/'build/m14-native/stage7/cab-host/results.json';report=json.loads(report_path.read_text());assert report['passed'];records=report['originals'];assert [r['files']for r in records]==[106,217]
    headers=[];cab_sizes=[];cab_hashes=[]
    for i,row in enumerate(records):
        raw=(ROOT/'build/m14-native/stage7/cab-inputs'/(Path(row['package']).stem+'.cab')).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['cabinet_sha256'];cab_sizes.append(len(raw));cab_hashes.append('{'+','.join('0x'+row['cabinet_sha256'][n:n+2]for n in range(0,64,2))+'}')
        reference=ROOT/'build/m14-native/stage7/cab-host'/('reference-'+Path(row['package']).stem)
        headers.append('static const expected147 cab147_items'+str(i)+'[]={')
        for name,digest in row['all_file_sha256'].items():
            data=(reference/name).read_bytes();assert hashlib.sha256(data).hexdigest()==digest;headers.append('{'+json.dumps(name)+','+str(len(data))+',{'+','.join('0x'+digest[n:n+2]for n in range(0,64,2))+'}},')
        headers.append('};')
    headers+=['static const unsigned cab147_counts[]={106,217};','static const unsigned cab147_sizes[]={'+','.join(map(str,cab_sizes))+'};','static const uint8_t cab147_hashes[2][32]={'+','.join(cab_hashes)+'};']
    header=out/'cab147_expected.h';header.write_bytes(('\n'.join(headers)+'\n').encode())
    names=['GlobalAlloc','GlobalFree','CreateFileW','GetFileSize','ReadFile','CloseHandle','GetStdHandle','WriteFile','ExitProcess'];definition=out/'kernel32.def';definition.write_bytes(('LIBRARY kernel32.dll\nEXPORTS\n'+'\n'.join(names)+'\n').encode());command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/'kernel32.lib')]);objects=[]
    sources=['tests/m14/cab147_native.c','user/windows8/cab147.c','runtime/sha256.c','third_party/libmspack/lzxd.c']
    for source in sources:
        obj=out/(Path(source).stem+'.obj');command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-DMSPACK_NO_DEFAULT_SYSTEM','-DSIZEOF_OFF_T=8','-DDEBUG=0','-I',ROOT/'include','-I',ROOT/'third_party/libmspack-port','-I',ROOT/'third_party/libmspack','-I',ROOT/'user/windows8','-I',out,'-c',ROOT/source,'-o',obj]);objects.append(obj)
    output=out/'cab.exe';command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(output),*objects,out/'kernel32.lib'])
    inputs=sources+['user/windows8/cab147.h','include/engine/sha256.h','tests/m14/cab147_build.py'];receipt=dict(fixture_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in inputs},independent_expected_header_sha256=hashlib.sha256(header.read_bytes()).hexdigest(),supporting_host_report_sha256=hashlib.sha256(report_path.read_bytes()).hexdigest(),scope='Owned native probe; original archives are data only, original file hashes come from independent data-only decoding')
    (out/'compile-inputs.json').write_bytes((json.dumps(receipt,indent=2)+'\n').encode());return output

if __name__=='__main__':build()
