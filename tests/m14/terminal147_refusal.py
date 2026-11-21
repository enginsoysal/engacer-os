"""Original MSI/CAB staging, immutable ownership, and extent promotion on actual V6."""
import ctypes as c,hashlib,importlib.util,json,os,re,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'tools/build'),str(ROOT/'tests/m6')]
from m1 import command,pinned_tools
spec=importlib.util.spec_from_file_location('files147_disk',ROOT/'tests/m11/volume_host.py');storage=importlib.util.module_from_spec(spec);spec.loader.exec_module(storage);Volume=storage.Volume

def main():
 out=ROOT/'build/m14-native/stage7/terminal-refusal';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools();objects=[]
 sources=['user/windows8/msi-remove147.c','user/windows8/msi-install147.c','user/windows8/msi-registry147.c','user/windows8/msi-files147.c','user/windows8/msi-shortcuts147.c','user/windows8/msi-journal147.c','user/windows8/msi-plan147.c','user/windows8/msi-cost147.c','user/windows8/msi_db.c','user/windows8/cab147.c','third_party/libmspack/lzxd.c','runtime/sha256.c','kernel/storage/volume6.c','tests/m14/files147_host.c']
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
 package=ROOT/'third_party/7zip/7z2606-x64.msi';raw=package.read_bytes();data=c.create_string_buffer(raw);lib.open147(data,len(raw));assert lib.set147(b'ALLUSERS',b'1')==0 and lib.set147(b'Privileged',b'1')==0;lib.cost147(b'C:\\Users\\Owner');disk=storage.Disk(bytearray(64*1024*1024));v=disk.volume();assert lib.v6_format(c.byref(v))==0
 for path in [b'/Applications',b'/Applications/Windows']:assert lib.v6_mkdir(c.byref(v),path)==0
 try:
  lib.files_init147(c.byref(v),size,data,len(raw));assert lib.install_controller147()==0;root=b'/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}';lib.remove_pending_delete_fault147(1);assert lib.remove_controller147()==1117;entries={e.path:e for e in v.entries if e.kind};assert root+b'/.EngacerMSI/transaction.bin'in entries and root+b'/.EngacerMSI/source.msi'not in entries;assert lib.remove_controller147()==2
  report=dict(passed=False,reproduced=True,scope='Before-fix host reproduction: cache deletion succeeded, the next pending-record deletion failed, and retry refused because the original cached source was already gone. No user data loss was observed; automatic cleanup/reinstall remains blocked.',package_sha256=hashlib.sha256(raw).hexdigest(),sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources+['tests/m14/terminal147_refusal.py']});(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('REPRODUCED terminal cleanup refusal after source-cache deletion');lib.files_close147();lib.close147();assert not live
 finally:cleanup()
if __name__=='__main__':main()
