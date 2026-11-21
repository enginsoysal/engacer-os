"""Build a test-only installer-context dispatcher and own registry caller.

The production kernel and API objects remain unchanged. Only the owned clone's
runtime entry dispatcher is replaced, so normal user confirmation creates the
real REMOVE authority. This dispatcher is never included in release media.
"""
from pathlib import Path
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command
from m5_layout import compact_elf

def build():
 out=ROOT/'build/m14-native/stage7/machine-native-fixture';out.mkdir(parents=True,exist_ok=True);t=pinned_tools();work=ROOT/'build/m14-native';meta=json.loads((ROOT/'dist/m14stage7-build-manifest.json').read_text())
 for name in ['kernel/windows8/registry143.inc','user/windows8/registry143.inc']:assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==meta['source_sha256'][name]
 source=ROOT/'tests/m14/machine147_native.c';names=re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;',source.read_text());libraries=[]
 for provider in ['kernel32','advapi32']:
  symbols=[n for n in names if n.startswith('Reg')==(provider=='advapi32')];definition=out/(provider+'.def');definition.write_bytes(('LIBRARY '+provider+'.dll\nEXPORTS\n'+'\n'.join(symbols)+'\n').encode());lib=out/(provider+'.lib');command([t['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(lib)]);libraries.append(lib)
 command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-I',ROOT/'include','-c',source,'-o',out/'probe.obj']);exe=out/'probe.exe';command([t['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(exe),out/'probe.obj',*libraries])
 adapter=out/'dispatcher.c';adapter.write_bytes(b'#include "runtime.h"\nvoid msi8_execute(void){char path[256];copy8(path,job8->product_root,256);append8(path,"/machine147.exe",256);init_win8();pe8_run(path,"");}\n')
 obj=out/'dispatcher.o';command([t['clang'],'--target=x86_64-unknown-none-elf','-std=c17','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-red-zone','-mgeneral-regs-only','-mcmodel=large','-fno-pic','-fno-pie','-fno-asynchronous-unwind-tables','-DENGINE_M14','-I',ROOT/'include','-I',ROOT/'user/windows8','-c',adapter,'-o',obj])
 objects=[work/('windows8-'+name+'.o')for name in ['runtime','pe','api','msi_db','cab','sha256','lzxd']];elf=out/'runtime.elf';command([t['ld.lld'],'-T',ROOT/'user/windows8/linker.ld','--build-id=none','-o',elf,*objects,obj]);elf.write_bytes(compact_elf(elf.read_bytes()))
 sources=['tests/m14/machine147_native.c','tests/m14/machine147_build.py'];report=dict(scope=__doc__,os_build_id=meta['build_id'],source_commit=meta['source_commit'],sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources},production_objects={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in objects},dispatcher_source=adapter.read_text(),dispatcher_sha256=hashlib.sha256(adapter.read_bytes()).hexdigest(),fixture_sha256=hashlib.sha256(exe.read_bytes()).hexdigest(),runtime_sha256=hashlib.sha256(elf.read_bytes()).hexdigest());(out/'compile-inputs.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());return exe,elf
if __name__=='__main__':build()
