"""Compile the owned M14.5 raster/control probe using pinned LLVM."""
import re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools

def build():
 out=ROOT/'build/m14-native/stage5/raster-fixture';out.mkdir(parents=True,exist_ok=True)
 tools=pinned_tools();source=ROOT/'tests/m14/raster145_native.c'
 exports=set(re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;',source.read_text(encoding='utf-8')))
 kernel={'GetStdHandle','WriteFile','GetLastError','ExitProcess','LoadLibraryW','FreeLibrary'}
 common={n for n in exports if n.startswith('ImageList_')};gdi={'GetTextExtentPoint32W','TextOutW','DeleteObject'}
 providers={'kernel32':kernel,'comctl32':common,'gdi32':gdi,'user32':exports-kernel-common-gdi}
 for provider,names in providers.items():
  definition=out/(provider+'.def');definition.write_bytes(('LIBRARY '+provider+'.dll\nEXPORTS\n'+'\n'.join(sorted(names))+'\n').encode())
  command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/(provider+'.lib'))])
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',source,'-o',out/'raster.obj'])
 command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:windows','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(out/'raster.exe'),out/'raster.obj',*[out/(n+'.lib')for n in providers]])
 return out/'raster.exe'

if __name__=='__main__':build()
