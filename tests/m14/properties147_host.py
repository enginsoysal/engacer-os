"""Lazy production property ownership, failure rollback and scalar field bounds."""
import ctypes
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command

def main():
    out=ROOT/'build/m14-native/stage7/properties-host';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
    command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',ROOT/'tests/m14/properties147_host.c','-o',out/'properties.obj'])
    command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'properties.dll'),out/'properties.obj'])
    lib=ctypes.CDLL(str(out/'properties.dll'));alloc_type=ctypes.CFUNCTYPE(ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t);free_type=ctypes.CFUNCTYPE(None,ctypes.c_void_p,ctypes.c_void_p)
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
    lib.init147.argtypes=[alloc_type,free_type,ctypes.c_void_p];lib.set147.argtypes=[ctypes.c_char_p,ctypes.c_char_p];lib.set147.restype=ctypes.c_uint;lib.get147.argtypes=[ctypes.c_char_p];lib.get147.restype=ctypes.c_char_p;lib.format147.argtypes=[ctypes.c_char_p,ctypes.c_void_p,ctypes.c_uint];lib.format147.restype=ctypes.c_uint
    checks=0
    def check(yes):
        nonlocal checks
        assert yes;checks+=1
    def reset():
        lib.destroy147();check(not live and state['bytes']==0 and not state['bad_free']);state['fail']=-1;lib.init147(alloc,release,None)
    def setp(name,value):return lib.set147(name.encode() if name is not None else None,value.encode() if value is not None else None)
    reset();check(lib.bytes147()==lib.count147()==0)
    for fail in [0,1]:
        state['fail']=fail;check(setp('A','value')==8);check(lib.count147()==0 and not live);reset()
    check(setp('A','old')==0);state['fail']=0;check(setp('A','new')==8);check(lib.get147(b'A')==b'old');state['fail']=-1
    check(setp('a','other')==0);check(lib.get147(b'A')==b'old' and lib.get147(b'a')==b'other')
    check(setp('A',None)==0 and lib.get147(b'A')==b'');check(setp('a','')==0 and lib.count147()==0);reset()
    for i in range(16):check(setp('P'+str(i),'v')==0)
    before=state['bytes'];state['fail']=1;check(setp('Grow','v')==8);check(lib.count147()==16 and state['bytes']==before and lib.get147(b'Grow')==b'');reset()
    for i in range(256):check(setp('P'+str(i),'v')==0)
    check(setp('Overflow','v')==1816 and lib.count147()==256);reset()
    for name in [None,'','1Bad','Bad Name','A'*73]:check(setp(name,'v')==87)
    check(setp('Okay','v'*4097)==1816 and not live)
    for i in range(40):
        result=setp('Large'+str(i),'v'*4096)
        if result:check(result==1816);break
        check(state['bytes']==lib.bytes147() and state['bytes']<=131072)
    else:raise AssertionError('Property budget not enforced')
    reset()
    for key,value in {'SystemFolder':'C:\\Windows\\System32\\','LocalizationFolder':'C:\\Program Files\\Notepad++\\localization\\','INSTALLFOLDER':'C:\\Program Files\\Notepad++\\','NPP_LANG':'english','ProductName':'Notepad++ (x64)'}.items():check(setp(key,value)==0)
    cases=[('"[SystemFolder]xcopy.exe" "[LocalizationFolder][NPP_LANG].xml" "[INSTALLFOLDER]nativeLang.xml*" /Y /Q','"C:\\Windows\\System32\\xcopy.exe" "C:\\Program Files\\Notepad++\\localization\\english.xml" "C:\\Program Files\\Notepad++\\nativeLang.xml*" /Y /Q'),('"[SystemFolder]cmd.exe" /C del /F /Q "[INSTALLFOLDER]nativeLang.xml"','"C:\\Windows\\System32\\cmd.exe" /C del /F /Q "C:\\Program Files\\Notepad++\\nativeLang.xml"'),('A[Missing]B','AB'),('[\\[]Bracket[\\]]','[Bracket]'),('{GUID}','{GUID}'),('unmatched [text','unmatched [text'),('A newer version of [ProductName] is installed.','A newer version of Notepad++ (x64) is installed.')]
    for text,expected in cases:
        raw=expected.encode()
        for capacity in [len(raw)+1,len(raw)+2,1,len(raw)]:
            buf=(ctypes.c_ubyte*(capacity+16))(*([0x9b]*(capacity+16)));result=lib.format147(text.encode(),buf,capacity);check(bytes(buf)[capacity:]==b'\x9b'*16)
            if capacity>len(raw):check(result==0 and bytes(buf)[:len(raw)+1]==raw+b'\0')
            else:check(result==1816 and buf[0]==0)
    for text in ['[~]','{optional [ProductName]}','[[NPP_LANG]]','[%PATH]','[#File]']:
        buf=ctypes.create_string_buffer(4097);check(lib.format147(text.encode(),buf,len(buf))==87 and buf.value==b'')
    reset();check(state['peak']<=131072)
    sources=['user/windows8/msi-properties147.h','tests/m14/properties147_host.c','tests/m14/properties147_host.py'];report=dict(passed=True,checks=checks,peak_host_allocated_bytes=state['peak'],retained_allocations=len(live),scope='Supporting production property ownership/scalar formatting with deterministic allocation failures; no native MSI/custom-action/installation qualification',limits=['256 properties, 72-byte names, 4096-byte values, 128-KiB total transient allocation budget','Nested keys, optional formatted groups and binary NUL formatting currently refuse; external costed references require an explicit resolver'],sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources})
    (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS property/session host checks',checks)

if __name__=='__main__':main()
