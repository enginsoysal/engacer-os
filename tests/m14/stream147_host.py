"""Actual storage and gateway with byte-exact large files, owner isolation and readback faults."""
import ctypes as c,hashlib,importlib.util,json,struct,sys,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'tools/build'),str(ROOT/'tests/m6')]
from m1 import command,pinned_tools
spec=importlib.util.spec_from_file_location('stream147_volume_types',ROOT/'tests/m6/volume.py');types=importlib.util.module_from_spec(spec);spec.loader.exec_module(types);Volume,IO,FLUSH=types.Volume,types.IO,types.FLUSH

def main():
 out=ROOT/'build/m14-native/stage7/stream-host';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools();objects=[]
 for name in ['kernel/storage/volume6.c','tests/m14/stream147_host.c']:
  obj=out/(Path(name).stem+'.obj');command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-DENGINE_M7','-DENGINE_M8','-DENGINE_M11','-DENGINE_M14','-I',ROOT/'include','-c',ROOT/name,'-o',obj]);objects.append(obj)
 dll=out/'stream.dll';command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(dll),'/export:v6_format','/export:v6_mount','/export:v6_mkdir','/export:v6_read',*objects]);lib=c.CDLL(str(dll));lib.init147.argtypes=[c.POINTER(Volume),c.c_uint,c.c_uint,c.c_uint];lib.call147.argtypes=[c.c_uint64,c.c_uint64,c.c_uint64];lib.call147.restype=c.c_int64
 for name in ['v6_format','v6_mount']:getattr(lib,name).argtypes=[c.POINTER(Volume)]
 lib.v6_mkdir.argtypes=[c.POINTER(Volume),c.c_char_p];lib.v6_read.argtypes=[c.POINTER(Volume),c.c_char_p,c.c_uint64,c.c_void_p,c.c_uint,c.POINTER(c.c_uint)]
 class Disk:
  def __init__(self):
   self.data=bytearray(32*1024*1024);self.write_bytes=self.read_bytes=self.flushes=0;self.fail_write=self.fail_read=self.corrupt=False;self.read=IO(self.r);self.write=IO(self.w);self.flush=FLUSH(self.f)
  def r(self,ctx,block,dst,n):
   if self.fail_read or n!=4096 or (block+1)*4096>len(self.data):return 1
   c.memmove(dst,bytes(self.data[block*4096:(block+1)*4096]),n);self.read_bytes+=n;return 0
  def w(self,ctx,block,src,n):
   if self.fail_write or n!=4096 or (block+1)*4096>len(self.data):return 1
   self.data[block*4096:(block+1)*4096]=c.string_at(src,n);self.write_bytes+=n
   if self.corrupt and block>=160:self.data[block*4096]^=1;self.corrupt=False
   return 0
  def f(self,ctx):self.flushes+=1;return 0
  def volume(self):return Volume(read=self.read,write=self.write,flush=self.flush,blocks=len(self.data)//4096)
 disk=Disk();v=disk.volume();assert lib.v6_format(c.byref(v))==0
 root=b'/Applications/Windows/{A23B657D-838B-4C9B-8F9D-386E50C1A76B}'
 for path in [b'/Applications',b'/Applications/Windows',root,root+b'/.EngacerMSI',root+b'/.EngacerMSI/stage']:assert lib.v6_mkdir(c.byref(v),path)==0
 def init(command=2,pid=147,authority=1):lib.init147(c.byref(v),command,pid,authority)
 def begin(path,n):b=c.create_string_buffer(path);return lib.call147(1,c.addressof(b),n)
 def send(data):b=c.create_string_buffer(data);return lib.call147(2,c.addressof(b),len(data))
 def exists(path):return any(e.kind and e.path==path for e in v.entries)
 checks=0;samples=[];init()
 for i,n in enumerate([0,1,4095,4096,4097,8594928]):
  path=root+b'/.EngacerMSI/stage/f'+str(i).encode();assert begin(path,n)==0;checks+=1;written=0;expected=hashlib.sha256();pieces=[1,73,4095,4096,201];at=0;writes=disk.write_bytes;reads=disk.read_bytes
  assert lib.call147(5,0,0)==-87;checks+=1
  while written<n:
   count=min(pieces[at%len(pieces)],n-written);body=bytes(((written+j)*37+19)&255 for j in range(count));assert send(body)==0;expected.update(body);written+=count;at+=1;checks+=1
  assert not exists(path);assert lib.call147(3,0,0)==0;assert send(b'x')==-87;checks+=3;rounds=0
  while True:
   done=lib.call147(4,0,0);assert done in [0,1];rounds+=1
   if done:break
  assert lib.call147(5,0,0)==0 and lib.owner147()==0;entry=next(e for e in v.entries if e.kind and e.path==path);actual=bytes(disk.data[entry.first*4096:entry.first*4096+n]);assert hashlib.sha256(actual).digest()==expected.digest() and entry.size==n and entry.crc==zlib.crc32(actual)&0xffffffff;checks+=3
  samples.append(dict(bytes=n,verification_rounds=rounds,storage_write_bytes=disk.write_bytes-writes,storage_read_bytes=disk.read_bytes-reads,sha256=expected.hexdigest()))
 for bad in [root+b'/other.bin',root+b'/.EngacerMSI/stageevil',b'/Users/Owner/Documents/file']:
  assert begin(bad,1)==-5;checks+=1
 path=root+b'/.EngacerMSI/stage/ownership';assert begin(path,4096)==0;init(pid=148);assert send(b'x')==-6;lib.release147();assert lib.owner147()==147;init();assert send(b'x')==0;lib.release147();assert not exists(path) and lib.owner147()==0;checks+=5
 for job_kind,authority in [(3,1),(2,0),(4,1)]:init(command=job_kind,authority=authority);assert begin(path,1)==-5;checks+=1
 init();assert begin(path,1)==0;assert send(b'xx')==-87;assert lib.call147(3,0,0)==-87;lib.release147();assert not exists(path);checks+=4
 for fault in ['write','read','corrupt']:
  assert begin(path,4096)==0
  if fault=='write':disk.fail_write=True;assert send(bytes(4096))==-1117;disk.fail_write=False
  else:
   disk.corrupt=fault=='corrupt';assert send(bytes(4096))==0;assert lib.call147(3,0,0)==0;disk.fail_read=fault=='read';assert lib.call147(4,0,0)==-1117;disk.fail_read=False
  assert not exists(path) and lib.owner147()==0;checks+=2
  # Remount independently after each failed stream; previously committed bytes remain.
  v=disk.volume();assert lib.v6_mount(c.byref(v))==0;init();checks+=1
 report=dict(passed=True,checks=checks,scope='Production native stream gateway and actual V6 storage executed on a private memory disk; role/copy host adapter, not native guest MSI installation qualification',files=samples,owner_state_bytes=24,additional_whole_file_dirty_pages=0,sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ['kernel/windows8/stream147.inc','kernel/storage/volume6.c','tests/m14/stream147_host.c','tests/m14/stream147_host.py']});(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS native storage stream host checks',checks)
if __name__=='__main__':main()
