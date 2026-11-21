"""Original MSI/CAB staging, immutable ownership, and extent promotion on actual V6."""
import ctypes as c,hashlib,importlib.util,json,os,re,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'tools/build'),str(ROOT/'tests/m6')]
from m1 import command,pinned_tools
spec=importlib.util.spec_from_file_location('files147_disk',ROOT/'tests/m11/volume_host.py');storage=importlib.util.module_from_spec(spec);spec.loader.exec_module(storage);Volume=storage.Volume

def main():
 out=ROOT/'build/m14-native/stage7/remove-host';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools();objects=[]
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
 lib.init147.argtypes=[Alloc,Free,Failure];lib.init147(allocate,release,failure);lib.open147.argtypes=[c.c_void_p,c.c_uint];lib.cost147.argtypes=[c.c_char_p];lib.set147.argtypes=[c.c_char_p,c.c_char_p];lib.files_init147.argtypes=[c.POINTER(Volume),Size,c.c_void_p,c.c_uint];lib.journal_data147.restype=c.c_void_p;lib.fixture_write147.argtypes=[c.c_char_p,c.c_void_p,c.c_uint];lib.fixture_delete147.argtypes=[c.c_char_p]
 lib.v6_format.argtypes=[c.POINTER(Volume)];lib.v6_mkdir.argtypes=[c.POINTER(Volume),c.c_char_p];lib.v6_mount.argtypes=[c.POINTER(Volume)]
 from registry147_adapter import create
 registry,cleanup,registry_state=create();lib.files_registry147.argtypes=[type(registry)];lib.files_registry147(registry)
 originals=json.loads((ROOT/'evidence/M14/7/development/cab-host-initial.json').read_text(encoding='utf-8'))['originals'];metadata=json.loads((ROOT/'evidence/M14/7/development/msi-tables147.json').read_text(encoding='utf-8-sig'))['packages'];checks=0;samples=[]
 packages=[ROOT/'third_party/7zip/7z2606-x64.msi',Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/npp.8.9.9.1.Installer.x64.msi']
 try:
  for index,package in enumerate(packages):
   raw=package.read_bytes();data=c.create_string_buffer(raw);lib.open147(data,len(raw));assert lib.set147(b'ALLUSERS',b'1')==0 and lib.set147(b'Privileged',b'1')==0;
   if index==2:assert lib.set147(b'NPP_LANG',b'french')==0
   lib.cost147(b'C:\\Users\\Owner')
   disk=storage.Disk(bytearray(64*1024*1024));v=disk.volume();assert lib.v6_format(c.byref(v))==0
   for path in [b'/Applications',b'/Applications/Windows']:assert lib.v6_mkdir(c.byref(v),path)==0
   lib.files_init147(c.byref(v),size,data,len(raw));before=hashlib.sha256(disk.data).digest();base=state['bytes']
   if index<2:
    for shape in range(2 if index==0 else 3):assert lib.install_order_fixture147(shape)==50 and hashlib.sha256(disk.data).digest()==before;checks+=2
   status=lib.install_unknown_body147() if index==2 else lib.install_controller147()
   if index==2:
    assert status==50 and hashlib.sha256(disk.data).digest()==before;(samples.append(dict(package=package.name,refused_custom_actions_before_effects=True)));checks+=3;lib.files_close147();lib.close147();continue
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
   tables=next(p['tables']for p in metadata if p['file']==package.name);enabled={r[0]for r in tables['Feature']if 0<int(r[5])<=1};selected_components={r[1]for r in tables['FeatureComponents']if r[0]in enabled};expected_registry=sum(r[5]in selected_components for r in tables['Registry'])
   assert not remaining and files==(106 if index==0 else 217) and links==(2 if index==0 else 1) and registry_rows==expected_registry,(package.name,len(remaining),files,links,registry_rows);checks+=4
   # Existing product refuses before any filesystem or registry publication.
   disk_before=hashlib.sha256(disk.data).digest();allocated=state['bytes'];assert lib.install_controller147()==1638;assert hashlib.sha256(disk.data).digest()==disk_before and state['bytes']==allocated;checks+=3
   # A damaged cache must refuse before any external undo or record retirement.
   cache=root+b'/.EngacerMSI/source.msi';bad_source=c.create_string_buffer(b'damaged source cache');assert lib.fixture_write147(cache,bad_source,len(bad_source.raw)-1)==0;damaged_disk=hashlib.sha256(disk.data).digest();assert lib.remove_controller147()==23;assert hashlib.sha256(disk.data).digest()==damaged_disk;assert lib.fixture_write147(cache,data,len(raw))==0;checks+=4
   changed={root+(b'/7zFM.exe'if index==0 else b'/notepad++.exe'):b'my modified application binary',root+b'/User-\xc3\xa9\xf0\x9f\x9a\x80.txt':b'my own Unicode-named document'}
   link_path=next(path for path in entries if path.endswith(b'.lnk'));changed[link_path]=b'my customized shortcut'
   if index==0:changed[root+b'/Large personal file.bin']=bytes((n*17+5)&255 for n in range(256))*(33*1024*1024//256)
   personal=b'/Users/Owner/Documents/Personal.txt';personal_data=c.create_string_buffer(b'outside the application');assert lib.fixture_write147(personal,personal_data,len(personal_data.raw)-1)==0
   for path,value in changed.items():buffer=c.create_string_buffer(value);assert lib.fixture_write147(path,buffer,len(value))==0
   # Interrupt the first preservation move after the journal/buddy are durable.
   lib.remove_move_fault147(1);assert lib.remove_controller147()==1117;partial={e.path:e for e in v.entries if e.kind};assert root+b'/.EngacerMSI/transaction.bin'in partial and root+b'/product.bin'not in partial;checks+=3
   recovery_prefix=b'/Users/Owner/Documents/Recovered applications/'+root.rsplit(b'/',1)[1]+b'/'
   buddy_path=next(path for path in partial if path.startswith(recovery_prefix)and path.endswith(b'.txt'));buddy_entry=partial[buddy_path];buddy_bytes=bytes(disk.data[buddy_entry.first*4096:buddy_entry.first*4096+buddy_entry.size]);foreign=c.create_string_buffer(b'foreign file: never overwrite')
   assert lib.fixture_write147(buddy_path,foreign,len(foreign.raw)-1)==0;collision_disk=hashlib.sha256(disk.data).digest();assert lib.remove_controller147()==183 and hashlib.sha256(disk.data).digest()==collision_disk;original_buddy=c.create_string_buffer(buddy_bytes);assert lib.fixture_write147(buddy_path,original_buddy,len(buddy_bytes))==0;checks+=4
   assert lib.fixture_write147(buddy_path[:-4],foreign,len(foreign.raw)-1)==0;collision_disk=hashlib.sha256(disk.data).digest();assert lib.remove_controller147()==183 and hashlib.sha256(disk.data).digest()==collision_disk;assert lib.fixture_delete147(buddy_path[:-4])==0;checks+=4
   # Reopen the source, journal and properties as a fresh worker before retrying.
   assert lib.remove_controller147()==0,(package.name,registry_state);assert lib.remove_kept147()==len(changed);remaining_entries={e.path:e for e in v.entries if e.kind};assert not any(path==root or path.startswith(root+b'/')for path in remaining_entries);checks+=3
   recovery=b'/Users/Owner/Documents/Recovered applications/'+root.rsplit(b'/',1)[1]+b'/';preserved={}
   for path,entry in remaining_entries.items():
    if entry.kind!=1 or not path.startswith(recovery):continue
    value=bytes(disk.data[entry.first*4096:entry.first*4096+entry.size])
    if value.startswith(b'Preserved application file\n'):
     original=re.search(rb'Original path: ([^\n]+)\n',value)[1];wanted=changed[original];assert b'Bytes: '+str(len(wanted)).encode()+b'\n'in value and hashlib.sha256(wanted).hexdigest().encode()in value;target=remaining_entries[path[:-4]];actual=bytes(disk.data[target.first*4096:target.first*4096+target.size]);assert actual==wanted;preserved[original.decode()]=dict(backup=path[:-4].decode(),sha256=hashlib.sha256(actual).hexdigest(),bytes=len(actual));checks+=3
   assert len(preserved)==len(changed);outside=remaining_entries[personal];assert bytes(disk.data[outside.first*4096:outside.first*4096+outside.size])==b'outside the application';checks+=2
   assert lib.reinstall_controller147()==0;assert lib.installed_read147()==0 and lib.verify147()==0;checks+=3
   duplicate_path=next(iter(changed));duplicate_data=c.create_string_buffer(changed[duplicate_path]);assert lib.fixture_write147(duplicate_path,duplicate_data,len(changed[duplicate_path]))==0
   assert lib.remove_controller147()==0 and lib.remove_kept147()==1;checks+=2
   interrupted=[]
   for fault_at in [1,files+1,files+links+1]:
    lib.install_promote_fault147(fault_at);assert lib.reinstall_controller147()==1117;partial={e.path:e for e in v.entries if e.kind};assert root+b'/.EngacerMSI/transaction.bin'in partial and root+b'/product.bin'not in partial;assert lib.remove_controller147()==0;assert not any(e.kind and(e.path==root or e.path.startswith(root+b'/'))for e in v.entries);interrupted.append(fault_at);checks+=4
   samples.append(dict(package=package.name,payloads=files,shortcuts=links,registry_rows=registry_rows,journal_bytes=n,journal_sha256=hashlib.sha256(journal).hexdigest(),registered_after_verification=True,duplicate_refused=True,preserved=preserved,interrupted_preservation_retried=True,reinstall_after_preservation=True,interrupted_install_recovery_move_positions=interrupted));lib.files_close147();lib.close147();assert not live and state['bytes']==0 and not state['bad'];checks+=1
  assert not registry_state['error'];report=dict(passed=True,checks=checks,scope='Production install/remove controllers, MSI/CAB, actual V6 and stream/rename helpers with explicit host syscall adapters with confined real Windows registry adapter; host supporting test only, native removal/recovery, Windows file metadata preservation and selected deferred custom bodies remain unqualified',packages=samples,peak_host_tracked_bytes=state['peak'],retained_host_tracked_bytes=state['bytes'],sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources+['kernel/windows8/path-access147.inc','include/engine/winproduct147.h','tests/m14/remove147_host.py','user/windows8/msi-remove147.h','user/windows8/msi-journal147.h','user/windows8/msi-files147.h','tests/m14/registry147_adapter.py','user/windows8/msi-install147.h','user/windows8/msi-condition147.h','kernel/windows8/transaction147.inc']});(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS original MSI removal/preservation/retry/reinstall',checks)
 finally:cleanup()
if __name__=='__main__':main()
