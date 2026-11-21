"""Original MSI/CAB staging, immutable ownership, and extent promotion on actual V6."""
import ctypes as c,hashlib,importlib.util,json,os,re,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'tools/build'),str(ROOT/'tests/m6')]
from m1 import command,pinned_tools
spec=importlib.util.spec_from_file_location('files147_disk',ROOT/'tests/m11/volume_host.py');storage=importlib.util.module_from_spec(spec);spec.loader.exec_module(storage);Volume=storage.Volume

def main():
 out=ROOT/'build/m14-native/stage7/terminal-host';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools();objects=[]
 sources=['user/windows8/msi-actions147.c','user/windows8/msi-remove147.c','user/windows8/msi-install147.c','user/windows8/msi-registry147.c','user/windows8/msi-files147.c','user/windows8/msi-shortcuts147.c','user/windows8/msi-journal147.c','user/windows8/msi-plan147.c','user/windows8/msi-cost147.c','user/windows8/msi_db.c','user/windows8/cab147.c','third_party/libmspack/lzxd.c','runtime/sha256.c','kernel/storage/volume6.c','tests/m14/files147_host.c']
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
 lib.init147.argtypes=[Alloc,Free,Failure];lib.init147(allocate,release,failure);lib.open147.argtypes=[c.c_void_p,c.c_uint];lib.cost147.argtypes=[c.c_char_p];lib.set147.argtypes=[c.c_char_p,c.c_char_p];lib.files_init147.argtypes=[c.POINTER(Volume),Size,c.c_void_p,c.c_uint];lib.journal_data147.restype=c.c_void_p;lib.fixture_write147.argtypes=[c.c_char_p,c.c_void_p,c.c_uint];lib.access_role147.argtypes=[c.c_uint,c.c_char_p,c.c_uint]
 lib.v6_format.argtypes=[c.POINTER(Volume)];lib.v6_mkdir.argtypes=[c.POINTER(Volume),c.c_char_p];lib.v6_mount.argtypes=[c.POINTER(Volume)]
 from registry147_adapter import create
 registry,cleanup,registry_state=create();lib.files_registry147.argtypes=[type(registry)];lib.files_registry147(registry)
 package=ROOT/'third_party/7zip/7z2606-x64.msi';raw=package.read_bytes();data=c.create_string_buffer(raw);checks=0;cases=[]
 try:
  for mode in ['pending','cache','private','root','done','bad-checksum','wrong-user','wrong-product','late-file','damaged-pending','late-cache']:
   lib.open147(data,len(raw));assert lib.set147(b'ALLUSERS',b'1')==0 and lib.set147(b'Privileged',b'1')==0;lib.cost147(b'C:\\Users\\Owner');disk=storage.Disk(bytearray(64*1024*1024));v=disk.volume();assert lib.v6_format(c.byref(v))==0
   for path in [b'/Applications',b'/Applications/Windows',b'/Users',b'/Users/Owner',b'/Users/Owner/Documents']:assert lib.v6_mkdir(c.byref(v),path)==0
   lib.files_init147(c.byref(v),size,data,len(raw));assert lib.install_controller147()==0;root=b'/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}';done=b'/Data/Windows/Transactions/{23170F69-40C1-2702-2606-000001000000}.done';other=b'/Data/Windows/Transactions/{13170F69-40C1-2702-2606-000001000000}.done'
   for role in [2,4]:
    for write in [0,1]:assert lib.access_role147(role,done,write)==1 and lib.access_role147(role,other,write)==0;checks+=2
   for write in [0,1]:assert lib.access_role147(3,done,write)==0;checks+=1
   if mode=='cache':lib.terminal_delete_fault147_set(1)
   elif mode=='private':lib.terminal_delete_fault147_set(2)
   elif mode=='root':lib.terminal_delete_fault147_set(3)
   elif mode=='done':lib.terminal_delete_fault147_set(4)
   else:lib.remove_pending_delete_fault147(1)
   assert lib.remove_controller147()==1117;entries={e.path:e for e in v.entries if e.kind};assert done in entries and lib.keep147()==2;entry=entries[done];image=bytes(disk.data[entry.first*4096:entry.first*4096+entry.size]);assert image[72:104]==hashlib.sha256(image[:72]+bytes(32)+image[104:]).digest();checks+=4
   if mode=='done':assert not any(path==root or path.startswith(root+b'/')for path in entries);checks+=1
   elif mode!='cache':assert root+b'/.EngacerMSI/source.msi'not in entries;checks+=1
   before=hashlib.sha256(disk.data).digest();assert lib.reinstall_controller147()==1618 and hashlib.sha256(disk.data).digest()==before;checks+=2
   if mode in ['bad-checksum','wrong-user','wrong-product']:
    corrupt=bytearray(image)
    if mode=='bad-checksum':corrupt[72]^=1
    else:
     if mode=='wrong-user':corrupt[144:400]=b'/Users/Other'+bytes(256-len(b'/Users/Other'))
     else:corrupt[104:144]=b'{13170F69-40C1-2702-2606-000001000000}'+bytes(2)
     corrupt[72:104]=bytes(32);corrupt[72:104]=hashlib.sha256(corrupt).digest()
    bad=c.create_string_buffer(bytes(corrupt));assert lib.fixture_write147(done,bad,len(corrupt))==0;before=hashlib.sha256(disk.data).digest();assert lib.finish_controller147()==13 and hashlib.sha256(disk.data).digest()==before;good=c.create_string_buffer(image);assert lib.fixture_write147(done,good,len(image))==0;checks+=4
   extra=None
   if mode in ['late-file','damaged-pending','late-cache']:
    extra=root+(b'/Late personal document.txt'if mode=='late-file'else b'/.EngacerMSI/transaction.bin'if mode=='damaged-pending'else b'/.EngacerMSI/source.msi');value=b'personal data arriving after semantic undo';buffer=c.create_string_buffer(value);assert lib.fixture_write147(extra,buffer,len(value))==0;checks+=1
   registry_calls=registry_state['calls'];terminal_status=lib.finish_controller147();assert registry_state['calls']==registry_calls;checks+=1;assert terminal_status==0,(mode,terminal_status);entries={e.path:e for e in v.entries if e.kind};assert done not in entries and not any(path==root or path.startswith(root+b'/')for path in entries);assert lib.keep147()==0;checks+=4
   if extra:
    recovered=b'/Users/Owner/Documents/Recovered applications/'+root.rsplit(b'/',1)[1]+b'/';saved=[]
    for path,entry in entries.items():
     if path.startswith(recovered)and entry.kind==1:
      actual=bytes(disk.data[entry.first*4096:entry.first*4096+entry.size])
      if actual==value:saved.append(path.decode())
    assert len(saved)==1 and lib.remove_kept147()==1;checks+=2
   assert lib.reinstall_controller147()==0 and lib.remove_controller147()==0;checks+=2;cases.append(dict(mode=mode,source_free_cleanup=True,reinstall_succeeds=True,late_data_preserved=extra is not None));lib.files_close147();lib.close147();assert not live and state['bytes']==0;checks+=1
  report=dict(passed=True,checks=checks,cases=cases,scope='Production completion record, cached-source cleanup and real kernel path grants/V6 with confined Windows registry adapter; all parsed MSI/source state is discarded before terminal retry. Supporting host tests, not native tail-fault qualification.',sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources+['tests/m14/registry147_adapter.py','user/windows8/msi-remove147.h','user/windows8/msi-journal147.h','include/engine/wintxn147.h','tests/m14/terminal147_host.py','kernel/windows8/path-access147.inc','kernel/windows8/transaction147.inc','include/engine/winproduct147.h']});(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS terminal cleanup without source and protected completion grants',checks)
 finally:cleanup()
if __name__=='__main__':main()
