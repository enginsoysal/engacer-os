"""Build only own native pipe callers; never execute them on the host."""
import hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command

def build():
 out=ROOT/'build/m14-native/stage7/pipe-fixture';out.mkdir(parents=True,exist_ok=True);t=pinned_tools();source=ROOT/'tests/m14/pipe147_native.c';names=re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;',source.read_text());libraries=[]
 for provider in ['kernel32','advapi32']:
  symbols=[n for n in names if n.startswith('Reg')==(provider=='advapi32')];definition=out/(provider+'.def');definition.write_bytes(('LIBRARY '+provider+'.dll\nEXPORTS\n'+'\n'.join(symbols)+'\n').encode());lib=out/(provider+'.lib');command([t['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(lib)]);libraries.append(lib)
 flags=['--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-I',ROOT/'include']
 command([t['clang'],*flags,'-c',ROOT/'runtime/sha256.c','-o',out/'sha.obj']);files={}
 for name,extra in [('probe',[]),('authorized',['-DPIPE_AUTH147']),('block-read',['-DPIPE_BLOCK147=1']),('block-write',['-DPIPE_BLOCK147=2'])]:
  obj=out/(name+'.obj');exe=out/(name+'.exe');command([t['clang'],*flags,*extra,'-c',source,'-o',obj]);command([t['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(exe),obj,out/'sha.obj',*libraries]);files[name]=exe
 expected=hashlib.sha256(bytes((i*37+(i>>8))&255 for i in range(1024*1024))).digest();assert ','.join('0x%02x'%x for x in expected) in source.read_text()
 inputs=['tests/m14/pipe147_native.c','tests/m14/pipe147_build.py','runtime/sha256.c','include/engine/sha256.h','include/engine/windows8.h'];report=dict(scope='Exact own caller compilation; native protocol and original WiX execution are separate gates',sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in inputs},artifacts={name:hashlib.sha256(p.read_bytes()).hexdigest()for name,p in files.items()},independent_stream_sha256=expected.hex());(out/'compile-inputs.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());return files
def probe():return build()['probe']

if __name__=='__main__':build()
