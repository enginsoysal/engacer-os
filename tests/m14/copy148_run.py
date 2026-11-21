"""Derive a fresh owned software-exception scenario without altering accepted hardware tests."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 from exe148_probe_build import build
 private,inputs=build();production=private.parent/'WINDOWS8.ELF'
 import replay8
 replay8.REPLACEMENTS.extend([('EngacerOS-M14STAGE2','EngacerOS-M14STAGE8'),('stage2','stage8')])
 loader=replay8.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  source=ROOT/'tests/m14/unwind_native2.py';raw=source.read_bytes();text=raw.decode()
  for a,b in replay8.REPLACEMENTS:text=text.replace(a,b)
  replacements=[('from unwind_fixtures2 import build','from copy148_build import build'),('m142-unwind','m148-copy'),("stage8/unwind'","stage8/copy-native'"),('M142_C_SEH_FINALLY_UNWIND_PASS','M148_COPY_FILE_BYTES_REPLACEMENT_METADATA_GUARDS_PASS'),('Native compiler-generated C filters/finally across five thread stacks; not C++ exception qualification','Native CopyFileW bytes, replacement, metadata, readonly/hidden guards, same-file protection, missing source and empty file'),('handled_faults_per_execution=60','copied_payload_bytes=8193,large_copied_payload_bytes=11*1024*1024')]
  for a,b in replacements:
   assert a in text,a
   text=text.replace(a,b)
  needle="try:mounted.put(product+'/7z.exe',binary)"
  assert text.count(needle)==1
  text=text.replace(needle,"try:\n   mounted.put('/System/Windows/runtime8.elf',production.read_bytes())\n   mounted.put(product+'/7z.exe',binary)\n   mounted.put('/Users/Owner/Downloads/copy148-large.bin',(fixtures/'large-source.bin').read_bytes())")
  out=ROOT/'build/m14-native/stage8/copy-native';out.mkdir(parents=True,exist_ok=True)
  (out/'observer.json').write_text(json.dumps(dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),large_source_bytes=11*1024*1024,large_source_sha256=hashlib.sha256(bytes((i*37+11)&255 for i in range(256))*(11*1024*1024//256)).hexdigest(),production_worker_inputs=inputs,production_worker_sha256=hashlib.sha256(production.read_bytes()).hexdigest(),replacements=replacements),indent=2)+'\n')
  namespace=dict(__file__=str(source),__name__='rtl148_derived',production=production);exec(compile(text,str(source),'exec'),namespace);namespace['main']()
 finally:sys.meta_path.remove(loader)
if __name__=='__main__':main()
