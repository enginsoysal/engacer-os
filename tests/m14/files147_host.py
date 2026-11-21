"""Original MSI/CAB staging, immutable ownership, and extent promotion on actual V6."""
import ctypes as c,hashlib,importlib.util,json,os,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'tools/build'),str(ROOT/'tests/m6')]
from m1 import command,pinned_tools
spec=importlib.util.spec_from_file_location('files147_disk',ROOT/'tests/m11/volume_host.py');storage=importlib.util.module_from_spec(spec);spec.loader.exec_module(storage);Volume=storage.Volume

def main():
 out=ROOT/'build/m14-native/stage7/files-host';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools();objects=[]
 sources=['user/windows8/msi-files147.c','user/windows8/msi-journal147.c','user/windows8/msi-plan147.c','user/windows8/msi-cost147.c','user/windows8/msi_db.c','user/windows8/cab147.c','third_party/libmspack/lzxd.c','runtime/sha256.c','kernel/storage/volume6.c','tests/m14/files147_host.c']
 for source in sources:
  obj=out/(Path(source).stem+'.obj');command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-DENGINE_M7','-DENGINE_M8','-DENGINE_M11','-DENGINE_M14','-DMSPACK_NO_DEFAULT_SYSTEM','-DSIZEOF_OFF_T=8','-DDEBUG=0','-I',ROOT/'include','-I',ROOT/'third_party/libmspack-port','-I',ROOT/'third_party/libmspack','-c',ROOT/source,'-o',obj]);objects.append(obj)
 dll=out/'files.dll';command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(dll),'/export:v6_format','/export:v6_mkdir','/export:v6_mount',*objects]);lib=c.CDLL(str(dll));Alloc=c.CFUNCTYPE(c.c_void_p,c.c_void_p,c.c_size_t);Free=c.CFUNCTYPE(None,c.c_void_p,c.c_void_p);Failure=c.CFUNCTYPE(None,c.c_char_p);Size=c.CFUNCTYPE(c.c_size_t,c.c_void_p);live={};state=dict(bytes=0,peak=0,bad=False)
 @Alloc
 def allocate(context,n):
  b=c.create_string_buffer(n);address=c.addressof(b);live[address]=(b,n);state['bytes']+=n;state['peak']=max(state['peak'],state['bytes']);return address
 @Free
 def release(context,address):
  if address not in live:state['bad']=True;return
  state['bytes']-=live.pop(address)[1]
 @Size
 def size(address):return live[address][1]
 @Failure
 def failure(message):(out/'unexpected-refusal.json').write_bytes(json.dumps(dict(passed=False,error=message.decode())).encode());os._exit(87)
 lib.init147.argtypes=[Alloc,Free,Failure];lib.init147(allocate,release,failure);lib.open147.argtypes=[c.c_void_p,c.c_uint];lib.cost147.argtypes=[c.c_char_p];lib.set147.argtypes=[c.c_char_p,c.c_char_p];lib.files_init147.argtypes=[c.POINTER(Volume),Size,c.c_void_p,c.c_uint];lib.journal_data147.restype=c.c_void_p
 lib.v6_format.argtypes=[c.POINTER(Volume)];lib.v6_mkdir.argtypes=[c.POINTER(Volume),c.c_char_p];lib.v6_mount.argtypes=[c.POINTER(Volume)]
 originals=json.loads((ROOT/'evidence/M14/7/development/cab-host-initial.json').read_text(encoding='utf-8'))['originals'];metadata=json.loads((ROOT/'evidence/M14/7/development/msi-tables147.json').read_text(encoding='utf-8-sig'))['packages'];samples=[];checks=0
 packages=[ROOT/'third_party/7zip/7z2606-x64.msi',Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/npp.8.9.9.1.Installer.x64.msi']
 for package in packages:
  raw=package.read_bytes();reference=next(p for p in originals if p['package_sha256']==hashlib.sha256(raw).hexdigest());data=c.create_string_buffer(raw);lib.open147(data,len(raw));assert lib.set147(b'ALLUSERS',b'1')==0;lib.cost147(b'C:\\Users\\Owner')
  disk=storage.Disk(bytearray(64*1024*1024));v=disk.volume();assert lib.v6_format(c.byref(v))==0
  for path in [b'/Applications',b'/Applications/Windows']:assert lib.v6_mkdir(c.byref(v),path)==0
  lib.files_init147(c.byref(v),size,data,len(raw));status=lib.stage147();assert status==0,(package.name,'stage',status);checks+=1
  before={e.path:(e.first,e.size,e.crc)for e in v.entries if e.kind==1};assert all(b'/.EngacerMSI/'in path for path in before);checks+=1
  assert lib.pending147()==0 and lib.keep147()==2;checks+=2
  n=lib.journal_bytes147();journal=c.string_at(lib.journal_data147(),n);assert journal[72:104]==hashlib.sha256(journal[:72]+bytes(32)+journal[104:]).digest();root=b'/Applications/Windows/'+journal[104:144].split(b'\0')[0];owned={};at=1024
  while at<n:
   kind,count=struct.unpack_from('<II',journal,at)
   if kind==1:
    relative=journal[at+8:at+264].split(b'\0')[0];digest=journal[at+264:at+296].hex();length,flags=struct.unpack_from('<QI',journal,at+296);owned[root+b'/'+relative]=(digest,length,flags)
   at+=count
  assert len(owned)==lib.selected147()+1 and at==n;assert lib.promote147()==0;assert lib.verify147()==0 and lib.keep147()==2;checks+=4
  entries={e.path:e for e in v.entries if e.kind==1};payload_digests=reference['all_file_sha256'];matched=[]
  tables=next(p['tables']for p in metadata if p['file']==package.name);directories={r[0]:r for r in tables['Directory']};components={r[0]:r for r in tables['Component']};root_id=next(r[0]for r in tables['Directory']if r[1]in ['ProgramFiles64Folder','ProgramFilesFolder'])
  def name(field):return field.split(':')[0].split('|')[-1]
  def relative(directory):
   if directory==root_id:return ''
   row=directories[directory];parent=relative(row[1]);leaf=name(row[2]);return '/'.join(x for x in [parent,''if leaf=='.'else leaf]if x)
  expected={root+b'/'+('/'.join(x for x in [relative(components[r[1]][2]),name(r[2])]if x)).encode():(payload_digests[r[0]],int(r[3]))for r in tables['File']}
  assert {path for path,value in owned.items()if value[2]==1}==set(expected);checks+=1
  for path,(digest,length,flags)in owned.items():
   e=entries[path];payload=bytes(disk.data[e.first*4096:e.first*4096+e.size]);assert len(payload)==length and hashlib.sha256(payload).hexdigest()==digest
   if flags==1:assert (digest,length)==expected[path];matched.append(digest);assert (e.first,e.size,e.crc)in before.values()
   else:assert flags==4 and digest==hashlib.sha256(raw).hexdigest() and payload==raw
   checks+=3
  # A changed final payload is refused while the immutable recovery image survives.
  changed=next(e for path,e in entries.items()if path in owned and owned[path][2]==1);disk.data[changed.first*4096]^=1;assert lib.verify147()==23 and lib.keep147()==2;disk.data[changed.first*4096]^=1;checks+=2
  independent=disk.volume();assert lib.v6_mount(c.byref(independent))==0;assert {e.path:(e.first,e.size,e.crc)for e in independent.entries if e.kind}=={e.path:(e.first,e.size,e.crc)for e in v.entries if e.kind};checks+=2
  samples.append(dict(package=package.name,source_sha256=hashlib.sha256(raw).hexdigest(),selected_payloads=len(matched),payload_bytes=sum(length for _,length,flags in owned.values()if flags==1),journal_bytes=n,extent_promotion_preserves_data=True,pending_record_retained=True));lib.files_close147();lib.close147();assert not live and state['bytes']==0 and not state['bad'];checks+=1
 report=dict(passed=True,checks=checks,scope='Actual production MSI/CAB file staging, journal, kernel stream/move routines and V6 on a private memory disk with host syscall/file-handle adapters; original custom sequence, external effects, native guest installation and recovery remain unqualified',packages=samples,peak_host_tracked_bytes=state['peak'],retained_host_tracked_bytes=state['bytes'],sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources+['user/windows8/msi-files147.h','user/windows8/msi-journal147.h','include/engine/wintxn147.h','kernel/windows8/stream147.inc','kernel/windows8/transaction147.inc','tests/m14/files147_host.py']});(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS original MSI file staging/promotion',checks)
if __name__=='__main__':main()
