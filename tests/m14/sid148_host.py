"""Compare actual SID serialization with Windows; no vendor application execution."""
import ctypes as c,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 out=ROOT/'build/m14-native/stage8/sid-host';out.mkdir(parents=True,exist_ok=True);binary=out/'sid148.dll'
 subprocess.run(['clang','-shared','-O2','-Wall','-Wextra','-Werror','-I',str(ROOT/'include'),str(ROOT/'tests/m14/sid148_host.c'),'-o',str(binary)],check=True,cwd=ROOT)
 own=c.CDLL(str(binary));win=c.WinDLL('advapi32',use_last_error=True)
 own.sid148.argtypes=[c.c_void_p,c.c_ubyte,c.c_void_p,c.POINTER(c.c_void_p)];own.release148.argtypes=[c.c_void_p]
 own.size148.argtypes=own.valid148.argtypes=[c.c_void_p];own.size148.restype=c.c_uint;own.equal148.argtypes=[c.c_void_p,c.c_void_p]
 win.AllocateAndInitializeSid.argtypes=[c.c_void_p,c.c_ubyte]+[c.c_uint]*8+[c.POINTER(c.c_void_p)];win.FreeSid.argtypes=[c.c_void_p];win.FreeSid.restype=c.c_void_p
 differences=[];checks=0
 for authority in [(0,0,0,0,0,5),(0,0,0,0,0,1),(1,2,3,4,5,6)]:
  a=(c.c_ubyte*6)(*authority);values=(c.c_uint*8)(32,544,0xffffffff,0,1,0x11223344,9,10)
  for count in range(10):
   left=c.c_void_p();right=c.c_void_p();x=bool(own.sid148(a,count,values,c.byref(left)));y=bool(win.AllocateAndInitializeSid(a,count,*values,c.byref(right)));checks+=1
   try:
    if x!=y:differences.append(dict(count=count,actual=x,expected=y))
    elif x:
     size=8+count*4;assert own.valid148(left) and own.size148(left)==size and own.equal148(left,left)
     if c.string_at(left,size)!=c.string_at(right,size):differences.append(dict(count=count,actual=c.string_at(left,size).hex(),expected=c.string_at(right,size).hex()))
   finally:
    if left:own.release148(left)
    if right:win.FreeSid(right)
 report=dict(passed=not differences,scope=__doc__,checks=checks,differences=differences,sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ['user/windows8/sid148.inc','tests/m14/sid148_host.c','tests/m14/sid148_host.py']})
 (out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2));assert not differences
if __name__=='__main__':main()
