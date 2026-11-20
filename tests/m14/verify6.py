"""Additive exact-source M14.6 native/media qualification; public delivery is separate."""
import hashlib,json,sys,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tests/m14'))

def read(path):return json.loads(path.read_text(encoding='utf-8'))
def write(path,value):path.write_bytes((json.dumps(value,indent=2)+'\n').encode())
def main():
 work=ROOT/'build/m14-native/stage6';meta=read(ROOT/'dist/m14stage6-build-manifest.json');build=meta['build_id']
 final=ROOT/'evidence/M14/6';assert not(final/'publication-results.json').exists()
 scratch=work/'verification-base';scratch.mkdir(exist_ok=True)
 source=ROOT/'tests/m14/verify4.py';raw=source.read_bytes();text=raw.decode()
 replacements=[('EngacerOS-M14STAGE4','EngacerOS-M14STAGE6'),('M14-STAGE4-VM-v1','M14-STAGE6-VM-v1'),('m14stage4','m14stage6'),('stage4','stage6'),('M14.4','M14.6'),('0.14.4','0.14.6')]
 for before,after in replacements:text=text.replace(before,after)
 before="out=ROOT/'evidence/M14/4'";assert before in text;text=text.replace(before,"out=ROOT/'build/m14-native/stage6/verification-base'")
 before="assert font['coverage_bytes']==251248 and font['header_sha256']==read(ROOT/'third_party/inter/raster-lock12.json')['header_sha256']";assert text.count(before)==1;text=text.replace(before,"assert font['coverage_bytes']==227452 and font['header_sha256']==read(ROOT/'third_party/inter/raster-lock146.json')['header_sha256'] and font['glyphs']==1663")
 before="assert fixed['bytes']==557692";assert text.count(before)==1;text=text.replace(before,"assert fixed['bytes']==557684")
 current_map=(ROOT/'dist/EngacerOS-M14STAGE6-installed-kernel.map').read_text();assert 'foreign_pointer144.cursor_owner144'not in current_map
 historical=read(ROOT/'evidence/M14/4/resources.json')['desktop_fixed'];assert historical['bytes']==557692
 namespace={'__name__':'verified_m146_base','__file__':str(source)};exec(compile(text,str(source),'exec'),namespace);namespace['main']()
 result=read(scratch/'acceptance-results.json');assert result['passed']and result['build_id']==build
 from verify_components import copy_report
 names=['raster-native-compact','raster-native-4k','dialog-native','menu145-native','list-native','keys-native','guard-native','protect-native','original-list','original-list-ordinary','original-list-4k','original-menu-compact','original-menu-4k']
 extra={name:read(work/name/'results.json')for name in names}
 for name,r in extra.items():assert r['passed']and r['build_id']==build,name
 for name in ('dialog-native','menu145-native','list-native','keys-native','protect-native'):
  assert len(extra[name]['cycles'])==21 and all(row['retained_pages']==0 for row in extra[name]['cycles']),name
 for profile in ('compact','4k'):
  r=extra['raster-native-'+profile];assert len(r['pixel_checks'])==19 and r['short_label_matches_gdi_reference'];assert len(r['cycles'])==(21 if profile=='compact'else 1);assert all(c['retained_pages']==0 for c in r['cycles'])
  assert r['physical_dimensions']==([1280,800]if profile=='compact'else[3840,2160])
  r=extra['original-menu-'+profile];assert r['retained_pages']==1
 for name in ('original-list','original-list-ordinary','original-list-4k'):
  r=extra[name];assert r['single_click_keeps_root']and r['back_to_parent']and r['actual_size_visible']and r['native_fixture_bytes_unchanged']and r['retained_pages']==1
 assert all(row['real_access_faults']==8 for row in extra['protect-native']['cycles'])
 assert extra['guard-native']['retained_pages']==0 and extra['guard-native']['static_call_refused']and extra['guard-native']['optional_discovery_returns_null']and extra['guard-native']['subsequent_original_console_success']
 host_names=['keys-host','keymap-host','targets-host','source-host','dialog-host']
 hosts={name:read(work/name/'results.json')for name in host_names}
 for name,r in hosts.items():
  assert r['passed'],name
  for path,digest in r.get('sources',r.get('source_sha256',{})).items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,(name,path)
 # Canonical/executed receipts are independently required; orchestration hashes alone cannot qualify observers.
 observers=[]
 import re
 suite=read(work/'development/full1/suite-results.json');assert suite['passed']and suite['build_id']==build and len(suite['tasks'])==94
 required=[]
 for task in suite['tasks'].values():
  assert task['exit_code']==0
  command=task['command']
  if command[0]!='tests/m14/replay6.py':continue
  target,arguments=command[1],command[2:];suffix='-'.join(re.sub('[^a-zA-Z0-9_-]','',a)for a in arguments)
  required.append(work/'replay-observers'/(target+('-'+suffix if suffix else'')+'.json'))
 assert len(required)==90
 for p in required:
  r=read(p);assert r['passed']and r['build_id']==build
  assert r['adapter_sha256']==hashlib.sha256((ROOT/'tests/m14/replay6.py').read_bytes()).hexdigest()
  for path,row in r['observer_sources'].items():
   raw=(ROOT/path).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['canonical_sha256'],path
   executed=raw.decode('utf-8')
   for before,after in r['replacements']:executed=executed.replace(before,after)
   module=Path(path).stem
   if module=='original_window_trace4':executed=executed.replace('title=wide(56,312),class_name=wide(312,440)',"menu_height=struct.unpack_from('<I',raw,452)[0],title=wide(56,312),class_name=wide(312,440)")
   if module in ('original_window_trace4','original_menu145_run'):
    executed=executed.replace("pointers=struct.unpack('<32Q',ui.memory(g,ui.symbol('ui_windows144',installed=True)[0],256))","slots=ui.symbol('ui_windows144',installed=True);assert slots[1]==128*8;pointers=struct.unpack('<128Q',ui.memory(g,slots[0],slots[1]))")
   if module=='dialog145_build':executed=executed.replace('104:template(count=32),105:template(count=31)','104:template(count=128),105:template(count=127)')
   if module=='dialog145_host':
    for before,after in [('capacity=400','capacity=1600'),('values[1]<=31','values[1]<=127'),('control_quota=31','control_quota=127')]:executed=executed.replace(before,after)
   if module=='original144_run':executed=executed.replace("node['bounds'][1]+40;scale=","node['bounds'][1]+40+node.get('menu_height',0);scale=")
   if module=='controls144_run':executed=executed.replace('from controls144_build import build','from controls145_build import build')
   if module=='vmware4':executed=executed.replace('assert stage==4','assert stage==5')
   assert hashlib.sha256(executed.encode()).hexdigest()==row['executed_sha256'],(path,'Executed replay observer differs')
  observers.append(r)
 assert observers
 # Additional common-dialog, clipboard, mapping and exact Unicode raster gates.
 additional=['global-native','clipboard-native','chords-native','mapping-native','picker-native','picker-lifetime-native']
 for profile in ('compact','ordinary','4k'):
  suffix=''if profile=='compact'else'-'+profile
  additional.extend(['original-clipboard'+suffix,'original-picker-native'+suffix,'font-native'+suffix])
 new={name:read(work/name/'results.json')for name in additional}
 for name,r in new.items():assert r['passed']and r['build_id']==build,name
 for name in ('global-native','clipboard-native','mapping-native','picker-native','picker-lifetime-native'):
  assert len(new[name]['cycles'])==21 and all(row['retained_pages']==0 for row in new[name]['cycles']),name
 life=new['picker-lifetime-native']
 generations=[]
 for cycle in life['cycles']:
  assert cycle['expected_process_exit']==42 and cycle['picker_and_window_pages_released']
  assert [v['phase']for v in cycle['phases']]==['owner','thread','process']
  for phase in cycle['phases']:
   assert phase['actual_native_picker_displayed']and phase['blocked_halted_cpus']==2
   generations.append(phase['generation'])
 assert generations==sorted(set(generations))
 assert new['picker-native']['saved_bytes_independently_verified']and new['picker-native']['source_unchanged']
 for profile in ('compact','ordinary','4k'):
  suffix=''if profile=='compact'else'-'+profile
  r=new['font-native'+suffix];assert len(r['cycles'])==(21 if profile=='compact'else 1)
  assert all(v['retained_pages']==0 for v in r['cycles'])and len(r['pixel_rows'])==2
  assert r['physical_dimensions']=={'compact':[1280,800],'ordinary':[1920,1080],'4k':[3840,2160]}[profile]
  assert r['reported_work_area']=={'compact':[1280,740],'ordinary':[1920,1020],'4k':[1920,1020]}[profile]
  r=new['original-clipboard'+suffix];assert r['retained_original_process_pages']==0 and r['native_saved_bytes_verified']and r['source_file_unchanged']and r['scalar_cursor_backspace_delete_preserve_utf8']
  r=new['original-picker-native'+suffix];assert r['retained_process_pages']==0 and r['source_bytes_independently_unchanged']and r['original_common_dialog_task_completed']
 additional_hosts=['global-host','mapping-host','document-host','pack-host','font-host']
 new_hosts={name:read(work/name/'results.json')for name in additional_hosts}
 for name,r in new_hosts.items():
  assert r['passed'],name
  for path,digest in r.get('sources',r.get('source_sha256',{})).items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,(name,path)
 tree=read(work/'development/full1/observer-tree.json')
 assert hashlib.sha256(json.dumps(tree['files'],sort_keys=True).encode()).hexdigest()==tree['source_tree_sha256']
 verifier_maintenance=[]
 for path,digest in tree['files'].items():
  current=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
  if current!=digest and path=='tests/m14/verify6.py':
   # This verifier does not execute any campaign task. Preserve its exact
   # campaign-start source and bind its additive acceptance-only corrections.
   import subprocess
   historical=subprocess.check_output(['git','show','3f64eeeae7037664481140b61d4c52e790fa39e2:'+path],cwd=ROOT)
   assert hashlib.sha256(historical).hexdigest()==digest
   verifier_maintenance.append(dict(path=path,campaign_start_sha256=digest,current_sha256=current,canonical_commit='3f64eeeae7037664481140b61d4c52e790fa39e2',scope='Acceptance-only verifier correction; no executed native/host observer or fixture changes'))
  else:assert current==digest,('Suite observer input changed',path)
 assert all(r['source_tree_sha256']==tree['source_tree_sha256']for r in suite['tasks'].values())
 names.extend(additional);host_names.extend(additional_hosts)
 final.mkdir(exist_ok=True)
 for path in scratch.iterdir():
  if path.is_dir():shutil.copytree(path,final/path.name,dirs_exist_ok=True)
  elif path.name!='acceptance-results.json':shutil.copyfile(path,final/path.name)
 for name in names+host_names:copy_report(work/name,final/name)
 write(final/'drawing-observer-sources.json',observers)
 write(final/'fixed-state-change.json',dict(previous_bytes=557676,current_bytes=557684,delta_bytes=8,reason='Add the eight-byte generation-bound foreign picker state relative to accepted M14.5',current_map_sha256=hashlib.sha256((ROOT/'dist/EngacerOS-M14STAGE6-installed-kernel.map').read_bytes()).hexdigest(),scope='Desktop session object BSS/data only; not total OS RAM or M14.15 optimization qualification'))
 write(final/'base-acceptance-derivation.json',dict(canonical_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),replacements=replacements,fixed_state_assertion={'previous':557692,'current':557684,'explanation':'Cursor removal plus new picker generation; see fixed-state-change.json'},output_isolation=str(scratch.relative_to(ROOT))))
 result['native_groups'].extend(names);result['host_groups'].extend(host_names)
 result['limits'].extend(['Original Notepad++ and Sumatra startup reaches FlsAlloc but their interfaces, installation and tasks remain unqualified; required runtime work continues in M14.10 and complete corpus acceptance in M14.12','Read-only/read-write/execute-read image/allocation protections only; general Windows virtual-memory semantics remain incomplete','Original 7-Zip details clip at requested column widths; universal controls, theme, drag services and arbitrary Windows application compatibility are not qualified'])
 write(final/'common-dialog-observer-tree.json',tree);write(final/'verifier-maintenance.json',verifier_maintenance);write(final/'acceptance-results.json',result);print('PASS additive M14.6 acceptance',build)
if __name__=='__main__':main()
