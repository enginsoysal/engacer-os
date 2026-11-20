"""Check compact refusal lookup; never invoke a refusal body or original app."""
import ctypes as c
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
from m14_targets145 import generate

def main():
 for path,data in generate().items():assert(ROOT/path).read_bytes()==data,path
 out=ROOT/'build/m14-native/stage5/targets-host';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',ROOT/'tests/m14/targets145_host.c','-o',out/'targets.obj'])
 command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'targets.dll'),out/'targets.obj'])
 lib=c.CDLL(str(out/'targets.dll'));lib.refusal_key145.argtypes=[c.c_uint,c.c_char_p,c.c_uint];lib.refusal_key145.restype=c.c_uint64;lib.refusal_lookup145.argtypes=lib.refusal_key145.argtypes;lib.refusal_lookup145.restype=c.c_uint;lib.refusal_bytes145.restype=c.c_uint
 data=json.loads((ROOT/'docs/roadmap/target-import-refusals145.json').read_text(encoding='utf-8'));checked=0
 for row in data['imports']:
  symbol=row['symbol'];ordinal=int(symbol[1:])if symbol.startswith('#')else 0;name=None if ordinal else symbol.encode();provider=data['provider_ids'][row['dll']]
  assert lib.refusal_key145(provider,name,ordinal)==int(row['key'],16)
  assert lib.refusal_lookup145(provider,name,ordinal)==1
  checked+=2
 for provider in data['provider_ids'].values():
  assert lib.refusal_lookup145(provider,b'EngacerUnknownExport145',0)==0
  checked+=1
 assert lib.refusal_lookup145(1,b'GetStdHandle',0)==0 and lib.refusal_lookup145(3,b'SysAllocString',0)==0
 size=lib.refusal_bytes145();assert size==data['table_bytes']and size<=8192
 result=dict(passed=True,scope='Host refusal-key and generation checks only; no refusal-body invocation or API compatibility proof',assertions=checked+3,keys=data['refusal_keys'],immutable_key_bytes=size,sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in('user/windows8/target-guards145.inc','user/windows8/target-refusals145.inc','user/windows8/providers145.inc','tools/build/m14_targets145.py','tests/m14/targets145_host.c')})
 (out/'results.json').write_bytes((json.dumps(result,indent=2)+'\n').encode());print(json.dumps(result))

if __name__=='__main__':main()
