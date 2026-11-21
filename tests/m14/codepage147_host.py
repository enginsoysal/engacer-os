"""Production codecs against independent Python codecs and guarded buffers."""
import ctypes as c,hashlib,json,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools

def main():
 out=ROOT/'build/m14-native/stage7/codepage-host';out.mkdir(parents=True,exist_ok=True);t=pinned_tools()
 command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-DENGINE_M14','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-I',ROOT/'include','-c',ROOT/'tests/m14/codepage147_host.c','-o',out/'codec.obj'])
 command([t['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'codec.dll'),out/'codec.obj']);lib=c.CDLL(str(out/'codec.dll'));U=c.c_uint;P=c.c_void_p;I=c.c_int
 lib.mb147.argtypes=[U,U,P,I,P,I];lib.wc147.argtypes=[U,U,P,I,P,I,P,P];lib.info147.argtypes=[U,P];checks=0
 def check(value):
  nonlocal checks
  assert value;checks+=1
 check(lib.acp147()==65001 and lib.oem147()==65001)
 for cp in [65001,1252,0,1,65000,42,932,0xffffffff]:
  check(lib.valid147(cp)==(cp in [65001,1252]));buf=(c.c_ubyte*36)(*([0x9b]*36));status=lib.info147(cp,buf)
  if cp in [0,1,65001,1252]:check(status==1 and bytes(buf)[20:]==b'\x9b'*16);check(int.from_bytes(bytes(buf)[:4],'little')==(1 if cp==1252 else 4));check(bytes(buf)[4:18]==b'?'+b'\0'*13)
  else:check(status==0 and lib.error_get147()==87 and bytes(buf)==b'\x9b'*36)
 check(not lib.info147(65001,None) and lib.error_get147()==87)
 # Python intentionally rejects five undefined 1252 bytes; the existing
 # Windows profile preserves their corresponding C1 controls explicitly.
 for value in range(256):
  source=bytes([value]);text=chr(value)if value in [0x81,0x8d,0x8f,0x90,0x9d]else source.decode('cp1252');expected=text.encode('utf-16-le');wide=(c.c_ubyte*12)(*([0x9b]*12));check(lib.mb147(1252,0,source,1,wide,1)==1 and bytes(wide)[:2]==expected and bytes(wide)[2:]==b'\x9b'*10)
  encoded=(c.c_ubyte*12)(*([0x9b]*12));used=I(99);check(lib.wc147(1252,0,wide,1,encoded,1,None,c.byref(used))==1 and bytes(encoded)[:1]==source and used.value==0 and bytes(encoded)[1:]==b'\x9b'*11)
 # Strictly unrepresentable characters use the requested default, including
 # during size-only queries. No best-fit approximation is claimed here.
 for cp in [0x80,0x100,0x3bb,0x4e00,0x1f600]:
  source=chr(cp).encode('utf-16-le');wide=c.create_string_buffer(source);used=I(0);check(lib.wc147(1252,0x400,wide,len(source)//2,None,0,b'!',c.byref(used))==1 and used.value==1);buf=c.create_string_buffer(2);check(lib.wc147(1252,0x400,wide,len(source)//2,buf,1,b'!',c.byref(used))==1 and buf.raw[:1]==b'!' and used.value==1)
 rng=random.Random(147);scalars=[0,1,127,128,0x20ac,0xd7ff,0xe000,0xffff,0x10000,0x10ffff]+[rng.randrange(0x110000)for _ in range(3000)]
 for cp in scalars:
  if 0xd800<=cp<=0xdfff:continue
  text=chr(cp);source=text.encode('utf-8');wide=text.encode('utf-16-le');units=len(wide)//2;buf=(c.c_ubyte*12)(*([0x9b]*12));check(lib.mb147(65001,8,source,len(source),None,0)==units);check(lib.mb147(65001,8,source,len(source),buf,units)==units and bytes(buf)[:len(wide)]==wide and bytes(buf)[len(wide):]==b'\x9b'*(12-len(wide)))
  output=(c.c_ubyte*12)(*([0x9b]*12));check(lib.wc147(65001,0,buf,units,None,0,None,None)==len(source));check(lib.wc147(65001,0,buf,units,output,len(source),None,None)==len(source) and bytes(output)[:len(source)]==source and bytes(output)[len(source):]==b'\x9b'*(12-len(source)))
  if len(source)>1:check(lib.wc147(65001,0,buf,units,output,len(source)-1,None,None)==0 and lib.error_get147()==122)
 for source in [b'\x80',b'\xc0\x80',b'\xc1\xbf',b'\xe0\x80\x80',b'\xed\xa0\x80',b'\xf0\x80\x80\x80',b'\xf4\x90\x80\x80']+[bytes([lead])+b'\x80'*3 for lead in range(0xf5,256)]:check(lib.mb147(65001,8,source,len(source),None,0)==0 and lib.error_get147()==1113)
 check(lib.mb147(65001,0,b'A',1,None,1)==0 and lib.error_get147()==87);check(lib.wc147(65001,0,c.create_string_buffer(b'A\0'),1,None,1,None,None)==0 and lib.error_get147()==87)
 sources=['user/windows8/codepage147.inc','tests/m14/codepage147_host.c','tests/m14/codepage147_host.py'];report=dict(passed=True,checks=checks,scope='Own selected codecs vs Python data references; no host execution of original app, CRT or custom action',limits=['UTF-8 ACP/OEM and explicit Windows-1252 only','Existing strict malformed-input profile retained; not all Windows replacement, best-fit, normalization or flag semantics'],sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources});(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS own codec and code-page checks',checks)
if __name__=='__main__':main()
