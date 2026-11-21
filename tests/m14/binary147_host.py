"""Original MSI plans through the production builder, byte oracle and I/O fault adapter."""
import ctypes,hashlib,json,os,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools

def main():
 out=ROOT/'build/m14-native/stage7/binary-host';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools();objects=[]
 sources=['user/windows8/msi-plan147.c','user/windows8/msi-cost147.c','user/windows8/msi_db.c','runtime/sha256.c','tests/m14/binary147_host.c']
 for source in sources:
  obj=out/(Path(source).stem+'.obj');command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-I',ROOT/'include','-c',ROOT/source,'-o',obj]);objects.append(obj)
 dll=out/'binary.dll';command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(dll),*objects]);lib=ctypes.CDLL(str(dll))
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
 lib.init147.argtypes=[Alloc,Free,Failure];lib.init147(allocate,release,failure);lib.open147.argtypes=[ctypes.c_void_p,ctypes.c_uint];lib.binary_stream147.argtypes=[ctypes.c_char_p,ctypes.POINTER(ctypes.c_void_p)];lib.binary_free147.argtypes=[ctypes.c_void_p]
 package=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/npp.8.9.9.1.Installer.x64.msi';raw=package.read_bytes();source=ctypes.create_string_buffer(raw);lib.open147(source,len(raw));baseline=state['bytes'];results=[]
 for name in [b'Binary.Wix4UtilCA_X64',b'Wix4UtilCA_X64',b'Binary.DoesNotExist']:
  output=ctypes.c_void_p();n=lib.binary_stream147(name,ctypes.byref(output))
  if name==b'Binary.Wix4UtilCA_X64':
   assert n==423704;data=ctypes.string_at(output,n);digest=hashlib.sha256(data).hexdigest();assert digest=='54febbd1f0a3875df16a4b88621cc0a10729b3c94b9a68639aab27d36fe39381';assert data==(Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/msi-streams/npp.8.9.9.1.Installer.x64/Wix4UtilCA_X64.bin').read_bytes();checks+=3;results.append(dict(stream=name.decode(),bytes=n,sha256=digest,independent_extractor_bytes_match=True))
  else:assert n==0 and not output.value;checks+=1
  lib.binary_free147(output);assert state['bytes']==baseline;checks+=1
 lib.close147();assert not live and state['bytes']==0 and not state['bad'];checks+=1
 report=dict(passed=True,checks=checks,scope='Read the actual original MSI Binary stream with the production reader and compare independent extraction. Opaque data only: no vendor code, installer or DLL executes on host.',package_sha256=hashlib.sha256(raw).hexdigest(),streams=results,retained_host_tracked_bytes=state['bytes'],sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources+['tests/m14/binary147_host.py','user/windows8/msi_db.h']});(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS actual original MSI Binary stream extraction',checks)
if __name__=='__main__':main()
