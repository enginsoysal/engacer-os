"""Independent binary producer and SHA oracle for production transaction admission."""
import ctypes,hashlib,json,random,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools

def main():
 out=ROOT/'build/m14-native/stage7/transaction-host';out.mkdir(parents=True,exist_ok=True);t=pinned_tools();objects=[]
 for name in ['tests/m14/transaction147_host.c','runtime/sha256.c']:
  obj=out/(Path(name).stem+'.obj');command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-I',ROOT/'include','-c',ROOT/name,'-o',obj]);objects.append(obj)
 dll=out/'transaction.dll';command([t['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(dll),*objects]);lib=ctypes.CDLL(str(dll));lib.validate147.argtypes=[ctypes.c_void_p,ctypes.c_uint];lib.digest147.argtypes=[ctypes.c_void_p,ctypes.c_uint,ctypes.c_void_p];checks=0
 def check(data,wanted):
  nonlocal checks
  b=ctypes.create_string_buffer(bytes(data));actual=lib.validate147(b,len(data));assert actual==wanted,(checks,len(data),actual,wanted);checks+=1
 def seal(data):
  data=bytearray(data);data[72:104]=bytes(32);data[72:104]=hashlib.sha256(data).digest();return bytes(data)
 def record(kind,value):
  n=(8+len(value)+7)&~7;return struct.pack('<II',kind,n)+value+bytes(n-8-len(value))
 def make(records=()):
  counts=[0]*6
  for r in records:counts[struct.unpack_from('<I',r)[0]]+=1
  body=b''.join(records);header=struct.pack('<Q8I32s32s40s256s256s96s32s96s40s104s',0x314e58544d474e45,1,1024+len(body),len(records),*counts[1:],hashlib.sha256(b'original package').digest(),bytes(32),b'{A23B657D-838B-4C9B-8F9D-386E50C1A76B}',b'/Users/Owner',b'C:\\Program Files\\Notepad++',b'Notepad++',b'8.9.9.1',b'Publisher',b'{CDB13460-04DF-4708-A7FD-4CB4A0684605}',bytes(104));assert len(header)==1024;return seal(header+body)
 def file(path=b'localization/french.xml',flags=1):return record(1,struct.pack('<256s32sQII',path,hashlib.sha256(b'original package'if flags==4 else path).digest(),122556,flags,0))
 def reg(before=b''):
  key=b'Software\\Notepad++\\Lang\0';name=b'active\0';after='french\0'.encode('utf-16le');return record(2,struct.pack('<10I',2,64,1,1 if before else 0,len(after),len(before),len(key),len(name),bool(before),0)+key+name+after+before)
 key=b'Software\\Notepad++\0';kr=record(4,struct.pack('<4I',2,64,len(key),0)+key)
 prop=record(5,struct.pack('<II',9,7)+b'NPP_LANG\0french\0')
 link=record(3,struct.pack('<256s32sQII',b'AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Notepad++.lnk',hashlib.sha256(b'link').digest(),200,0,0))
 good=make([file(),reg(),kr,prop,link]);check(good,1);check(make(),1);check(make([reg('prior\0'.encode('utf-16le'))]),1)
 for n in range(len(good)):check(good[:n],0)
 for offset in [0,8,12,16,20,24,28,32,36,40,72,104,920,1024,1028,1032]:
  bad=bytearray(good);bad[offset]^=128;check(bad,0)
 for offset in [0,8,12,16,20,24,28,32,36,104,920,1024,1028]:
  bad=bytearray(good);bad[offset]^=128;check(seal(bad),0)
 for path in [b'',b'../file',b'a/../../file',b'/absolute',b'a//b',b'a\\b',b'a:stream',b'a/*',b'a/.',b'a/..',b'a/'+b'x'*64,b'a/trailing.',b'a/trailing ']:check(make([file(path)]),0)
 for flag in [0,3,5,8,0xffffffff]:check(make([file(flags=flag)]),0)
 for flag in [1,2]:check(make([file(flags=flag)]),1)
 check(make([file(b'.EngacerMSI/source.msi',4)]),1)
 for path,flag in [(b'wrong-cache.msi',4),(b'.EngacerMSI/source.msi',1),(b'.engacermsi/other',2)]:check(make([file(path,flag)]),0)
 check(make([file(),file()]),0);check(make([file(b'folder/FILE'),file(b'FOLDER/file')]),0)
 check(make([reg(b'bad')]),1);check(make([reg(),reg()]),0);check(make([prop,prop]),0);check(make([file(b'product.bin')]),0)
 for alias in [b'',b'C:\\Windows\\System32',b'C:\\Program Files',b'C:\\Program Files\\..\\Windows',b'C:\\Program Files\\A\\..\\B',b'C:\\Program Files\\']:
  bad=bytearray(good);bad[400:656]=alias.ljust(256,b'\0');check(seal(bad),0)
 rng=random.Random(147)
 for _ in range(2500):
  path=('dir'+str(rng.randrange(100))+'/file'+str(rng.randrange(100000))+'.bin').encode();data=make([file(path,rng.choice([1,2])),reg()]);check(data,1)
  b=ctypes.create_string_buffer(data);digest=(ctypes.c_ubyte*32)();assert lib.digest147(b,len(data),digest);assert bytes(digest)==data[72:104];checks+=1
  bad=bytearray(data);bad[rng.randrange(len(data))]^=1;check(bad,0)
 lib.keep147.argtypes=[ctypes.c_void_p,ctypes.c_uint,ctypes.c_uint,ctypes.c_uint,ctypes.c_char_p,ctypes.c_char_p];lib.alias147.argtypes=[ctypes.c_uint,ctypes.c_char_p];lib.alias147.restype=ctypes.c_int64
 root=b'/Applications/Windows/{A23B657D-838B-4C9B-8F9D-386E50C1A76B}';user=b'/Users/Owner'
 for mode in [1,2]:
  b=ctypes.create_string_buffer(good);assert lib.keep147(b,len(good),mode,0xffffffff,root,user)==2;checks+=1
  assert lib.keep147(b,len(good),mode,0,root,user)==3;checks+=1
  assert lib.keep147(b,len(good),mode,0xffffffff,root,b'/Users/Other')==3;checks+=1
  assert lib.keep147(b,len(good),mode,0xffffffff,root.replace(b'A23B',b'A24B'),user)==3;checks+=1
 for data in [good[:20],good[:1023],good[:-1],good+b'x']:
  b=ctypes.create_string_buffer(data);assert lib.keep147(b,len(data),1,0xffffffff,root,user)==3;checks+=1
 b=ctypes.create_string_buffer(good);assert lib.keep147(b,len(good),0,0xffffffff,root,user)==0;checks+=1
 for job_kind in [1,2,4]:
  for alias in [b'C:\\Program Files\\Notepad++',b'C:\\Program Files (x86)\\Example']:
   assert lib.alias147(job_kind,alias)==0;checks+=1
  for alias in [b'C:\\Windows\\System32',b'C:\\Program Files\\..\\Windows',b'C:\\Program Files\\',b'C:\\Program Files\\a/child']:
   assert lib.alias147(job_kind,alias)==-87;checks+=1
 for job_kind in [0,3,5,0xffffffff]:assert lib.alias147(job_kind,b'C:\\Program Files\\Notepad++')==-5;checks+=1
 lib.grant147.argtypes=[ctypes.c_char_p,ctypes.c_uint];lib.move147.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];lib.move147.restype=ctypes.c_int64
 programs=user+b'/AppData/Roaming/Microsoft/Windows/Start Menu/Programs';recovery=user+b'/Documents/Recovered applications/'+root.rsplit(b'/',1)[1]
 for parent in [programs,recovery,b'/Data/Windows/Common/Programs']:
  for path in [parent,parent+b'/owned-file']:
   assert lib.grant147(path,0)==1 and lib.grant147(path,1)==1;checks+=2
 for path in [user+b'/AppData',user+b'/Documents/Recovered applications']:
  assert lib.grant147(path,0)==0 and lib.grant147(path,1)==1;checks+=2
 for path in [user,user+b'/Documents/private.txt',user+b'/AppData/private',programs+b'/../private',recovery+b'/../../private',recovery.replace(b'A23B',b'A24B'),b'/Users/Other/AppData']:
  assert lib.grant147(path,0)==0 and lib.grant147(path,1)==0;checks+=2
 assert lib.move147(root+b'/outside.bin',root+b'/target.bin',2)==-5;checks+=1
 assert lib.move147(root+b'/.EngacerMSI/stage/file',b'/Users/Owner/Documents/file',2)==-5;checks+=1
 assert lib.move147(root+b'/.EngacerMSI/stage/file',root+b'/file',3)==-5;checks+=1
 assert lib.validate147(None,1024)==0;checks+=1
 report=dict(passed=True,checks=checks,scope='Production transaction binary/checksum/shape admission only; native durable write/recovery is not qualified',sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ['include/engine/wintxn147.h','runtime/sha256.c','tests/m14/transaction147_host.c','tests/m14/transaction147_host.py','kernel/windows8/transaction147.inc','include/engine/windows8.h']});(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS transaction admission',checks)
if __name__=='__main__':main()
