"""Qualify the exact M13.1 native artifact, never infer production website closure."""
import hashlib,importlib.util,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('resource_rules12',ROOT/'tests/m12/verify_components.py');rules=importlib.util.module_from_spec(spec);spec.loader.exec_module(rules)
def read(path):return json.loads(path.read_text(encoding='utf-8'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 work=ROOT/'build/m13/stage1';out=ROOT/'evidence/M13/1';meta=read(ROOT/'dist/m13stage1-build-manifest.json');starter=read(ROOT/'dist/m13stage1-starter-manifest.json')
 assert meta['qualification_scope']=='M13-STAGE1-VM-v1' and meta['release_version']=='0.13.1'
 iso=meta['artifacts']['EngacerOS-M13STAGE1.iso']['sha256'];profiles={name:read(work/name/'results.json') for name in ('ordinary','compact','1024','150','4k')};vmware=read(work/'vmware-results/results.json');host=read(work/'host-results.json')
 for report in [*profiles.values(),vmware]:assert report['passed'] and report['build_id']==meta['build_id'] and report['iso_sha256']==iso
 assert host['passed'] and starter['passed'] and starter['build_id']==meta['build_id']
 assert vmware['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive']) and vmware['existing_vm_inventory_unchanged']
 for name,report in profiles.items():
  assert len(report['checks'])==4 and report['resources']['retained_task_delta_pages']==0
  expected={'ordinary':(1920,1080,2),'compact':(1280,800,2),'1024':(1024,768,2),'150':(1920,1200,3),'4k':(3840,2160,4)}[name];assert tuple(report['physical'])==expected[:2] and report['scale_units']==expected[2]
  for theme in ('light','dark','high-contrast'):
   capture=read(work/name/('component-gallery-'+theme+'-capture.json'));assert (capture['width'],capture['height'])==expected[:2]
 current=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE1-installed-kernel.map');baseline=rules.desktop_state(ROOT/'dist/EngacerOS-M12STAGE18-installed-kernel.map');assert current['bytes']==baseline['bytes']
 font=read(ROOT/'build/m13-native/font73-manifest.json');assert font['coverage_bytes']==251248 and font['header_sha256']==read(ROOT/'third_party/inter/raster-lock12.json')['header_sha256']
 for name,record in meta['artifacts'].items():assert sha(ROOT/'dist'/name)==record['sha256']
 assert sha(ROOT/'dist/EngacerOS-M12STAGE18.iso')=='f63b78973c9da269b4eead46873d947e94fcd2266dff4b4c06f2666b743aa3f9'
 assert sha(ROOT/'dist/EngacerOS-M12STAGE18-VMware.zip')=='dafd107340e11ea74898c4c7ffab45dc4e31b50856421076e0b2f4787ee5bed4'
 rules.git_inputs(meta['source_sha256'])
 out.mkdir(parents=True,exist_ok=True)
 for name in [*profiles,'vmware-results']:rules.copy_report(work/name,out/name)
 shutil.copyfile(work/'host-results.json',out/'host-results.json');shutil.copyfile(work/'ordinary/component-gallery-interactive.png',out/'feature.png')
 resources=dict(passed=True,scope='Fixed shell state, immutable font masks, managed allocator pages and framebuffer storage measured separately; configured guest RAM is not consumption.',fixed_desktop=current,baseline_fixed_desktop=baseline,font=font,profiles={name:report['resources'] for name,report in profiles.items()})
 (out/'resources.json').write_bytes((json.dumps(resources,indent=2)+'\n').encode())
 harness={p.relative_to(ROOT).as_posix():sha(p) for p in [*(ROOT/'tests/m13').glob('*.py'),*(ROOT/'tests/m13').glob('*.mjs')]}
 accepted=dict(passed=True,stage='M13.1',version='0.13.1',qualification='M13-STAGE1-VM-v1',build_id=meta['build_id'],iso_sha256=iso,vmware_zip_sha256=starter['sha256'],source_inputs_verified=len(meta['source_sha256']),native_checks=[c for report in profiles.values() for c in report['checks']],vmware_checks=vmware['checks'],harness_sha256=harness,resources='resources.json',limits=['Scoped native shared-control qualification on named virtual profiles; later M13 whole-product qualification remains M13.12','No physical/ARM, vendor GPU 3D, universal devices or general DOS/Windows qualification','Agent visual/scenario review is separate from human usability research','GitHub and public BrixCanvas acceptance remain separate publication gates'])
 (out/'acceptance-results.json').write_bytes((json.dumps(accepted,indent=2)+'\n').encode());print(json.dumps(accepted,indent=2))
if __name__=='__main__':main()
