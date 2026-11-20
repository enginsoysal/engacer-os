"""Full frozen M14.5 task orchestration; individual receipts and release gates remain required.

Preserves the M14.4 scenarios through the recorded replay adapter. New control
coverage is additive. Resume requires identical media, commands and observer tree.
"""
import argparse,concurrent.futures,hashlib,json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--workers',type=int,default=3);parser.add_argument('--revision',default='revision17');parser.add_argument('--resume',action='store_true');args=parser.parse_args();assert 1<=args.workers<=3 and args.revision.isalnum()
 out=ROOT/'build/m14-native/stage5/development'/args.revision;out.mkdir(parents=True,exist_ok=True)
 manifest=ROOT/'dist/m14stage5-build-manifest.json';meta=json.loads(manifest.read_text());assert meta['qualification_scope']=='M14-STAGE5-VM-v1';build=meta['build_id']
 for name,row in meta['artifacts'].items():assert hashlib.sha256((ROOT/'dist'/name).read_bytes()).hexdigest()==row['sha256'],name
 tasks={}
 def add(name,script,arguments=(),dependencies=(),priority=20):
  assert name not in tasks
  if script.startswith('tests/m14/') and script!='tests/m14/native1.py':
   command=[sys.executable,'tests/m14/replay5.py',Path(script).stem,*arguments]
  else:command=[sys.executable,script,*arguments]
  tasks[name]={'command':command,'dependencies':set(dependencies),'priority':priority}
 for profile in ('compact','ordinary','4k'):
  add(profile,'tests/m14/native1.py',('--stage','5','--profile',profile),priority=0)
  add('apps-'+profile,'tests/m14/apps_native4.py',('--profile',profile),(profile,),2)
  add('original-'+profile,'tests/m14/original144_run.py',('--profile',profile,'--cycles','21'if profile=='compact'else'1'),('apps-'+profile,),7)
 add('owners','tests/m14/owner144_run.py',dependencies=('apps-compact',),priority=3)
 for name,script in [('windows','window144_native.py'),('resources','resource144_run.py'),('controls','controls144_run.py'),('menus','menu144_run.py'),('com','com144_run.py'),('formats','clipformat144_run.py'),('paint','paint144_run.py'),('timers','timer144_run.py'),('deep','deep144_run.py'),('faults','fault144_run.py'),('heap','heap144_after.py'),('original-resources','original_resources144.py')]:
  add(name,'tests/m14/'+script,dependencies=('apps-compact',))
 from runtime_regressions4 import CASES
 from files_regressions4 import CASES as FILE_CASES
 for case in CASES:
  host=case.endswith('-host')or case=='download-stream'
  add('runtime-'+case,'tests/m14/runtime_regressions4.py',(case,),('ordinary',)if host else('compact',),30 if host else 12)
 for case in FILE_CASES:
  add('files-'+case,'tests/m14/files_regressions4.py',(case,),('ordinary',)if case=='browser-download'else('apps-compact',),5 if case=='state-lifetime'else 16)
 for name,script in [('queue-host','queue144_host.py'),('resource-host','resource144_host.py'),('dib-host','dib144_host.py')]:add(name,'tests/m14/'+script,priority=30)
 add('starter','tools/release/vmware_starter14.py',('--stage','5'),priority=1)
 add('vmware','tests/m14/vmware4.py',('--stage','5'),('starter','owners'),8)
 for profile in ('compact','4k'):
  add('raster-'+profile,'tests/m14/raster145_run.py',('--profile',profile,'--cycles','21'if profile=='compact'else'1'),('apps-'+profile,),4)
  add('original-menu-'+profile,'tests/m14/original_menu145_run.py',('--profile',profile),('apps-'+profile,),4)
 for name,script,arguments in (
  ('dialogs145','dialog145_run.py',('--cycles','21')),
  ('menus145','menu145_run.py',('--cycles','21')),
  ('list145','list145_run.py',('--cycles','21')),
  ('keys145','keys145_run.py',('--cycles','21')),
  ('original-list145','original_list145_run.py',()),
  ('guard145','guard145_run.py',()),
  ('protect145','protect145_run.py',())):
  add(name,'tests/m14/'+script,arguments,('apps-compact',),4)
 for name,script in (('keys145-host','keys145_host.py'),('keymap145-host','keymap145_host.py'),('targets145-host','targets145_host.py'),('source145-host','source145_host.py'),('dialog145-host','dialog145_host.py')):
  add(name,'tests/m14/'+script,priority=30)
 assert len(tasks)==72,len(tasks)
 assert all(t['dependencies']<=tasks.keys()for t in tasks.values())
 # Cache only an actual successful task on these identical frozen artifact bytes.
 tree={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for directory in ('tests','tools/build','tools/release')for p in (ROOT/directory).rglob('*')if p.is_file()and p.suffix in ('.py','.c','.h','.inc','.mjs')}
 source_tree=hashlib.sha256(json.dumps(tree,sort_keys=True).encode()).hexdigest()
 previous=json.loads((out/'suite-results.json').read_text())if args.resume else None
 completed=set();running={};records={};pending=set(tasks);failed=False;started=time.monotonic()
 if previous:
  assert previous['build_id']==build,'A different candidate must run its own suite'
  for name,r in previous['tasks'].items():
   if r['exit_code']or name not in tasks or r.get('command')!=tasks[name]['command'][1:]:continue
   if r.get('source_tree_sha256')!=source_tree:continue
   records[name]={**r,'resumed_verified_same_candidate':True};completed.add(name);pending.remove(name);print('REUSE matching passed task',name,flush=True)

 def run(name):
  assert json.loads(manifest.read_text())['build_id']==build,'Frozen media changed before task'
  begin=time.monotonic()
  with(out/(name+'.log')).open('wb')as log:code=subprocess.call(tasks[name]['command'],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
  assert json.loads(manifest.read_text())['build_id']==build,'Frozen media changed during task'
  return {'exit_code':code,'observer_wall_seconds':time.monotonic()-begin,'command':tasks[name]['command'][1:],'source_tree_sha256':source_tree}
 def save():
  (out/'suite-results.json').write_bytes((json.dumps({'passed':not failed and not pending and not running,'build_id':build,'workers':args.workers,'tasks':records,'pending':sorted(pending),'running':sorted(running.values()),'observer_wall_seconds':time.monotonic()-started,'scope':'Task orchestration only; direct native/host/source/media and public acceptance remain separate gates'},indent=2)+'\n').encode())
 with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers)as pool:
  while pending or running:
   ready=sorted((n for n in pending if tasks[n]['dependencies']<=completed),key=lambda n:(tasks[n]['priority'],n))
   while ready and len(running)<args.workers and not failed:
    name=ready.pop(0);pending.remove(name);running[pool.submit(run,name)]=name;print('START',name,flush=True)
   if not running:
    if failed:break
    raise RuntimeError('Blocked task graph: '+str(sorted(pending)))
   done,_=concurrent.futures.wait(running,timeout=1,return_when=concurrent.futures.FIRST_COMPLETED)
   for future in done:
    name=running.pop(future)
    try:r=future.result()
    except Exception as error:r={'exit_code':1,'error':str(error)}
    records[name]=r
    if r['exit_code']:failed=True
    else:completed.add(name)
    print('END',name,'exit',r['exit_code'],'completed',len(completed),'of',len(tasks),flush=True)
   save()
 save();print('PASS'if not failed and not pending else'FAIL','frozen candidate task suite',build,flush=True)
 if failed or pending:raise SystemExit(1)
if __name__=='__main__':main()
