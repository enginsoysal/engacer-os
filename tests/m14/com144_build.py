import re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
def build():
 out=ROOT/'build/m14-native/stage4/com-fixture';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools();source=(ROOT/'tests/m14/com144_native.c').read_text(encoding='utf-8');all_=set(re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;',source));ole={'CoInitializeEx','CoInitialize','CoUninitialize','OleInitialize','OleUninitialize','RegisterDragDrop','RevokeDragDrop'};user={'RegisterClassW','CreateWindowExW','DefWindowProcW','DestroyWindow','IsWindow'};kernel=all_-ole-user
 for provider,names in [('kernel32',kernel),('user32',user),('ole32',ole)]:
  definition=out/(provider+'.def');definition.write_bytes(('LIBRARY '+provider+'.dll\nEXPORTS\n'+'\n'.join(sorted(names))+'\n').encode());command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/(provider+'.lib'))])
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',ROOT/'tests/m14/com144_native.c','-o',out/'com.obj']);command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(out/'com.exe'),out/'com.obj',*[out/(n+'.lib')for n in ('kernel32','user32','ole32')]]);return out
if __name__=='__main__':build()
