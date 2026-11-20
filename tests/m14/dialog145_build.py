"""Build our standard/extended/malformed/quota dialog resources and Win64 probe."""
import re,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools

def template(extended=False,count=4):
 word=lambda n:struct.pack('<H',n);text=lambda s:s.encode('utf-16-le')+b'\0\0'
 style=0x90c80840
 raw=bytearray(struct.pack('<HHIIIHhhhh',1,65535,0,0,style,count,0,0,220,90)if extended else struct.pack('<IIHhhhh',style,0,count,0,0,220,90))
 raw+=word(0)+word(0)+text('Extended native dialog'if extended else'Standard native dialog')+word(9)
 if extended:raw+=word(400)+bytes([0,1])
 raw+=text('Segoe UI')
 controls=[(10,0x82,'Original callback, native controls',0x50000000,10,10,200,14),(11,0x81,'',0x50810080,10,30,200,16),(1,0x80,'OK',0x50010001,150,62,60,14),(2,0x80,'Cancel',0x50010000,80,62,60,14)]
 if count!=4:controls=[(100+n,0x82,'Quota',0x50000000,1,1,20,8)for n in range(count)]
 for identifier,kind,label,flags,x,y,w,h in controls:
  raw+=bytes((-len(raw))%4)
  raw+=struct.pack('<IIIhhhhI',0,0,flags,x,y,w,h,identifier)if extended else struct.pack('<IIhhhhH',flags,0,x,y,w,h,identifier)
  raw+=word(65535)+word(kind)+text(label)+word(0)
 return bytes(raw)

def build():
 out=ROOT/'build/m14-native/stage5/dialog-fixture';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
 resources={100:template(),101:template(True),102:template(),103:template()[:-1],104:template(count=32),105:template(count=31)}
 lines=['.section .rsrc,"dr"','.p2align 2','dialog_root145:','.long 0,0','.short 0,0,0,1','.long 5,dialog_names145-dialog_root145+0x80000000','dialog_names145:','.long 0,0','.short 0,0,0,'+str(len(resources))]
 for identifier in resources:lines+=['.long '+str(identifier)+',dialog_lang145_'+str(identifier)+'-dialog_root145+0x80000000']
 for identifier,raw in resources.items():
  suffix=str(identifier);lines+=['dialog_lang145_'+suffix+':','.long 0,0','.short 0,0,0,1','.long 1033,dialog_entry145_'+suffix+'-dialog_root145','dialog_entry145_'+suffix+':','.rva dialog_payload145_'+suffix,'.long '+str(len(raw))+',0,0']
 for identifier,raw in resources.items():lines+=['.p2align 2','dialog_payload145_'+str(identifier)+':','.byte '+','.join(map(str,raw))]
 lines+=['.data','.p2align 3','.globl dialog_relocation145','dialog_relocation145:','.quad dialog_relocation145']
 asm=out/'dialogs.s';asm.write_bytes(('\n'.join(lines)+'\n').encode());command([tools['clang'],'--target=x86_64-pc-windows-msvc','-c',asm,'-o',out/'dialogs.obj']);command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/dynamicbase','/fixed:no','/export:dialog_relocation145,data','/out:'+str(out/'dialogs145.dll'),out/'dialogs.obj'])
 source=ROOT/'tests/m14/dialog145_native.c';exports=set(re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;',source.read_text(encoding='utf-8')));kernel={'GetStdHandle','WriteFile','GetLastError','ExitProcess','LoadLibraryW','FreeLibrary'}
 for provider,names in [('kernel32',kernel),('user32',exports-kernel)]:
  definition=out/(provider+'.def');definition.write_bytes(('LIBRARY '+provider+'.dll\nEXPORTS\n'+'\n'.join(sorted(names))+'\n').encode());command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/(provider+'.lib'))])
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',source,'-o',out/'dialog-main.obj'])
 command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:windows','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(out/'dialog.exe'),out/'dialog-main.obj',out/'kernel32.lib',out/'user32.lib'])
 return out

if __name__=='__main__':build()
