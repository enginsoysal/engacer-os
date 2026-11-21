"""Verify the complete frozen stage-eight campaign and original EXE chain.

Public assets, native editor Save and public website readback are separate
closure gates. This verifier does not promote a development-only worker.
"""
import hashlib,json,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_bytes((json.dumps(v,indent=2)+'\n').encode())

def main():
 work=ROOT/'build/m14-native/stage8';final=ROOT/'evidence/M14/8';assert not(final/'publication-results.json').exists()
 meta=read(ROOT/'dist/m14stage8-build-manifest.json');build=meta['build_id'];assert meta['qualification_scope']=='M14-STAGE8-VM-v1'
 for path,digest in meta['source_sha256'].items():assert sha(ROOT/path)==digest,path
 for name,row in meta['artifacts'].items():assert sha(ROOT/'dist'/name)==row['sha256'],name
 campaign=work/'development/final8';suite=read(campaign/'suite-results.json');tree=read(campaign/'observer-tree.json')
 assert suite['passed']and suite['build_id']==build and len(suite['tasks'])==147 and not suite['pending']and not suite['running']
 assert hashlib.sha256(json.dumps(tree['files'],sort_keys=True).encode()).hexdigest()==tree['source_tree_sha256']
 for path,digest in tree['files'].items():assert sha(ROOT/path)==digest,('Observer changed',path)
 for name,record in suite['tasks'].items():assert record['exit_code']==0 and record['source_tree_sha256']==tree['source_tree_sha256'],name
 original=read(work/'exe-chain-native/results.json');assert original['passed']and original['build_id']==build and original['full_production_media']and not original['development_worker_sha256']
 assert original['observer_sha256']==sha(ROOT/'tests/m14/exe148_chain_native.py')and len(original['cycles'])==3
 for i,cycle in enumerate(original['cycles']):
  assert cycle['cycle']==i and cycle['removing']==(i==1)and cycle['state']['state']==2 and cycle['state']['status']==0
  if i!=1:assert len(cycle['cold_payload_readback'])==4 and len(cycle['windows_original_shortcut_readback'])==2
 for name in ['session-native','font-native','copy-native','rtl-native','software-native','exe-review-native','static-host']:
  record=read(work/name/'results.json');assert record['passed']and record.get('build_id',record.get('kernel_build_id'))==build,name
 starter=read(ROOT/'dist/m14stage8-starter-manifest.json');assert starter['build_id']==build and sha(ROOT/'dist'/starter['archive'])==starter['sha256']
 # Preserve bounded receipts and screenshots, never sparse VM disks or originals.
 import sys
 sys.path.insert(0,str(ROOT/'tests/m12'));from verify_components import copy_report
 final.mkdir(parents=True,exist_ok=True)
 for folder in work.iterdir():
  if folder.is_dir()and(folder/'results.json').is_file():
   candidate=read(folder/'results.json');identity=candidate.get('build_id',candidate.get('kernel_build_id',candidate.get('os_build_id')))
   if identity is None or identity==build:copy_report(folder,final/folder.name)
 write(final/'campaign-results.json',suite);write(final/'campaign-observer-tree.json',tree)
 static=read(work/'static-resource-comparison.json');assert static['passed']and static['build_id']==build;write(final/'static-resource-comparison.json',static)
 result=dict(passed=True,stage='M14.8',qualification='M14-STAGE8-VM-v1',build_id=build,compiled_source=meta.get('source_commit'),campaign_tasks=len(suite['tasks']),source_inputs=len(meta['source_sha256']),vmware_zip_sha256=starter['sha256'],original_exe_cycles=3,original_exe_payloads=4,original_exe_shortcuts=2,native_groups=read(ROOT/'evidence/M14/7/acceptance-results.json')['native_groups']+['session-native','font-native','copy-native','rtl-native','software-native','exe-review-native','exe-chain-native'],host_groups=read(ROOT/'evidence/M14/7/acceptance-results.json')['host_groups']+['batch-host','registry-info-reference'],limits=['Original SumatraPDF 3.6.1 EXE GUI installation, removal and reinstall only; reader, PDF filter and preview tasks remain unqualified.','Original 7-Zip and Notepad++ MSI profiles retain their existing bounded scope; arbitrary installers and universal Windows x64 compatibility are not established.','Automatic rollback of an interrupted EXE is not qualified; preserve its protected record for inspection.','Canonical Inter fallback differs from original Windows fonts, including decorative logo width.','Configured RAM, fixed image load, task peaks and retained caches are separate measurements; whole-system optimization remains M14.16.'],verifier_sha256=sha(Path(__file__)))
 write(final/'acceptance-results.json',result);print('PASS complete M14.8 native/source/media acceptance',build)

if __name__=='__main__':main()
