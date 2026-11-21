"""Read owned link bytes using original Windows metadata interfaces; never activate or resolve a link."""
import ctypes as C,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
from link147_reader import read
from link147_host import GUID,guid

def read_icon(path):
 path=Path(path).resolve();assert path.is_relative_to((ROOT/'build/m14-native').resolve())and path.suffix=='.lnk'
 ole=C.OleDLL('ole32');ole.CoInitializeEx.argtypes=[C.c_void_p,C.c_uint];ole.CoCreateInstance.argtypes=[C.POINTER(GUID),C.c_void_p,C.c_uint,C.POINTER(GUID),C.POINTER(C.c_void_p)];assert ole.CoInitializeEx(None,2)in[0,1]
 def method(pointer,slot,*types):return C.WINFUNCTYPE(C.c_int32,C.c_void_p,*types)(C.cast(pointer,C.POINTER(C.POINTER(C.c_void_p))).contents[slot])
 link=C.c_void_p();persist=C.c_void_p();clsid=guid('00021401-0000-0000-C000-000000000046');iid=guid('000214F9-0000-0000-C000-000000000046');file_iid=guid('0000010B-0000-0000-C000-000000000046')
 try:
  assert ole.CoCreateInstance(C.byref(clsid),None,1,C.byref(iid),C.byref(link))==0
  assert method(link,0,C.POINTER(GUID),C.POINTER(C.c_void_p))(link,C.byref(file_iid),C.byref(persist))==0
  assert method(persist,5,C.c_wchar_p,C.c_uint)(persist,str(path),0)==0
  text=C.create_unicode_buffer(260);index=C.c_int();assert method(link,16,C.c_wchar_p,C.c_int,C.POINTER(C.c_int))(link,text,260,C.byref(index))==0
  return dict(path=text.value,index=index.value)
 finally:
  if persist:method(persist,2)(persist)
  if link:method(link,2)(link)
  ole.CoUninitialize()

def main():
 out=ROOT/'build/m14-native/stage8/shell-reference';out.mkdir(parents=True,exist_ok=True);t=pinned_tools();source=ROOT/'tests/m14/shell148_host.c'
 command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-c',source,'-o',out/'reference.obj']);command([t['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'reference.dll'),out/'reference.obj'])
 encode=C.CDLL(str(out/'reference.dll')).encode148;encode.argtypes=[*[C.c_char_p]*5,C.c_int,C.c_uint,C.c_uint,C.c_void_p,C.c_uint,C.POINTER(C.c_uint)];encode.restype=C.c_uint
 cases=[];target=r'C:\Program Files\Example\hello.exe';work=r'C:\Users\Owner\Documents';args='--native "148"';desc='Owned shortcut '+chr(0xe4)
 for index in [-17,0,7]:
  buffer=C.create_string_buffer(b'G'*4112,4112);n=C.c_uint();assert encode(*[x.encode()for x in[target,work,args,desc,target]],index,3,123456,buffer,4096,C.byref(n))==0 and buffer.raw[n.value:]==b'G'*(4112-n.value)
  path=out/('icon'+str(index)+'.lnk');path.write_bytes(buffer.raw[:n.value]);metadata=read(path);icon=read_icon(path)
  assert metadata==dict(target=target,working_directory=work,arguments=args,description=desc,show=3)and icon==dict(path=target,index=index),(metadata,icon)
  cases.append(dict(bytes=n.value,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),windows_readback=metadata,icon=icon))
 for icon,capacity,status in [(target.encode(),17,234),(b'\xc0\x80',4096,1113)]:
  buffer=C.create_string_buffer(b'G'*4112,4112);n=C.c_uint(99);assert encode(*[x.encode()for x in[target,work,args,desc]],icon,7,3,0,buffer,capacity,C.byref(n))==status and n.value==0 and buffer.raw[capacity:]==b'G'*(4112-capacity)
 inputs=[source,Path(__file__),ROOT/'user/windows8/shell-link-format148.h',ROOT/'user/windows8/msi-link147.h',ROOT/'user/windows8/msi-text147.h',ROOT/'tests/m14/link147_reader.py']
 report=dict(passed=True,scope=__doc__,cases=cases,refused_cases=2,source_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in inputs})
 (out/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,cases=len(cases),refused_cases=2)))
if __name__=='__main__':main()
