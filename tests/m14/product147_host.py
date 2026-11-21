"""Canonical independent UUIDs and malformed physical product grants."""
import ctypes,hashlib,json,random,sys,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command

def main():
 out=ROOT/'build/m14-native/stage7/product-host';out.mkdir(parents=True,exist_ok=True);t=pinned_tools()
 command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-c',ROOT/'tests/m14/product147_host.c','-o',out/'product.obj']);command([t['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'product.dll'),out/'product.obj']);lib=ctypes.CDLL(str(out/'product.dll'));lib.root147.argtypes=[ctypes.c_char_p];lib.make147.argtypes=[ctypes.c_void_p,ctypes.c_uint,ctypes.c_char_p];rng=random.Random(147);checks=0;prefix='/Applications/Windows/'
 for _ in range(1000):
  u=uuid.UUID(int=rng.getrandbits(128));code='{'+str(u)+'}';root=prefix+code.upper();assert lib.root147(root.encode())==1;checks+=1
  for cap in [1,len(root),len(root)+1,len(root)+2]:
   buf=(ctypes.c_ubyte*(cap+16))(*([0x9b]*(cap+16)));result=lib.make147(buf,cap,code.encode());assert bytes(buf)[cap:]==b'\x9b'*16;checks+=1
   if cap>len(root):assert result==1 and bytes(buf)[:len(root)+1]==root.encode()+b'\0';checks+=1
   else:assert result==0 and buf[0]==0;checks+=1
  for bad in [root+'/',root+'/../Other',root.replace('/Windows/','/WindowsX/'),root[:-1],root.replace('{',''),prefix+code+'x',prefix+'../'+code,root[:30]+'g'+root[31:]]:assert lib.root147(bad.encode())==0;checks+=1
 for bad in [None,b'',b'/System',b'/Applications/Windows/',b'/Applications/Windows/\xff',b'/Applications/Windows/{00000000-0000-0000-0000-00000000000/}']:assert lib.root147(bad)==0;checks+=1
 sources=['include/engine/winproduct147.h','tests/m14/product147_host.c','tests/m14/product147_host.py'];report=dict(passed=True,checks=checks,scope='Shared production canonical GUID/product-root parser; native grant inheritance is separately required',sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources});(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS canonical product root checks',checks)
if __name__=='__main__':main()
