"""Compile changed physical display and input providers under legacy/M12 guards."""
import hashlib,json,subprocess
from pathlib import Path
from syntax_stage import pinned_tools
ROOT=Path(__file__).resolve().parents[2];out=ROOT/'build/m12/stage17/access-guards';out.mkdir(parents=True,exist_ok=True);compiler=pinned_tools()['clang'];flags=['--target=x86_64-unknown-none-elf','-std=c17','-O2','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-red-zone','-mgeneral-regs-only','-Wall','-Wextra','-Werror','-fsyntax-only','-Iinclude','-Ibuild/m12','-Ithird_party/bearssl/inc','-Ithird_party/bearssl-port'];names=('M2','M3','M4','M45','M5','M51','M6','M7','M71','M72','M73','M74','M75','M8','M9','M92','M10','M11');checks=[]
for mode in ('M11','M12'):
 for source in ('kernel/core/display.c','kernel/input/legacy.c','kernel/usb/xhci.c'):
  result=subprocess.run([compiler,*flags,*['-DENGINE_'+n for n in names],*(['-DENGINE_M12'] if mode=='M12' else []),source],cwd=ROOT,capture_output=True);assert result.returncode==0,(mode,source,result.stderr.decode(errors='replace'));checks.append(dict(mode=mode,source=source,passed=True))
paths=['kernel/core/graphics9.inc','kernel/core/graphics73.inc','kernel/core/display.c','kernel/input/legacy.c','kernel/usb/xhci.c','tests/m12/perf_guards17.py'];report=dict(passed=True,checks=checks,scope='Compile-only changed display/input provider guards; native M12 runtime remains separately required, and earlier M11 binaries are not requalified.',source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths});(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('PASS: six changed physical display/input guarded compilations',flush=True)
