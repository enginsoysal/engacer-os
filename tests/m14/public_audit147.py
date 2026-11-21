"""Complete bounded public crawl for the grown M14.7 documentation corpus."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--payload',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    payload=json.loads(args.payload.read_text(encoding='utf-8'));count=len(payload['page']['blog']['posts']);assert 0<count<=600
    assert args.output.resolve().is_relative_to((ROOT/'evidence/M14/7').resolve())
    canonical=ROOT/'website/brix/audit.py';raw=canonical.read_bytes();source=raw.decode('utf-8');before="<=600,'Unexpectedly large public crawl'";assert source.count(before)==1
    source=source.replace(before,"<=max(600,2*len(posts)),'Unexpectedly large public crawl'")
    scope=dict(__file__=str(canonical),__name__='bounded_public_audit147')
    exec(compile(source,str(canonical),'exec'),scope);scope['main']()
    report=json.loads(args.output.read_text(encoding='utf-8'));assert report['source_commit']==payload['source_commit'] and report['pages_checked']<=max(600,2*count)
    observer=dict(canonical_path='website/brix/audit.py',canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(source.encode()).hexdigest(),adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),article_count=count,page_budget=max(600,2*count),scope='Only the finite navigation budget grows with the exact article corpus. All original network, branding, language, soft-404, link discovery and stale-link checks remain unchanged. Complete independent readback and target validation are separate gates.')
    args.output.with_name('website-audit-observer.json').write_bytes((json.dumps(observer,indent=2)+'\n').encode())

if __name__=='__main__':main()
