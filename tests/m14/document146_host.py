"""Production document staging with cross-page UTF-8 and retained failure checks."""
import hashlib,json,struct,subprocess,sys,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools

def main():
 out=ROOT/'build/m14-native/stage6/document-host';out.mkdir(parents=True,exist_ok=True)
 data=bytearray(b'A'*8191);data[10:12]=bytes.fromhex('c3a9');data[4095:4099]=bytes.fromhex('f09f9880');data[7000:7003]=bytes.fromhex('e282ac')
 fixture=out/'source.bin';fixture.write_bytes(struct.pack('<I',zlib.crc32(data))+data)
 exe=out/'document.exe';subprocess.run([pinned_tools()['clang'],'-std=c17','-O2','-Wall','-Wextra','-Werror','-Iinclude','tests/m12/document_host.c','-o',str(exe)],cwd=ROOT,check=True)
 result=json.loads(subprocess.check_output([str(exe),str(fixture)],cwd=ROOT));assert result['passed'];result.update(scope='Supporting hosted production staging with actual multibyte UTF-8 crossing a 4096-byte read boundary; original fourteen failure/ownership checks retained; not native execution qualification',fixture_sha256=hashlib.sha256(data).hexdigest(),source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ['kernel/desktop/document12.inc','include/engine/desktop/text146.h','tests/m12/document_host.c','tests/m14/document146_host.py']})
 (out/'results.json').write_bytes((json.dumps(result,indent=2)+'\n').encode());print(json.dumps(result,indent=2))
if __name__=='__main__':main()
