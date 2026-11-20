"""Reuse canonical runtime scenarios with isolated M14.4 observation/output paths.

Source/output identity strings and the explicitly smaller M14.4 metadata-page
layout expectation change. Functional assertions and Windows fixture code
remain the canonical scenarios; this is not a requalification of old media.
"""
import argparse,hashlib,importlib.abc,importlib.util,json,os,sys,types
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DIRECTORY=ROOT/'tests/m14'
CASES={'threads':'thread_native2','tls':'tls_native2','last-thread':'last_thread_native2',
       'processes':'process_native2','named-sync':'named_sync_native2','named-sync-cancel':'named_sync_cancel_native2',
       'cancel':'cancel_native2','msi-cancel':'msi_cancel2','exceptions':'exception_native2',
       'exception-nested':'exception_nested_native2','exception-invalid':'exception_invalid_native2',
       'unwind':'unwind_native2','unwind-chain':'unwind_chain_native2','unwind-invalid':'unwind_invalid_native2',
       'inspection':'inspect_native2','probes':'lifetime_native2',
       'paths':'path143_native','files':'files143_native','registry':'registry143_native',
       'environment':'environment143_native','metadata':'metadata143_native','find':'find143_native',
       'state-lifetime':'state_lifetime143_native','browser-download':'browser_download3',
       'unicode-host':'unicode143_host','path-host':'path143_host','find-host':'find143_host',
       'http-host':'http3','download-stream':'download_stream3'}
REPLACEMENTS=[('evidence/M14/3','evidence/M14/4'),('M14.3','M14.4'),('0.14.3','0.14.4'),('EngacerOS-M14STAGE3','EngacerOS-M14STAGE4'),('stage3','stage4'),('m143-regress-','m144-regress-'),('m143-','m144-'),
              ('EngacerOS-M14STAGE2','EngacerOS-M14STAGE4'),('EngacerOS-M14STAGE1','EngacerOS-M14STAGE4'),
              ('stage2','stage4'),('stage1','stage4'),('m142-','m144-regress-'),
              ('build/m14-native/fixtures','build/m14-native/stage4/regression-fixtures'),
              ('M14.2 development','M14.4 runtime regression'),('M14.25','M14.15'),
              ('assert metadata==[41,45,45,45],metadata','assert metadata==[28,32,32,32],metadata')]
observed={}

def source_for(name):
 path=DIRECTORY/(name+'.py');raw=path.read_bytes();text=raw.decode('utf-8')
 for before,after in REPLACEMENTS:text=text.replace(before,after)
 observed[path.relative_to(ROOT).as_posix()]={'canonical_sha256':hashlib.sha256(raw).hexdigest(),'executed_source_sha256':hashlib.sha256(text.encode('utf-8')).hexdigest()}
 return path,text

class NativeSourceLoader(importlib.abc.MetaPathFinder,importlib.abc.Loader):
 def find_spec(self,fullname,path=None,target=None):
  if '.' not in fullname and fullname!='runtime_regressions4' and (DIRECTORY/(fullname+'.py')).is_file():return importlib.util.spec_from_loader(fullname,self)
  return None
 def create_module(self,spec):return None
 def exec_module(self,module):
  path,text=source_for(module.__name__);module.__file__=str(path);exec(compile(text,str(path),'exec'),module.__dict__)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('case',choices=CASES);args=parser.parse_args()
 assert not (ROOT/'evidence/M14/4/publication-results.json').exists(),'Accepted stage is immutable'
 meta=json.loads((ROOT/'dist/m14stage4-build-manifest.json').read_text(encoding='utf-8'))
 assert meta['release_version']=='0.14.4' and meta['qualification_scope']=='M14-STAGE4-VM-v1'
 os.environ['ENGACER12_IMAGE']='EngacerOS-M14STAGE4';sys.path.insert(0,str(DIRECTORY));sys.meta_path.insert(0,NativeSourceLoader())
 out=ROOT/'build/m14-native/stage4/regression-observers';out.mkdir(parents=True,exist_ok=True)
 report={'passed':False,'stage':'M14.4 development regression','case':args.case,'build_id':meta['build_id'],'replacements':REPLACEMENTS}
 try:
  path,text=source_for(CASES[args.case]);module=types.ModuleType('__main__');module.__file__=str(path);module.__package__=None
  exec(compile(text,str(path),'exec'),module.__dict__);report['passed']=True
 finally:
  report['observer_sources']=observed;report['adapter_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
  (out/(args.case+'.json')).write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
