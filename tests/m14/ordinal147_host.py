"""Inspect own PE export/import metadata; never execute a Windows image on host."""
import hashlib,json,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from msi147 import ORDINALS147

def pe(path):
 data=path.read_bytes();off=struct.unpack_from('<I',data,60)[0];assert data[off:off+4]==b'PE\0\0';machine,count=struct.unpack_from('<HH',data,off+4);assert machine==0x8664;optional=off+24;assert struct.unpack_from('<H',data,optional)[0]==0x20b
 sections=optional+struct.unpack_from('<H',data,off+20)[0]
 def rva(address):
  for i in range(count):
   at=sections+40*i;size,start,raw,position=struct.unpack_from('<IIII',data,at+8)
   if start<=address<start+max(size,raw):assert address-start<raw;return position+address-start
  raise AssertionError(('Unmapped RVA',address))
 def text(address):
  start=rva(address);end=data.index(b'\0',start);return data[start:end].decode('ascii')
 return data,optional,rva,text

def main():
 out=ROOT/'build/m14-native/stage7/api-native-fixture';dll=out/'msi147/msi.dll';exe=out/'api.exe';data,opt,rva,text=pe(dll);directory=struct.unpack_from('<I',data,opt+112)[0];at=rva(directory);base,functions,names,ft,nt,ot=struct.unpack_from('<IIIIII',data,at+16);exports={}
 for i in range(names):
  name=text(struct.unpack_from('<I',data,rva(nt)+i*4)[0]);index=struct.unpack_from('<H',data,rva(ot)+i*2)[0];address=struct.unpack_from('<I',data,rva(ft)+index*4)[0];assert address;exports[name]=base+index
 for ordinal,name in ORDINALS147.items():assert exports[name]==ordinal,(name,exports[name],ordinal)
 for name,ordinal in exports.items():assert ordinal in ORDINALS147 or ordinal>=0x7000,(name,ordinal)
 for ordinal in [26,32,34,49,51,76,120,159,160,162,163,166]:
  index=ordinal-base
  assert index<0 or index>=functions or struct.unpack_from('<I',data,rva(ft)+index*4)[0]==0,ordinal
 # Actual caller thunks must contain ordinal imports, not merely named aliases.
 data,opt,rva,text=pe(exe);at=rva(struct.unpack_from('<I',data,opt+120)[0]);imports=[]
 while any(data[at:at+20]):
  original,_,_,name,_=struct.unpack_from('<IIIII',data,at);module=text(name).lower();pos=rva(original)
  while True:
   thunk=struct.unpack_from('<Q',data,pos)[0];pos+=8
   if not thunk:break
   if module=='msi.dll':imports.append(thunk)
  at+=20
 ordinal_imports=[x&65535 for x in imports if x>>63];assert len(ordinal_imports)>=8 and 171 in ordinal_imports
 for ordinal in ordinal_imports:assert ordinal in ORDINALS147
 report=dict(passed=True,scope='Own PE metadata only; native ordinal execution is separately required',implemented_ordinals={str(o):n for o,n in ORDINALS147.items()},actual_caller_ordinals=ordinal_imports,named_caller_imports=len(imports)-len(ordinal_imports),artifacts={str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [dll,exe]})
 (out/'ordinal-metadata.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS own MSI ordinal metadata',len(ORDINALS147),len(ordinal_imports))
if __name__=='__main__':main()
