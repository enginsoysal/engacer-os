"""Accept only the matching final native/controller/device/application regression."""
import hashlib,json,os,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'evidence/M11/6'

def load(p):return json.loads(p.read_text(encoding='utf-8'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,r):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(r,indent=2)+'\n').encode())

def main():
 meta=load(ROOT/'dist/m11final-build-manifest.json');starter=load(ROOT/'dist/m11final-starter-manifest.json')
 assert (meta['milestone'],meta['build_revision'],meta['release_version'])==('M11','final','0.11.6')
 iso=meta['artifacts']['EngacerOS-M11FINAL.iso']['sha256'];build=meta['build_id']
 assert starter['passed'] and starter['build_id']==build and digest(ROOT/'dist'/starter['archive'])==starter['sha256']
 paths=['selection/results.json','files/results.json','files/preferences-results.json','files/drag-cancel/results.json','start/results.json','start/controls-results.json','windows/results.json','windows/keys/results.json','windows/motion/results.json']
 paths+=['setup/'+p+'/results.json' for p in ('ordinary','150','4k','safety','packages','vmware')]
 paths+=['hardware/'+p+'/results.json' for p in ('uefi-1280x800-128','uefi-1280x800-64','bios-1280x800-128','uefi-3840x2160-128-hub','uefi-1280x800-128-large-usb')]
 paths+=['usb-negative/results.json','usb-quota/results.json']
 pairs=[c+'-'+f for c in ('sata','ide','lsilogic','lsisas1068','pvscsi','nvme') for f in ('efi','bios')]+['buslogic-bios','sata-efi-starter']
 paths+=['matrix-results/'+p+'/results.json' for p in pairs]
 reports={}
 for path in paths:
  r=load(ROOT/'build/m11'/path);assert r['passed'],path
  if 'iso_sha256' in r:assert r['iso_sha256']==iso,path
  if 'build_id' in r:assert r['build_id']==build,path
  if path.startswith('matrix-results/'):
   assert r['existing_vm_inventory_unchanged'] and r['same_vm_reused'] and not r['boot_order_forced'] and r['all_shipped_devices_enabled'],path
  reports[path]=r
 exact=reports['matrix-results/sata-efi-starter/results.json']
 assert exact['starter_sha256']==starter['sha256'] and len(exact['original_payload_sha256'])==106
 assert reports['setup/vmware/results.json']['starter_sha256']==starter['sha256']
 assert reports['windows/results.json']['window_operations_retained_managed_page_delta']==0
 assert reports['setup/packages/results.json']['retained_page_delta']==0
 assert len(reports['selection/results.json']['checks'])>=14
 assert len(reports['files/results.json']['checks'])>=20
 assert len(reports['windows/results.json']['checks'])>=11
 for profile in ('ordinary','150','4k'):
  r=reports['setup/'+profile+'/results.json'];assert len(r['checks'])>=5 and len(r['idle_observations'])>=3 and all(r['idle_observations'][-3:])
 motion=reports['windows/motion/results.json']['profiles']
 assert [p['physical'] for p in motion]==[[1280,800],[1920,1200],[3840,2160]]
 for p in motion:
  assert p['managed_bytes_before']==p['managed_bytes_after'] and p['cached_copy_frames']>0 and p['all_cpus_halted_when_idle'] and p['idle_paints_unchanged']
  assert len(p['comparisons'])==4 and all(c['cached_equals_full_viewport'] for c in p['comparisons'])
 for path in ('input-host/results.json','start-host/results.json','volume-host/results.json'):
  r=load(ROOT/'build/m11'/path);assert r['passed']
  for name,sha in r['source_sha256'].items():assert digest(ROOT/name)==sha,name
  reports[path]=r
 assert reports['volume-host/results.json']['fault_cases']==288
 for path in ('input-host/results.json','filesystem-host/results.json'):
  r=load(ROOT/'build/m10'/path);assert r['passed']
  for name,sha in r['source_sha256'].items():assert digest(ROOT/name)==sha,name
  reports['hardware-host/'+path]=r
 known=load(ROOT/'build/m11/known-uefi64-boot-usb/results.json')
 assert known['passed'] is False and not known['qualified'] and known['expected_refusal_recorded'] and known['build_id']==build and known['iso_sha256']==iso
 requests=''.join(':'+p+'\n' for p in meta['source_sha256']).encode()
 raw=subprocess.run(['git','cat-file','--batch'],cwd=ROOT,input=requests,capture_output=True,check=True).stdout;at=0
 for name,sha in meta['source_sha256'].items():
  assert digest(ROOT/name)==sha,('Changed compiled input',name)
  end=raw.index(b'\n',at);header=raw[at:end].split();assert len(header)==3 and header[1]==b'blob',name
  size=int(header[2]);assert hashlib.sha256(raw[end+1:end+1+size]).hexdigest()==sha,('Staged bytes differ',name);at=end+size+2
 for name,r in meta['artifacts'].items():assert digest(ROOT/'dist'/name)==r['sha256'],name
 preserved=[]
 for p in [ROOT/'evidence/M10/m10-build-manifest.json']+[ROOT/f'evidence/M11/{n}/candidate-manifest.json' for n in range(1,6)]:
  old=load(p)
  for name,r in old['artifacts'].items():assert digest(ROOT/'dist'/name)==r['sha256'],('Accepted artifact changed',name)
  preserved.append({'manifest':p.relative_to(ROOT).as_posix(),'unchanged_artifacts':len(old['artifacts'])})
 fixed={}
 for revision in ('STAGE1','STAGE5','FINAL'):
  p=ROOT/('dist/EngacerOS-M11'+revision+'-installed-kernel.map');text=p.read_text(encoding='utf-8');parts={}
  for section in ('bss','data'):
   values=re.findall(r'^\s*[0-9a-f]+\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+.*kernel_desktop_session-kernel.o:\(\.'+section+r'\)$',text,re.M);assert len(values)==1;parts[section]=int(values[0],16)
  fixed[revision]={'bytes':sum(parts.values()),'sections':parts,'map_sha256':digest(p)}
 assert fixed['FINAL']['bytes']-fixed['STAGE1']['bytes']<512*1024
 font=load(ROOT/'build/m11/font73-manifest.json')
 assert font['secondary_sizes']==[14,21,28] and font['coverage_bytes']<1024**2
 assert font['header_sha256']==load(ROOT/'third_party/inter/raster-lock11.json')['header_sha256']
 # Publish only observations, never private owned-image pointers or raw VRAM.
 for path,r in reports.items():
  source=ROOT/('build/m10/'+path.removeprefix('hardware-host/') if path.startswith('hardware-host/') else 'build/m11/'+path)
  target=OUT/Path(path).parent;target.mkdir(parents=True,exist_ok=True)
  for p in source.parent.iterdir():
   if not p.is_file() or p.suffix not in ('.json','.png','.log') or p.name in ('owned-work.json','harness.log'):continue
   data=p.read_bytes()
   if p.suffix!='.png':
    data=data.replace(str(ROOT).encode(),b'<project-root>')
    assert b'C:\\Users\\' not in data and b'C:/Users/' not in data,p.name
   (target/p.name).write_bytes(data)
 for task,folders in {'files':('install','detached'),'start':('install','disk-only'),'windows':('install','disk-only','native-4k')}.items():
  base=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6'/('m11-'+task)
  owned=max(base.iterdir(),key=lambda p:p.stat().st_mtime_ns)
  assert owned.resolve().is_relative_to(base.resolve())
  for folder in folders:
   serial=(owned/folder/'serial.log').read_text(encoding='utf-8',errors='replace')
   assert 'M7_DESKTOP_READY build='+build in serial and 'KERNEL_PANIC' not in serial,(task,folder)
   (OUT/task/(folder+'.log')).write_bytes(serial.replace(str(ROOT),'<project-root>').encode())
 write(OUT/'known-unqualified/uefi64-boot-usb.json',known)
 write(OUT/'candidate-manifest.json',meta);write(OUT/'starter-manifest.json',starter);write(OUT/'preserved-releases.json',preserved)
 boots={}
 for profile in ('ordinary','150','4k','vmware'):
  serial=(OUT/'setup'/profile/'install.log').read_text(encoding='utf-8')
  values=re.findall(r'M7_DESKTOP_STATS current=0x([0-9a-f]+) peak=0x([0-9a-f]+) allocation_failures=0x([0-9a-f]+)',serial);assert values
  current,peak,failures=[int(v,16) for v in values[-1]]
  boots[profile]={'managed_current_bytes':current,'managed_peak_bytes':peak,'allocation_failure_counter_including_boot_stress_probes':failures}
 write(OUT/'resources.json',{'passed':True,'fixed_desktop':fixed,'added_from_stage1_bytes':fixed['FINAL']['bytes']-fixed['STAGE1']['bytes'],'budget_bytes':512*1024,'native_motion':motion,'boot_managed_observations':boots,'font':font,'scope':'Fixed desktop state and managed pages are measured separately; configured guest RAM is not consumption.'})
 result={'passed':True,'stage':'M11.6','version':'0.11.6','qualification':'M11-FINAL-VM-v1','build_id':build,'iso_sha256':iso,'vmware_zip_sha256':starter['sha256'],'source_inputs_verified':len(meta['source_sha256']),'artifacts_verified':len(meta['artifacts'])+1,'native_profiles':paths,'controller_profiles':pairs,'native_tasks':[c for r in reports.values() for c in r.get('checks',[])],'source_index_matches_compiled_bytes':True,'test_source_sha256':{p.relative_to(ROOT).as_posix():digest(p) for p in sorted((ROOT/'tests/m11').iterdir()) if p.suffix in ('.py','.c')},'limits':meta['limits']+['64-MiB OVMF boot-attached USB remains unqualified; the 64-MiB passing journey connects storage after installed startup.'],'publication':'Visible release, exact downloads and fresh public website verification are separate required gates.'}
 result['release_harness_sha256']={name:digest(ROOT/name) for name in ('tools/release/vmware_starter11.py','tools/release/m11_final_assets.py')}
 result['evidence_sha256']={p.relative_to(OUT).as_posix():digest(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='acceptance-results.json'}
 write(OUT/'acceptance-results.json',result);print('M11.6 matching final qualification PASS')
if __name__=='__main__':main()
