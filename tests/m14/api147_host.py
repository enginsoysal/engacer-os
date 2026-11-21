"""Call production native MSI exports with original database data and real host locks.

Only Engacer-authored functions execute. This is supporting host API evidence,
not original installer/custom-action or native OS qualification.
"""
import concurrent.futures,ctypes,hashlib,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command

def main():
 out=ROOT/'build/m14-native/stage7/api-host';out.mkdir(parents=True,exist_ok=True);t=pinned_tools();objects=[]
 definition=out/'kernel32.def';definition.write_bytes(b'LIBRARY kernel32.dll\nEXPORTS\nInitializeCriticalSection\nEnterCriticalSection\nLeaveCriticalSection\nDeleteCriticalSection\n')
 command([t['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/'kernel32.lib')])
 sources=['user/windows8/msi-api147.c','user/windows8/msi-plan147.c','user/windows8/msi-cost147.c','user/windows8/msi_db.c','runtime/sha256.c','tests/m14/api147_host.c']
 for source in sources:
  obj=out/(Path(source).stem+'.obj');command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-I',ROOT/'include','-c',ROOT/source,'-o',obj]);objects.append(obj)
 command([t['lld-link'],'/dll','/entry:EngacerMsiDllEntry147','/nodefaultlib','/timestamp:0','/out:'+str(out/'api.dll'),*objects,out/'kernel32.lib']);lib=ctypes.CDLL(str(out/'api.dll'))
 alloc_type=ctypes.CFUNCTYPE(ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t);free_type=ctypes.CFUNCTYPE(None,ctypes.c_void_p,ctypes.c_void_p);failure_type=ctypes.CFUNCTYPE(None,ctypes.c_char_p);live={};state={'bytes':0,'peak':0,'bad_free':False,'fail':False}
 @alloc_type
 def allocate(context,n):
  if state['fail']:return None
  buf=ctypes.create_string_buffer(n);address=ctypes.addressof(buf);live[address]=(buf,n);state['bytes']+=n;state['peak']=max(state['peak'],state['bytes']);return address
 @free_type
 def release(context,address):
  if address not in live:state['bad_free']=True;return
  state['bytes']-=live.pop(address)[1]
 @failure_type
 def failure(message):print('Unexpected fatal refusal',message,flush=True);os._exit(87)
 lib.init147.argtypes=[alloc_type,free_type,failure_type];lib.open147.argtypes=[ctypes.c_void_p,ctypes.c_uint];lib.init147(allocate,release,failure)
 U=ctypes.c_uint;P=ctypes.c_void_p;W=ctypes.c_wchar_p
 signatures={'MsiCreateRecord':[U],'MsiCloseHandle':[U],'MsiRecordSetStringW':[U,U,W],'MsiRecordSetStringA':[U,U,ctypes.c_char_p],'MsiRecordGetStringW':[U,U,P,ctypes.POINTER(U)],'MsiRecordGetInteger':[U,U],'MsiRecordSetInteger':[U,U,ctypes.c_int32],'MsiRecordDataSize':[U,U],'MsiRecordIsNull':[U,U],'MsiRecordClearData':[U],'MsiRecordGetFieldCount':[U],'MsiGetPropertyW':[U,W,P,ctypes.POINTER(U)],'MsiGetPropertyA':[U,ctypes.c_char_p,P,ctypes.POINTER(U)],'MsiSetPropertyW':[U,W,W],'MsiEvaluateConditionW':[U,W],'MsiProcessMessage':[U,U,U]}
 for name,args in signatures.items():getattr(lib,name).argtypes=args
 lib.MsiCreateRecord.restype=U;lib.bind147.restype=U;checks=0;packages=[]
 def check(v):
  nonlocal checks
  assert v;checks+=1
 for path in [ROOT/'third_party/7zip/7z2606-x64.msi',Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/npp.8.9.9.1.Installer.x64.msi']:
  data=path.read_bytes();buf=ctypes.create_string_buffer(data);lib.open147(buf,len(data));h=lib.bind147();check(h!=0);before=state['bytes']
  for prop in ['ProductName','ProductCode','Missing']:
   output=ctypes.create_unicode_buffer(128);size=U(128);check(lib.MsiGetPropertyW(h,prop,output,ctypes.byref(size))==0 and size.value==len(output.value));check(bool(output.value)==(prop!='Missing'))
  text='Euro \u20ac Smile \U0001f600';check(lib.MsiSetPropertyW(h,'TestUnicode',text)==0);size=U(0);output=ctypes.create_unicode_buffer(1);check(lib.MsiGetPropertyW(h,'TestUnicode',output,ctypes.byref(size))==234 and size.value==len(text.encode('utf-16-le'))//2)
  output=ctypes.create_unicode_buffer(size.value+1);size=U(len(output));check(lib.MsiGetPropertyW(h,'TestUnicode',output,ctypes.byref(size))==0 and output.value==text)
  check(lib.MsiEvaluateConditionW(h,'TestUnicode AND NOT Missing')==1 and lib.MsiEvaluateConditionW(h,'Bad === 2')==3)
  record=lib.MsiCreateRecord(2);check(record!=0 and lib.MsiRecordGetFieldCount(record)==2);check(lib.MsiRecordSetStringW(record,0,text)==0 and lib.MsiRecordDataSize(record,0)==len(text.encode('utf-16-le'))//2)
  for cap in [0,1,3,20,64]:
   output=ctypes.create_unicode_buffer(max(cap,1));size=U(cap);code=lib.MsiRecordGetStringW(record,0,output,ctypes.byref(size));check(code==(0 if cap>len(text.encode('utf-16-le'))//2 else 234))
   if cap:output.value.encode('utf-16-le');checks+=1
  check(lib.MsiRecordSetInteger(record,1,-123)==0 and lib.MsiRecordGetInteger(record,1)==-123);check(lib.MsiRecordIsNull(record,2)==1)
  check(lib.MsiProcessMessage(h,0x04000000,record)==0 and lib.MsiProcessMessage(h,0x09000000,record)==-1)
  state['fail']=True;check(lib.MsiRecordSetStringW(record,0,'replacement')==8);state['fail']=False
  size=U(64);output=ctypes.create_unicode_buffer(64);check(lib.MsiRecordGetStringW(record,0,output,ctypes.byref(size))==0 and output.value==text)
  check(lib.MsiCloseHandle(record)==0 and lib.MsiCloseHandle(record)==6);check(lib.MsiSetPropertyW(h,'TestUnicode',None)==0 and state['bytes']==before)
  def threaded(index):
   for n in range(200):
    r=lib.MsiCreateRecord(1);assert r and lib.MsiRecordSetInteger(r,1,index*200+n)==0 and lib.MsiRecordGetInteger(r,1)==index*200+n and lib.MsiCloseHandle(r)==0
   return 800
  with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:checks+=sum(pool.map(threaded,range(4)))
  check(state['bytes']==before);r=lib.MsiCreateRecord(1);check(r!=0);lib.unbind147();check(lib.MsiCloseHandle(r)==6 and lib.MsiSetPropertyW(h,'stale','bad')==6);lib.close147();check(not live and state['bytes']==0 and not state['bad_free']);packages.append(dict(file=path.name,sha256=hashlib.sha256(data).hexdigest()))
 sources+=['user/windows8/msi-record147.h','user/windows8/msi-text147.h','tests/m14/api147_host.py','tests/m14/plan147_host.c'];report=dict(passed=True,checks=checks,scope=__doc__,packages=packages,peak_host_allocated_bytes=state['peak'],retained_allocations=len(live),sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources});(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS MSI API checks',checks)
if __name__=='__main__':main()
