"""Diagnose actual mapping handles on a labelled production-worker development clone."""
import argparse,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--development-worker',type=Path,required=True);args=parser.parse_args();worker=args.development_worker.resolve();assert worker.is_relative_to((ROOT/'build/m14-native').resolve())
 import replay8
 loader=replay8.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  canonical=ROOT/'tests/m14/mapping146_run.py';raw=canonical.read_bytes();source=raw.decode()
  for old,new in replay8.REPLACEMENTS:source=source.replace(old,new)
  source=source.replace('stage8/mapping-native','stage8/mapping148-development')
  needle="try:mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())";assert source.count(needle)==1
  source=source.replace(needle,"try:\n  mounted.put('/System/Windows/runtime8.elf',development_worker148.read_bytes())\n  mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())")
  sys.argv=[str(canonical),'--cycles','1'];namespace=dict(__name__='mapping148_development',__file__=str(canonical),development_worker148=worker)
  exec(compile(source,str(canonical),'exec'),namespace);namespace['main']()
  out=ROOT/'build/m14-native/stage8/mapping148-development';record=json.loads((out/'results.json').read_text());record.update(full_production_media=False,development_worker_sha256=hashlib.sha256(worker.read_bytes()).hexdigest(),observer_derivation=dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(source.encode()).hexdigest(),adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()));(out/'results.json').write_bytes((json.dumps(record,indent=2)+'\n').encode())
 finally:sys.meta_path.remove(loader)

if __name__=='__main__':main()
