"""Create controlled valid/malformed unwind metadata in synthetic Windows fixtures."""
import struct
from pathlib import Path
from unwind_fixtures2 import build

def variants():
 work=build();original=(work/'unwind.exe').read_bytes();pe=struct.unpack_from('<I',original,60)[0];opt=pe+24;count=struct.unpack_from('<H',original,pe+6)[0];options=struct.unpack_from('<H',original,pe+20)[0];sections=[]
 for i in range(count):
  at=opt+options+i*40;virtual,base,raw,offset=struct.unpack_from('<4I',original,at+8);sections.append((base,max(virtual,raw),offset,raw))
 def file_at(rva,n=1):
  for base,size,offset,raw in sections:
   if base<=rva and rva+n<=base+raw:return offset+rva-base
  raise ValueError(('not file-backed',rva,n))
 def virtual_at(offset):
  for base,size,start,raw in sections:
   if start<=offset<start+raw:return base+offset-start
  raise ValueError(offset)
 directory,size=struct.unpack_from('<2I',original,opt+136);table=file_at(directory,size);functions=[struct.unpack_from('<3I',original,table+i) for i in range(0,size,12)];fault_offset=original.index(bytes.fromhex('c70007000000'));fault=virtual_at(fault_offset);index=next(i for i,row in enumerate(functions) if row[0]<=fault<row[1]);begin,end,info=functions[index];at=file_at(info,4);slots=original[at+2];length=4+((slots+1)&~1)*2;assert original[at]&7==1 and original[at]>>3==0 and slots
 scratch_file=original.index(b'ENGACER_UNWIND_SCRATCH_142');scratch=virtual_at(scratch_file);assert scratch%4==0;file_at(scratch,128)
 for mode in ['chain','cycle','opcode','scope','directory']:
  data=bytearray(original)
  if mode in ['chain','cycle','opcode']:
   data[scratch_file:scratch_file+128]=bytes(128);data[scratch_file:scratch_file+length]=original[at:at+length];struct.pack_into('<I',data,table+index*12+8,scratch)
   if mode=='opcode':data[scratch_file+5]=0x21
   else:
    data[scratch_file]=0x21;struct.pack_into('<3I',data,scratch_file+length,begin,end,scratch if mode=='cycle' else scratch+64);data[scratch_file+64:scratch_file+68]=bytes([1,0,0,0])
  elif mode=='scope':
   for begin,end,info in functions:
    at=file_at(info,4);flags=original[at]>>3
    if flags&3:
     scope=at+4+((original[at+2]+1)&~1)*2+4;struct.pack_into('<I',data,scope,4097);break
   else:raise AssertionError('No compiler C scope table')
  else:struct.pack_into('<I',data,opt+140,size+1)
  (work/('unwind-'+mode+'.exe')).write_bytes(data)
 return work
if __name__=='__main__':variants();print('Controlled unwind variants built; no host execution')
