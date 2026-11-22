"""Retain complete public crawl/readback gates under stage-eight evidence paths.

Independent article provenance is not a native homepage Save receipt.
"""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 kind=sys.argv.pop(1);assert kind in ('audit','readback')
 canonical=ROOT/('tests/m14/public_audit147.py'if kind=='audit'else'tests/m14/public_readback147.py')
 raw=canonical.read_bytes();source=raw.decode('utf-8').replace('evidence/M14/7','evidence/M14/8')
 assert source!=raw.decode('utf-8')
 scope=dict(__file__=str(canonical),__name__='public148_'+kind)
 exec(compile(source,str(canonical),'exec'),scope);scope['main']()
 out=ROOT/'evidence/M14/8'
 (out/('website-'+kind+'-stage148-derivation.json')).write_bytes((json.dumps(dict(passed=True,scope=__doc__,canonical_path=canonical.relative_to(ROOT).as_posix(),canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(source.encode()).hexdigest(),adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),only_change='Output evidence confinement changes from stage seven to stage eight. Full finite crawl, all link/branding/language/soft-404/source-reference checks remain.'),indent=2)+'\n').encode())
if __name__=='__main__':main()
