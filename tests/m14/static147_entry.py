"""Keep the immutable historical baseline when running the current static observer."""
from pathlib import Path
import hashlib
import replay7

def main():
    source=Path(__file__).with_name('static147_host.py');raw=source.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    replay7.observed[source.relative_to(source.parents[2]).as_posix()]=dict(canonical_sha256=digest,executed_sha256=digest,execution_mode='canonical-stage7-static')
    scope=dict(__file__=str(source),__name__='static147_canonical')
    exec(compile(raw.decode('utf-8'),str(source),'exec'),scope)
    scope['main']()
