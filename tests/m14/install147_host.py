"""Original MSI/CAB staging, immutable ownership, and extent promotion on actual V6."""
import ctypes as c,hashlib,importlib.util,json,os,re,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'tools/build'),str(ROOT/'tests/m6')]
from m1 import command,pinned_tools
spec=importlib.util.spec_from_file_location('files147_disk',ROOT/'tests/m11/volume_host.py');storage=importlib.util.module_from_spec(spec);spec.loader.exec_module(storage);Volume=storage.Volume

def main():
 out=ROOT/'build/m14-native/stage7/install-host';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools();objects=[]
 sources=['user/windows8/msi-install147.c','user/windows8/msi-registry147.c','user/windows8/msi-files147.c','user/windows8/msi-shortcuts147.c','user/windows8/msi-journal147.c','user/windows8/msi-plan147.c','user/windows8/msi-cost147.c','user/windows8/msi_db.c','user/windows8/cab147.c','third_party/libmspack/lzxd.c','runtime/sha256.c','kernel/storage/volume6.c','tests/m14/files147_host.c']
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
 from registry147_adapter import create
 registry,cleanup,registry_state=create();lib.files_registry147.argtypes=[type(registry)];lib.files_registry147(registry)
 originals=json.loads((ROOT/'evidence/M14/7/development/cab-host-initial.json').read_text(encoding='utf-8'))['originals'];checks=0;samples=[]
 packages=[ROOT/'third_party/7zip/7z2606-x64.msi',Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/npp.8.9.9.1.Installer.x64.msi']
 try:
  for index,package in enumerate(packages):
   raw=package.read_bytes();data=c.create_string_buffer(raw);lib.open147(data,len(raw));assert lib.set147(b'ALLUSERS',b'1')==0 and lib.set147(b'Privileged',b'1')==0;lib.cost147(b'C:\\Users\\Owner')
   disk=storage.Disk(bytearray(64*1024*1024));v=disk.volume();assert lib.v6_format(c.byref(v))==0
   for path in [b'/Applications',b'/Applications/Windows']:assert lib.v6_mkdir(c.byref(v),path)==0
   lib.files_init147(c.byref(v),size,data,len(raw));before=hashlib.sha256(disk.data).digest();base=state['bytes'];status=lib.install_controller147()
   if index:
    assert status==50 and hashlib.sha256(disk.data).digest()==before and state['bytes']==base;(samples.append(dict(package=package.name,refused_custom_actions_before_effects=True)));checks+=3;lib.files_close147();lib.close147();continue
   assert status==0,(status,registry_state);assert lib.installed_read147()==0;assert lib.verify147()==0;assert lib.keep147()==0;checks+=4
   n=lib.journal_bytes147();journal=c.string_at(lib.journal_data147(),n);assert journal[72:104]==hashlib.sha256(journal[:72]+bytes(32)+journal[104:]).digest();root=b'/Applications/Windows/'+journal[104:144].split(b'\0')[0];entries={e.path:e for e in v.entries if e.kind};assert root+b'/product.bin'in entries and root+b'/.EngacerMSI/transaction.bin'not in entries;checks+=3
   reference=next(p for p in originals if p['package_sha256']==hashlib.sha256(raw).hexdigest());remaining=list(reference['all_file_sha256'].values());at=1024;files=0;links=0;registry_rows=0
   while at<n:
    kind,count=struct.unpack_from('<II',journal,at)
    if kind in [1,3]:
     relative=journal[at+8:at+264].split(b'\0')[0];digest=journal[at+264:at+296].hex();length,flags=struct.unpack_from('<QI',journal,at+296);basepath=root if kind==1 else b'/Data/Windows/Common/Programs'if flags else b'/Users/Owner';entry=entries[basepath+b'/'+relative];actual=hashlib.sha256(disk.data[entry.first*4096:entry.first*4096+entry.size]).hexdigest();assert actual==digest and length==entry.size;checks+=2
     if kind==1 and flags==1:assert actual in remaining;remaining.remove(actual);files+=1;checks+=1
     elif kind==3:links+=1
    elif kind==2:registry_rows+=1
    at+=count
   assert not remaining and files==106 and links==2 and registry_rows==16;checks+=4
   # Existing product refuses before any filesystem or registry publication.
   disk_before=hashlib.sha256(disk.data).digest();allocated=state['bytes'];assert lib.install_controller147()==1638;assert hashlib.sha256(disk.data).digest()==disk_before and state['bytes']==allocated;checks+=3
   assert lib.installed_undo_registry147()==0;checks+=1
   samples.append(dict(package=package.name,payloads=files,shortcuts=links,registry_rows=registry_rows,journal_bytes=n,journal_sha256=hashlib.sha256(journal).hexdigest(),registered_after_verification=True,duplicate_refused=True));lib.files_close147();lib.close147();assert not live and state['bytes']==0 and not state['bad'];checks+=1
  assert not registry_state['error'];report=dict(passed=True,checks=checks,scope='Production fresh-install controller, MSI/CAB, V6 and kernel stream/rename routines with confined real Windows registry adapter; host supporting test only, native controller/removal/custom actions remain unqualified',packages=samples,peak_host_tracked_bytes=state['peak'],retained_host_tracked_bytes=state['bytes'],sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources+['tests/m14/install147_host.py','tests/m14/registry147_adapter.py','user/windows8/msi-install147.h','user/windows8/msi-condition147.h','kernel/windows8/transaction147.inc']});(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS original MSI fresh-install controller',checks)
 finally:cleanup()
if __name__=='__main__':main()
