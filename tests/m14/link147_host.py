"""Validate own binary links with the trusted Windows reader, never activate a shortcut."""
import ctypes as c,hashlib,json,struct,sys,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
class GUID(c.Structure):_fields_=[('data',c.c_ubyte*16)]
def guid(text):return GUID.from_buffer_copy(uuid.UUID(text).bytes_le)

def main():
 out=ROOT/'build/m14-native/stage7/link-host';out.mkdir(parents=True,exist_ok=True);t=pinned_tools();obj=out/'link.obj';dll=out/'link.dll';command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',ROOT/'tests/m14/link147_host.c','-o',obj]);command([t['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(dll),obj]);lib=c.CDLL(str(dll));lib.encode147.argtypes=[c.c_char_p,c.c_char_p,c.c_char_p,c.c_char_p,c.c_uint,c.c_uint,c.c_void_p,c.c_uint,c.POINTER(c.c_uint)]
 ole=c.OleDLL('ole32');ole.CoInitializeEx.argtypes=[c.c_void_p,c.c_uint];ole.CoCreateInstance.argtypes=[c.POINTER(GUID),c.c_void_p,c.c_uint,c.POINTER(GUID),c.POINTER(c.c_void_p)];assert ole.CoInitializeEx(None,2)in [0,1];clsid=guid('00021401-0000-0000-C000-000000000046');iid=guid('000214F9-0000-0000-C000-000000000046');persist=guid('0000010B-0000-0000-C000-000000000046');checks=0;samples=[]
 def method(pointer,index,*types):return c.WINFUNCTYPE(c.c_int32,c.c_void_p,*types)(c.cast(pointer,c.POINTER(c.POINTER(c.c_void_p))).contents[index])
 def encode(target,working='',arguments='',description='',show=1,capacity=4096):
  buffer=c.create_string_buffer(b'G'*4112,4112);n=c.c_uint(123);status=lib.encode147(target.encode(),working.encode(),arguments.encode(),description.encode(),show,123456,buffer,capacity,c.byref(n));return status,buffer.raw,n.value
 try:
  cases=[(r'C:\Program Files\7-Zip\7zFM.exe','','','',1),(r'C:\Program Files\7-Zip\7zip.chm','','','',1),(r'C:\Program Files\Notepad++\notepad++.exe','C:\\Program Files\\Notepad++\\','','',1),(r'C:\Program Files\Example\app.exe',r'C:\Users\Owner\Documents','--name "example"','Open '+chr(0x1f680),3),(r'C:\Program Files\Example\app.exe',r'C:\Users\Owner\Documents','','Unicode '+chr(0xe9),7)]
  for index,(target,working,arguments,description,show)in enumerate(cases):
   status,raw,n=encode(target,working,arguments,description,show);assert status==0 and n<4096 and raw[n:]==b'G'*(4112-n);data=raw[:n];assert struct.unpack_from('<I',data)[0]==76 and data[4:20]==uuid.UUID('00021401-0000-0000-C000-000000000046').bytes_le;assert struct.unpack_from('<I',data,52)[0]==123456 and struct.unpack_from('<I',data,60)[0]==show;checks+=4
   path=out/('case'+str(index)+'.lnk');path.write_bytes(data);link=c.c_void_p();file=c.c_void_p();assert ole.CoCreateInstance(c.byref(clsid),None,1,c.byref(iid),c.byref(link))==0
   try:
    assert method(link,0,c.POINTER(GUID),c.POINTER(c.c_void_p))(link,c.byref(persist),c.byref(file))==0
    try:assert method(file,5,c.c_wchar_p,c.c_uint)(file,str(path),0)==0
    finally:method(file,2)(file)
    result=c.create_unicode_buffer(1024);path_status=method(link,3,c.c_wchar_p,c.c_int,c.c_void_p,c.c_uint)(link,result,1024,None,4);assert path_status==0 and result.value==target,(path_status,result.value,target);checks+=2
    for slot,wanted in [(6,description),(8,working),(10,arguments)]:
     result=c.create_unicode_buffer(1024);assert method(link,slot,c.c_wchar_p,c.c_int)(link,result,1024)==0;assert result.value==wanted,(slot,result.value,wanted);checks+=2
    shown=c.c_int();assert method(link,14,c.POINTER(c.c_int))(link,c.byref(shown))==0 and shown.value==show;checks+=1
   finally:method(link,2)(link)
   for capacity in range(n):
    code,guarded,count=encode(target,working,arguments,description,show,capacity);assert code==234 and count==0 and guarded==b'G'*4112;checks+=1
   samples.append(dict(target=target,working_directory=working,arguments=arguments,description=description,show=show,bytes=n,sha256=hashlib.sha256(data).hexdigest(),trusted_windows_readback=True))
  for target in ['',r'\\server\share\file',r'C:relative.exe','C:\\Program Files\\'+('x'*256),r'C:\path\*.exe','C:\\path\\'+chr(0xe9)+'.exe']:
   code,guarded,n=encode(target);assert code in [50,87] and n==0 and guarded==b'G'*4112;checks+=1
  for show in [0,2,4,0xffffffff]:code,guarded,n=encode(r'C:\path\app.exe',show=show);assert code==87 and n==0 and guarded==b'G'*4112;checks+=1
  code,guarded,n=encode(r'C:\path\app.exe',description='x'*260);assert code==234 and n==0 and guarded==b'G'*4112;checks+=1
 finally:ole.CoUninitialize()
 report=dict(passed=True,checks=checks,scope=__doc__,cases=samples,shortcut_activations=0,sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ['user/windows8/msi-link147.h','user/windows8/msi-text147.h','tests/m14/link147_host.c','tests/m14/link147_host.py']});(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS own links / Windows metadata-only COM reader',checks)
if __name__=='__main__':main()
