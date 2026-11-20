"""Read-only original PE resources and malformed tables; never run foreign code."""
import ctypes as c,hashlib,json,os,random,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command
class Key(c.Structure):_fields_=[('numeric',c.c_uint32),('id',c.c_uint32),('units',c.c_uint32),('text',c.c_uint16*128)]
class Result(c.Structure):_fields_=[('entry',c.c_uint32),('data',c.c_uint32),('bytes',c.c_uint32),('language',c.c_uint32)]
def key(value):
 k=Key()
 if isinstance(value,int):k.numeric=1;k.id=value
 else:
  data=value.encode('utf-16-le');k.units=len(data)//2;assert k.units<=128
  for i in range(k.units):k.text[i]=int.from_bytes(data[i*2:i*2+2],'little')
 return k
def mapped(path):
 raw=path.read_bytes();pe=struct.unpack_from('<I',raw,60)[0];opt=pe+24;assert struct.unpack_from('<H',raw,opt)[0]==0x20b
 size,headers=struct.unpack_from('<II',raw,opt+56);assert size<=32*1024**2;image=bytearray(size);image[:headers]=raw[:headers]
 count=struct.unpack_from('<H',raw,pe+6)[0];table=opt+struct.unpack_from('<H',raw,pe+20)[0]
 for i in range(count):
  sec=table+i*40;va,amount,offset=struct.unpack_from('<III',raw,sec+12);image[va:va+amount]=raw[offset:offset+amount]
 directory,bytes_=struct.unpack_from('<II',raw,opt+128);return image,directory,bytes_
def entries(image,directory,offset):
 n=sum(struct.unpack_from('<HH',image,directory+offset+12));assert n<=4096;result=[]
 for i in range(n):
  name,child=struct.unpack_from('<II',image,directory+offset+16+i*8)
  if name&0x80000000:
   at=directory+(name&0x7fffffff);units=struct.unpack_from('<H',image,at)[0];name=bytes(image[at+2:at+2+units*2]).decode('utf-16-le')
  result.append((name,child))
 return result
def main():
 out=ROOT/'build/m14-native/stage4/resource-host';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-std=c17','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-c',ROOT/'tests/m14/resource144_host.c','-o',out/'resource.obj'])
 command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'resource.dll'),out/'resource.obj'])
 lib=c.CDLL(str(out/'resource.dll'));lib.lookup144.argtypes=[c.c_void_p,c.c_uint32,c.c_uint32,c.c_uint32,c.POINTER(Key),c.POINTER(Key),c.c_uint32,c.c_uint32,c.POINTER(Result)];lib.string144.argtypes=[c.c_void_p,c.c_uint32,c.c_uint32,c.POINTER(c.c_void_p),c.POINTER(c.c_uint32)]
 scratch=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0';targets=json.loads((ROOT/'docs/roadmap/m14-targets.json').read_text(encoding='utf-8'))['targets'];rows=[]
 for target,relative in zip(targets,('7zip/_7zFM.exe','notepadpp/notepad++.exe','sumatra/SumatraPDF-3.6.1-64.exe')):
  path=scratch/relative;digest=hashlib.sha256(path.read_bytes()).hexdigest();assert digest==target['payload']['sha256'];image,directory,bytes_=mapped(path);array=(c.c_uint8*len(image)).from_buffer(image);resources=0;strings=0
  for type_,names in entries(image,directory,0):
   assert names&0x80000000
   for name,languages in entries(image,directory,names&0x7fffffff):
    assert languages&0x80000000
    for language,data_entry in entries(image,directory,languages&0x7fffffff):
     assert not data_entry&0x80000000;data,size=struct.unpack_from('<II',image,directory+data_entry);result=Result();assert lib.lookup144(array,len(image),directory,bytes_,c.byref(key(type_)),c.byref(key(name)),language,1,c.byref(result))==0
     assert (result.entry,result.data,result.bytes,result.language)==(directory+data_entry,data,size,language);resources+=1
     if type_==6:
      at=data
      for slot in range(16):
       units=struct.unpack_from('<H',image,at)[0];at+=2;pointer=c.c_void_p();actual=c.c_uint32();assert lib.string144(c.byref(array,data),size,slot,c.byref(pointer),c.byref(actual))==0;assert actual.value==units and c.string_at(pointer.value,units*2)==bytes(image[at:at+units*2]);at+=units*2;strings+=1
  rows.append(dict(target=target['id'],original_sha256=digest,resources=resources,string_slots=strings))
 # Mutate only our scratch memory, preserving original downloads and binaries.
 image,directory,bytes_=mapped(scratch/'7zip/_7zFM.exe');array=(c.c_uint8*len(image)).from_buffer(image);rng=random.Random(144);cases=20000;errors={}
 for turn in range(cases):
  offset=directory+rng.randrange(bytes_//4)*4;old=image[offset:offset+4];struct.pack_into('<I',image,offset,rng.getrandbits(32));result=Result();status=lib.lookup144(array,len(image),directory,bytes_,c.byref(key(rng.choice([3,6,10,14,24]))),c.byref(key(rng.randrange(1,300))),0x409,rng.randrange(2),c.byref(result));errors[status]=errors.get(status,0)+1
  if status==0:assert result.data<=len(image) and result.bytes<=len(image)-result.data and result.entry>=directory and result.entry+16<=directory+bytes_
  image[offset:offset+4]=old
 result=dict(passed=True,scope='Host-only resource parser against independently enumerated original data; not original GUI execution',originals=rows,malformed_mutations=cases,mutation_results=errors,sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ('user/windows8/resource-core144.h','tests/m14/resource144_host.c','tests/m14/resource144_host.py')})
 (out/'results.json').write_bytes((json.dumps(result,indent=2)+'\n').encode());print(json.dumps(result))
if __name__=='__main__':main()
