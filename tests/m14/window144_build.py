"""Compile our own Win64 GUI fixture, never run a foreign app on the host."""
import re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command
def build():
 out=ROOT/'build/m14-native/stage4/window-fixture';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
 source=(ROOT/'tests/m14/window144.c').read_text(encoding='utf-8')
 kernel={'GetStdHandle','WriteFile','ExitProcess','GetLastError'}
 exports=re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;',source)
 assert len(exports)==20,exports
 for provider,names in [('kernel32',sorted(kernel)),('user32',sorted(set(exports)-kernel))]:
  definition=out/(provider+'.def');definition.write_bytes(('LIBRARY '+provider+'.dll\nEXPORTS\n'+'\n'.join(names)+'\n').encode())
  command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/(provider+'.lib'))])
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',ROOT/'tests/m14/window144.c','-o',out/'window.obj'])
 command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:windows','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(out/'window.exe'),out/'window.obj',out/'kernel32.lib',out/'user32.lib'])
 print('Owned AMD64 GUI fixture compiled.');return out/'window.exe'
if __name__=='__main__':build()
