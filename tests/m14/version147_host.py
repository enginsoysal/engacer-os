"""Own version parsing vs trusted Windows data-only version APIs; original images never execute."""
import ctypes as c,hashlib,json,os,random,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools

def main():
 out=ROOT/'build/m14-native/stage7/version-host';out.mkdir(parents=True,exist_ok=True);t=pinned_tools();command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-I',ROOT/'include','-c',ROOT/'tests/m14/version147_host.c','-o',out/'version.obj'])
 definition=out/'kernel32.def';definition.write_bytes(b'LIBRARY kernel32.dll\nEXPORTS\nGetProcessHeap\nHeapAlloc\nHeapFree\n');command([t['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/'kernel32.lib')]);command([t['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'version.dll'),out/'version.obj',out/'kernel32.lib']);lib=c.CDLL(str(out/'version.dll'));U=c.c_uint;P=c.c_void_p
 lib.source147.argtypes=[P,U];lib.size147.argtypes=[P];lib.info147.argtypes=[U,P];lib.query147.argtypes=[P,c.c_wchar_p,P,P];lib.query_bound147.argtypes=[P,U,c.c_wchar_p,P,P];lib.live_get147.restype=c.c_uint64;lib.peak_get147.restype=c.c_uint64
 trusted=c.WinDLL('version',use_last_error=True);trusted.GetFileVersionInfoSizeW.argtypes=[c.c_wchar_p,P];trusted.GetFileVersionInfoW.argtypes=[c.c_wchar_p,U,U,P];trusted.VerQueryValueW.argtypes=[P,c.c_wchar_p,P,P]
 paths=[Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/7zip/_7z.exe',Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/msi-streams/npp.8.9.9.1.Installer.x64/Wix4UtilCA_X64.bin',Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/notepadpp/notepad++.exe'];checks=0;packages=[];seeds=[]
 def check(value):
  nonlocal checks
  assert value;checks+=1
 for path in paths:
  data=path.read_bytes();source=c.create_string_buffer(data);lib.source147(source,len(data));handle=U(99);n=lib.size147(c.byref(handle));check(n>0 and n<=65535 and handle.value==0 and lib.live_get147()==0 and not lib.opens_get147());blob=(c.c_ubyte*(n+16))(*([0x9b]*(n+16)));check(lib.info147(n,blob)==1 and bytes(blob)[n:]==b'\x9b'*16 and lib.live_get147()==0 and not lib.opens_get147());seeds.append(bytes(blob)[:n]);reference_bytes=trusted.GetFileVersionInfoSizeW(str(path),None);check(reference_bytes>0);reference=c.create_string_buffer(reference_bytes);check(trusted.GetFileVersionInfoW(str(path),0,reference_bytes,reference)==1)
  values={}
  for query in ['\\','\\VarFileInfo\\Translation']:
   actual=P();count=U(0);expect=P();expected_count=U(0);check(lib.query147(blob,query,c.byref(actual),c.byref(count))==1);check(trusted.VerQueryValueW(reference,query,c.byref(expect),c.byref(expected_count))==1);check(count.value==expected_count.value and c.string_at(actual,count.value)==c.string_at(expect,expected_count.value));values[query]=c.string_at(actual,count.value).hex()
  translation=bytes.fromhex(values['\\VarFileInfo\\Translation']);language,codepage=struct.unpack_from('<HH',translation)
  for name in ['FileVersion','ProductVersion','CompanyName','ProductName','FileDescription']:
   query='\\StringFileInfo\\%04x%04x\\%s'%(language,codepage,name);actual=P();count=U(0);expect=P();expected_count=U(0);wanted=trusted.VerQueryValueW(reference,query,c.byref(expect),c.byref(expected_count));got=lib.query147(blob,query,c.byref(actual),c.byref(count));check(bool(got)==bool(wanted))
   if wanted:check(count.value==expected_count.value and c.string_at(actual,count.value*2)==c.string_at(expect,count.value*2));values[query]=c.wstring_at(actual,count.value)
  tiny=(c.c_ubyte*17)(*([0x9b]*17));check(lib.info147(1,tiny)==1 and bytes(tiny)[:1]==bytes(blob)[:1] and bytes(tiny)[1:]==b'\x9b'*16)
  actual=P(99);count=U(99);check(lib.query147(blob,'\\Missing',c.byref(actual),c.byref(count))==0 and not actual.value and count.value==0);check(lib.query147(blob,'no-leading-slash',c.byref(actual),c.byref(count))==0 and lib.error_get147()==87)
  packages.append(dict(file=path.name,sha256=hashlib.sha256(data).hexdigest(),resource_bytes=n,reference_buffer_bytes=reference_bytes,values=values))
 # Deterministic truncation/mutation checks never read outside callback input or declared block bounds.
 rng=random.Random(147);original=paths[1].read_bytes()
 for turn in range(1200):
  if turn<100:body=original[:turn]
  else:
   body=bytearray(original);at=rng.randrange(min(len(body),1024));body[at:at+4]=rng.getrandbits(32).to_bytes(4,'little');body=bytes(body)
  source=c.create_string_buffer(body);lib.source147(source,len(body));handle=U(99);size=lib.size147(c.byref(handle));check(handle.value==0 and 0<=size<=65535 and lib.live_get147()==0 and not lib.opens_get147())
 for seed in seeds:
  for end in range(len(seed)+1):
   blob=c.create_string_buffer(seed);offset=U();n=U();status=lib.query_bound147(blob,end,'\\',c.byref(offset),c.byref(n));check(status!=0 or(offset.value+n.value<=end and n.value==52))
  for turn in range(1000):
   body=bytearray(seed);at=rng.randrange(len(body));body[at]=rng.randrange(256);blob=c.create_string_buffer(bytes(body));offset=U();n=U();status=lib.query_bound147(blob,len(body),'\\StringFileInfo\\040904b0\\ProductName',c.byref(offset),c.byref(n));check(status!=0 or offset.value+n.value*2<=len(body))
 check(lib.live_get147()==0 and not lib.opens_get147());sources=['user/windows8/version147.h','user/windows8/version147.inc','tests/m14/version147_host.c','tests/m14/version147_host.py'];report=dict(passed=True,scope=__doc__,checks=checks,packages=packages,peak_transient_host_bytes=lib.peak_get147(),retained_host_bytes=lib.live_get147(),sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources});(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS version resource checks',checks)
if __name__=='__main__':main()
