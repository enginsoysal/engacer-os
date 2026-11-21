"""Confined real-Windows registry adapter for production MSI integration tests."""
import ctypes as c,re,uuid,winreg
from msireg147_host import Request,Result

def create():
 Registry=c.CFUNCTYPE(c.c_int64,c.c_uint,c.c_uint64)
 fixture='Software\\EngacerOS-M147-Test-'+uuid.uuid4().hex
 assert re.fullmatch(r'Software\\EngacerOS-M147-Test-[0-9a-f]{32}',fixture)
 bucket='controller';handles={};state=dict(error=None)
 api=c.WinDLL('advapi32',use_last_error=True)
 api.RegSetValueExW.argtypes=[c.c_void_p,c.c_wchar_p,c.c_uint32,c.c_uint32,c.c_void_p,c.c_uint32];api.RegSetValueExW.restype=c.c_int32
 api.RegQueryValueExW.argtypes=[c.c_void_p,c.c_wchar_p,c.c_void_p,c.POINTER(c.c_uint32),c.c_void_p,c.POINTER(c.c_uint32)];api.RegQueryValueExW.restype=c.c_int32
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
 def close():
  for handle in handles.values():winreg.CloseKey(handle)
  handles.clear();remove_tree(fixture)
 with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER,fixture,0,winreg.KEY_ALL_ACCESS):pass
 return registry,close,state
