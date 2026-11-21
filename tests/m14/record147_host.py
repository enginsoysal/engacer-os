"""Production MSI records: stale handles, field typing, quotas and allocation failure."""
import ctypes,hashlib,json,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command

def main():
    out=ROOT/'build/m14-native/stage7/record-host';out.mkdir(parents=True,exist_ok=True);t=pinned_tools()
    command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',ROOT/'tests/m14/record147_host.c','-o',out/'record.obj'])
    command([t['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'record.dll'),out/'record.obj'])
    lib=ctypes.CDLL(str(out/'record.dll'));alloc_type=ctypes.CFUNCTYPE(ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t);free_type=ctypes.CFUNCTYPE(None,ctypes.c_void_p,ctypes.c_void_p)
    state={'fail':-1,'peak':0,'bytes':0,'bad_free':False};live={}
    @alloc_type
    def alloc(context,n):
        if state['fail']==0:return None
        if state['fail']>0:state['fail']-=1
        buf=ctypes.create_string_buffer(n);address=ctypes.addressof(buf);live[address]=(buf,n);state['bytes']+=n;state['peak']=max(state['peak'],state['bytes']);return address
    @free_type
    def release(context,address):
        if address not in live:state['bad_free']=True;return
        state['bytes']-=live.pop(address)[1]
    lib.init147.argtypes=[alloc_type,free_type];lib.create147.argtypes=[ctypes.c_uint];lib.create147.restype=ctypes.c_uint
    lib.set147.argtypes=[ctypes.c_uint,ctypes.c_uint,ctypes.c_char_p];lib.get147.argtypes=[ctypes.c_uint,ctypes.c_uint];lib.get147.restype=ctypes.c_char_p
    lib.number147.argtypes=[ctypes.c_uint,ctypes.c_uint,ctypes.c_int32];lib.getnumber147.argtypes=[ctypes.c_uint,ctypes.c_uint];lib.getnumber147.restype=ctypes.c_int32
    checks=0
    def check(v):
        nonlocal checks
        assert v;checks+=1
    lib.init147(alloc,release);check(not live and lib.bytes147()==0);check(lib.create147(33)==0)
    state['fail']=0;check(lib.create147(3)==0 and not live);state['fail']=-1
    h=lib.create147(2);check(h!=0);check(lib.get147(h,0)==b'' and lib.getnumber147(h,0)==-2147483648)
    check(lib.set147(h,0,b'old')==0);before=state['bytes'];state['fail']=0;check(lib.set147(h,0,b'new')==8);check(lib.get147(h,0)==b'old' and state['bytes']==before);state['fail']=-1
    check(lib.set147(h,3,b'invalid')==87 and lib.set147(0,0,b'invalid')==6)
    for v in [0,1,-1,2147483647,-2147483647,-2147483648]:
        check(lib.number147(h,1,v)==0);check(lib.getnumber147(h,1)==v);check(lib.get147(h,1)==(b'' if v==-2147483648 else str(v).encode()))
    for text,value in [(b'42',42),(b'-42',-42),(b'0001',1),(b'2147483648',-2147483648),(b'9999999999999999999',-2147483648),(b'x',-2147483648),(b'-',-2147483648),(b'',-2147483648)]:
        check(lib.set147(h,1,text)==0);check(lib.getnumber147(h,1)==value)
    check(lib.set147(h,0,'Hello \u20ac \U0001f600'.encode())==0);check(lib.get147(h,0)=='Hello \u20ac \U0001f600'.encode());check(lib.set147(h,0,b'x'*4097)==1816)
    check(lib.clear147(h)==0 and lib.get147(h,0)==b'');check(lib.close147(h)==0);check(lib.close147(h)==6 and lib.get147(h,0)is None and not live)
    new=lib.create147(0);check(new!=h and lib.set147(h,0,b'stale')==6);check(lib.close147(new)==0)
    handles=[lib.create147(0)for _ in range(64)];check(all(handles) and len(set(handles))==64 and lib.create147(0)==0);lib.destroy147();check(not live)
    rng=random.Random(147)
    for cycle in range(1000):
        h=lib.create147(rng.randrange(33));check(h!=0);field=0;v=rng.randrange(-2147483647,2147483648);check(lib.number147(h,field,v)==0 and lib.getnumber147(h,field)==v);check(lib.close147(h)==0 and lib.close147(h)==6)
    handles=[]
    while True:
        h=lib.create147(32)
        if not h:break
        handles.append(h)
        for i in range(33):
            code=lib.set147(h,i,b'q'*4096)
            if code:check(code==1816);break
        if code:break
    check(state['bytes']==lib.bytes147()<=262144);lib.destroy147();check(not live and state['bytes']==0 and not state['bad_free'])
    sources=['user/windows8/msi-record147.h','tests/m14/record147_host.c','tests/m14/record147_host.py'];report=dict(passed=True,checks=checks,peak_host_allocated_bytes=state['peak'],retained_allocations=len(live),scope='Production record ownership core; native exported MSI API and original WiX execution remain separate',sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources})
    (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS record checks',checks)
if __name__=='__main__':main()
