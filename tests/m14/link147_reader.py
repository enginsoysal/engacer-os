"""Trusted Windows metadata-only reader for own freshly generated fixture links."""
import ctypes as c
from pathlib import Path
from link147_host import GUID,guid
ROOT=Path(__file__).resolve().parents[2]

def read(path):
 path=Path(path).resolve();assert path.is_relative_to((ROOT/'build/m14-native').resolve())and path.suffix=='.lnk'
 ole=c.OleDLL('ole32');ole.CoInitializeEx.argtypes=[c.c_void_p,c.c_uint];ole.CoCreateInstance.argtypes=[c.POINTER(GUID),c.c_void_p,c.c_uint,c.POINTER(GUID),c.POINTER(c.c_void_p)];assert ole.CoInitializeEx(None,2)in[0,1]
 def method(pointer,index,*args):return c.WINFUNCTYPE(c.c_int32,c.c_void_p,*args)(c.cast(pointer,c.POINTER(c.POINTER(c.c_void_p))).contents[index])
 link=c.c_void_p();persist=c.c_void_p();clsid=guid('00021401-0000-0000-C000-000000000046');iid=guid('000214F9-0000-0000-C000-000000000046');file_iid=guid('0000010B-0000-0000-C000-000000000046')
 try:
  assert ole.CoCreateInstance(c.byref(clsid),None,1,c.byref(iid),c.byref(link))==0
  try:
   assert method(link,0,c.POINTER(GUID),c.POINTER(c.c_void_p))(link,c.byref(file_iid),c.byref(persist))==0
   try:assert method(persist,5,c.c_wchar_p,c.c_uint)(persist,str(path),0)==0
   finally:method(persist,2)(persist)
   target=c.create_unicode_buffer(1024);assert method(link,3,c.c_wchar_p,c.c_int,c.c_void_p,c.c_uint)(link,target,1024,None,4)==0;result={'target':target.value}
   for slot,name in[(6,'description'),(8,'working_directory'),(10,'arguments')]:
    value=c.create_unicode_buffer(1024);assert method(link,slot,c.c_wchar_p,c.c_int)(link,value,1024)==0;result[name]=value.value
   show=c.c_int();assert method(link,14,c.POINTER(c.c_int))(link,c.byref(show))==0;result['show']=show.value;return result
  finally:method(link,2)(link)
 finally:ole.CoUninitialize()
