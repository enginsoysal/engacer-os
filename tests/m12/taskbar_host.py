"""Production taskbar union/layout bounds; not native window interaction proof."""
import ctypes,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
work=ROOT/'build/m12/stage10/taskbar-host';work.mkdir(parents=True,exist_ok=True);t=pinned_tools()
command([t['clang'],'--target=x86_64-pc-windows-msvc','-std=c17','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-I',ROOT/'include','-c',ROOT/'tests/m12/taskbar_host.c','-o',work/'checks.obj'])
command([t['lld-link'],'/dll','/noentry','/nodefaultlib','/export:taskbar12_checks','/export:taskbar12_total','/out:'+str(work/'checks.dll'),work/'checks.obj'])
dll=ctypes.CDLL(str(work/'checks.dll'));result=dll.taskbar12_checks();assert result==0,('Production taskbar assertion',result)
inputs=['include/engine/ui/taskbar12.h','tests/m12/taskbar_host.c','tests/m12/taskbar_host.py']
report=dict(passed=True,checks=dll.taskbar12_total(),scope='Actual production union/geometry bounds including corrupt IDs and unsigned width edges; real native group/close/overflow tasks remain required',source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs})
(work/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode('utf-8'));print(json.dumps(report))
