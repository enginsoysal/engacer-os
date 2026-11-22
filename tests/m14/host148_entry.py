"""Recreate read-only archive inputs and exercise newly exposed codec helpers."""
import ctypes,hashlib,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 import replay8
 kind=sys.argv[1];assert kind in ('cab','codepage')
 loader=replay8.ReplayLoader();sys.meta_path.insert(0,loader)
 folder=ROOT/f'build/m14-native/stage8/{kind}-host';folder.mkdir(parents=True,exist_ok=True);records={}
 try:
  if kind=='cab':
   canonical=ROOT/'tools/m14/cab_extract147.ps1';raw=canonical.read_bytes();s=raw.decode('utf-8').replace("$projectRoot147 = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path","$projectRoot147 = '"+str(ROOT).replace("'","''")+"'").replace('stage7','stage8');generated=folder/'extract148.ps1';generated.write_bytes(s.encode('utf-8-sig'));subprocess.run(['pwsh','-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass','-File',str(generated)],check=True,cwd=ROOT);records['extraction']=dict(canonical_sha256=sha(raw),executed_sha256=sha(generated.read_bytes()))
   module=__import__('cab147_host');module.main()
  else:
   canonical=ROOT/'tests/m14/codepage147_host.c';raw=canonical.read_bytes();s=raw.decode('utf-8').replace('"../../user/windows8/', '"'+(ROOT/'user/windows8').as_posix()+'/')
   s+='\n__declspec(dllexport) int lead148(unsigned char value){return f_IsDBCSLeadByte(value);}\n__declspec(dllexport) int leadex148(unsigned cp,unsigned char value){return f_IsDBCSLeadByteEx(cp,value);}\n'
   generated=folder/'codepage148_host.c';generated.write_bytes(s.encode());runner=ROOT/'tests/m14/codepage147_host.py';rr=runner.read_bytes();adapted=rr.decode('utf-8')
   for before,after in replay8.REPLACEMENTS:adapted=adapted.replace(before,after)
   adapted=adapted.replace("ROOT/'tests/m14/codepage147_host.c'",repr(str(generated)))
   scope=dict(__file__=str(runner),__name__='codepage148_host');exec(compile(adapted,str(runner),'exec'),scope);scope['main']()
   lib=ctypes.CDLL(str(folder/'codec.dll'));lib.lead148.argtypes=[ctypes.c_ubyte];lib.leadex148.argtypes=[ctypes.c_uint,ctypes.c_ubyte];checks=0
   for value in range(256):
    assert lib.lead148(value)==0;checks+=1
    for cp in (0,1,3,65001,1252):assert lib.leadex148(cp,value)==0;checks+=1
   assert lib.leadex148(932,0x81)==0 and lib.error_get147()==87;checks+=1
   records['codecs']=dict(canonical_c_sha256=sha(raw),generated_c_sha256=sha(generated.read_bytes()),canonical_runner_sha256=sha(rr),executed_runner_sha256=sha(adapted.encode()),additional_dbcs_checks=checks)
  records.update(passed=True,scope=__doc__,adapter_sha256=sha(Path(__file__).read_bytes()));(folder/'preparation-receipt.json').write_bytes((json.dumps(records,indent=2)+'\n').encode())
 finally:sys.meta_path.remove(loader)
if __name__=='__main__':main()
