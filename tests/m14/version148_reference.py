"""Read-only original Windows condition-mask reference against the shared native encoder."""
import ctypes as C,hashlib,json,sys,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
def main():
 out=ROOT/'build/m14-native/stage8/version-reference';out.mkdir(parents=True,exist_ok=True);t=pinned_tools()
 source=ROOT/'tests/m14/version148_host.c';header=ROOT/'user/windows8/version-mask148.h';compare_header=ROOT/'user/windows8/version-compare148.h'
 command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-c',source,'-o',out/'reference.obj'])
 command([t['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'reference.dll'),out/'reference.obj'])
 native=C.CDLL(str(out/'reference.dll')).condition148;original=C.WinDLL('kernel32').VerSetConditionMask
 for f in [native,original]:f.argtypes=[C.c_uint64,C.c_uint32,C.c_ubyte];f.restype=C.c_uint64
 cases=[]
 for mask in [0,7,0x123456789abcdef0,0xffffffffffffffff]:
  for type in [0,*[1<<bit for bit in range(32)],3,0xff,0xffffffff]:
   for condition in [*range(9),255]:
    expected=original(mask,type,condition);actual=native(mask,type,condition);assert actual==expected,(mask,type,condition,actual,expected)
    cases.append(dict(mask=mask,type=type,condition=condition,result=expected))
 class Info(C.Structure):
  _fields_=[('size',C.c_uint32),('major',C.c_uint32),('minor',C.c_uint32),('build',C.c_uint32),('platform',C.c_uint32),('csd',C.c_uint16*128),('spmajor',C.c_uint16),('spminor',C.c_uint16),('suite',C.c_uint16),('product',C.c_ubyte),('reserved',C.c_ubyte)]
 k=C.WinDLL('kernel32',use_last_error=True);k.GetVersionExW.argtypes=[C.POINTER(Info)];k.VerifyVersionInfoW.argtypes=[C.POINTER(Info),C.c_uint32,C.c_uint64]
 current=Info();current.size=C.sizeof(Info);assert current.size==284 and k.GetVersionExW(C.byref(current))
 fields=['minor','major','build','platform','spminor','spmajor','suite','product'];values=[getattr(current,f)for f in fields];array=C.c_uint32*8
 compare=C.CDLL(str(out/'reference.dll')).compare148;compare.argtypes=[C.POINTER(C.c_uint32),C.POINTER(C.c_uint32),C.c_uint32,C.c_uint64];compare.restype=C.c_uint
 comparisons=[];rng=random.Random(148)
 for index in range(2400):
  requested=Info.from_buffer_copy(current);types=rng.choice([1,2,3,0x10,0x20,0x33,4,8,128,255]);mask=0
  for bit,field in enumerate(fields):
   if types&(1<<bit):
    setattr(requested,field,max(0,getattr(current,field)+rng.choice([-1,0,1])));mask=original(mask,1<<bit,rng.choice([6,7]if bit==6 else[1,2,3,4,5]))
  C.set_last_error(0);result=k.VerifyVersionInfoW(C.byref(requested),types,mask);expected=0 if result else C.get_last_error();query=[getattr(requested,f)for f in fields]
  actual=compare(array(*values),array(*query),types,mask);assert actual==expected,(index,values,query,hex(types),hex(mask),actual,expected)
  comparisons.append(dict(requested=query,types=types,mask=mask,status=expected))
 malformed=[]
 for size,types,mask in [(284,0,0),(284,256,1),(284,1,0),(276,1,1),(0,1,1)]:
  query=Info.from_buffer_copy(current);query.size=size;C.set_last_error(0);ok=k.VerifyVersionInfoW(C.byref(query),types,mask);malformed.append(dict(size=size,types=types,mask=mask,windows_status=0 if ok else C.get_last_error(),native_documented_input_guard=87))
 report=dict(passed=True,scope=__doc__,cases=cases,current_reference_version=values,comparisons=comparisons,malformed_reference_observations=malformed,malformed_scope='Observed Windows tolerance differs from the explicit native documented-input guard; not equivalence checks',source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,header,compare_header,Path(__file__)]})
 (out/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,cases=len(cases),comparisons=len(comparisons))))
if __name__=='__main__':main()
