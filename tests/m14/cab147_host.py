"""Streaming original CAB bytes vs an independent system data-only decoder."""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import random
import struct
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command

def main():
    out=ROOT/'build/m14-native/stage7/cab-host';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools();objects=[]
    for source in ['user/windows8/cab147.c','third_party/libmspack/lzxd.c','tests/m14/cab147_host.c']:
        obj=out/(Path(source).stem+'.obj')
        command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-std=c17','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-Wall','-Wextra','-Werror','-DMSPACK_NO_DEFAULT_SYSTEM','-DSIZEOF_OFF_T=8','-DDEBUG=0','-I',ROOT/'third_party/libmspack-port','-I',ROOT/'third_party/libmspack','-I',ROOT/'include','-I',ROOT/'user/windows8','-c',ROOT/source,'-o',obj]);objects.append(obj)
    dll=out/'cab147.dll';command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(dll),*objects]);lib=ctypes.CDLL(str(dll))
    alloc_type=ctypes.CFUNCTYPE(ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t);free_type=ctypes.CFUNCTYPE(None,ctypes.c_void_p,ctypes.c_void_p)
    live={};state={'fail':-1,'bytes':0,'peak':0,'bad_free':False}
    @alloc_type
    def allocate(context,n):
        if state['fail']==0:return None
        if state['fail']>0:state['fail']-=1
        buf=ctypes.create_string_buffer(n);address=ctypes.addressof(buf);live[address]=(buf,n);state['bytes']+=n;state['peak']=max(state['peak'],state['bytes']);return address
    @free_type
    def release(context,address):
        if address not in live:state['bad_free']=True;return
        state['bytes']-=live.pop(address)[1]
    class File(ctypes.Structure):
        _fields_=[('name',ctypes.c_char_p),('offset',ctypes.c_uint),('size',ctypes.c_uint),('date',ctypes.c_ushort),('time',ctypes.c_ushort),('attributes',ctypes.c_ushort)]
    sink_type=ctypes.CFUNCTYPE(ctypes.c_int,ctypes.c_void_p,ctypes.POINTER(File),ctypes.c_uint,ctypes.c_void_p,ctypes.c_uint)
    lib.init147.argtypes=[alloc_type,free_type];lib.open147.argtypes=[ctypes.c_void_p,ctypes.c_uint];lib.walk147.argtypes=[sink_type,ctypes.c_void_p];lib.file147.argtypes=[ctypes.c_uint];lib.file147.restype=ctypes.POINTER(File);lib.init147(allocate,release)
    inputs=ROOT/'build/m14-native/stage7/cab-inputs';receipt=json.loads((inputs/'inputs.json').read_text(encoding='utf-8-sig'));reports=[]
    targets=json.loads((ROOT/'docs/roadmap/m14-targets.json').read_text());reviewed={t['installer']['file']:t['installer']['sha256']for t in targets['targets']}
    expand=Path(os.environ['SystemRoot'])/'System32/expand.exe';assert expand.is_file()
    checks=0
    def check(yes):
        nonlocal checks
        assert yes;checks+=1
    for item in receipt['inputs']:
        check(not live and state['bytes']==0);state['peak']=0
        check(reviewed[item['package']]==item['package_sha256']);cab=inputs/item['cabinet'];raw=cab.read_bytes();check(hashlib.sha256(raw).hexdigest()==item['cabinet_sha256']);buffer=ctypes.create_string_buffer(raw)
        reference=out/('reference-'+cab.stem);reference.mkdir(exist_ok=True)
        # Built-in expand only decodes archive data to owned scratch. It never
        # executes an MSI action, installer, DLL or Windows payload.
        subprocess.run([str(expand),str(cab),'-F:*',str(reference)],cwd=ROOT,check=True,capture_output=True)
        check(lib.open147(buffer,len(raw))==0);count=lib.count147();total=lib.bytes147();check(count in (106,217));expected={};observed={};errors=[]
        for i in range(count):
            f=lib.file147(i).contents;name=f.name.decode();data=(reference/name).read_bytes();check(len(data)==f.size);expected[name]=hashlib.sha256(data).hexdigest();observed[name]={'offset':0,'hash':hashlib.sha256()}
        @sink_type
        def sink(context,file,offset,data,n):
            try:
                f=file.contents;name=f.name.decode();record=observed[name];assert offset==record['offset'] and offset+n<=f.size
                record['hash'].update(ctypes.string_at(data,n) if n else b'');record['offset']+=n;return 0
            except Exception as error:errors.append(type(error).__name__+': '+str(error));return 1
        check(lib.walk147(sink,None)==0 and not errors)
        for i in range(count):
            f=lib.file147(i).contents;name=f.name.decode();check(observed[name]['offset']==f.size and observed[name]['hash'].hexdigest()==expected[name])
        # Force early sink cancellation; all decoder-owned allocations release.
        metadata_bytes=state['bytes']
        @sink_type
        def refuse(context,file,offset,data,n):return 1
        check(lib.walk147(refuse,None)==3 and state['bytes']==metadata_bytes)
        for fail in range(4):
            state['fail']=fail;status=lib.walk147(refuse,None);check(status in (2,3) and state['bytes']==metadata_bytes);state['fail']=-1
        peak=state['peak'];lib.close147();check(not live and not state['bad_free'])
        state['fail']=0;check(lib.open147(buffer,len(raw))==2 and not live);state['fail']=-1
        # Full validation precedes every sink call; corrupted format metadata
        # and checked data checksums cannot expose partial caller output.
        mutations=[(8,struct.pack('<I',len(raw)+1)),(26,b'\x02\x00'),(28,b'\x01\x01'),(30,b'\x01\x00'),(36,struct.pack('<I',len(raw))),(40,b'\x01\x04')]
        for at,value in mutations:
            changed=bytearray(raw);changed[at:at+len(value)]=value;bad=ctypes.create_string_buffer(bytes(changed));check(lib.open147(bad,len(changed))==1 and not live)
        reports.append(dict(package=item['package'],package_sha256=item['package_sha256'],cabinet_sha256=item['cabinet_sha256'],files=count,expanded_bytes=total,decoder_and_metadata_peak_bytes=peak,all_file_sha256=expected,retained_allocations=len(live)))
    # Bounded malformed/truncated headers do not allocate or dereference past
    # the declared range; every trial closes any successfully parsed metadata.
    rng=random.Random(147)
    for _ in range(2000):
        data=bytes(rng.randrange(256) for _ in range(rng.randrange(128)));buffer=ctypes.create_string_buffer(data);check(lib.open147(buffer,len(data))==1 and not live)
    sources=['user/windows8/cab147.c','user/windows8/cab147.h','tests/m14/cab147_host.c','tests/m14/cab147_host.py','tools/m14/cab_extract147.ps1','third_party/libmspack/lzxd.c']
    report=dict(passed=True,checks=checks,scope='Production streaming LZX and every original file hash vs built-in data-only expand; no original installer/application or native guest execution',decoder_reference_sha256=hashlib.sha256(expand.read_bytes()).hexdigest(),originals=reports,limits=['Self-contained single-folder LZX, 8-MiB cabinet input, 256 files, 1024 blocks, 32-MiB expanded data','Peak excludes caller-owned original MSI/CAB bytes and caller transaction state; it is not total process or OS RAM'],sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources})
    (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS streaming original CAB checks',checks)

if __name__=='__main__':main()
