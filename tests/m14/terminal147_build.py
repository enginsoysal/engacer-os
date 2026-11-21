"""Relink only an explicitly labelled native DELETE fault adapter into a private MSI DLL."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
from m8 import privacy_input
from remove147_build import build as build_routing

def build():
 fixture=build_routing();base=fixture.parent/'msi147';out=fixture.parent/'delete-fault';out.mkdir(exist_ok=True);tools=pinned_tools();source=ROOT/'tests/m14/terminal147_native_io.c';obj=out/'msi-native-fault.obj'
 flags=['--target=x86_64-pc-windows-msvc','-O2','-std=c17','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-I',ROOT/'include']
 command([tools['clang'],*flags,'-c',source,'-o',obj]);objects=sorted(p for p in base.glob('*.obj')if p.name not in ['msi-native147.obj','msiexec147.obj']);assert objects
 dll=out/'msi-delete-fault.dll';command([tools['lld-link'],'/def:'+str(base/'msi.def'),'/dll','/entry:EngacerMsiDllEntry147','/nodefaultlib','/timestamp:0','/dynamicbase','/fixed:no','/out:'+str(dll),'/implib:'+str(out/'fault.lib'),*objects,obj,base/'kernel32.lib']);raw=dll.read_bytes();assert str(ROOT).encode()not in privacy_input(raw)
 report=dict(scope=__doc__,routing_receipt_sha256=hashlib.sha256((fixture.parent/'routing-inputs.json').read_bytes()).hexdigest(),test_sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ['tests/m14/terminal147_native_io.c','tests/m14/terminal147_build.py']},objects={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in objects+[obj]},artifact=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()));(out/'compile-inputs.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());return fixture,dll
if __name__=='__main__':build()
