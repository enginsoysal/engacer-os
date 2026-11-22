"""Preserve original WiX/system assertions through each nested own observer."""
import hashlib,json,os,sys
from types import ModuleType
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
stages148=[]

def map_nested148(source):
 import replay8
 original=hashlib.sha256(source.encode()).hexdigest();source=replay8.map_current148(source)
 source=source.replace('raw.decode()',"__import__('wix_system148_native').map_nested148(raw.decode())")
 stages148.append(dict(canonical_sha256=original,executed_sha256=hashlib.sha256(source.encode()).hexdigest()))
 return source

def main():
 import replay8
 os.environ['ENGACER147_ACTION_CYCLES']='21'
 sys.modules['wix_system148_native']=sys.modules[__name__]
 loader=replay8.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  builder=ROOT/'tests/m14/wix_system147_build.py';builder_raw=builder.read_bytes();builder_source=map_nested148(builder_raw.decode('utf-8'));module=ModuleType('wix_system147_build');module.__file__=str(builder);sys.modules[module.__name__]=module
  replay8.observed[builder.relative_to(ROOT).as_posix()]=dict(canonical_sha256=hashlib.sha256(builder_raw).hexdigest(),executed_sha256=hashlib.sha256(builder_source.encode()).hexdigest(),execution_mode='explicit nested current-stage builder')
  exec(compile(builder_source,str(builder),'exec'),module.__dict__)
  canonical=ROOT/'tests/m14/wix_system147_run.py';raw=canonical.read_bytes();source=map_nested148(raw.decode('utf-8'))
  scope=dict(__file__=str(canonical),__name__='wix_system148_native')
  exec(compile(source,str(canonical),'exec'),scope);scope['main']()
  out=ROOT/'build/m14-native/stage8/wix-system-native'
  (out/'entry-observer.json').write_bytes((json.dumps(dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),nested_stages=stages148,cycles=21,scope=__doc__),indent=2)+'\n').encode())
 finally:sys.meta_path.remove(loader)

if __name__=='__main__':main()
