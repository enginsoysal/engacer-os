"""Retain all 21 original WiX action assertions with explicit nested stage mapping."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 import replay8
 loader=replay8.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  canonical=ROOT/'tests/m14/wix_action147_lifetimes.py';raw=canonical.read_bytes();source=replay8.map_current148(raw.decode('utf-8'))
  needle='text=raw.decode()';assert source.count(needle)==1
  source=source.replace(needle,'text=map_current148(raw.decode())')
  scope=dict(__file__=str(canonical),__name__='wix_action148_lifetimes',map_current148=replay8.map_current148)
  exec(compile(source,str(canonical),'exec'),scope);scope['main']()
  out=ROOT/'build/m14-native/stage8/wix-action-native'
  (out/'entry-observer.json').write_bytes((json.dumps(dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(source.encode()).hexdigest(),adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cycles=21,scope=__doc__),indent=2)+'\n').encode())
 finally:sys.meta_path.remove(loader)

if __name__=='__main__':main()
