"""Preserve accepted checks, correcting their column-order IDs against the SDK.

M14.4's fixture mirrored the implementation's incorrect IDs. Its accepted bytes
remain immutable. The generated source keeps every assertion and records both
hashes; only SET/GETCOLUMNORDERARRAY message constants are corrected here.
"""
import hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
def build():
 out=ROOT/'build/m14-native/stage5/controls-fixture';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools();canonical=(ROOT/'tests/m14/controls144_native.c').read_bytes();text=canonical.decode('utf-8');counts={value:text.count(value)for value in ['0x1039','0x103a']};assert all(counts.values())
 text=re.sub(r'0x103[9a]\b',lambda match:{'0x1039':'0x103a','0x103a':'0x103b'}[match[0]],text);source=out/'controls145-native.c';source.write_text(text,encoding='utf-8',newline='')
 receipt=dict(canonical_sha256=hashlib.sha256(canonical).hexdigest(),compiled_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),replacements={'0x1039':'0x103a','0x103a':'0x103b'},counts=counts,reason='Correct published Win32 message identifiers; all functional assertions retained',reference='https://github.com/microsoft/win32metadata/blob/main/generation/WinSDK/RecompiledIdlHeaders/um/CommCtrl.h');(out/'source-correction.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
 exports=set(re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;',text));kernel={'GetStdHandle','WriteFile','GetLastError','ExitProcess'};common={'InitCommonControlsEx','CreateToolbarEx','CreateStatusWindowW','ImageList_GetImageCount'};shell={'SHGetFileInfoW'};user=exports-kernel-common-shell
 for provider,names in [('kernel32',kernel),('user32',user),('comctl32',common),('shell32',shell)]:
  definition=out/(provider+'.def');definition.write_text('LIBRARY '+provider+'.dll\nEXPORTS\n'+'\n'.join(sorted(names))+'\n',encoding='utf-8');command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/(provider+'.lib'))])
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',source,'-o',out/'controls.obj']);command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(out/'controls.exe'),out/'controls.obj',*[out/(p+'.lib')for p in ('kernel32','user32','comctl32','shell32')]]);return out
if __name__=='__main__':build()
