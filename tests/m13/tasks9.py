"""Run only the scoped M13.9 functional queues on one frozen candidate."""
import argparse,datetime,hashlib,json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--group',choices=['small','large'],required=True);group=parser.parse_args().group
 manifest=ROOT/'dist/m13stage9-build-manifest.json';original=manifest.read_bytes();meta=json.loads(original)
 assert not (ROOT/'evidence/M13/9/publication-results.json').exists()
 commands=[]
 for profile in (('compact','1024','150') if group=='small' else ('ordinary','4k')):
  if group=='small':commands.append(['native_controls8.py','--stage','9','--profile',profile])
  commands.extend([['cursors9.py','--profile',profile],['windows_profiles9.py','--profile',profile,'--fixture']])
 if group=='large':commands.append(['motion_pixels9.py','--stage','9','--native-group','ordinary','--fixture-family','m13-stage9-ordinary'])
 out=ROOT/'build/m13/stage9'/('queue-'+group);out.mkdir(parents=True,exist_ok=True)
 report=dict(passed=False,build_id=meta['build_id'],group=group,steps=[],scope='Functional control/cursor/window/pixel journeys only; no stability, historical baseline, duration or reset-chain work')
 try:
  for number,command in enumerate(commands):
   assert manifest.read_bytes()==original,'Frozen media changed during task queue'
   print('M13.9 '+group+' task '+str(number+1)+'/'+str(len(commands))+': '+' '.join(command),flush=True)
   began=time.monotonic()
   with (out/(str(number+1)+'-output.txt')).open('w',encoding='utf-8') as output:
    result=subprocess.run([sys.executable,str(ROOT/'tests/m13'/command[0]),*command[1:]],cwd=ROOT,stdout=output,stderr=subprocess.STDOUT)
   report['steps'].append(dict(command=command,exit_code=result.returncode,elapsed_seconds=time.monotonic()-began));(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
   assert result.returncode==0,'Functional task failed; preserved '+str(number+1)+'-output.txt'
  assert manifest.read_bytes()==original
  report['passed']=True
 finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
