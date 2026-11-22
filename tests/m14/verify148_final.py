"""Verify the fresh release8 campaign with the unchanged stage-eight gates."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 canonical=ROOT/'tests/m14/verify8.py';raw=canonical.read_bytes();source=raw.decode('utf-8');before="work/'development/final8'";assert source.count(before)==1;source=source.replace(before,"work/'development/release8'")
 scope=dict(__file__=str(canonical),__name__='final148_verification');exec(compile(source,str(canonical),'exec'),scope);scope['main']()
 out=ROOT/'evidence/M14/8';accepted=json.loads((out/'acceptance-results.json').read_text(encoding='utf-8'))
 (out/'verification-derivation.json').write_bytes((json.dumps(dict(passed=True,build_id=accepted['build_id'],scope=__doc__,canonical_path='tests/m14/verify8.py',canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(source.encode()).hexdigest(),adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),only_change={'before':'development/final8','after':'development/release8'},reason='A fresh, non-resumed campaign follows exact generated-source correction and replacement production media.'),indent=2)+'\n').encode())
if __name__=='__main__':main()
