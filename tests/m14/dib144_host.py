"""Compare real 7-Zip bitmap/icon pixels with Pillow, without executing its code."""
import ctypes as c,hashlib,io,json,os,random,struct,sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command
from resource144_host import mapped,entries
class Info(c.Structure):_fields_=[(n,c.c_uint32)for n in ('width','height','bits','stride','palette','pixels','mask','mask_stride','top','icon')]
def main():
 out=ROOT/'build/m14-native/stage4/dib-host';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-std=c17','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-c',ROOT/'tests/m14/dib144_host.c','-o',out/'dib.obj'])
 command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'dib.dll'),out/'dib.obj'])
 lib=c.CDLL(str(out/'dib.dll'));lib.info144.argtypes=[c.c_void_p,c.c_uint32,c.c_uint32,c.POINTER(Info)];lib.decode144.argtypes=[c.c_void_p,c.c_uint32,c.c_uint32,c.POINTER(c.c_uint32),c.c_uint32]
 path=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/7zip/_7zFM.exe';assert hashlib.sha256(path.read_bytes()).hexdigest()=='a12710799d5cb9b3076b86dd0f92d4a503b7062bc3efac62b7f4cb8a74e05931';image,directory,_=mapped(path);rows=[];sample=None
 for kind,names in entries(image,directory,0):
  if kind not in (2,3):continue
  for name,languages in entries(image,directory,names&0x7fffffff):
   for language,record in entries(image,directory,languages&0x7fffffff):
    at,bytes_=struct.unpack_from('<II',image,directory+record);raw=bytes(image[at:at+bytes_]);array=c.create_string_buffer(raw);info=Info();assert lib.info144(array,len(raw),kind==3,c.byref(info))==0;pixels=info.width*info.height;actual=(c.c_uint32*(pixels+2))();actual[0]=actual[pixels+1]=0x2f8762ab
    assert lib.decode144(array,len(raw),kind==3,c.cast(c.byref(actual,4),c.POINTER(c.c_uint32)),pixels)==0;assert actual[0]==actual[pixels+1]==0x2f8762ab
    if kind==2:
     wrapper=b'BM'+struct.pack('<IHHI',14+len(raw),0,0,14+info.pixels)+raw
    else:
     wrapper=struct.pack('<HHH',0,1,1)+struct.pack('<BBBBHHII',info.width if info.width<256 else 0,info.height if info.height<256 else 0,0,0,1,info.bits,len(raw),22)+raw
    reference=Image.open(io.BytesIO(wrapper)).convert('RGBA');assert reference.size==(info.width,info.height)
    for index,(red,green,blue,alpha)in enumerate(reference.getdata()):
     value=actual[index+1];assert value>>24==alpha,(kind,name,index,'alpha',hex(value),alpha)
     if alpha:assert value&0xffffff==(red<<16|green<<8|blue),(kind,name,index,'color')
    rows.append(dict(type=kind,id=name,language=language,width=info.width,height=info.height,bits=info.bits,pixel_sha256=hashlib.sha256(bytes(actual)[4:-4]).hexdigest()))
    if sample is None:sample=raw
 rng=random.Random(144);mutations=10000;results={};pixels=1000000;buffer=(c.c_uint32*(pixels+2))();buffer[0]=buffer[pixels+1]=0x8eadb33f
 for turn in range(mutations):
  raw=bytearray(sample);offset=rng.randrange(min(64,len(raw)-4));raw[offset:offset+4]=rng.getrandbits(32).to_bytes(4,'little');array=(c.c_uint8*len(raw)).from_buffer(raw);status=lib.decode144(array,len(raw),rng.randrange(2),c.cast(c.byref(buffer,4),c.POINTER(c.c_uint32)),pixels);results[status]=results.get(status,0)+1;assert buffer[0]==buffer[pixels+1]==0x8eadb33f
 report=dict(passed=True,scope='Host-only real resource pixels versus independent Pillow decoding; not GUI qualification',original_images=rows,hostile_mutations=mutations,mutation_results=results,sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ('user/windows8/dib-core144.h','tests/m14/dib144_host.c','tests/m14/dib144_host.py')})
 (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS',len(rows),'original bitmap/icon resources;',mutations,'hostile mutations')
if __name__=='__main__':main()
