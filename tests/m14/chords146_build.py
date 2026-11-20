"""Compile an owned Windows ABI fixture without host execution."""
import re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools

def build():
 out=ROOT/'build/m14-native/stage6/chords-fixture';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools();source=(ROOT/'tests/m14/chords146_native.c').read_text(encoding='utf-8')
 exports=set(re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;',source));user={'RegisterClassW','CreateWindowExW','DestroyWindow','DefWindowProcW','GetKeyState','GetMessageW','DispatchMessageW','PostQuitMessage'}
 for provider,names in [('kernel32',exports-user),('user32',user)]:
  definition=out/(provider+'.def');definition.write_bytes(('LIBRARY '+provider+'.dll\nEXPORTS\n'+'\n'.join(sorted(names))+'\n').encode());command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/(provider+'.lib'))])
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',ROOT/'tests/m14/chords146_native.c','-o',out/'chords.obj'])
 command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(out/'chords.exe'),out/'chords.obj',out/'kernel32.lib',out/'user32.lib']);return out/'chords.exe'

if __name__=='__main__':build()
