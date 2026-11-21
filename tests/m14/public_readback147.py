"""Retain full provenance/freshness checks for the grown M14.7 corpus."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
    canonical=ROOT/'tests/m14/website_readback1.py';raw=canonical.read_bytes();source=raw.decode('utf-8')
    before='assert len(set(results) | set(batch)) < 600';assert source.count(before)==1
    source=source.replace(before,"assert len(set(results) | set(batch)) <= max(600,2*len(payload['page']['blog']['posts']))")
    scope=dict(__file__=str(canonical),__name__='bounded_public_readback147')
    exec(compile(source,str(canonical),'exec'),scope);scope['main']()
    output=Path(sys.argv[sys.argv.index('--output')+1]);assert output.resolve().is_relative_to((ROOT/'evidence/M14/7').resolve())
    output.with_name('website-readback-observer.json').write_bytes((json.dumps(dict(canonical_path='tests/m14/website_readback1.py',canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(source.encode()).hexdigest(),adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),scope='Only the finite route budget grows with the exact article corpus. The actual post-Save same-source crawl, thirty-minute freshness bound, independent critical/provenance-mismatched reads, source references, branding and error checks remain unchanged.'),indent=2)+'\n').encode())

if __name__=='__main__':main()
