"""Build only our own Windows control/API fixture."""
import re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
def build():
 out=ROOT/'build/m14-native/stage4/controls-fixture';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools();source=(ROOT/'tests/m14/controls144_native.c').read_text(encoding='utf-8');exports=set(re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;',source));kernel={'GetStdHandle','WriteFile','GetLastError','ExitProcess'};common={'InitCommonControlsEx','CreateToolbarEx','CreateStatusWindowW','ImageList_GetImageCount'};shell={'SHGetFileInfoW'};user=exports-kernel-common-shell
 for provider,names in [('kernel32',kernel),('user32',user),('comctl32',common),('shell32',shell)]:
  definition=out/(provider+'.def');definition.write_bytes(('LIBRARY '+provider+'.dll\nEXPORTS\n'+'\n'.join(sorted(names))+'\n').encode());command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/(provider+'.lib'))])
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',ROOT/'tests/m14/controls144_native.c','-o',out/'controls.obj'])
 command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(out/'controls.exe'),out/'controls.obj',*[out/(p+'.lib')for p in ('kernel32','user32','comctl32','shell32')]])
 print('Owned Win64 control/geometry fixture compiled.');return out
if __name__=='__main__':build()
