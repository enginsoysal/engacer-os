"""Seed stopped disposable native test disks using the production volume code."""
import ctypes as c
import importlib.util
import os
from pathlib import Path
import struct
import sys
import uuid

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/build'),str(ROOT/'tests/m6')]
from m1 import pinned_tools, command
spec = importlib.util.spec_from_file_location('volume_types141', ROOT/'tests/m6/volume.py')
types = importlib.util.module_from_spec(spec)
spec.loader.exec_module(types)

def library(extra=()):
    assert all(name in ['remove']for name in extra)
    work = ROOT/'build/m14-native/host-volume'/uuid.uuid4().hex
    work.mkdir(parents=True, exist_ok=True)
    tools = pinned_tools()
    obj = work/'volume.obj'
    command([tools['clang'], '--target=x86_64-pc-windows-msvc', '-std=c17', '-O2',
             '-Wall', '-Wextra', '-Werror', '-ffreestanding', '-fno-builtin',
             '-fno-stack-protector', '-DENGINE_M7', '-DENGINE_M8', '-DENGINE_M11', '-DENGINE_M14',
             '-I', ROOT/'include', '-c', ROOT/'kernel/storage/volume6.c', '-o', obj])
    names = ['mount','mkdir','put','read','verify','stream_begin','stream_append','stream_finish','stream_abort']+list(extra)
    dll = work/'volume.dll'
    command([tools['lld-link'], '/dll','/noentry','/nodefaultlib','/timestamp:0',
             *['/export:v6_'+n for n in names], obj, '/out:'+str(dll)])
    lib = c.CDLL(str(dll))
    vp = c.POINTER(types.Volume)
    for n in ['mount','stream_finish','stream_abort']:
        getattr(lib,'v6_'+n).argtypes=[vp]
    for n in ['mkdir','verify']:
        getattr(lib,'v6_'+n).argtypes=[vp,c.c_char_p]
    lib.v6_put.argtypes=[vp,c.c_char_p,c.c_uint64,types.SOURCE,c.c_void_p]
    lib.v6_stream_begin.argtypes=[vp,c.c_char_p,c.c_uint64]
    lib.v6_stream_append.argtypes=[vp,c.c_void_p,c.c_uint]
    lib.v6_read.argtypes=[vp,c.c_char_p,c.c_uint64,c.c_void_p,c.c_uint,c.POINTER(c.c_uint)]
    if 'remove'in extra:lib.v6_remove.argtypes=[vp,c.c_char_p]
    return lib

class StoppedDisk:
    def __init__(self, path, lib):
        path = Path(path).resolve()
        base = (Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6').resolve()
        assert path.is_relative_to(base) and path.name=='owned.img' and path.is_file()
        self.file = path.open('r+b')
        self.file.seek(1024+4*128)
        part = self.file.read(128)
        first,last = struct.unpack_from('<QQ',part,32)
        assert first==2369536 and first<last<path.stat().st_size//512
        self.offset = first*512
        self.blocks = (last-first+1)//8
        self.read_cb = types.IO(self.read)
        self.write_cb = types.IO(self.write)
        self.flush_cb = types.FLUSH(self.flush)
        self.volume = types.Volume(read=self.read_cb,write=self.write_cb,flush=self.flush_cb,blocks=self.blocks)
        self.lib = lib
        assert lib.v6_mount(c.byref(self.volume))==0

    def read(self,ctx,block,out,n):
        if n!=4096 or block>=self.blocks:return 1
        self.file.seek(self.offset+block*4096)
        data=self.file.read(n)
        if len(data)!=n:return 1
        c.memmove(out,data,n)
        return 0

    def write(self,ctx,block,data,n):
        if n!=4096 or block>=self.blocks:return 1
        self.file.seek(self.offset+block*4096)
        self.file.write(c.string_at(data,n))
        return 0

    def flush(self,ctx):
        self.file.flush()
        return 0

    def put(self,path,data):
        @types.SOURCE
        def source(ctx,offset,out,n):
            c.memmove(out,data[offset:offset+n],n)
            return 0
        assert self.lib.v6_put(c.byref(self.volume),path.encode(),len(data),source,None)==0,path
        assert self.lib.v6_verify(c.byref(self.volume),path.encode())==0

    def close(self):
        self.file.flush()
        self.file.close()
