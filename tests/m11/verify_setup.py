"""Freeze M11.5 only after matching source, native setup, safety and VMware tasks."""
import hashlib,json,re,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'evidence/M11/5'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,value):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(value,indent=2)+'\n').encode())
def main():
 meta=load(ROOT/'dist/m11stage5-build-manifest.json');starter=load(ROOT/'dist/m11stage5-starter-manifest.json');base=ROOT/'build/m11/setup';reports={k:load(base/k/'results.json') for k in ('ordinary','150','4k','safety','packages','vmware')}
 assert meta['milestone']=='M11' and meta['build_revision']=='stage5' and meta['release_version']=='0.11.5'
 iso=meta['artifacts']['EngacerOS-M11STAGE5.iso']['sha256']
 for name,r in reports.items():
  assert r['passed'] and r['build_id']==meta['build_id'],name
  if name!='safety':assert r['iso_sha256']==iso,name
 assert starter['passed'] and starter['sha256']==reports['vmware']['starter_sha256']==digest(ROOT/'dist'/starter['archive'])
 assert reports['vmware']['existing_vm_inventory_unchanged']
 requests=''.join(':'+p+'\n' for p in meta['source_sha256']).encode()
 batch=subprocess.run(['git','cat-file','--batch'],input=requests,cwd=ROOT,capture_output=True,check=True).stdout;offset=0
 for path,expected in meta['source_sha256'].items():
  assert digest(ROOT/path)==expected,('Compiled source changed',path)
  end=batch.index(b'\n',offset);header=batch[offset:end].split();assert len(header)==3 and header[1]==b'blob',path
  size=int(header[2]);blob=batch[end+1:end+1+size];offset=end+size+2
  assert hashlib.sha256(blob).hexdigest()==expected,('Staged source differs from compiled bytes',path)
 for path,r in meta['artifacts'].items():assert digest(ROOT/'dist'/path)==r['sha256'],path
 fixed={}
 for stage in (1,4,5):
  path=ROOT/('dist/EngacerOS-M11STAGE'+str(stage)+'-installed-kernel.map');text=path.read_text();sections={}
  for part in ('bss','data'):
   values=re.findall(r'^\s*[0-9a-f]+\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+.*kernel_desktop_session-kernel.o:\(\.'+part+r'\)$',text,re.M);assert len(values)==1;sections[part]=int(values[0],16)
  fixed[str(stage)]={'bytes':sum(sections.values()),'sections':sections,'map_sha256':digest(path)}
 assert fixed['5']['bytes']-fixed['1']['bytes']<512*1024
 preserved=[]
 for path in [ROOT/'evidence/M10/m10-build-manifest.json']+[ROOT/('evidence/M11/'+str(n)+'/candidate-manifest.json') for n in (1,2,3,4)]:
  record=load(path)
  for filename,r in record['artifacts'].items():assert digest(ROOT/'dist'/filename)==r['sha256'],('Accepted media changed',filename)
  preserved.append({'manifest':path.relative_to(ROOT).as_posix(),'unchanged_artifacts':len(record['artifacts'])})
 for folder in reports:
  destination=OUT/folder;destination.mkdir(parents=True,exist_ok=True)
  for p in (base/folder).iterdir():
   if p.is_file() and p.suffix in ('.json','.png','.log'):
    data=p.read_bytes();assert p.suffix=='.png' or str(ROOT).encode() not in data
    (destination/p.name).write_bytes(data)
 for profile in ('ordinary','150','4k'):
  captures=[load(p) for p in (OUT/profile).glob('*-capture.json')]
  assert captures and all(c['width']=={'ordinary':1280,'150':1920,'4k':3840}[profile] for c in captures)
  assert len(reports[profile]['checks'])>=5
 boot_stats={}
 for profile in ('ordinary','150','4k','vmware'):
  text=(OUT/profile/'install.log').read_text();values=re.findall(r'M7_DESKTOP_STATS current=0x([0-9a-f]+) peak=0x([0-9a-f]+) allocation_failures=0x([0-9a-f]+)',text)
  assert values;current,peak,failures=map(lambda x:int(x,16),values[-1]);boot_stats[profile]={'managed_current_bytes':current,'managed_peak_bytes':peak,'allocation_failure_counter_including_boot_stress_probes':failures}
 resources={'passed':True,'boot_managed_observations':boot_stats,'offline_app_lifecycle':{k:reports['packages'][k] for k in ('managed_current_bytes','managed_peak_bytes','retained_page_delta')},'scope':'Fixed desktop BSS/data only; firmware, kernel, fonts, shared framebuffer and managed-page consumption are separate','fixed_desktop':fixed,'added_from_stage4_bytes':fixed['5']['bytes']-fixed['4']['bytes'],'added_from_stage1_bytes':fixed['5']['bytes']-fixed['1']['bytes'],'budget_bytes':512*1024,'idle':'Every profile observes three consecutive unchanged-paint idle intervals and all CPUs halted; legitimate DHCP/clock startup work is retained in observations'}
 write(OUT/'candidate-manifest.json',meta);write(OUT/'starter-manifest.json',starter);write(OUT/'resources.json',resources);write(OUT/'preserved-releases.json',preserved)
 tests=['tests/m11/setup.py','tests/m11/setup_safety.py','tests/m11/setup_packages.py','tests/m11/vmware_setup.py','tests/m11/verify_setup.py','tests/m11/ui.py','tools/release/vmware_starter11.py']
 report={'passed':True,'stage':'M11.5','version':'0.11.5','qualification':'M11-STAGE5-VM-v1','build_id':meta['build_id'],'iso_sha256':iso,'vmware_zip_sha256':starter['sha256'],'source_inputs_verified':len(meta['source_sha256']),'artifacts_verified':len(meta['artifacts'])+1,'native_tasks':[c for r in reports.values() for c in r['checks']],'native_profiles':list(reports),'source_index_matches_compiled_bytes':True,'test_source_sha256':{p:digest(ROOT/p) for p in tests},'scope':'Expanded setup, real partition operations/consent/error/retry/recovery, ordinary/150%/4K installed journeys, and exact enabled-device VMware SATA/UEFI starter with retained-ISO reset and two detached boots. Full controller/device/original-app regression remains M11.6.','publication':'Visible release, exact downloads, English manuals and complete fresh public website verification remain required before completion'}
 write(OUT/'acceptance-results.json',report);print('M11.5 exact-source/native/safety/VMware acceptance PASS')
if __name__=='__main__':main()
