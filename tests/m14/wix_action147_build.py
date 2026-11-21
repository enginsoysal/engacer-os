"""Test-only session owner added to exact production MSI objects; no host PE execution."""
import hashlib,json,re,sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command
from msi147 import build as service

def build():
 out=ROOT/'build/m14-native/stage7/wix-action-fixture';out.mkdir(parents=True,exist_ok=True);t=pinned_tools();service(out,t);msi=out/'msi147'
 flags=['--target=x86_64-pc-windows-msvc','-O2','-std=c17','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-I',ROOT/'include']
 sources=['tests/m14/wix_action147_engine.c','tests/m14/wix_action147_caller.c','tests/m14/wix_action147_child.c'];names=[]
 for source in sources:names+=re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;',(ROOT/source).read_text(encoding='utf-8'))
 definition=out/'kernel32.def';definition.write_bytes((msi/'kernel32.def').read_bytes()+('\n'+'\n'.join(sorted(set(names)))+'\n').encode());command([t['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/'kernel32.lib')])
 for source in sources:command([t['clang'],*flags,'-c',ROOT/source,'-o',out/(Path(source).stem+'.obj')])
 # The fixture's extra session owner is explicit and absent from release binaries.
 definition=out/'msi.def';definition.write_bytes((msi/'msi.def').read_bytes()+b'TestOriginalAction147 @32767\n');objects=sorted(p for p in msi.glob('*.obj')if p.name!='msiexec147.obj')
 dll=msi/'msi.dll';command([t['lld-link'],'/def:'+str(definition),'/dll','/entry:EngacerMsiDllEntry147','/nodefaultlib','/timestamp:0','/dynamicbase','/fixed:no','/out:'+str(dll),*objects,out/'wix_action147_engine.obj',out/'kernel32.lib'])
 for stem,name in [('caller','probe.exe'),('child','quiet-child147.exe')]:command([t['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(out/name),out/('wix_action147_'+stem+'.obj'),out/'kernel32.lib'])
 original=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/msi-streams/npp.8.9.9.1.Installer.x64/Wix4UtilCA_X64.bin';data=original.read_bytes();assert hashlib.sha256(data).hexdigest()=='54febbd1f0a3875df16a4b88621cc0a10729b3c94b9a68639aab27d36fe39381';(out/'wix147.dll').write_bytes(data)
 report=json.loads((msi/'build-inputs.json').read_text(encoding='utf-8'));report['scope']=__doc__;report['test_sources']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources+['tests/m14/wix_action147_build.py']};report['fixture_artifacts']={p.relative_to(out).as_posix():dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())for p in[dll,out/'probe.exe',out/'quiet-child147.exe',out/'wix147.dll']};(out/'compile-inputs.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());return out/'probe.exe'
if __name__=='__main__':build()
