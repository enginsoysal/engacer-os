"""Retain native picker fixture leaf identities while replaying current media."""
from pathlib import Path
import hashlib,json
from nested147 import map_source

def main():
    canonical=Path(__file__).with_name('picker146_run.py')
    raw=canonical.read_bytes();source=map_source(raw.decode())
    scope=dict(__file__=str(canonical),__name__='picker147_derived')
    exec(compile(source,str(canonical),'exec'),scope)
    scope['main']()
    out=canonical.parents[2]/'build/m14-native/stage7/picker-native'
    (out/'observer.json').write_bytes((json.dumps(dict(canonical_path='tests/m14/picker146_run.py',canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(source.encode()).hexdigest(),adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n').encode())
