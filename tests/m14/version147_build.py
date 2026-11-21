"""Build an own version caller and copy the pinned original only as data."""
import hashlib,json,re,sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools

def build():
 out=ROOT/'build/m14-native/stage7/version-native-fixture';out.mkdir(parents=True,exist_ok=True);t=pinned_tools();source=ROOT/'tests/m14/version147_native.c';names=re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;',source.read_text(encoding='utf-8'))
 libs=[]
 for dll,selected in [('version',[n for n in names if n in ['GetFileVersionInfoSizeW','GetFileVersionInfoW','VerQueryValueW']]),('kernel32',[n for n in names if n not in ['GetFileVersionInfoSizeW','GetFileVersionInfoW','VerQueryValueW']])]:
  definition=out/(dll+'.def');definition.write_bytes(('LIBRARY '+dll+'.dll\nEXPORTS\n'+'\n'.join(selected)+'\n').encode());lib=out/(dll+'.lib');command([t['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(lib)]);libs.append(lib)
 command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',source,'-o',out/'probe.obj']);exe=out/'probe.exe';command([t['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(exe),out/'probe.obj',*libs]);original=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/msi-streams/npp.8.9.9.1.Installer.x64/Wix4UtilCA_X64.bin';data=original.read_bytes();assert hashlib.sha256(data).hexdigest()=='54febbd1f0a3875df16a4b88621cc0a10729b3c94b9a68639aab27d36fe39381';(out/'wix147.dll').write_bytes(data);report=dict(scope=__doc__,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),fixture_sha256=hashlib.sha256(exe.read_bytes()).hexdigest(),original_sha256=hashlib.sha256(data).hexdigest());(out/'compile-inputs.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());return exe
if __name__=='__main__':build()
