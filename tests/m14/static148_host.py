"""Measure current stage-eight images against the immutable accepted stage seven."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 canonical=ROOT/'tests/m14/static147_host.py';raw=canonical.read_bytes();text=raw.decode()
 replacements=[('M14.7','M14.8'),('M14.6','M14.7'),('STAGE7','STAGE8'),('stage7','stage8'),('evidence/M14/6','evidence/M14/7')]
 for before,after in replacements:text=text.replace(before,after)
 namespace=dict(__name__='static148_measurement',__file__=str(canonical))
 exec(compile(text,str(canonical),'exec'),namespace);namespace['main']()
 report_path=ROOT/'build/m14-native/stage8/static-host/results.json';report=json.loads(report_path.read_text())
 report['derivation']=dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),replacements=replacements)
 for path in [report_path,ROOT/'build/m14-native/stage8/static-resource-comparison.json']:path.write_bytes((json.dumps(report,indent=2)+'\n').encode())

if __name__=='__main__':main()
