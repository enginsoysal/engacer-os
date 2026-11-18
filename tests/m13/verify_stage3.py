"""Exact M13.3 disk safety, named transports, layout and installed-start gate."""
import hashlib,json,shutil
from pathlib import Path
import verify_stage2 as base
ROOT=base.ROOT;rules=base.rules
read=base.read;sha=base.sha;write=base.write
def main():
 out=ROOT/'evidence/M13/3';assert not (out/'publication-results.json').exists();work=ROOT/'build/m13/stage3';meta=read(ROOT/'dist/m13stage3-build-manifest.json');starter=read(ROOT/'dist/m13stage3-starter-manifest.json');iso=meta['artifacts']['EngacerOS-M13STAGE3.iso']['sha256']
 profiles={n:read(work/n/'results.json') for n in ('ordinary','compact','1024','150','4k')}
 names=['disk-compact-sata-keyboard','disk-150-sata','disk-4k-sata',*['disk-ordinary-'+c+'-blank' for c in ('sata','ide','mptsas','nvme','virtio')],'disk-safety','disk-protection','disk-resources','qemu-pvscsi-refusal'];tasks={n:read(work/n/'results.json') for n in names};vm=read(work/'vmware-results/results.json')
 assert meta['release_version']=='0.13.3' and meta['qualification_scope']=='M13-STAGE3-VM-v1'
 for r in [*profiles.values(),*tasks.values(),vm]:assert r['passed'] and r['build_id']==meta['build_id'] and r['iso_sha256']==iso
 for n,r in profiles.items():
  expected={'ordinary':(1920,1080,2),'compact':(1280,800,2),'1024':(1024,768,2),'150':(1920,1200,3),'4k':(3840,2160,4)}[n];assert tuple(r['physical'])==expected[:2] and r['scale_units']==expected[2] and r['resources']['retained_task_delta_pages']==0
  assert len(r['idle_observations'])>=3 and all(t['before']==t['after'] and t['halted']==2 for t in r['idle_observations'][-3:])
 for n in names[:8]:
  r=tasks[n];assert len(r['checks'])==5;capture=read(work/n/'create-fields-capture.json');assert [capture['width'],capture['height']]==r['physical']
 resources_task=tasks['disk-resources'];assert resources_task['retained_delta_pages']==0 and resources_task['both_cpus_halted'];assert len({r[0] for r in resources_task['repeated_format']})==1
 assert len(tasks['disk-safety']['checks'])==3 and len(tasks['disk-protection']['checks'])==4
 failed=read(out/'diagnostics/qemu-pvscsi-positive-attempt.json');assert not failed['passed'] and failed['build_id']=='fd173865af63691840baef35ba866d63' and failed['controller']=='pvscsi';assert tasks['qemu-pvscsi-refusal']['scope'].startswith('Expected refusal only')
 assert vm['existing_vm_inventory_unchanged'] and starter['passed'] and vm['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive'])
 host=read(work/'host-results.json');assert host['passed'];rules.git_inputs(meta['source_sha256'])
 for n,r in meta['artifacts'].items():assert sha(ROOT/'dist'/n)==r['sha256']
 old=read(ROOT/'evidence/M13/2/acceptance-results.json');assert sha(ROOT/'dist/EngacerOS-M13STAGE2.iso')==old['iso_sha256'] and sha(ROOT/'dist/EngacerOS-M13STAGE2-VMware.zip')==old['vmware_zip_sha256']
 current=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE3-installed-kernel.map');previous=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE2-installed-kernel.map');assert current['bytes']==previous['bytes'];setup=base.fixed_setup(ROOT/'dist/EngacerOS-M13STAGE3-kernel.map');old_setup=base.fixed_setup(ROOT/'dist/EngacerOS-M13STAGE2-kernel.map')
 font=read(ROOT/'build/m13-native/font73-manifest.json');assert font['coverage_bytes']==251248 and font['header_sha256']==read(ROOT/'third_party/inter/raster-lock12.json')['header_sha256']
 out.mkdir(parents=True,exist_ok=True)
 for n in [*profiles,*names,'vmware-results']:rules.copy_report(work/n,out/n)
 shutil.copyfile(work/'host-results.json',out/'host-results.json');shutil.copyfile(work/'disk-ordinary-sata-blank/created.png',out/'feature.png')
 write(out/'resources.json',dict(passed=True,fixed_desktop=current,baseline_fixed_desktop=previous,fixed_installer=setup,baseline_fixed_installer=old_setup,installer_delta_bytes=setup['bytes']-old_setup['bytes'],font=font,disk_tool_allocator=resources_task,profiles={n:r['resources'] for n,r in profiles.items()},scope='Fixed state, font masks, framebuffer storage, allocator current/peak pages and configured guest RAM are separate.'))
 accepted=dict(passed=True,stage='M13.3',version='0.13.3',qualification='M13-STAGE3-VM-v1',build_id=meta['build_id'],iso_sha256=iso,vmware_zip_sha256=starter['sha256'],source_inputs_verified=len(meta['source_sha256']),native_checks=[c for r in [*profiles.values(),*tasks.values()] for c in r.get('checks',[])],vmware_checks=vm['checks'],harness_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in [*(ROOT/'tests/m13').glob('*.py'),*(ROOT/'tests/m13').glob('*.mjs')]},resources='resources.json',qualified_qemu_disk_tool_transports=['SATA/AHCI','IDE','LSI SAS mptsas','NVMe','VirtIO block'],negative_qemu_pvscsi='Expected safe refusal only; original failed positive attempt retained separately',limits=['Exact SATA/UEFI VMware starter is separate from QEMU disk-tool profiles; full controller/firmware startup matrix belongs to M13.4','No universal hardware, GPU 3D or general Windows compatibility','Whole-disk installer; no data-preserving resize or dual boot','Agent visual/scenario review is not a human novice study','Public release and complete website closure remain separate gates'])
 write(out/'acceptance-results.json',accepted);print('PASS: M13.3 exact native safety, five transport lifecycles, five display installs and VMware startup; '+str(len(meta['source_sha256']))+' committed input digests')
if __name__=='__main__':main()
