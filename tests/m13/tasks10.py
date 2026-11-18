"""Ordered functional M13.10 profile checks on one immutable candidate."""
import argparse,json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--group',choices=['small','large'],required=True);parser.add_argument('--resume',action='store_true');a=parser.parse_args()
    manifest=ROOT/'dist/m13stage10-build-manifest.json';frozen=manifest.read_bytes();meta=json.loads(frozen)
    out=ROOT/'build/m13/stage10'/('queue-'+a.group);out.mkdir(parents=True,exist_ok=True)
    report=dict(passed=False,build_id=meta['build_id'],group=a.group,steps=[],scope='Functional tasks only; stability remains M13.13')
    commands=[]
    for profile in (('compact','1024') if a.group=='small' else ('150','4k')):
        commands.extend([['native_controls8.py','--stage','10','--profile',profile],
                         ['settings_fast10.py','--profile',profile],['cursors10.py','--profile',profile]])
    completed=0
    if a.resume:
        prior=json.loads((out/'results.json').read_text(encoding='utf-8'))
        assert prior['build_id']==meta['build_id'] and not prior['passed']
        for step in prior['steps']:
            if step['exit_code']:break
            assert step['command']==commands[completed]
            report['steps'].append(step);completed+=1
    try:
        for number,command in enumerate(commands,1):
            if number<=completed:continue
            assert manifest.read_bytes()==frozen,'Frozen native media changed'
            print('M13.10 '+a.group+' '+str(number)+'/'+str(len(commands))+': '+' '.join(command),flush=True)
            began=time.monotonic()
            with (out/(str(number)+'-output.txt')).open('w',encoding='utf-8') as stream:
                result=subprocess.run([sys.executable,str(ROOT/'tests/m13'/command[0]),*command[1:]],cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
            report['steps'].append(dict(command=command,exit_code=result.returncode,elapsed_seconds=time.monotonic()-began))
            (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode('utf-8'))
            assert result.returncode==0,'Functional failure preserved in '+str(number)+'-output.txt'
        assert manifest.read_bytes()==frozen;report['passed']=True
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode('utf-8'));print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':main()
