"""Compile our owned list-view callback/input fixture; never execute it on host."""
import re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
def build():
 out=ROOT/'build/m14-native/stage5/list-fixture';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools();source=ROOT/'tests/m14/list145_native.c';names=set(re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;',source.read_text(encoding='utf-8')));kernel={'GetStdHandle','WriteFile','ExitProcess','GetFileAttributesW','RemoveDirectoryW','FindFirstChangeNotificationW','GetLastError'}
 shell={'SHGetFileInfoW','SHGetSpecialFolderPathW'}
 for provider,exports in [('kernel32',kernel),('user32',names-kernel-shell),('shell32',shell)]:
  definition=out/(provider+'.def');definition.write_text('LIBRARY '+provider+'.dll\nEXPORTS\n'+'\n'.join(sorted(exports))+'\n',encoding='utf-8');command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/(provider+'.lib'))])
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',source,'-o',out/'list.obj']);command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:windows','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(out/'list.exe'),out/'list.obj',out/'kernel32.lib',out/'user32.lib',out/'shell32.lib']);return out/'list.exe'
if __name__=='__main__':build()
