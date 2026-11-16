"""Exercise the actual bounded C decoder against generated and installed pages."""
import argparse,hashlib,json,random,struct,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'tools/build')]
from m1 import pinned_tools
from m12_pack import compress,record

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',type=int,required=True);stage=parser.parse_args().stage;assert 8<=stage<=18
    assert not (ROOT/f'evidence/M12/{stage}/publication-results.json').exists()
    out=ROOT/f'build/m12/stage{stage}/pack-host';out.mkdir(exist_ok=True,parents=True)
    rnd=random.Random(127);pages=[bytes(4096),b'A'*4096,bytes(range(256))*16]
    pages += [rnd.randbytes(4096) for _ in range(30)]
    pages += [(rnd.randbytes(n)*4096)[:4096] for n in (1,2,3,4,7,15,16,127,128,255,256,1024)]
    for _ in range(200):
        p=bytearray(rnd.randbytes(4096));start=rnd.randrange(4000);p[start:]=bytes(4096-start);pages.append(bytes(p))
    # Exercise the actual installed payload, not a synthetic model alone.
    payload_hashes={}
    for name in ('build/m12/installed/KERNEL.ELF','build/m12/BOOTX64.EFI'):
        data=(ROOT/name).read_bytes();payload_hashes[name]=hashlib.sha256(data).hexdigest()
        pages += [data[i:i+4096].ljust(4096,b'\0') for i in range(0,len(data),4096)]
    tests=[(compress(p),p) for p in pages if len(compress(p))<4096]
    good=len(tests)
    for encoded,expected in list(tests[:12]):
        for n in range(len(encoded)):tests.append((encoded[:n],None))
    tests += [(bytes([0,0,0]),None),(bytes([0x1f,65,1,0,255])*80,None),(bytes([0xff])+bytes([255])*30,None)]
    # Arbitrary malformed blocks need memory safety; accidental valid ones are allowed.
    tests += [(rnd.randbytes(rnd.randrange(1,100)),False) for _ in range(10000)]
    data=struct.pack('<I',len(tests))+b''.join(struct.pack('<I',len(x))+x for x,_ in tests)
    inp=out/'cases.bin';res=out/'decoded.bin';inp.write_bytes(data)
    exe=out/'decoder.exe';subprocess.run([pinned_tools()['clang'],'-std=c17','-O2','-Wall','-Wextra','-Werror','-Iinclude','tests/m12/pack_host.c','-o',str(exe)],cwd=ROOT,check=True)
    subprocess.run([str(exe),str(inp),str(res)],cwd=ROOT,check=True)
    decoded=res.read_bytes();assert len(decoded)==len(tests)*4100
    for i,(_,expected) in enumerate(tests):
        at=i*4100;valid=struct.unpack_from('<I',decoded,at)[0]
        if isinstance(expected,bytes):assert valid and decoded[at+4:at+4100]==expected,i
        elif expected is None:assert not valid,i
    # Raw random, zero and encoded pages use distinct backward-readable flags.
    assert struct.unpack_from('<I',record(8,bytes(4096)))[0]==0x80000008
    assert struct.unpack_from('<I',record(8,pages[3]))[0]==8
    assert struct.unpack_from('<I',record(8,b'A'*4096))[0]==0x40000008
    result=dict(passed=True,roundtrip_pages=good,payload_sha256=payload_hashes,malformed_and_fuzz_cases=len(tests)-good,guard_bytes_unchanged=True,heap_allocations=0,page_bytes=4096,
        source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ('include/engine/install/pack12.h','tools/build/m12_pack.py','tests/m12/pack_host.c','tests/m12/pack_stage.py')},
        scope='Actual production C block decoder and build encoder. Native install/recovery and firmware startup remain separate required gates.')
    (out/'results.json').write_bytes((json.dumps(result,indent=2)+'\n').encode());print(json.dumps(result))
if __name__=='__main__':main()
