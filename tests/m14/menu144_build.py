"""Build only our own Windows menu/API fixture."""
import re,sys,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
def build():
 out=ROOT/'build/m14-native/stage4/menu-fixture';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools();source=(ROOT/'tests/m14/menu144_native.c').read_text(encoding='utf-8');exports=set(re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;',source));kernel={'GetStdHandle','WriteFile','GetLastError','ExitProcess','LoadLibraryW','FreeLibrary'};common=set();user=exports-kernel-common
 for provider,names in [('kernel32',kernel),('user32',user),('comctl32',common)]:
  definition=out/(provider+'.def');definition.write_bytes(('LIBRARY '+provider+'.dll\nEXPORTS\n'+'\n'.join(sorted(names))+'\n').encode());command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/(provider+'.lib'))])
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',ROOT/'tests/m14/menu144_native.c','-o',out/'menu.obj'])
 command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(out/'menu.exe'),out/'menu.obj',*[out/(p+'.lib')for p in ('kernel32','user32','comctl32')]])
 def string(value):return(value+'\0').encode('utf-16-le')
 def item(kind,state,id,flags,text):
  b=struct.pack('<IIIH',kind,state,id,flags)+string(text)
  return b+bytes((-len(b))%4)
 extended=struct.pack('<HHI',1,4,0)+item(0,0,0,0x81,'&File')+struct.pack('<I',0)+item(0,0,41,0,'Open')+item(0,8,42,0x80,'Close')
 standard=struct.pack('<HHHH',0,0,0x80,81)+string('Standard')
 payloads=[extended,standard,extended[:-3]]
 lines=['.section .rsrc,"dr"','.p2align 2','root144:','.long 0,0','.short 0,0,0,1','.long 4,names144-root144+0x80000000','names144:','.long 0,0','.short 0,0,0,3']
 for i in range(3):lines+=['.long '+str(i+1)+',lang144_'+str(i)+'-root144+0x80000000']
 for i,data in enumerate(payloads):lines+=['lang144_'+str(i)+':','.long 0,0','.short 0,0,0,1','.long 0x409,entry144_'+str(i)+'-root144','entry144_'+str(i)+':','.rva data144_'+str(i),'.long '+str(len(data))+',0,0']
 for i,data in enumerate(payloads):lines+=['.p2align 2','data144_'+str(i)+':','.byte '+','.join(map(str,data))]
 lines+=['.data','.p2align 3','.globl menu_anchor144','menu_anchor144:','.quad menu_anchor144']
 asm=out/'menu-resources.s';asm.write_bytes(('\n'.join(lines)+'\n').encode());command([tools['clang'],'--target=x86_64-pc-windows-msvc','-c',asm,'-o',out/'menu-resources.obj']);command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/dynamicbase','/fixed:no','/export:menu_anchor144,data','/out:'+str(out/'menus144.dll'),out/'menu-resources.obj'])
 print('Owned Win64 menu fixture compiled.');return out
if __name__=='__main__':build()
