"""Test-only owner drives the production deferred-thread dispatcher and unchanged WiX."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def build():
 source=ROOT/'tests/m14/wix_tools147_build.py';raw=source.read_bytes();text=raw.decode();changes=[('stage7/wix-tools-fixture','stage7/wix-system-fixture'),('wix_tools147_engine.c','wix_system147_engine.c'),('wix_tools147_engine.obj','wix_system147_engine.obj')]
 for a,b in changes:assert text.count(a)==1,(a,text.count(a));text=text.replace(a,b)
 namespace={'__file__':str(source),'__name__':'wix_threads147_fixture'};exec(compile(text,str(source),'exec'),namespace);exe=namespace['build']();report=json.loads((exe.parent/'compile-inputs.json').read_text(encoding='utf-8'));report['thread_builder']=dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),changes=changes);(exe.parent/'compile-inputs.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());return exe
if __name__=='__main__':build()
