"""Production staging helper: invalid/I/O/changed sources never invoke app load."""
import hashlib,json,struct,subprocess,sys,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools

def main():
    out=ROOT/'build/m12/stage8/document-host';out.mkdir(parents=True,exist_ok=True)
    data=(b'ASCII text with tabs\t and newlines\n'*300)[:8191];assert len(data)==8191
    fixture=out/'source.bin';fixture.write_bytes(struct.pack('<I',zlib.crc32(data))+data)
    exe=out/'document.exe';subprocess.run([pinned_tools()['clang'],'-std=c17','-O2','-Wall','-Wextra','-Werror','-Iinclude','tests/m12/document_host.c','-o',str(exe)],cwd=ROOT,check=True)
    result=json.loads(subprocess.check_output([str(exe),str(fixture)],cwd=ROOT));assert result['passed']
    result['scope']='Hosted production document staging helper with mocked filesystem/IPC. Does not qualify CPL3 execution, actual native app dialogs or disk behavior; those remain native gates.'
    result['source_sha256']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ('kernel/desktop/document12.inc','kernel/desktop/app.c','include/engine/desktop/app.h','tests/m12/document_host.c','tests/m12/document_host.py')}
    (out/'results.json').write_bytes((json.dumps(result,indent=2)+'\n').encode());print(json.dumps(result,indent=2))
if __name__=='__main__':main()
