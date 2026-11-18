"""M13.5 exact workspace/window scope, never inferred from older media."""
import json,shutil
from pathlib import Path
import verify_stage2 as base
ROOT=base.ROOT;rules=base.rules;read=base.read;write=base.write;sha=base.sha

def copy_case(source,dest,diagnostics):
 dest.mkdir(parents=True,exist_ok=True);diagnostics.mkdir(parents=True,exist_ok=True)
 for file in source.iterdir():
  if not file.is_file() or file.suffix not in ('.json','.png','.log'):continue
  if file.name in ('close-all-failure.png','close-all-failure-capture.json'):continue # Superseded failure is explicitly retained in diagnostics/false-snap-overlay.png.
  target=diagnostics/(source.name+'-'+file.name) if file.name.startswith('initial-') else dest/file.name
  if file.suffix=='.png':shutil.copyfile(file,target)
  else:target.write_bytes(file.read_bytes().replace(str(ROOT).encode(),b'<project-root>'))

def main():
 out=ROOT/'evidence/M13/5';assert not (out/'publication-results.json').exists();work=ROOT/'build/m13/stage5';meta=read(ROOT/'dist/m13stage5-build-manifest.json');starter=read(ROOT/'dist/m13stage5-starter-manifest.json');iso=meta['artifacts']['EngacerOS-M13STAGE5.iso']['sha256']
 assert meta['release_version']=='0.13.5' and meta['qualification_scope']=='M13-STAGE5-VM-v1'
 profiles={n:read(work/n/'results.json') for n in ('ordinary','compact','1024','150','4k')};windows={n:read(work/('windows-'+n)/'results.json') for n in ('ordinary','compact','1024','150','4k','odd150')};desktop=read(work/'desktop-native/results.json');chrome=read(work/'chrome-native/results.json');vm=read(work/'vmware-results/results.json');motion=read(work/'motion/results.json')
 for r in [*profiles.values(),*windows.values(),desktop,chrome,vm,motion]:assert r['passed'] and r['build_id']==meta['build_id'] and r['iso_sha256']==iso
 for n,r in profiles.items():
  expected={'ordinary':(1920,1080,2),'compact':(1280,800,2),'1024':(1024,768,2),'150':(1920,1200,3),'4k':(3840,2160,4)}[n];assert tuple(r['physical'])==expected[:2] and r['scale_units']==expected[2] and r['resources']['retained_task_delta_pages']==0
  cap=read(work/n/'desktop-capture.json');assert (cap['width'],cap['height'])==expected[:2]
  idle=r['idle_observations'];assert len(idle)>=3 and all(t['before']==t['after'] and t['halted']==2 for t in idle[-3:])
 for n,r in windows.items():
  assert len(r['checks'])==4 and r['resources']['retained_pages']==0
  cap=read(work/('windows-'+n)/'two-real-windows-capture.json');assert (cap['width'],cap['height'])==tuple(r['physical']);idle=r['idle_observations'];assert len(idle)>=3 and all(t['before']==t['after'] and t['halted']==2 for t in idle[-3:])
 assert windows['odd150']['logical'][0]%2==1 and windows['odd150']['physical']==[2048,1152]
 assert len(motion['profiles'])==3
 for r in motion['profiles']:
  assert len(r['comparisons'])==4 and all(c['cached_equals_full_viewport'] for c in r['comparisons']) and r['managed_bytes_before']==r['managed_bytes_after'] and r['cached_copy_frames']>0 and r['all_cpus_halted_when_idle'] and r['idle_paints_unchanged']
 assert len(chrome['checks'])==9 and len(desktop['checks'])==8 and chrome['resources']['retained_pages']==desktop['resources']['retained_pages']==0
 assert len(desktop['icon_comparisons'])==17 and all(r['max_channel_difference']<=1 for r in desktop['icon_comparisons']);assert {r['physical_size'] for r in desktop['icon_comparisons']}=={48,72,96}
 assert vm['existing_vm_inventory_unchanged'] and vm['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive']) and starter['passed']
 host=read(work/'host-results.json');grid=read(work/'desktop-host/host-results.json');assert host['passed'] and grid['passed'];rules.git_inputs(meta['source_sha256']);rules.git_inputs(grid['source_sha256'])
 for n,r in meta['artifacts'].items():assert sha(ROOT/'dist'/n)==r['sha256']
 old=read(ROOT/'evidence/M13/4/acceptance-results.json');assert sha(ROOT/'dist/EngacerOS-M13STAGE4.iso')==old['iso_sha256'] and sha(ROOT/'dist/EngacerOS-M13STAGE4-VMware.zip')==old['vmware_zip_sha256']
 diagnostic=read(out/'diagnostics/offscreen-keyboard-snap.json');assert diagnostic['qualification_excluded'] and not diagnostic['observation']['passed'] and diagnostic['superseded_build']=='f75973fdc3df5b84742b7732b245c3be' and diagnostic['replacement_build']==meta['build_id']
 current=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE5-installed-kernel.map');previous=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE4-installed-kernel.map');assert current['bytes']<=previous['bytes'];setup=base.fixed_setup(ROOT/'dist/EngacerOS-M13STAGE5-kernel.map');previous_setup=base.fixed_setup(ROOT/'dist/EngacerOS-M13STAGE4-kernel.map');assert setup['bytes']==previous_setup['bytes']
 font=read(ROOT/'build/m13-native/font73-manifest.json');assert font['coverage_bytes']==251248 and font['header_sha256']==read(ROOT/'third_party/inter/raster-lock12.json')['header_sha256']
 for n in [*profiles,*['windows-'+n for n in windows],'desktop-native','chrome-native','vmware-results','desktop-host','motion']:copy_case(work/n,out/n,out/'diagnostics')
 shutil.copyfile(work/'host-results.json',out/'host-results.json');shutil.copyfile(work/'ordinary/desktop.png',out/'feature.png')
 write(out/'resources.json',dict(passed=True,fixed_desktop=current,baseline_fixed_desktop=previous,fixed_desktop_delta_bytes=current['bytes']-previous['bytes'],fixed_installer=setup,baseline_fixed_installer=previous_setup,font=font,profiles={n:r['resources'] for n,r in profiles.items()},window_profiles={n:r['resources'] for n,r in windows.items()},cached_move_profiles=motion['profiles'],scope='Fixed state, font masks, framebuffer bytes and managed current/peak/retained pages are separate. Wallpaper uses existing damage and no new framebuffer, cache, worker or timer. Motion latency targets remain M13.9.'))
 accepted=dict(passed=True,stage='M13.5',version='0.13.5',qualification='M13-STAGE5-VM-v1',build_id=meta['build_id'],iso_sha256=iso,vmware_zip_sha256=starter['sha256'],source_inputs_verified=len(meta['source_sha256']),native_checks=[c for r in [*profiles.values(),*windows.values(),desktop,chrome] for c in r['checks']]+['Twelve actual cached versus full native viewport pixel comparisons pass across ordinary, 150% and physical 4K scenes; no motion FPS claim'],vmware_checks=vm['checks'],harness_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in [*(ROOT/'tests/m13').glob('*.py'),*(ROOT/'tests/m13').glob('*.mjs'),*(ROOT/'tests/m13').glob('*.c')]},resources='resources.json',reference_window_profiles=list(windows),limits=['Exact SATA/UEFI VMware starter and named QEMU display/window tasks; the older fourteen-controller qualification does not qualify these bytes','Original failed keyboard-snap candidate and earlier harness attempts remain excluded diagnostics','Motion frame/latency targets remain separately measured in M13.9','Universal/physical hardware, Secure Boot signing, vendor GPU 3D and general Windows compatibility remain outside this stage','Agent review is separate from a human novice study','Public release and website closure remain separate gates'])
 write(out/'acceptance-results.json',accepted);print('PASS: M13.5 exact native desktop, six window profiles, glyph pixels and enabled-device VMware startup')
if __name__=='__main__':main()
