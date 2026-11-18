"""Bounded frozen M13.11 functional queues; no stability tasks."""
import argparse,hashlib,json,shutil,subprocess,sys,time
from pathlib import Path
from close_stage import verify_inputs_at_commit
ROOT=Path(__file__).resolve().parents[2]
GROUPS={
 'ordinary':[['native_controls8.py','--stage','11','--profile','ordinary'],['saver_native11.py'],['saver_persistence11.py'],['settings_native11.py'],['settings_fast11.py','--profile','ordinary'],['saver_write_failure11.py']],
 'small':[['native_controls8.py','--stage','11','--profile','compact'],['native_controls8.py','--stage','11','--profile','1024'],['saver_profiles11.py','--profile','compact'],['saver_profiles11.py','--profile','1024'],['saver_invalid11.py']],
 'large':[['native_controls8.py','--stage','11','--profile','150'],['native_controls8.py','--stage','11','--profile','4k'],['saver_profiles11.py','--profile','150'],['saver_profiles11.py','--profile','4k'],['saver_profiles11.py','--profile','ordinary'],['apps_frames11.py','--profile','ordinary']],
}


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--group',choices=GROUPS,required=True);p.add_argument('--resume',action='store_true');a=p.parse_args()
    manifest=ROOT/'dist/m13stage11-build-manifest.json';raw=manifest.read_bytes();meta=json.loads(raw);verify_inputs_at_commit('HEAD',meta['source_sha256'])
    harness={p:sha(p) for p in (ROOT/'tests/m13').glob('*.py')};out=ROOT/'build/m13/stage11'/('queue-'+a.group);out.mkdir(parents=True,exist_ok=True);path=out/'results.json'
    report=dict(passed=False,group=a.group,build_id=meta['build_id'],steps=[],scope='Ordered functional feature tasks within M13.11; no duration, natural-freeze or reset-chain tests')
    if a.resume and path.exists():
        old=json.loads(path.read_text(encoding='utf-8'));assert old['build_id']==meta['build_id'],'Cannot resume different candidate'
        for index,step in enumerate(old['steps']):
            if step['exit_code']!=0:break
            assert step['command']==GROUPS[a.group][index];report['steps'].append(step)
    try:
        for index,command in enumerate(GROUPS[a.group][len(report['steps']):],len(report['steps'])):
            assert manifest.read_bytes()==raw
            for file,digest in harness.items():assert sha(file)==digest,('Harness changed during qualification',file.name)
            if command[0]=='saver_invalid11.py':
                deadline=time.monotonic()+600;printed=False
                while True:
                    dep=ROOT/'build/m13/stage11/screensaver-native/results.json'
                    if dep.exists():
                        value=json.loads(dep.read_text(encoding='utf-8'))
                        if value['build_id']==meta['build_id']:
                            assert value['passed'],'Current saver prerequisite failed';break
                    if not printed:print('Waiting for current frozen saver source fixture',flush=True);printed=True
                    if time.monotonic()>deadline:raise TimeoutError('Current saver source fixture was not qualified')
                    time.sleep(1)
            target=out/(str(index+1)+'-output.txt')
            if target.exists():shutil.copyfile(target,out/(str(index+1)+'-previous-output.txt'))
            print('M13.11 '+a.group+' '+str(index+1)+'/'+str(len(GROUPS[a.group]))+': '+' '.join(command),flush=True);start=time.monotonic()
            with target.open('wb') as output:code=subprocess.run([sys.executable,str(ROOT/'tests/m13'/command[0]),*command[1:]],cwd=ROOT,stdout=output,stderr=subprocess.STDOUT).returncode
            step=dict(command=command,exit_code=code,elapsed_seconds=time.monotonic()-start);report['steps'].append(step);path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
            assert code==0,(command,'See bounded task output')
            assert manifest.read_bytes()==raw
            for file,digest in harness.items():assert sha(file)==digest,('Harness changed during qualification',file.name)
        report['passed']=True
    except Exception as e:report['error']=str(e);raise
    finally:path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':main()
