"""Additive exact-source M14.5 native/media qualification; public delivery is separate."""
import hashlib,json,sys,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tests/m14'))

def read(path):return json.loads(path.read_text(encoding='utf-8'))
def write(path,value):path.write_bytes((json.dumps(value,indent=2)+'\n').encode())
def main():
 work=ROOT/'build/m14-native/stage5';meta=read(ROOT/'dist/m14stage5-build-manifest.json');build=meta['build_id']
 final=ROOT/'evidence/M14/5';assert not(final/'publication-results.json').exists()
 scratch=work/'verification-base';scratch.mkdir(exist_ok=True)
 source=ROOT/'tests/m14/verify4.py';raw=source.read_bytes();text=raw.decode()
 replacements=[('EngacerOS-M14STAGE4','EngacerOS-M14STAGE5'),('M14-STAGE4-VM-v1','M14-STAGE5-VM-v1'),('m14stage4','m14stage5'),('stage4','stage5'),('M14.4','M14.5'),('0.14.4','0.14.5')]
 for before,after in replacements:text=text.replace(before,after)
 before="out=ROOT/'evidence/M14/4'";assert before in text;text=text.replace(before,"out=ROOT/'build/m14-native/stage5/verification-base'")
 before="assert fixed['bytes']==557692";assert text.count(before)==1;text=text.replace(before,"assert fixed['bytes']==557676")
 current_map=(ROOT/'dist/EngacerOS-M14STAGE5-installed-kernel.map').read_text();assert 'foreign_pointer144.cursor_owner144'not in current_map
 historical=read(ROOT/'evidence/M14/4/resources.json')['desktop_fixed'];assert historical['bytes']==557692
 namespace={'__name__':'verified_m145_base','__file__':str(source)};exec(compile(text,str(source),'exec'),namespace);namespace['main']()
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
 suite=read(work/'development/full18/suite-results.json');assert suite['passed']and suite['build_id']==build and len(suite['tasks'])==74
 required=[]
 for task in suite['tasks'].values():
  assert task['exit_code']==0
  command=task['command']
  if command[0]!='tests/m14/replay5.py':continue
  target,arguments=command[1],command[2:];suffix='-'.join(re.sub('[^a-zA-Z0-9_-]','',a)for a in arguments)
  required.append(work/'replay-observers'/(target+('-'+suffix if suffix else'')+'.json'))
 assert len(required)==70
 for p in required:
  r=read(p);assert r['passed']and r['build_id']==build
  assert r['adapter_sha256']==hashlib.sha256((ROOT/'tests/m14/replay5.py').read_bytes()).hexdigest()
  for path,row in r['observer_sources'].items():
   raw=(ROOT/path).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['canonical_sha256'],path
   executed=raw.decode('utf-8')
   for before,after in r['replacements']:executed=executed.replace(before,after)
   module=Path(path).stem
   if module=='original_window_trace4':executed=executed.replace('title=wide(56,312),class_name=wide(312,440)',"menu_height=struct.unpack_from('<I',raw,452)[0],title=wide(56,312),class_name=wide(312,440)")
   if module=='original144_run':executed=executed.replace("node['bounds'][1]+40;scale=","node['bounds'][1]+40+node.get('menu_height',0);scale=")
   if module=='controls144_run':executed=executed.replace('from controls144_build import build','from controls145_build import build')
   if module=='vmware4':executed=executed.replace('assert stage==4','assert stage==5')
   assert hashlib.sha256(executed.encode()).hexdigest()==row['executed_sha256'],(path,'Executed replay observer differs')
  observers.append(r)
 assert observers
 final.mkdir(exist_ok=True)
 for path in scratch.iterdir():
  if path.is_dir():shutil.copytree(path,final/path.name,dirs_exist_ok=True)
  elif path.name!='acceptance-results.json':shutil.copyfile(path,final/path.name)
 for name in names+host_names:copy_report(work/name,final/name)
 write(final/'drawing-observer-sources.json',observers)
 write(final/'fixed-state-change.json',dict(previous_bytes=557692,current_bytes=557676,delta_bytes=-16,reason='Obsolete eight-byte foreign_pointer144.cursor_owner144 was removed; subsequent BSS alignment accounts for the other eight bytes',current_map_sha256=hashlib.sha256((ROOT/'dist/EngacerOS-M14STAGE5-installed-kernel.map').read_bytes()).hexdigest(),scope='Desktop session object BSS/data only; not total OS RAM or M14.15 optimization qualification'))
 write(final/'base-acceptance-derivation.json',dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),replacements=replacements,fixed_state_assertion={'previous':557692,'current':557676,'explanation':'Removed cursor owner and alignment; see fixed-state-change.json'},output_isolation=str(scratch.relative_to(ROOT))))
 result['native_groups'].extend(names);result['host_groups'].extend(host_names)
 result['limits'].extend(['Original Notepad++ and Sumatra startup reaches FlsAlloc but their interfaces, installation and tasks remain unqualified; required runtime work continues in M14.10 and complete corpus acceptance in M14.12','Read-only/read-write/execute-read image/allocation protections only; general Windows virtual-memory semantics remain incomplete','Original 7-Zip details clip at requested column widths; universal controls, theme, drag services and arbitrary Windows application compatibility are not qualified'])
 write(final/'acceptance-results.json',result);print('PASS additive M14.5 acceptance',build)
if __name__=='__main__':main()
