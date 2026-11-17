"""Sequential owned VMware controller/firmware lifecycle matrix on one frozen ISO."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 assert not (ROOT/'evidence/M12/18/publication-results.json').exists(),'Final published evidence is immutable'
 p=argparse.ArgumentParser();p.add_argument('--resume',action='store_true');a=p.parse_args();meta=json.loads((ROOT/'dist/m12stage18-build-manifest.json').read_text(encoding='utf-8'));iso=meta['artifacts']['EngacerOS-M12STAGE18.iso']['sha256'];assert hashlib.sha256((ROOT/'dist/EngacerOS-M12STAGE18.iso').read_bytes()).hexdigest()==iso
 pairs=[(c,f) for c in ['sata','ide','lsilogic','lsisas1068','pvscsi','nvme'] for f in ['efi','bios']]+[('buslogic','bios')];failed=[]
 for controller,firmware in [('sata','efi-starter')]+pairs:
  label=controller+'-'+firmware;path=ROOT/'build/m12/stage18/matrix-results'/label/'results.json'
  if a.resume and path.is_file():
   r=json.loads(path.read_text(encoding='utf-8'))
   if r.get('passed') and r.get('harness_sha256')==hashlib.sha256((ROOT/'tests/m12/final_vmware18.py').read_bytes()).hexdigest() and r.get('build_id')==meta['build_id'] and r.get('iso_sha256')==iso and (firmware!='efi-starter' or r.get('starter_sha256')==hashlib.sha256((ROOT/'dist/EngacerOS-M12STAGE18-VMware.zip').read_bytes()).hexdigest()):print('Already qualified',label,flush=True);continue
  command=[sys.executable,str(ROOT/'tests/m12/final_vmware18.py'),'--controller',controller,'--firmware',firmware.split('-')[0]]+(['--starter'] if firmware=='efi-starter' else [])
  print('Starting owned VMware lifecycle',label,flush=True)
  path.parent.mkdir(parents=True,exist_ok=True)
  with (path.parent/'harness.log').open('w',encoding='utf-8') as log:result=subprocess.run(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
  print('Finished',label,'exit',result.returncode,flush=True)
  assert hashlib.sha256((ROOT/'dist/EngacerOS-M12STAGE18.iso').read_bytes()).hexdigest()==iso,'Build changed during matrix; freeze inputs and artifacts'
  if result.returncode:failed.append(label)
 print('Controller matrix failures:',failed,flush=True)
 if failed:raise SystemExit(1)
if __name__=='__main__':main()
