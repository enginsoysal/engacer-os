"""Keep historical paint/fault coverage with actual selected-font metrics."""
import hashlib,json,os,sys
from pathlib import Path
from types import ModuleType
ROOT=Path(__file__).resolve().parents[2]
def digest(value):return hashlib.sha256(value).hexdigest()
def main():
 import replay8
 kind=sys.argv[1];assert kind in ('fault','paint')
 os.environ['ENGACER12_IMAGE']='EngacerOS-M14STAGE8'
 loader=replay8.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  canonical=ROOT/f'tests/m14/{kind}144_native.c';raw=canonical.read_bytes();source=raw.decode('utf-8')
  assert source.count('int size[2];')==1 and source.count('size[1]==16')==1
  source=source.replace('int size[2];','int size[2],metrics[15];').replace('size[1]==16','GetTextMetricsW(dc,metrics)&&metrics[0]>0&&size[1]==metrics[0]')
  source=source.replace('__declspec(dllimport) int TextOutW','__declspec(dllimport) int GetTextMetricsW(H,void*);\n__declspec(dllimport) int TextOutW')
  assert '__declspec(dllimport) int GetTextMetricsW(H,void*);'in source
  out=ROOT/f'build/m14-native/stage8/{kind}148-fixture';out.mkdir(parents=True,exist_ok=True);generated=out/f'{kind}148_native.c';generated.write_bytes(source.encode())
  builder=ROOT/f'tests/m14/{kind}144_build.py';builder_raw=builder.read_bytes();adapted=builder_raw.decode('utf-8')
  for before,after in replay8.REPLACEMENTS:adapted=adapted.replace(before,after)
  adapted=adapted.replace(f"ROOT/'tests/m14/{kind}144_native.c'",repr(str(generated))).replace("source=(",'source=(Path(').replace(").read_text(encoding='utf-8');exports", ")).read_text(encoding='utf-8');exports")
  adapted=adapted.replace(f"stage8/{kind}-fixture",f"stage8/{kind}148-fixture").replace("'SetBkMode'}","'SetBkMode','GetTextMetricsW'}")
  module=ModuleType(f'{kind}144_build');module.__file__=str(builder);sys.modules[module.__name__]=module
  exec(compile(adapted,str(builder),'exec'),module.__dict__)
  original=module.build
  def build():
   result=original();(out/'compile-receipt.json').write_bytes((json.dumps(dict(canonical_c_sha256=digest(raw),generated_c_sha256=digest(generated.read_bytes()),canonical_builder_sha256=digest(builder_raw),executed_builder_sha256=digest(adapted.encode()),adapter_sha256=digest(Path(__file__).read_bytes()),pe_sha256=digest((result/f'{kind}.exe').read_bytes()),scope=__doc__),indent=2)+'\n').encode());return result
  module.build=build
  runner=__import__(f'{kind}144_run');runner.main()
 finally:sys.meta_path.remove(loader)
if __name__=='__main__':main()
