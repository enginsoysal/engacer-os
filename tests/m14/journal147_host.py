"""Original MSI plans through the production builder, byte oracle and I/O fault adapter."""
import ctypes,hashlib,json,os,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools

def main():
 out=ROOT/'build/m14-native/stage7/journal-host';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools();objects=[]
 sources=['user/windows8/msi-journal147.c','user/windows8/msi-plan147.c','user/windows8/msi-cost147.c','user/windows8/msi_db.c','runtime/sha256.c','tests/m14/journal147_host.c']
 for source in sources:
  obj=out/(Path(source).stem+'.obj');command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-I',ROOT/'include','-c',ROOT/source,'-o',obj]);objects.append(obj)
 dll=out/'journal.dll';command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(dll),*objects]);lib=ctypes.CDLL(str(dll))
 Alloc=ctypes.CFUNCTYPE(ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t);Free=ctypes.CFUNCTYPE(None,ctypes.c_void_p,ctypes.c_void_p);Failure=ctypes.CFUNCTYPE(None,ctypes.c_char_p);Size=ctypes.CFUNCTYPE(ctypes.c_size_t,ctypes.c_void_p);live={};state=dict(bytes=0,peak=0,fail_after=-1,bad=False);checks=0
 @Alloc
 def allocate(context,n):
  if state['fail_after']==0:return None
  if state['fail_after']>0:state['fail_after']-=1
  b=ctypes.create_string_buffer(n);address=ctypes.addressof(b);live[address]=(b,n);state['bytes']+=n;state['peak']=max(state['peak'],state['bytes']);return address
 @Free
 def release(context,address):
  if address not in live:state['bad']=True;return
  state['bytes']-=live.pop(address)[1]
 @Size
 def size(address):return live[address][1]
 @Failure
 def failure(message):
  (out/'unexpected-refusal.json').write_bytes(json.dumps(dict(passed=False,error=message.decode())).encode());os._exit(87)
 lib.init147.argtypes=[Alloc,Free,Failure];lib.init147(allocate,release,failure);lib.journal_init147.argtypes=[Size];lib.journal_init147(size);lib.open147.argtypes=[ctypes.c_void_p,ctypes.c_uint];lib.cost147.argtypes=[ctypes.c_char_p];lib.set147.argtypes=[ctypes.c_char_p,ctypes.c_char_p];lib.journal_file147.argtypes=[ctypes.c_char_p,ctypes.c_uint64,ctypes.c_void_p,ctypes.c_uint];lib.journal_data147.restype=ctypes.c_void_p;lib.get147.argtypes=[ctypes.c_char_p];lib.get147.restype=ctypes.c_char_p
 packages=[ROOT/'third_party/7zip/7z2606-x64.msi',Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/npp.8.9.9.1.Installer.x64.msi'];samples=[]
 for package in packages:
  raw=package.read_bytes();source=ctypes.create_string_buffer(raw);lib.open147(source,len(raw));assert lib.set147(b'ALLUSERS',b'1')==0;lib.cost147(b'C:\\Users\\Owner');baseline=state['bytes']
  for fail_after in range(18):
   state['fail_after']=fail_after
   if lib.journal_create147():
    digest=ctypes.create_string_buffer(hashlib.sha256(raw).digest())
    lib.journal_file147(b'.EngacerMSI/source.msi',len(raw),digest,4);lib.journal_properties147();lib.journal_seal147();lib.journal_close147()
   assert state['bytes']==baseline and not state['bad'];checks+=1
  state['fail_after']=-1;assert lib.journal_create147();digest=ctypes.create_string_buffer(hashlib.sha256(raw).digest());assert lib.journal_file147(b'.EngacerMSI/source.msi',len(raw),digest,4)==0;assert lib.journal_properties147()==0;assert lib.journal_seal147()==0;checks+=4
  n=lib.journal_bytes147();data=ctypes.string_at(lib.journal_data147(),n);assert n<131072;assert data[40:72]==hashlib.sha256(raw).digest();assert data[72:104]==hashlib.sha256(data[:72]+bytes(32)+data[104:]).digest();checks+=3
  # Independently decode every recorded property and preserve exact case/value bytes.
  at=1024;actual={};cache=0
  while at<n:
   kind,count=struct.unpack_from('<II',data,at);assert count>=8 and count%8==0 and at+count<=n
   if kind==5:
    a,b=struct.unpack_from('<II',data,at+8);name=data[at+16:at+16+a-1].decode();value=data[at+16+a:at+16+a+b-1].decode();assert name not in actual;actual[name]=value
   elif kind==1:cache+=1;assert data[at+8:at+264].split(b'\0')[0]==b'.EngacerMSI/source.msi'
   else:raise AssertionError(kind)
   at+=count;checks+=1
  assert at==n and cache==1 and actual['ProductName'] and actual['ALLUSERS']=='1' and actual['ProgramMenuFolder']==r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs'+'\\';checks+=1
  for fault,wanted in [(1,5),(2,29),(3,1117),(4,1117),(5,1117),(0,0)]:assert lib.journal_write147(fault)==wanted;checks+=1
  assert lib.journal_read147(0)==1 and lib.journal_read147(1)==0;checks+=2
  samples.append(dict(package=package.name,source_sha256=hashlib.sha256(raw).hexdigest(),journal_bytes=n,properties=len(actual),journal_sha256=hashlib.sha256(data).hexdigest()));lib.journal_close147();assert state['bytes']==baseline;lib.close147();assert not live and state['bytes']==0 and not state['bad'];checks+=2
  # Reopen the original source and reconstruct the exact selection atomically.
  lib.open147(source,len(raw));assert lib.journal_import_image147()==0;checks+=1
  for fail_after in range(61):
   state['fail_after']=-1;assert lib.set147(b'EngacerUserSentinel',b'keep until successful restore')==0;baseline=state['bytes'];state['fail_after']=fail_after;status=lib.journal_restore147();state['fail_after']=-1
   if status==8:assert lib.get147(b'EngacerUserSentinel')==b'keep until successful restore' and state['bytes']==baseline
   else:assert status==0 and not lib.get147(b'EngacerUserSentinel') and lib.get147(b'ProductVersion')==actual['ProductVersion'].encode()
   assert not state['bad'];checks+=3
  assert lib.journal_restore147()==0;lib.cost147(b'C:\\Users\\Owner');assert lib.journal_restore147()==87;checks+=2
  lib.journal_close147();lib.close147();assert not live and state['bytes']==0;checks+=1
 report=dict(passed=True,checks=checks,scope='Production builder and original MSI properties with independent binary/SHA decoding, allocation failures, atomic selection restoration before recosting and simulated I/O faults; native durable filesystem recovery remains unqualified',packages=samples,peak_host_tracked_bytes=state['peak'],retained_host_tracked_bytes=state['bytes'],sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources+['user/windows8/msi-journal147.h','include/engine/wintxn147.h','tests/m14/journal147_host.py']});(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS journal builder',checks)
if __name__=='__main__':main()
