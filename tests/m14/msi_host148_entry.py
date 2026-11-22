"""Keep MSI host-only syscall adapters explicit after EXE context isolation."""
import ctypes,hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 import replay8
 kind=sys.argv[1];assert kind in ('files','install','remove','terminal','transaction')
 loader=replay8.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  original=ROOT/f"tests/m14/{'transaction'if kind=='transaction'else'files'}147_host.c";raw=original.read_bytes();source=raw.decode('utf-8')
  source=re.sub(r'#include "([^"]+)"',lambda m:'#include "'+(original.parent/m[1]).resolve().as_posix()+'"',source)
  needle='#include "'+(ROOT/'kernel/windows8/transaction147.inc').as_posix()+'"';assert source.count(needle)==1
  shim='''/* This existing host harness models ordinary MSI context only. */
static struct {unsigned exe_context148;} msi_space148;
static void *unused148;
static unsigned active_space142,exe_branch_calls148;
static __typeof__(msi_space148)*spaces142[]={&msi_space148};
static unsigned exe_user_grant148(const char*p,unsigned ancestor){(void)p;(void)ancestor;++exe_branch_calls148;return 0;}
__declspec(dllexport) unsigned exe_branch_count148(void){return exe_branch_calls148;}
'''.replace('static void *unused148;\n','')
  source=source.replace(needle,shim+needle)
  out=ROOT/f'build/m14-native/stage8/{kind}-host';out.mkdir(parents=True,exist_ok=True);generated=out/'msi-context148_host.c';generated.write_bytes(source.encode())
  canonical=ROOT/f'tests/m14/{kind}147_host.py';rr=canonical.read_bytes();adapted=rr.decode('utf-8')
  for before,after in replay8.REPLACEMENTS:adapted=adapted.replace(before,after)
  scope=dict(__file__=str(canonical),__name__='msi_host148_'+kind);exec(compile(adapted,str(canonical),'exec'),scope);command=scope['command']
  def compile_current(args):
   args=[generated if isinstance(a,(str,Path))and str(a)==str(original)else a for a in args];return command(args)
  scope['command']=compile_current;scope['main']()
  dlls=list(out.glob('*.dll'));assert len(dlls)==1,dlls;lib=ctypes.CDLL(str(dlls[0]));assert lib.exe_branch_count148()==0
  (out/'preparation-receipt.json').write_bytes((json.dumps(dict(passed=True,scope=__doc__,context='Ordinary MSI only. EXE branch is fail-closed and must never execute in this host harness; native EXE grants are tested separately.',exe_branch_calls=0,canonical_c_sha256=sha(raw),generated_c_sha256=sha(generated.read_bytes()),canonical_runner_sha256=sha(rr),executed_runner_sha256=sha(adapted.encode()),adapter_sha256=sha(Path(__file__).read_bytes())),indent=2)+'\n').encode())
 finally:sys.meta_path.remove(loader)
if __name__=='__main__':main()
