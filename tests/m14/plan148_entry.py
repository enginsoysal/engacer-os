"""Run original MSI plan workers against the same current-stage host library."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 import replay8
 loader=replay8.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  canonical=ROOT/'tests/m14/plan147_host.py';raw=canonical.read_bytes();source=raw.decode('utf-8')
  for before,after in replay8.REPLACEMENTS:source=source.replace(before,after)
  needle='str(Path(__file__).resolve())';assert source.count(needle)==1;source=source.replace(needle,"str(ROOT/'tests/m14/plan148_entry.py')")
  scope=dict(__file__=str(canonical),__name__='plan148_host');exec(compile(source,str(canonical),'exec'),scope);scope['main']()
  if len(sys.argv)==1:
   out=ROOT/'build/m14-native/stage8/plan-host';(out/'preparation-receipt.json').write_bytes((json.dumps(dict(passed=True,scope=__doc__,canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(source.encode()).hexdigest(),adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),workers=16),indent=2)+'\n').encode())
 finally:sys.meta_path.remove(loader)
if __name__=='__main__':main()
