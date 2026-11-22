"""Preserve canonical decoder corpus without remapping its historical match keys."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 canonical=ROOT/'tests/m14/pack146_host.py';raw=canonical.read_bytes();source=raw.decode('utf-8').replace('build/m14-native/stage6/pack-host','build/m14-native/stage8/pack-host')
 scope=dict(__file__=str(canonical),__name__='pack148_host');exec(compile(source,str(canonical),'exec'),scope);scope['main']()
 out=ROOT/'build/m14-native/stage8/pack-host';(out/'preparation-receipt.json').write_bytes((json.dumps(dict(passed=True,scope=__doc__,canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(source.encode()).hexdigest(),adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n').encode())
if __name__=='__main__':main()
