"""Own parent/child native global atom callers; no host original image execution."""
import hashlib,json,re,sys,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools

def build():
 out=ROOT/'build/m14-native/stage7/atom-native-fixture';out.mkdir(parents=True,exist_ok=True);t=pinned_tools();source=ROOT/'tests/m14/atom147_native.c';names=re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;',source.read_text(encoding='utf-8'));definition=out/'kernel32.def';definition.write_bytes(('LIBRARY kernel32.dll\nEXPORTS\n'+'\n'.join(names)+'\n').encode());command([t['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/'kernel32.lib')]);command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',source,'-o',out/'probe.obj']);exe=out/'probe.exe';command([t['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(exe),out/'probe.obj',out/'kernel32.lib']);shutil.copyfile(exe,out/'atom-child147.exe');report=dict(scope=__doc__,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),fixture_sha256=hashlib.sha256(exe.read_bytes()).hexdigest());(out/'compile-inputs.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());return exe
if __name__=='__main__':build()
