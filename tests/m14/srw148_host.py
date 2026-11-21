"""Actual production SRW algorithm under host threads/address waits; not native acceptance."""
import concurrent.futures,ctypes as c,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 out=ROOT/'build/m14-native/stage8/srw-host';out.mkdir(parents=True,exist_ok=True)
 source=ROOT/'tests/m14/srw148_host.c';binary=out/'srw148.dll'
 subprocess.run(['clang','-shared','-O2','-Wall','-Wextra','-Werror',str(source),'-o',str(binary)],check=True,cwd=ROOT)
 library=c.CDLL(str(binary));kernel=c.WinDLL('kernelbase');library.bind148.argtypes=[c.c_void_p,c.c_void_p]
 library.bind148(c.cast(kernel.WaitOnAddress,c.c_void_p),c.cast(kernel.WakeByAddressAll,c.c_void_p));assert library.basic148()==1
 library.writer148.argtypes=library.reader148.argtypes=[c.c_uint];library.count148.restype=c.c_uint64
 with concurrent.futures.ThreadPoolExecutor(max_workers=8)as pool:
  futures=[pool.submit(library.writer148 if i<4 else library.reader148,25000)for i in range(8)]
  assert all(f.result(timeout=90)==1 for f in futures)
 assert library.count148()==100000 and library.basic148()==1
 report=dict(passed=True,scope=__doc__,writer_threads=4,reader_threads=4,rounds_per_thread=25000,final_writes=100000,
  sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ['user/windows8/srw148.inc','tests/m14/srw148_host.c','tests/m14/srw148_host.py']})
 (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS production SRW host concurrency and exact final writes; native tests pending')
if __name__=='__main__':main()
