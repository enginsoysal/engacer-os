"""Compile an own native FLS caller; no host PE execution."""
from pathlib import Path
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools

def build():
 out=ROOT/'build/m14-native/stage7/fls-fixture';out.mkdir(parents=True,exist_ok=True);t=pinned_tools();source=ROOT/'tests/m14/fls147_native.c';names=re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;',source.read_text());definition=out/'kernel32.def';definition.write_bytes(('LIBRARY kernel32.dll\nEXPORTS\n'+'\n'.join(names)+'\n').encode());command([t['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/'kernel32.lib')]);command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',source,'-o',out/'probe.obj']);exe=out/'probe.exe';command([t['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(exe),out/'probe.obj',out/'kernel32.lib'])
 sources=['tests/m14/fls147_native.c','tests/m14/fls147_build.py'];report=dict(scope=__doc__,sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources},fixture_sha256=hashlib.sha256(exe.read_bytes()).hexdigest());(out/'compile-inputs.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());return exe
if __name__=='__main__':build()
