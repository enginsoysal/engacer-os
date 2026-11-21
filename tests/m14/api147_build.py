"""Build the owned caller plus exact production MSI DLL, never execute on host."""
from pathlib import Path
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command
from msi147 import build as service,ORDINALS147

def build():
 out=ROOT/'build/m14-native/stage7/api-native-fixture';out.mkdir(parents=True,exist_ok=True);t=pinned_tools();binaries=service(out,t)
 source=ROOT/'tests/m14/api147_native.c';names=re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;',source.read_text());kernel=[n for n in names if not n.startswith('Msi')]
 definition=out/'kernel32.def';definition.write_bytes(('LIBRARY kernel32.dll\nEXPORTS\n'+'\n'.join(kernel)+'\n').encode());command([t['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/'kernel32.lib')])
 # Link implemented selected APIs by ordinal, as the original WiX DLL does.
 selected={name:ordinal for ordinal,name in ORDINALS147.items()};msi=out/'caller-msi.def';msi.write_bytes(('LIBRARY msi.dll\nEXPORTS\n'+'\n'.join(n+(' @'+str(selected[n])+' NONAME'if n in selected else'')for n in names if n.startswith('Msi'))+'\n').encode());command([t['lld-link'],'/lib','/machine:x64','/def:'+str(msi),'/out:'+str(out/'caller-msi.lib')])
 command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',source,'-o',out/'api.obj']);exe=out/'api.exe'
 command([t['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(exe),out/'api.obj',out/'kernel32.lib',out/'caller-msi.lib'])
 report=json.loads((out/'msi147/build-inputs.json').read_text());report['sources'].update({p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ['tests/m14/api147_native.c','tests/m14/api147_build.py']});report['fixture_sha256']=hashlib.sha256(exe.read_bytes()).hexdigest();(out/'compile-inputs.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());return exe
if __name__=='__main__':build()
