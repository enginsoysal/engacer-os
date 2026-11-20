"""Compare streaming and retained one-shot SHA against Python's independent API."""
import ctypes
import hashlib
import json
from pathlib import Path
import random
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command

def main():
    out=ROOT/'build/m14-native/stage7/sha-host';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools();objects=[]
    for source in ['runtime/sha256.c','tests/m14/sha147_host.c']:
        obj=out/(Path(source).stem+'.obj');command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-I',ROOT/'include','-c',ROOT/source,'-o',obj]);objects.append(obj)
    dll=out/'sha147.dll';command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(dll),*objects]);lib=ctypes.CDLL(str(dll));lib.one147.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p];lib.stream147.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.POINTER(ctypes.c_uint),ctypes.c_uint,ctypes.c_void_p];lib.stream147.restype=ctypes.c_int;assert lib.bounds147()==0
    rng=random.Random(147);samples=[b'',b'abc',b'a'*1000000]+[bytes(rng.randrange(256)for _ in range(n))for n in [1,2,55,56,57,63,64,65,119,120,127,128,129,4095,4096,4097,65536]];checks=1
    for data in samples:
        buf=ctypes.create_string_buffer(data);digest=hashlib.sha256(data).digest();one=ctypes.create_string_buffer(32);lib.one147(buf,len(data),one);assert one.raw==digest;checks+=1
        for mode in range(12):
            at=0;chunks=[0]
            while at<len(data):
                n=min(len(data)-at,([1,7,55,56,63,64,65,4096][mode]if mode<8 else rng.randrange(1,8193)));chunks.append(n);at+=n
            chunks.append(0);array=(ctypes.c_uint*len(chunks))(*chunks);result=ctypes.create_string_buffer(32);assert lib.stream147(buf,len(data),array,len(chunks),result)==1 and result.raw==digest;(checks:=checks+1)
    sources=['runtime/sha256.c','include/engine/sha256.h','tests/m14/sha147_host.c','tests/m14/sha147_host.py'];report=dict(passed=True,checks=checks,scope='Production one-shot and incremental SHA-256 vs independent hashlib across padding/block boundaries and chunk partitions; not native installer qualification',sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources})
    (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS SHA-256 streaming and retained one-shot checks',checks)

if __name__=='__main__':main()
