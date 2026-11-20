"""Build the owned MSI core fixture; never execute this PE on the host."""
from pathlib import Path
import hashlib
import json
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command

def build():
    out=ROOT/'build/m14-native/stage7/session-fixture';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
    definition=out/'kernel32.def';definition.write_bytes(b'LIBRARY kernel32.dll\nEXPORTS\nGlobalAlloc\nGlobalFree\nGetStdHandle\nWriteFile\nExitProcess\n')
    command([tools['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/'kernel32.lib')])
    command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',ROOT/'tests/m14/session147_native.c','-o',out/'session.obj'])
    command([tools['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(out/'session.exe'),out/'session.obj',out/'kernel32.lib'])
    inputs=['tests/m14/session147_native.c','user/windows8/msi-condition147.h','user/windows8/msi-properties147.h','tests/m14/session147_build.py']
    (out/'compile-inputs.json').write_bytes((json.dumps(dict(fixture_sha256=hashlib.sha256((out/'session.exe').read_bytes()).hexdigest(),sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in inputs},scope='Exact owned PE compilation inputs; execution must be separately qualified in a native guest'),indent=2)+'\n').encode())
    return out/'session.exe'

if __name__=='__main__':build()
