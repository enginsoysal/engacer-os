"""Bind scoped M13.9 motion/cursor tasks; stability is exclusively M13.13."""
import shutil
import verify_stage2 as base
ROOT=base.ROOT;read=base.read;write=base.write;sha=base.sha;rules=base.rules

def main():
 out=ROOT/'evidence/M13/9';out.mkdir(parents=True,exist_ok=True);assert not (out/'publication-results.json').exists()
 work=ROOT/'build/m13/stage9';meta=read(ROOT/'dist/m13stage9-build-manifest.json');starter=read(ROOT/'dist/m13stage9-starter-manifest.json');iso=meta['artifacts']['EngacerOS-M13STAGE9.iso']['sha256']
 names=('ordinary','compact','1024','150','4k')
 profiles={n:read(work/n/'results.json') for n in names}
 windows={n:read(work/('windows-'+n)/'results.json') for n in names}
 cursors={n:read(work/('cursors-'+n)/'results.json') for n in names}
 motion=read(work/'motion/results.json')
 reference={n:read(work/'motion'/('whpx-legacy-'+n)/'results.json') for n in ('ordinary','4k')}
 vm=read(work/'vmware-results/results.json')
 reports=[*profiles.values(),*windows.values(),*cursors.values(),motion,*reference.values(),vm]
 for r in reports:assert r['passed'] and r['build_id']==meta['build_id'] and r['iso_sha256']==iso
 for n in names:
  assert profiles[n]['resources']['retained_task_delta_pages']==0
  assert windows[n]['resources']['retained_pages']==cursors[n]['resources']['retained_pages']==0
  assert len(windows[n]['checks'])==4 and len(cursors[n]['observations'])==7
 for r in motion['profiles']:assert all(v['cached_equals_full_viewport'] for v in r['comparisons'])
 assert len(motion['profiles'])==3
 for n,r in reference.items():
  assert r['native_completion_budget_passed'] and r['visible_positions']==r['requested_positions']>=32 and r['missed_requested_positions']==0
  assert r['native_budget_trace']['matched_positions']==r['native_budget_trace']['offered_positions']>=32 and r['resources']['retained_task_delta_pages']==0
  assert r['qualification_method'].startswith('native receipt-to-framebuffer')
 assert vm['existing_vm_inventory_unchanged'] and vm['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive'])
 previous=read(ROOT/'evidence/M13/8/acceptance-results.json')
 assert sha(ROOT/'dist/EngacerOS-M13STAGE8.iso')==previous['iso_sha256'] and sha(ROOT/'dist/EngacerOS-M13STAGE8-VMware.zip')==previous['vmware_zip_sha256']
 rules.git_inputs(meta['source_sha256'])
 for name,value in meta['artifacts'].items():assert sha(ROOT/'dist'/name)==value['sha256']
 current=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE9-installed-kernel.map');old=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE8-installed-kernel.map');assert current['bytes']-old['bytes']==2560
 setup=base.fixed_setup(ROOT/'dist/EngacerOS-M13STAGE9-kernel.map')
 write(out/'resources.json',dict(desktop_fixed=current,previous_m138_fixed=old,desktop_delta_bytes=2560,cursor_kind_extra_core_bytes=4,input_timestamp_extra_usb_bytes=16,setup=setup,profiles={n:r['resources'] for n,r in profiles.items()},scope='Native pointer ring and kind only; no new framebuffer, bitmap cache or idle worker. Configured RAM and framebuffer bytes remain separate from fixed/managed memory.'))
 checks=[c for r in [*profiles.values(),*windows.values(),*cursors.values()] for c in r['checks']]
 checks+=['Twelve clipped cached/full-repaint comparisons across ordinary, 150% and physical 4K are pixel-identical','Two exact hardware-virtualized reference profiles independently confirm all requested positions and pass the declared native receipt-to-framebuffer completion budgets']
 write(out/'acceptance-results.json',dict(passed=True,stage='M13.9',version='0.13.9',qualification='M13-STAGE9-VM-v1',build_id=meta['build_id'],iso_sha256=iso,vmware_zip_sha256=starter['sha256'],source_inputs_verified=len(meta['source_sha256']),native_checks=checks,vmware_checks=vm['checks'],resources='resources.json',reference_measurements=reference,limits=['Scoped motion/cursor and functional startup qualification only; all stability investigation and duration/reset qualification are deferred to M13.13 by explicit owner instruction','Processing budgets measure native input receipt through CPU composition/framebuffer/cursor completion; they do not measure physical scanout or GPU FPS','External RFB latency and cadence are separately published; original external goals remain unmet where recorded and are not claimed passed','Named virtual displays and exact enabled-device SATA/UEFI starter; the full integration controller matrix belongs to M13.12','No universal hardware, vendor 3D acceleration, general Windows compatibility or human novice-study claim','Matching public release, manuals and website remain separate closure gates']))
 for n in names:
  for label in (n,'windows-'+n,'cursors-'+n):
   dest=out/'native'/label;dest.mkdir(parents=True,exist_ok=True)
   for p in (work/label).iterdir():
    if p.suffix in ('.json','.png','.log'):shutil.copyfile(p,dest/p.name)
 for label in ('motion','motion/whpx-legacy-ordinary','motion/whpx-legacy-4k','vmware-results'):
  src=work/label
  if not src.exists():continue
  dest=out/'native'/label;dest.mkdir(parents=True,exist_ok=True)
  for p in src.iterdir():
   if p.suffix in ('.json','.png','.log'):shutil.copyfile(p,dest/p.name)
 print('PASS scoped M13.9 exact native motion, cursor, processing budgets and VMware tasks; stability remains M13.13')

if __name__=='__main__':main()
