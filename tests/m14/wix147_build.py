"""Build an own native caller; inspect and copy, never host-execute, original WiX."""
from pathlib import Path
import hashlib,json,re,sys,os
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command
from msi147 import build as service

def build():
 out=ROOT/'build/m14-native/stage7/wix-fixture';out.mkdir(parents=True,exist_ok=True);t=pinned_tools();service(out,t)
 original=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/msi-streams/npp.8.9.9.1.Installer.x64/Wix4UtilCA_X64.bin';data=original.read_bytes();assert hashlib.sha256(data).hexdigest()=='54febbd1f0a3875df16a4b88621cc0a10729b3c94b9a68639aab27d36fe39381';(out/'wix147.dll').write_bytes(data)
 source=ROOT/'tests/m14/wix147_native.c';names=re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;',source.read_text());definition=out/'kernel32.def';definition.write_bytes(('LIBRARY kernel32.dll\nEXPORTS\n'+'\n'.join(names)+'\n').encode());command([t['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/'kernel32.lib')]);command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',source,'-o',out/'probe.obj']);exe=out/'probe.exe';command([t['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(exe),out/'probe.obj',out/'kernel32.lib'])
 report=json.loads((out/'msi147/build-inputs.json').read_text());report['sources'].update({p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ['tests/m14/wix147_native.c','tests/m14/wix147_build.py']});report['original_wix_sha256']=hashlib.sha256(data).hexdigest();report['fixture_sha256']=hashlib.sha256(exe.read_bytes()).hexdigest();(out/'compile-inputs.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());return exe
if __name__=='__main__':build()
