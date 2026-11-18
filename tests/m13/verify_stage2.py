"""Bind M13.2 welcome/setup, exact media and measured native reports."""
import hashlib,importlib.util,json,re,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('resource_rules12',ROOT/'tests/m12/verify_components.py');rules=importlib.util.module_from_spec(spec);spec.loader.exec_module(rules)
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,r):p.write_bytes((json.dumps(r,indent=2)+'\n').encode())
def fixed_setup(path):
 text=path.read_text(encoding='utf-8');sections={}
 for section in ('bss','data'):
  values=re.findall(r'^\s*[0-9a-f]+\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+.*kernel_install_wizard6-kernel.o:\(\.'+section+r'\)$',text,re.M)
  assert len(values)==1,(section,values);sections[section]=int(values[0],16)
 return dict(bytes=sum(sections.values()),sections=sections)
def main():
 out=ROOT/'evidence/M13/2';assert not (out/'publication-results.json').exists()
 work=ROOT/'build/m13/stage2';meta=read(ROOT/'dist/m13stage2-build-manifest.json');starter=read(ROOT/'dist/m13stage2-starter-manifest.json')
 iso=meta['artifacts']['EngacerOS-M13STAGE2.iso']['sha256'];profiles={n:read(work/n/'results.json') for n in ('ordinary','compact','1024','150','4k')};journeys={n:read(work/('journey-'+n)/'results.json') for n in ('pointer','keyboard-compact','pointer-150','pointer-4k')};vm=read(work/'vmware-results/results.json');smoke=read(work/'candidate3-smoke/results.json')
 for r in [*profiles.values(),*journeys.values(),vm]:assert r['passed'] and r['build_id']==meta['build_id'] and r['iso_sha256']==iso
 assert smoke['passed'] and smoke['build_id']==meta['build_id'] and smoke['observed_startup_phase'] in (1,2,3)
 assert all(len(r['checks'])==6 for r in journeys.values())
 assert vm['existing_vm_inventory_unchanged'] and vm['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive']) and starter['passed']
 for n,r in profiles.items():
  assert r['resources']['retained_task_delta_pages']==0
  expected={'ordinary':(1920,1080,2),'compact':(1280,800,2),'1024':(1024,768,2),'150':(1920,1200,3),'4k':(3840,2160,4)}[n]
  assert tuple(r['physical'])==expected[:2] and r['scale_units']==expected[2]
  assert tuple(read(work/n/'welcome-capture.json')[k] for k in ('width','height'))==expected[:2]
 host=read(work/'host-results.json');assert host['passed']
 rules.git_inputs(meta['source_sha256'])
 for n,r in meta['artifacts'].items():assert sha(ROOT/'dist'/n)==r['sha256']
 baseline=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE1-installed-kernel.map');current=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE2-installed-kernel.map');assert current['bytes']==baseline['bytes']
 font=read(ROOT/'build/m13-native/font73-manifest.json');assert font['coverage_bytes']==251248
 assert font['header_sha256']==read(ROOT/'third_party/inter/raster-lock12.json')['header_sha256']
 old=read(ROOT/'evidence/M13/1/acceptance-results.json');assert sha(ROOT/'dist/EngacerOS-M13STAGE1.iso')==old['iso_sha256'];assert sha(ROOT/'dist/EngacerOS-M13STAGE1-VMware.zip')==old['vmware_zip_sha256']
 setup=fixed_setup(ROOT/'dist/EngacerOS-M13STAGE2-kernel.map');old_setup=fixed_setup(ROOT/'dist/EngacerOS-M13STAGE1-kernel.map')
 resources=dict(passed=True,fixed_desktop=current,baseline_fixed_desktop=baseline,fixed_installer=setup,baseline_fixed_installer=old_setup,installer_delta_bytes=setup['bytes']-old_setup['bytes'],font=font,profiles={n:r['resources'] for n,r in profiles.items()},scope='Fixed shell, installer, immutable fonts, framebuffer and managed task allocations are separate; configured RAM is not kernel consumption.')
 out.mkdir(parents=True,exist_ok=True)
 for n in [*profiles,'vmware-results',*['journey-'+n for n in journeys],'candidate3-smoke']:rules.copy_report(work/n,out/n)
 shutil.copyfile(work/'host-results.json',out/'host-results.json');shutil.copyfile(work/'candidate3-smoke/welcome.png',out/'feature.png');write(out/'resources.json',resources)
 accepted=dict(passed=True,stage='M13.2',version='0.13.2',qualification='M13-STAGE2-VM-v1',build_id=meta['build_id'],iso_sha256=iso,vmware_zip_sha256=starter['sha256'],source_inputs_verified=len(meta['source_sha256']),native_checks=[c for r in [*profiles.values(),*journeys.values()] for c in r['checks']],vmware_checks=vm['checks'],harness_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in [*(ROOT/'tests/m13').glob('*.py'),*(ROOT/'tests/m13').glob('*.mjs')]},resources='resources.json',limits=['Named VM setup/control profiles, not the M13.4 controller matrix or M13.12 whole product gate','No universal hardware, GPU 3D or general Windows compatibility','Agent scenario/visual review is not a human novice study','Public release/site closure is a separate gate'])
 write(out/'acceptance-results.json',accepted);print(json.dumps(accepted,indent=2))
if __name__=='__main__':main()
