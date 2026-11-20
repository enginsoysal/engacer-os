"""Generate our resource-only Win64 DLL with COFF relocations using pinned LLVM."""
import re,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
def build():
 out=ROOT/'build/m14-native/stage4/resource-fixture';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
 strings=bytearray()
 for i in range(16):
  value='Native resources' if i==2 else 'café' if i==3 else '';data=value.encode('utf-16-le');strings+=struct.pack('<H',len(data)//2)+data
 def dib(width,height,icon):
  header=struct.pack('<IiiHHIIiiII',40,width,height*2 if icon else height,1,4,0,0,0,0,2,2);palette=bytes.fromhex('00000000ff00ff00');row=bytes([0x01]*(width//2))+bytes((4-width//2)%4);pixels=row*height;mask=bytes([0x80,0,0,0])*height if icon else b'';return header+palette+pixels+mask
 bitmap=dib(8,2,False);icon=dib(4,2,True);group=struct.pack('<HHHBBBBHHIH',0,1,1,4,2,0,0,1,4,len(icon),2)
 resources=[(2,1,bitmap),(3,2,icon),(6,1,bytes(strings)),(10,1,b'immutable native resource\n'),(14,1,group)]
 lines=['.section .rsrc,"dr"','.p2align 2','resource_root144:','.long 0,0','.short 0,0,0,'+str(len(resources))]
 for index,(kind,name,data)in enumerate(resources):lines+=['.long '+str(kind)+', names144_'+str(index)+'-resource_root144+0x80000000']
 for index,(kind,name,data)in enumerate(resources):
  lines+=['names144_'+str(index)+':','.long 0,0','.short 0,0,0,1','.long '+str(name)+', languages144_'+str(index)+'-resource_root144+0x80000000','languages144_'+str(index)+':','.long 0,0','.short 0,0,0,1','.long 0x409, entry144_'+str(index)+'-resource_root144','entry144_'+str(index)+':','.rva payload144_'+str(index),'.long '+str(len(data))+',0,0']
 for index,(_,_,data)in enumerate(resources):lines+=['.p2align 2','payload144_'+str(index)+':','.byte '+','.join(map(str,data))]
 lines+=['.data','.p2align 3','.globl relocation144','relocation144:','.quad relocation144']
 asm=out/'resources.s';asm.write_bytes(('\n'.join(lines)+'\n').encode());command([tools['clang'],'--target=x86_64-pc-windows-msvc','-c',asm,'-o',out/'resources.obj']);command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/dynamicbase','/fixed:no','/export:relocation144,data','/out:'+str(out/'resources144.dll'),out/'resources.obj'])
 source=(ROOT/'tests/m14/resource144_native.c').read_text(encoding='utf-8');exports=re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;',source)
 user={'LoadStringW','LoadImageW','LoadBitmapW','DestroyIcon'};gdi={'DeleteObject'};common={v for v in exports if v.startswith('ImageList_')};kernel=set(exports)-user-gdi-common
 for provider,names in [('kernel32',kernel),('user32',user),('gdi32',gdi),('comctl32',common)]:
  definition=out/(provider+'.def');definition.write_bytes(('LIBRARY '+provider+'.dll\nEXPORTS\n'+'\n'.join(sorted(names))+'\n').encode());command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/(provider+'.lib'))])
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',ROOT/'tests/m14/resource144_native.c','-o',out/'resource-main.obj'])
 command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(out/'resource.exe'),out/'resource-main.obj',*[out/(v+'.lib')for v in ('kernel32','user32','gdi32','comctl32')]])
 print('Owned resource DLL and Win64 resource/image/heap fixture compiled.');return out
if __name__=='__main__':build()
