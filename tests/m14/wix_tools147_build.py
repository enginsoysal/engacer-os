"""Own utility/session fixtures around unchanged original WiX and production MSI objects."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from tools147 import build as utilities

def build():
 source=ROOT/'tests/m14/wix_action147_build.py';raw=source.read_bytes();text=raw.decode();changes=[('stage7/wix-action-fixture','stage7/wix-tools-fixture'),('wix_action147_engine.c','wix_tools147_engine.c'),('wix_action147_engine.obj','wix_tools147_engine.obj')]
 for a,b in changes:assert text.count(a)==1,(a,text.count(a));text=text.replace(a,b)
 namespace={'__file__':str(source),'__name__':'wix_tools147_fixture'};exec(compile(text,str(source),'exec'),namespace);exe=namespace['build']();tools=utilities(exe.parent);report=json.loads((exe.parent/'compile-inputs.json').read_text(encoding='utf-8'));report['utility_inputs']=json.loads((exe.parent/'tools147/build-inputs.json').read_text(encoding='utf-8'));report['fixture_builder']=dict(source=source.relative_to(ROOT).as_posix(),canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),changes=changes);(exe.parent/'compile-inputs.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());return exe
if __name__=='__main__':build()
