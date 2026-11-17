"""Production local-search ranking; host proof only, not native UI proof."""
import ctypes,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
work=ROOT/'build/m12/stage9/search-host';work.mkdir(parents=True,exist_ok=True)
t=pinned_tools()
command([t['clang'],'--target=x86_64-pc-windows-msvc','-std=c17','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-I',ROOT/'include','-c',ROOT/'tests/m12/search_host.c','-o',work/'checks.obj'])
command([t['lld-link'],'/dll','/noentry','/nodefaultlib','/export:search12_checks','/out:'+str(work/'checks.dll'),work/'checks.obj'])
value=ctypes.CDLL(str(work/'checks.dll')).search12_checks()
assert value==0,('Production search assertion',value)
inputs=['include/engine/ui/search12.h','include/engine/desktop/start11.h','tests/m12/search_host.c','tests/m12/search_host.py']
report=dict(passed=True,checks=16,scope='Host production ranking; native interaction and publication pending',source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs})
(work/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
print('PASS: 16 production local-search ranking and bounds checks')
