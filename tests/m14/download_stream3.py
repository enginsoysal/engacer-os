"""Exercise the production 128-MiB stream boundary without retaining the body in RAM."""
import ctypes as c,hashlib,json,os,sys,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tests/m12'),str(ROOT/'tests/m13')]
os.environ['ENGACER12_IMAGE']='EngacerOS-M14STAGE3'
import ui
from access_fixtures16 import clone
from fixture1 import library,StoppedDisk,types

def main():
    out=ROOT/'build/m14-native/stage3/download-stream';out.mkdir(parents=True,exist_ok=True)
    base=json.loads((ROOT/'build/m14-native/stage3/ordinary/results.json').read_text(encoding='utf-8'))
    source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage3-ordinary'/base['owned_fixture']/'owned.img'
    work,disk,cloned=clone(ui,source,'m143-regress-download-stream')
    lib=library();mounted=StoppedDisk(disk,lib);vp=c.byref(mounted.volume)
    report=dict(passed=False,scope='Production native C storage host execution; not an HTTPS or browser runtime test',source_sha256=hashlib.sha256((ROOT/'kernel/storage/volume6.c').read_bytes()).hexdigest(),clone=cloned,checks=[])
    try:
        target=b'/Users/Owner/Downloads/large-stream.bin'
        size=95924224;chunk=bytes(range(256))*16;digest=hashlib.sha256();crc=0
        assert lib.v6_stream_begin(vp,target,size)==0
        assert not any(e.kind and e.path==target for e in mounted.volume.entries)
        for offset in range(0,size,len(chunk)):
            body=chunk[:min(len(chunk),size-offset)]
            assert lib.v6_stream_append(vp,body,len(body))==0
            digest.update(body);crc=zlib.crc32(body,crc)
        assert lib.v6_stream_finish(vp)==0 and lib.v6_verify(vp,target)==0
        entry=next(e for e in mounted.volume.entries if e.kind and e.path==target)
        assert entry.size==size and entry.crc==crc
        stored=hashlib.sha256();buffer=c.create_string_buffer(4096)
        for offset in range(0,size,4096):
            got=c.c_uint();assert lib.v6_read(vp,target,offset,buffer,min(4096,size-offset),c.byref(got))==0
            stored.update(buffer.raw[:got.value])
        assert stored.digest()==digest.digest()
        report['checks'].append(dict(name='Firefox-sized create-only stream, durable CRC and independent readback',bytes=size,sha256=stored.hexdigest(),body_buffer_bytes=4096))
        for bound in (128*1024**2+1,2**64-1):assert lib.v6_stream_begin(vp,b'/Users/Owner/Downloads/refused.bin',bound)!=0
        partial=b'/Users/Owner/Downloads/cancelled.bin'
        assert lib.v6_stream_begin(vp,partial,128*1024**2)==0
        assert lib.v6_stream_append(vp,chunk,len(chunk))==0
        lib.v6_stream_abort(vp)
        assert not any(e.kind and e.path in (partial,b'/Users/Owner/Downloads/refused.bin') for e in mounted.volume.entries)
        assert lib.v6_stream_begin(vp,target,4096)!=0
        assert lib.v6_verify(vp,target)==0
        report['checks'].append('Oversize reservations, cancellation and existing-target refusal preserve the namespace and committed original')
        report['passed']=True
    finally:
        mounted.close();(out/'results.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
