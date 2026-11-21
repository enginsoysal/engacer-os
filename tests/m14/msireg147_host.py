"""Original authored registry effects against real Windows APIs in an owned HKCU subtree.

No installer or vendor code executes. Native kernel and durable recovery remain separate gates.
"""
import ctypes as c,hashlib,json,os,re,struct,sys,uuid,winreg
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
class Request(c.Structure):_fields_=[('root',c.c_uint64),('name',c.c_uint64),('data',c.c_uint64),('result',c.c_uint64),('access',c.c_uint32),('flags',c.c_uint32),('bytes',c.c_uint32),('type',c.c_uint32),('index',c.c_uint32),('name_capacity',c.c_uint32),('name_output',c.c_uint64)]
class Result(c.Structure):_fields_=[('handle',c.c_uint64),('time',c.c_uint64),('type',c.c_uint32),('bytes',c.c_uint32),('name_units',c.c_uint32),('disposition',c.c_uint32)]

def main():
 out=ROOT/'build/m14-native/stage7/msireg-host';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools();objects=[]
 sources=['user/windows8/msi-registry147.c','user/windows8/msi-journal147.c','user/windows8/msi-plan147.c','user/windows8/msi-cost147.c','user/windows8/msi_db.c','runtime/sha256.c','tests/m14/msireg147_host.c']
 for source in sources:
  obj=out/(Path(source).stem+'.obj');command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-I',ROOT/'include','-c',ROOT/source,'-o',obj]);objects.append(obj)
 dll=out/'msireg.dll';command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(dll),*objects]);lib=c.CDLL(str(dll));Alloc=c.CFUNCTYPE(c.c_void_p,c.c_void_p,c.c_size_t);Free=c.CFUNCTYPE(None,c.c_void_p,c.c_void_p);Failure=c.CFUNCTYPE(None,c.c_char_p);Size=c.CFUNCTYPE(c.c_size_t,c.c_void_p);Registry=c.CFUNCTYPE(c.c_int64,c.c_uint,c.c_uint64)
 live={};handles={};state=dict(bytes=0,peak=0,bad=False,error=None);checks=0;samples=[];fixture='Software\\EngacerOS-M147-Test-'+uuid.uuid4().hex;assert re.fullmatch(r'Software\\EngacerOS-M147-Test-[0-9a-f]{32}',fixture);bucket=''
 api=c.WinDLL('advapi32',use_last_error=True);api.RegSetValueExW.argtypes=[c.c_void_p,c.c_wchar_p,c.c_uint32,c.c_uint32,c.c_void_p,c.c_uint32];api.RegSetValueExW.restype=c.c_int32;api.RegQueryValueExW.argtypes=[c.c_void_p,c.c_wchar_p,c.c_void_p,c.POINTER(c.c_uint32),c.c_void_p,c.POINTER(c.c_uint32)];api.RegQueryValueExW.restype=c.c_int32
 def context(root,access):return fixture+'\\'+bucket+'\\'+('CU'if root==0x80000001 else'LM32'if access&0x200 else'LM64')
 def full(root,access,key):
  assert root in [0x80000001,0x80000002];return context(root,access)+('\\'+key if key else'')
 def counts(path):
  try:
   with winreg.OpenKey(winreg.HKEY_CURRENT_USER,path,0,winreg.KEY_READ)as h:
    keys,values,_=winreg.QueryInfoKey(h);total=keys
    for i in range(keys):a,b=counts(path+'\\'+winreg.EnumKey(h,i));total+=a;values+=b
    return total,values
  except FileNotFoundError:return 0,0
 @Alloc
 def allocate(ctx,n):
  b=c.create_string_buffer(n);address=c.addressof(b);live[address]=(b,n);state['bytes']+=n;state['peak']=max(state['peak'],state['bytes']);return address
 @Free
 def release(ctx,address):
  if address not in live:state['bad']=True;return
  state['bytes']-=live.pop(address)[1]
 @Size
 def size(address):return live[address][1]
 @Failure
 def failure(message):
  for h in handles.values():winreg.CloseKey(h)
  handles.clear();remove_tree(fixture);(out/'unexpected-refusal.json').write_bytes(json.dumps(dict(passed=False,error=message.decode(),owned_fixture_removed=True)).encode());os._exit(87)
 @Registry
 def registry(op,address):
  try:
   q=Request.from_address(address);r=Result.from_address(q.result)if q.result else None;name=c.wstring_at(q.name)if q.name else''
   if op in [1,2]:
    path=full(q.root,q.access,name);access=q.access&~0x300;opened=winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER,path,0,access)if op==2 else winreg.OpenKey(winreg.HKEY_CURRENT_USER,path,0,access);token=0x9000
    while token in handles:token+=1
    handles[token]=opened;r.handle=token;r.disposition=1;return 0
   if op==11:r.type,r.bytes=counts(context(q.root,q.access));r.name_units=64;r.disposition=128;return 0
   if op==10:winreg.DeleteKeyEx(winreg.HKEY_CURRENT_USER,full(q.root,q.access,name),0,0);return 0
   if q.root not in handles:return -6
   h=handles[q.root]
   if op==5:winreg.CloseKey(h);del handles[q.root];return 0
   if op==3:return -api.RegSetValueExW(int(h),name,0,q.type,q.data,q.bytes)
   if op==4:
    kind=c.c_uint32();n=c.c_uint32(q.bytes);code=api.RegQueryValueExW(int(h),name,None,c.byref(kind),q.data,c.byref(n));r.type=kind.value;r.bytes=n.value;return -code
   if op==6:winreg.DeleteValue(h,name);return 0
   if op in [7,9]:
    if op==7:leaf,_,kind=winreg.EnumValue(h,q.index);r.type=kind
    else:leaf=winreg.EnumKey(h,q.index)
    raw=leaf.encode('utf-16le')+b'\0\0';r.name_units=len(raw)//2-1
    if q.name_capacity<=r.name_units:return -234
    if not q.name_output:return -87
    c.memmove(q.name_output,raw,len(raw));return 0
   return -50
  except OSError as exc:return -exc.winerror
  except Exception as exc:state['error']=repr(exc);return -87
 lib.init147.argtypes=[Alloc,Free,Failure];lib.init147(allocate,release,failure);lib.registry_init147.argtypes=[Registry,Size,c.c_uint];lib.registry_init147(registry,size,1024);lib.open147.argtypes=[c.c_void_p,c.c_uint];lib.cost147.argtypes=[c.c_char_p];lib.set147.argtypes=[c.c_char_p,c.c_char_p];lib.get147.argtypes=[c.c_char_p];lib.get147.restype=c.c_char_p;lib.registry_data147.restype=c.c_void_p
 def seed(ctx,key,name,value,kind):
  with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER,fixture+'\\'+bucket+'\\'+ctx+'\\'+key,0,winreg.KEY_ALL_ACCESS)as h:winreg.SetValueEx(h,name,0,kind,value)
 def query(ctx,key,name):
  with winreg.OpenKey(winreg.HKEY_CURRENT_USER,fixture+'\\'+bucket+'\\'+ctx+'\\'+key)as h:return winreg.QueryValueEx(h,name)
 def tree_state(path):
  result={}
  try:
   with winreg.OpenKey(winreg.HKEY_CURRENT_USER,path,0,winreg.KEY_READ)as h:
    keys,values,_=winreg.QueryInfoKey(h);result['']=[winreg.EnumValue(h,i)for i in range(values)]
    for i in range(keys):
     name=winreg.EnumKey(h,i)
     for tail,value in tree_state(path+'\\'+name).items():result[name+('\\'+tail if tail else'')]=value
  except FileNotFoundError:pass
  return result
 def remove_tree(path):
  assert path==fixture or path.startswith(fixture+'\\')
  try:
   with winreg.OpenKey(winreg.HKEY_CURRENT_USER,path,0,winreg.KEY_READ)as h:
    children=[];index=0
    while True:
     try:children.append(winreg.EnumKey(h,index));index+=1
     except OSError as e:
      if e.winerror==259:break
      raise
   for child in children:remove_tree(path+'\\'+child)
   winreg.DeleteKeyEx(winreg.HKEY_CURRENT_USER,path,0,0)
  except FileNotFoundError:pass
 try:
  with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER,fixture,0,winreg.KEY_ALL_ACCESS):pass
  packages=[ROOT/'third_party/7zip/7z2606-x64.msi',Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/npp.8.9.9.1.Installer.x64.msi']
  for index,package in enumerate(packages):
   bucket='case'+str(index);raw=package.read_bytes();data=c.create_string_buffer(raw);lib.open147(data,len(raw));assert lib.set147(b'ALLUSERS',b'1')==0 and lib.set147(b'Privileged',b'1')==0
   if index==1:seed('LM64',r'Software\Notepad++\Lang','active','french',winreg.REG_SZ)
   assert lib.registry_search147()==0;assert (lib.get147(b'NPP_LANG')or b'')==(b'french'if index else b'');lib.cost147(b'C:\\Users\\Owner');checks+=2
   if index==0:seed('CU',r'Software\7-Zip','Path','old private path',winreg.REG_SZ);seed('CU',r'Software\7-Zip','Path64',0x123456789abcdef0,winreg.REG_QWORD);seed('CU',r'Software\7-Zip','User preference','keep me',winreg.REG_SZ)
   status=lib.registry_snapshot147();assert status==0,(package.name,status,state['error']);assert not handles;checks+=2
   n=lib.registry_bytes147();journal=c.string_at(lib.registry_data147(),n);assert journal[72:104]==hashlib.sha256(journal[:72]+bytes(32)+journal[104:]).digest();records=[];at=1024
   while at<n:
    kind,count=struct.unpack_from('<II',journal,at)
    if kind==2:
     fields=struct.unpack_from('<10I',journal,at+8);root,view,after_type,before_type,after_bytes,before_bytes,key_bytes,name_bytes,before_exists,_=fields;start=at+48;key=journal[start:start+key_bytes-1].decode();name=journal[start+key_bytes:start+key_bytes+name_bytes-1].decode();after=journal[start+key_bytes+name_bytes:start+key_bytes+name_bytes+after_bytes];records.append((root,view,key,name,after_type,after))
    at+=count
   tables=next(p['tables']for p in json.loads((ROOT/'evidence/M14/7/development/msi-tables147.json').read_text(encoding='utf-8-sig'))['packages']if p['file']==package.name);directories={r[0]:r for r in tables['Directory']};properties=dict(tables['Property']);properties.update(ALLUSERS='1',Privileged='1',NPP_LANG='french'if index else'',SystemFolder='C:\\Windows\\SysWOW64\\',System64Folder='C:\\Windows\\System32\\',WindowsFolder='C:\\Windows\\')
   def directory(name):
    if name=='TARGETDIR':return 'C:\\'
    if name=='ProgramFiles64Folder':return 'C:\\Program Files\\'
    if name=='ProgramFilesFolder':return 'C:\\Program Files (x86)\\'
    if name=='ProgramMenuFolder':return 'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\'
    row=directories[name];leaf=row[2].split(':')[0].split('|')[-1];return directory(row[1])+(''if leaf=='.'else leaf+'\\')
   for identifier in directories:properties[identifier]=directory(identifier)
   def formatted(text):return re.sub(r'\[([A-Za-z_][A-Za-z0-9_.]*)\]',lambda m:properties.get(m[1],''),text)
   components={r[0]:r for r in tables['Component']};authored={}
   for row in tables['Registry']:
    _,root_key,key,name,value,component=row;root_key=int(root_key);root_key=2 if root_key<=0 else root_key;view=64 if int(components[component][3])&256 else 32
    if root_key==1:view=64
    key=('Software\\Classes\\'if int(row[1])==0 else'')+formatted(key);name=formatted(name);value=formatted(value)
    if value.startswith('##'):kind=1;expected=(value[1:]+'\0').encode('utf-16le')
    elif value.startswith('#x'):kind=3;expected=bytes.fromhex(value[2:])
    elif value.startswith('#%'):kind=2;expected=(value[2:]+'\0').encode('utf-16le')
    elif value.startswith('#'):kind=4;expected=struct.pack('<I',int(value[1:])&0xffffffff)
    else:kind=1;expected=(value+'\0').encode('utf-16le')
    identity=(root_key,view,key.casefold(),name.casefold());assert identity not in authored;authored[identity]=(kind,expected)
   observed={(root_key,view,key.casefold(),name.casefold()):(kind,value)for root_key,view,key,name,kind,value in records};assert observed==authored,(package.name,observed,authored);checks+=len(authored)
   assert len(records)==(16 if index==0 else 10);assert lib.registry_apply147()==0;assert not handles;checks+=3
   for root,view,key,name,kind,expected in records:
    ctx='CU'if root==1 else'LM32'if view==32 else'LM64';with_key=fixture+'\\'+bucket+'\\'+ctx+'\\'+key
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER,with_key,0,winreg.KEY_READ)as h:
     kind_out=c.c_uint32();n_out=c.c_uint32(2048);actual=c.create_string_buffer(2048);assert api.RegQueryValueExW(int(h),name,None,c.byref(kind_out),actual,c.byref(n_out))==0;assert kind_out.value==kind and actual.raw[:n_out.value]==expected
    checks+=2
   assert lib.registry_apply147()==0;checks+=1
   # Independent later changes and unrelated values survive undo; opaque QWORD restores.
   if index==0:seed('CU',r'Software\7-Zip','Path','later user path',winreg.REG_SZ)
   else:seed('LM64',r'Software\Notepad++','Independent setting','leave me',winreg.REG_SZ)
   assert lib.registry_undo147()==0 and not handles;checks+=2
   if index==0:
    assert query('CU',r'Software\7-Zip','Path')==('later user path',winreg.REG_SZ);assert query('CU',r'Software\7-Zip','Path64')==(0x123456789abcdef0,winreg.REG_QWORD);assert query('CU',r'Software\7-Zip','User preference')==('keep me',winreg.REG_SZ);checks+=3
   else:assert query('LM64',r'Software\Notepad++','Independent setting')==('leave me',winreg.REG_SZ);assert query('LM64',r'Software\Notepad++\Lang','active')==('french',winreg.REG_SZ);checks+=2
   assert lib.registry_undo147()==0;checks+=1;samples.append(dict(package=package.name,source_sha256=hashlib.sha256(raw).hexdigest(),registry_values=len(records),journal_bytes=len(journal),later_changes_preserved=True));lib.registry_close147()
   # Quotas must refuse before changing any host fixture value or key.
   for qindex in range(70):
    with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER,fixture+'\\'+bucket+'\\LM64\\Quota'+str(qindex),0,winreg.KEY_ALL_ACCESS):pass
   old_tree=tree_state(fixture+'\\'+bucket);assert lib.registry_snapshot147()==1450;assert tree_state(fixture+'\\'+bucket)==old_tree and not handles;lib.registry_close147();checks+=2
   for qindex in range(70):winreg.DeleteKeyEx(winreg.HKEY_CURRENT_USER,fixture+'\\'+bucket+'\\LM64\\Quota'+str(qindex),0,0)
   old_tree=tree_state(fixture+'\\'+bucket);lib.registry_init147(registry,size,1);assert lib.registry_snapshot147()==1816;assert tree_state(fixture+'\\'+bucket)==old_tree and not handles;lib.registry_close147();lib.registry_init147(registry,size,1024);checks+=2
   lib.close147();assert not live and state['bytes']==0 and not handles and not state['bad']and state['error']is None;checks+=1
 finally:
  for h in handles.values():winreg.CloseKey(h)
  handles.clear();remove_tree(fixture)
 try:winreg.OpenKey(winreg.HKEY_CURRENT_USER,fixture);raise AssertionError('Owned fixture remains')
 except FileNotFoundError:pass
 report=dict(passed=True,checks=checks,scope=__doc__,packages=samples,owned_hkcu_fixture_removed=True,host_machine_registry_writes=0,retained_host_tracked_bytes=state['bytes'],peak_host_tracked_bytes=state['peak'],sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources+['user/windows8/msi-registry147.h','include/engine/wintxn147.h','tests/m14/msireg147_host.py']});(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS original MSI registry write/guarded undo',checks)
if __name__=='__main__':main()
