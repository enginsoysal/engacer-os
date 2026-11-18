"""Bind M13.4 real setup/recovery and fourteen VMware startup profiles."""
import json,shutil
from pathlib import Path
import verify_stage2 as base
ROOT=base.ROOT;rules=base.rules;read=base.read;write=base.write;sha=base.sha

def main():
 out=ROOT/'evidence/M13/4';assert not (out/'publication-results.json').exists();work=ROOT/'build/m13/stage4';meta=read(ROOT/'dist/m13stage4-build-manifest.json');starter=read(ROOT/'dist/m13stage4-starter-manifest.json');iso=meta['artifacts']['EngacerOS-M13STAGE4.iso']['sha256']
 assert meta['release_version']=='0.13.4' and meta['qualification_scope']=='M13-STAGE4-VM-v1'
 profiles={n:read(work/n/'results.json') for n in ('ordinary','compact','1024','150','4k')}
 names=['progress-recovery','progress-compact','progress-150','progress-4k','progress-compact800','setup-safety','startup-failure','4kn-refusal','progress-resources','progress-midwrite'];tasks={n:read(work/n/'results.json') for n in names}
 labels=[c+'-'+f for c in ('sata','ide','lsilogic','lsisas1068','pvscsi','nvme') for f in ('efi','bios')]+['buslogic-bios','sata-efi-starter'];matrix={n:read(work/'matrix-results'/n/'results.json') for n in labels}
 for r in [*profiles.values(),*tasks.values(),*matrix.values()]:assert r['passed'] and r['build_id']==meta['build_id'] and r['iso_sha256']==iso
 for n,r in profiles.items():
  expected={'ordinary':(1920,1080,2),'compact':(1280,800,2),'1024':(1024,768,2),'150':(1920,1200,3),'4k':(3840,2160,4)}[n];assert tuple(r['physical'])==expected[:2] and r['scale_units']==expected[2] and r['resources']['retained_task_delta_pages']==0
  assert len(r['idle_observations'])>=3 and all(t['before']==t['after'] and t['halted']==2 for t in r['idle_observations'][-3:])
 for n in names[:5]:
  r=tasks[n];assert r['observed_step']==5 and r['observed_busy']==1 and 0<r['observed_percent']<100
  for frame in ('recovery','actual-progress','finish'):
   cap=read(work/n/(frame+'-capture.json'));assert 'compressed at creation' in cap['raw_storage']
 assert tasks['progress-midwrite']['disk_bytes_changed'] and 25<=tasks['progress-midwrite']['observed_percent']<100
 assert tasks['progress-resources']['visible_frame_events']<tasks['progress-resources']['progress_callbacks']
 assert len(tasks['setup-safety']['checks'])==5 and len(tasks['startup-failure']['checks'])==3 and len(tasks['4kn-refusal']['checks'])==3
 for n,r in matrix.items():
  assert r['existing_vm_inventory_unchanged'] and r['all_shipped_devices_enabled'] and r['same_vm_reused'] and not r['boot_order_forced'] and len(r['checks'])>=(4 if n.endswith('starter') else 3)
  assert r['harness_sha256']==sha(ROOT/'tests/m13/vmware_matrix4.py')
 assert matrix['sata-efi-starter']['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive']) and starter['passed']
 host=read(work/'host-results.json');assert host['passed'];rules.git_inputs(meta['source_sha256'])
 for n,r in meta['artifacts'].items():assert sha(ROOT/'dist'/n)==r['sha256']
 old=read(ROOT/'evidence/M13/3/acceptance-results.json');assert sha(ROOT/'dist/EngacerOS-M13STAGE3.iso')==old['iso_sha256'] and sha(ROOT/'dist/EngacerOS-M13STAGE3-VMware.zip')==old['vmware_zip_sha256']
 current=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE4-installed-kernel.map');previous=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE3-installed-kernel.map');assert current['bytes']==previous['bytes'];setup=base.fixed_setup(ROOT/'dist/EngacerOS-M13STAGE4-kernel.map');old_setup=base.fixed_setup(ROOT/'dist/EngacerOS-M13STAGE3-kernel.map')
 font=read(ROOT/'build/m13-native/font73-manifest.json');assert font['coverage_bytes']==251248 and font['header_sha256']==read(ROOT/'third_party/inter/raster-lock12.json')['header_sha256']
 out.mkdir(parents=True,exist_ok=True)
 for n in [*profiles,*names]:rules.copy_report(work/n,out/n)
 for n in labels:rules.copy_report(work/'matrix-results'/n,out/'matrix'/n)
 shutil.copyfile(work/'host-results.json',out/'host-results.json');shutil.copyfile(work/'progress-4k/finish.png',out/'feature.png')
 write(out/'resources.json',dict(passed=True,fixed_desktop=current,baseline_fixed_desktop=previous,fixed_installer=setup,baseline_fixed_installer=old_setup,installer_delta_bytes=setup['bytes']-old_setup['bytes'],font=font,profiles={n:r['resources'] for n,r in profiles.items()},scope='Configured RAM, fixed state, immutable font masks, framebuffer storage and managed current/peak/retained pages are separate. Identical progress notifications skip repaint without skipping storage work or audio service.'))
 accepted=dict(passed=True,stage='M13.4',version='0.13.4',qualification='M13-STAGE4-VM-v1',build_id=meta['build_id'],iso_sha256=iso,vmware_zip_sha256=starter['sha256'],source_inputs_verified=len(meta['source_sha256']),native_checks=[c for r in [*profiles.values(),*tasks.values()] for c in r.get('checks',[])],vmware_checks={n:r['checks'] for n,r in matrix.items()},harness_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in [*(ROOT/'tests/m13').glob('*.py'),*(ROOT/'tests/m13').glob('*.mjs')]},resources='resources.json',vmware_profiles=labels,limits=['Named virtual profiles are separate from universal or physical hardware support','QEMU PVSCSI remains unqualified; actual VMware PVSCSI is separately tested','4096-byte-sector NVMe inspection does not qualify installer writes','Whole-disk installation; no data-preserving resize or dual boot','Boot-slot repair does not repair arbitrary personal data corruption','Secure Boot signing, vendor GPU 3D and general Windows compatibility remain outside this stage','Agent scenario and visual review are not a human novice study','Public release and full website closure remain separate gates'])
 write(out/'acceptance-results.json',accepted);print('PASS: M13.4 exact installation, recovery, five displays and fourteen VMware profiles')
if __name__=='__main__':main()
