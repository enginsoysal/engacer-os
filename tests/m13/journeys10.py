"""Finish independent M13.10 task groups without changing frozen native media."""
import argparse,json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--group',choices=['ordinary','small','large'],required=True);parser.add_argument('--resume',action='store_true');a=parser.parse_args()
    manifest=ROOT/'dist/m13stage10-build-manifest.json';frozen=manifest.read_bytes();meta=json.loads(frozen)
    commands=[]
    if a.group=='ordinary':
        commands=[['settings_fast10.py','--profile','ordinary'],['cursors10.py','--profile','ordinary'],
                  ['dialogs_profiles10.py','--profile','ordinary'],['transfers_native10.py'],['vmware_stage10.py','--stage','10']]
    else:
        for profile in (('compact','1024') if a.group=='small' else ('150','4k')):
            commands.extend([['apps_scaled10.py','--profile',profile],['dialogs_profiles10.py','--profile',profile]])
        commands.append(['settings_native10.py' if a.group=='small' else 'feedback_native10.py'])
    out=ROOT/'build/m13/stage10'/('journeys-'+a.group);out.mkdir(parents=True,exist_ok=True)
    report=dict(passed=False,build_id=meta['build_id'],group=a.group,steps=[],scope='Secondary/app/ordinary functional tasks only; stability is M13.13')
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
            assert manifest.read_bytes()==frozen,'Frozen candidate changed'
            print('M13.10 '+a.group+' journey '+str(number)+'/'+str(len(commands))+': '+' '.join(command),flush=True)
            began=time.monotonic()
            with (out/(str(number)+'-output.txt')).open('w',encoding='utf-8') as stream:
                result=subprocess.run([sys.executable,str(ROOT/'tests/m13'/command[0]),*command[1:]],cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
            report['steps'].append(dict(command=command,exit_code=result.returncode,elapsed_seconds=time.monotonic()-began))
            (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode('utf-8'))
            assert result.returncode==0,'Task failed; preserved '+str(number)+'-output.txt'
        assert manifest.read_bytes()==frozen;report['passed']=True
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode('utf-8'));print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':main()
