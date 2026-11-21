"""Owned Windows CopyFileW metadata reference; never execute original vendor apps."""
import ctypes as C,hashlib,json,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 k=C.WinDLL('kernel32',use_last_error=True)
 k.CreateFileW.argtypes=[C.c_wchar_p,C.c_ulong,C.c_ulong,C.c_void_p,C.c_ulong,C.c_ulong,C.c_void_p];k.CreateFileW.restype=C.c_void_p
 k.CloseHandle.argtypes=[C.c_void_p];k.SetFileTime.argtypes=[C.c_void_p,C.c_void_p,C.c_void_p,C.c_void_p]
 k.CopyFileW.argtypes=[C.c_wchar_p,C.c_wchar_p,C.c_int];k.GetFileAttributesExW.argtypes=[C.c_wchar_p,C.c_uint,C.c_void_p]
 def set_times(p,values):
  h=k.CreateFileW(str(p),0x100,7,None,3,0x80,None);assert h not in [None,C.c_void_p(-1).value]
  t=[C.c_ulonglong(x)for x in values];assert k.SetFileTime(h,*[C.byref(x)for x in t]);assert k.CloseHandle(h)
 def times(p):
  v=(C.c_uint32*9)();assert k.GetFileAttributesExW(str(p),0,C.byref(v));return [v[1+i*2]|v[2+i*2]<<32 for i in range(3)]
 with tempfile.TemporaryDirectory(prefix='engacer-copy148-') as tmp:
  root=Path(tmp).resolve();assert root.parent==Path(tempfile.gettempdir()).resolve() and root.name.startswith('engacer-copy148-')
  a=root/'source.bin';b=root/'target.bin';payload=bytes((i*37+11)&255 for i in range(256))*33;a.write_bytes(payload)
  source=[133000000000000000,133100000000000000,133200000000000000];set_times(a,source)
  assert k.CopyFileW(str(a),str(b),1);created=times(b);assert created[0]>source[0] and created[1]>source[1] and created[2]==source[2] and b.read_bytes()==payload
  old=[132000000000000000,132100000000000000,132200000000000000];set_times(b,old)
  assert k.CopyFileW(str(a),str(b),0);replaced=times(b);assert replaced[0]==old[0] and replaced[1]>old[1] and replaced[2]==source[2] and b.read_bytes()==payload
  assert not k.CopyFileW(str(a),str(b),1) and C.get_last_error()==80
  assert not k.CopyFileW(str(a),str(a),0) and C.get_last_error()==32
 report=dict(passed=True,scope=__doc__,source_times=source,new_destination_times=created,old_destination_times=old,replaced_destination_times=replaced,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),copied_source_creation_and_access_times=False)
 out=ROOT/'build/m14-native/stage8/copy-reference';out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
