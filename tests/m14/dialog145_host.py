"""Independent standard/extended binary templates, truncations and original resources."""
import ctypes as c,hashlib,json,os,random,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command
from resource144_host import mapped,entries

def template(extended):
 word=lambda n:struct.pack('<H',n);text=lambda s:s.encode('utf-16-le')+b'\0\0'
 if extended:raw=bytearray(struct.pack('<HHIIIHhhhh',1,65535,17,0,0x90c80040,1,-3,4,200,80))
 else:raw=bytearray(struct.pack('<IIHhhhh',0x90c80040,0,1,-3,4,200,80))
 raw+=word(0)+word(0)+text('Native dialog')+word(9)
 if extended:raw+=word(500)+bytes([1,1])
 raw+=text('Segoe UI');raw+=bytes((-len(raw))%4)
 if extended:raw+=struct.pack('<IIIhhhhI',33,0,0x50010000,5,6,70,14,70000)
 else:raw+=struct.pack('<IIhhhhH',0x50010000,0,5,6,70,14,7)
 raw+=word(65535)+word(0x80)+text('OK')
 raw+=word(4 if extended else 6)+b'\x11\x22\x33\x44'
 return bytes(raw)

def main():
 out=ROOT/'build/m14-native/stage5/dialog-host';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-std=c17','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',ROOT/'tests/m14/dialog145_host.c','-o',out/'dialog.obj'])
 command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'dialog.dll'),out/'dialog.obj'])
 lib=c.CDLL(str(out/'dialog.dll'));lib.inspect145.argtypes=[c.c_void_p,c.c_uint32,c.POINTER(c.c_uint64),c.c_uint32];lib.inspect145.restype=c.c_uint32
 marker=0x73f61a449ef028b1
 def parse(raw,capacity=400):
  storage=(c.c_uint64*(capacity+2))();storage[0]=storage[capacity+1]=marker;data=c.create_string_buffer(raw);status=lib.inspect145(data,len(raw),c.cast(c.byref(storage,8),c.POINTER(c.c_uint64)),capacity);assert storage[0]==storage[capacity+1]==marker
  return status,list(storage)[1:-1]
 truncations=0
 for extended in (False,True):
  raw=template(extended);status,values=parse(raw);assert status==0,(extended,status)
  assert values[:4]==[int(extended),1,0x90c80040,0] and values[4:10]==[(1<<64)-3,4,200,80,9,500 if extended else 0]
  assert values[10]==len(raw) and values[12]==(70000 if extended else 7)
  assert values[19:24]==[0x80,0,4 if extended else 6,33 if extended else 0,0x11 if extended else 6]
  assert parse(raw,1)[0]==122
  for length in range(len(raw)):assert parse(raw[:length])[0]!=0,(extended,length);truncations+=1
 randomizer=random.Random(145);mutations=10000
 for n in range(mutations):
  raw=bytearray(template(bool(n&1)))
  for _ in range(randomizer.randint(1,4)):raw[randomizer.randrange(len(raw))]=randomizer.randrange(256)
  status,values=parse(bytes(raw));assert status in(0,193,206,1816),status
  if not status:assert values[10]<=len(raw)and values[1]<=31
 research=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0';targets=json.loads((ROOT/'docs/roadmap/m14-targets.json').read_text(encoding='utf-8'))['targets'];original=[]
 paths={'7zip':'7zip/_7zFM.exe','notepadpp':'notepadpp/notepad++.exe','sumatra':'sumatra/SumatraPDF-3.6.1-64.exe'}
 for target in targets:
  path=research/paths[target['id']];assert hashlib.sha256(path.read_bytes()).hexdigest()==target['payload']['sha256'];image,directory,_=mapped(path)
  for kind,names in entries(image,directory,0):
   if kind!=5:continue
   for name,languages in entries(image,directory,names&0x7fffffff):
    for language,record in entries(image,directory,languages&0x7fffffff):
     at,size=struct.unpack_from('<II',image,directory+record);raw=bytes(image[at:at+size]);status,values=parse(raw)
     assert status in(0,1816),(target['id'],name,language,status)
     original.append(dict(app=target['id'],resource=name,language=language,sha256=hashlib.sha256(raw).hexdigest(),status=status,controls=values[1]if not status else None))
 result=dict(passed=True,scope='Host binary parsing only; not original native dialog execution',standard_and_extended=True,truncations=truncations,hostile_mutations=mutations,original_templates=original,control_quota=31,sources={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in[ROOT/'user/windows8/dialog-core145.h',ROOT/'tests/m14/dialog145_host.c']})
 (out/'results.json').write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PASS dialog templates:',len(original),'original,',truncations,'truncations,',mutations,'mutations')

if __name__=='__main__':main()
