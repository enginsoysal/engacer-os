"""Derive a fresh owned software-exception scenario without altering accepted hardware tests."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 import replay8
 replay8.REPLACEMENTS.extend([('EngacerOS-M14STAGE2','EngacerOS-M14STAGE8'),('stage2','stage8')])
 loader=replay8.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  source=ROOT/'tests/m14/unwind_native2.py';raw=source.read_bytes();text=raw.decode()
  for a,b in replay8.REPLACEMENTS:text=text.replace(a,b)
  replacements=[('from unwind_fixtures2 import build','from software148_build import build'),('m142-unwind','m148-software'),("stage8/unwind'","stage8/software-native'"),('M142_C_SEH_FINALLY_UNWIND_PASS','M148_SOFTWARE_VECTORED_C_SEH_FINALLY_PASS'),('Native compiler-generated C filters/finally across five thread stacks; not C++ exception qualification','Native software raises: 48 vectored resumptions and 60 C filters/finally across five stacks; continuable flags-zero profile only'),('handled_faults_per_execution=60','handled_faults_per_execution=60,vectored_continuations_per_execution=48')]
  for a,b in replacements:
   assert a in text,a
   text=text.replace(a,b)
  out=ROOT/'build/m14-native/stage8/software-native';out.mkdir(parents=True,exist_ok=True)
  (out/'observer.json').write_text(json.dumps(dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),replacements=replacements),indent=2)+'\n')
  namespace=dict(__file__=str(source),__name__='software148_derived');exec(compile(text,str(source),'exec'),namespace);namespace['main']()
 finally:sys.meta_path.remove(loader)
if __name__=='__main__':main()
