"""Independent static cross-checks and scope gates for M14.0, not guest execution."""
import hashlib,json,os,re,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'evidence/M14/0'
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 inventory=read('evidence/M14/0/binary-inventory.json');msi=read('evidence/M14/0/msi-inventory.json');targets=read('docs/roadmap/m14-targets.json');plan=read('docs/milestones/m14-progress.json')
 assert not (OUT/'publication-results.json').exists(),'Accepted research publication is immutable'
 assert inventory['passed'] and not inventory['downloaded_apps_executed'] and not inventory['native_compatibility_proven']
 assert len(inventory['packages'])==6 and len(inventory['binaries'])==23
 assert [r['id'] for r in plan['stages']]==[f'M14.{i}' for i in range(16)]
 assert plan['final_release_stage']=='M14.15' and plan['current_native_download']=='M13.13'
 assert len(targets['targets'])==3 and all(t['status']=='investigated_not_native_qualified' and len(t['tasks'])>=7 for t in targets['targets'])
 scratch=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0';llvm=Path(shutil.which('llvm-readobj'));assert llvm.is_file()
 corpus=read('evidence/M14/0/task-corpus.json');assert len(corpus['files'])==6
 for row in corpus['files']:assert sha(scratch/'corpus'/row['path'])==row['sha256']
 assert corpus['generator_sha256']==sha(ROOT/'tests/m14/corpus0.py')
 observed=[]
 records=[(scratch/r['file'],r['pe']) for r in inventory['packages'] if r.get('pe')]
 records += [(scratch/r['app']/r['relative_path'],r) for r in inventory['binaries']]
 for path,row in records:
  assert sha(path)==row['sha256']
  raw=subprocess.check_output([str(llvm),'--file-headers','--coff-imports',str(path)])
  result=raw.decode('utf-8',errors='replace');machine=re.search(r'Machine: \w+ \((0x[0-9A-Fa-f]+)\)',result);size=re.search(r'SizeOfImage: (\d+)',result)
  assert machine and int(machine[1],16)==int(row['machine'],16),(row['file'],'machine')
  assert size and int(size[1])==row['image_bytes'],(row['file'],'image bytes')
  dlls={name.lower() for name in re.findall(r'\bName: ([^\r\n ]+\.(?:dll|drv))',result,re.I)}
  assert dlls=={imp['dll'] for imp in row['imports']},(row['file'],'import DLLs',dlls)
  observed.append(dict(file=row['file'],sha256=row['sha256'],machine=row['machine'],image_bytes=row['image_bytes'],import_dlls=sorted(dlls),independent_tool_match=True))
 assert next(p for p in inventory['packages'] if p['file'].endswith('Installer.x64.exe'))['pe']['architecture']=='x86'
 assert all(p['template'].startswith('x64;') for p in msi['packages'])
 assert all(not isinstance(table,dict) or table.get('absent') for p in msi['packages'] for table in p['tables'].values())
 assert all(row for p in msi['packages'] for rows in p['tables'].values() if isinstance(rows,list) for row in rows)
 custom=msi['packages'][1]['tables']['CustomAction'];assert any('xcopy.exe' in row[3] for row in custom) and any('cmd.exe' in row[3] for row in custom)
 stream=msi['packages'][1]['tables']['Binary'][0][1];assert sha(scratch/stream['relative_path'])==stream['sha256']
 assert next(b for b in inventory['binaries'] if b['app']=='msi-streams')['architecture']=='x64'
 sys.path.insert(0,str(ROOT/'tests/m13'));from close_stage import verify_inputs_at_commit
 manifest=read('dist/m13stage13-build-manifest.json');verify_inputs_at_commit('HEAD',manifest['source_sha256'])
 assert all(sha(ROOT/path)==digest for path,digest in manifest['source_sha256'].items()),'Research must not change native inputs'
 for name,r in manifest['artifacts'].items():assert sha(ROOT/'dist'/name)==r['sha256']
 baseline=read('evidence/M13/13/resources.json')
 result=dict(passed=True,stage='M14.0',qualification='M14-RESEARCH0-v1',research_only=True,new_iso=False,current_native_download='M13.13',native_build_id=manifest['build_id'],native_iso_sha256=manifest['artifacts']['EngacerOS-M13STAGE13.iso']['sha256'],native_inputs_unchanged=len(manifest['source_sha256']),original_containers=6,original_pe_payloads=23,independent_pe_checks=observed,llvm_readobj_sha256=sha(llvm),msi_read_only_checks=True,msi_custom_actions_not_executed=True,performance_protocol='docs/architecture/windows-m14.md',gui_performance_measured=False,historical_native_resources=baseline,harness_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in [Path(__file__),ROOT/'tools/m14/inventory.py',ROOT/'tools/m14/msi_inventory.ps1']},limits=['Static metadata and independent tool checks are not original GUI execution or complete dynamic dependency closure','Original GUI install/start/use/remove tasks and absolute measured performance budgets remain future native stages','Current original Notepad++ EXE bootstrap is x86; original x64 MSI requires actual custom-action/command behavior','No new native ISO, universal Windows compatibility or faster-than-Windows claim'])
 result['task_corpus']='task-corpus.json';result['task_corpus_sha256']=sha(OUT/'task-corpus.json');result['harness_sha256']['tests/m14/corpus0.py']=sha(ROOT/'tests/m14/corpus0.py')
 (OUT/'acceptance-results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print('PASS M14.0: sixteen ordered stages, six original containers, 23 PE payloads,',len(observed),'independent LLVM checks, read-only MSI routes, 613 unchanged native inputs; research only')

if __name__=='__main__':main()
