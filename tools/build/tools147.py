"""Build Engacer-authored x64 command utilities; never execute on the host."""
import hashlib,json,re
from pathlib import Path
from m1 import ROOT,pinned_tools,command

def build(work,tools=None):
 tools=tools or pinned_tools();out=Path(work)/'tools147';out.mkdir(parents=True,exist_ok=True);source=ROOT/'user/windows8/tool147.c';names=re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;',source.read_text(encoding='utf-8'));definition=out/'kernel32.def';definition.write_bytes(('LIBRARY kernel32.dll\nEXPORTS\n'+'\n'.join(names)+'\n').encode());command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/'kernel32.lib')]);result={}
 for kind,name in [(1,'xcopy'),(2,'cmd')]:
  obj=out/(name+'.obj');command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-std=c17','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-DTOOL147_KIND='+str(kind),'-c',source,'-o',obj]);exe=out/(name+'.exe');command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(exe),obj,out/'kernel32.lib']);result[name]=exe
 sources=['user/windows8/tool147.c','user/windows8/tools147.h','user/windows8/batch148.h','tools/build/tools147.py'];report=dict(scope='Own noninteractive x64 utility profile only; native original-action and full shell/utility compatibility are separate qualification',sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources},artifacts={p.name:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())for p in result.values()});(out/'build-inputs.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());return result
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);args=p.parse_args();build(args.work)
