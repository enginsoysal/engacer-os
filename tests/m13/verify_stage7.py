"""Bind M13.7 exact Files/filter/provider tasks and enabled-device VMware media."""
import json,shutil
import verify_stage2 as base
ROOT=base.ROOT;rules=base.rules;read=base.read;write=base.write;sha=base.sha

def main():
 out=ROOT/'evidence/M13/7';assert not (out/'publication-results.json').exists();work=ROOT/'build/m13/stage7';meta=read(ROOT/'dist/m13stage7-build-manifest.json');starter=read(ROOT/'dist/m13stage7-starter-manifest.json');iso=meta['artifacts']['EngacerOS-M13STAGE7.iso']['sha256']
 profiles={n:read(work/n/'results.json') for n in ('ordinary','compact','1024','150','4k')};files={n:read(work/('files-'+n)/'results.json') for n in profiles};usb=read(work/'usb-native/results.json');transfers=read(work/'transfers-native/results.json');vm=read(work/'vmware-results/results.json')
 assert meta['release_version']=='0.13.7' and meta['qualification_scope']=='M13-STAGE7-VM-v1'
 for r in [*profiles.values(),*files.values(),usb,transfers,vm]:assert r['passed'] and r['build_id']==meta['build_id'] and r['iso_sha256']==iso
 for n,r in profiles.items():
  assert r['resources']['retained_task_delta_pages']==0 and files[n]['resources']['retained_pages']==0 and len(files[n]['checks'])>=6
  for frame in ('common-frame','filtered-names','no-matching-names','disk-only-1','disk-only-2','dark','high-contrast','light','filtered-icons'):
   capture=read(work/('files-'+n)/(frame+'-capture.json'));assert (capture['width'],capture['height'])==tuple(files[n]['physical'])
 assert usb['resources']['retained_pages']==0 and len(usb['checks'])>=8 and len(usb['profiles'])==2
 assert transfers['resources']['retained_pages']==0 and len(transfers['checks'])>=14 and transfers['refresh_keeps_active_progress_geometry']
 assert vm['existing_vm_inventory_unchanged'] and vm['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive']) and starter['passed']
 rules.git_inputs(meta['source_sha256'])
 for n,r in meta['artifacts'].items():assert sha(ROOT/'dist'/n)==r['sha256']
 previous=read(ROOT/'evidence/M13/6/acceptance-results.json');assert sha(ROOT/'dist/EngacerOS-M13STAGE6.iso')==previous['iso_sha256'] and sha(ROOT/'dist/EngacerOS-M13STAGE6-VMware.zip')==previous['vmware_zip_sha256']
 current=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE7-installed-kernel.map');old=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE6-installed-kernel.map');assert current['bytes']<=old['bytes']+768
 setup=base.fixed_setup(ROOT/'dist/EngacerOS-M13STAGE7-kernel.map');old_setup=base.fixed_setup(ROOT/'dist/EngacerOS-M13STAGE6-kernel.map');assert setup['bytes']==old_setup['bytes']
 font=read(ROOT/'build/m13-native/font73-manifest.json');assert font['coverage_bytes']==251248 and font['header_sha256']==read(ROOT/'third_party/inter/raster-lock12.json')['header_sha256'];assert read(work/'host-results.json')['passed']
 out.mkdir(parents=True,exist_ok=True)
 for name in [*profiles,*['files-'+n for n in files],'usb-native','transfers-native','vmware-results']:
  dest=out/name;dest.mkdir(parents=True,exist_ok=True)
  for p in (work/name).iterdir():
   if p.is_file() and p.suffix in ('.json','.png','.log') and not any(mark in p.name for mark in ('failure','unavailable-item')):
    if p.suffix=='.png':shutil.copyfile(p,dest/p.name)
    else:(dest/p.name).write_bytes(p.read_bytes().replace(str(ROOT).encode(),b'<project-root>'))
 shutil.copyfile(work/'files-ordinary/common-frame.png',out/'feature.png');shutil.copyfile(work/'host-results.json',out/'host-results.json')
 write(out/'resources.json',dict(passed=True,fixed_desktop=current,baseline_fixed_desktop=old,fixed_desktop_delta_bytes=current['bytes']-old['bytes'],fixed_installer=setup,font=font,profiles={n:r['resources'] for n,r in profiles.items()},files_profiles={n:r['resources'] for n,r in files.items()},usb=usb['resources'],transfers=transfers['resources'],scope='Fixed bounded query state, unchanged fonts/installer, configured RAM/framebuffer and managed task current/peak/retained pages remain separate. No index worker, heap cache or per-keystroke process.'))
 write(out/'acceptance-results.json',dict(passed=True,stage='M13.7',version='0.13.7',qualification='M13-STAGE7-VM-v1',build_id=meta['build_id'],iso_sha256=iso,vmware_zip_sha256=starter['sha256'],source_inputs_verified=len(meta['source_sha256']),native_checks=[c for r in [*profiles.values(),*files.values(),usb,transfers] for c in r['checks']],vmware_checks=vm['checks'],harness_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in [*(ROOT/'tests/m13').glob('*.py'),*(ROOT/'tests/m13').glob('*.mjs'),*(ROOT/'tests/m13').glob('*.c')]},resources='resources.json',limits=['Current native system-folder ASCII name substring filter, not recursive/content or USB filtering','Named Files/display/provider tasks and exact SATA/UEFI starter, not a fresh fourteen-controller or final M13.12 integration matrix','No general Windows, vendor GPU 3D or universal physical-device compatibility claim','Agent visual/scenario review is not a human novice study; native latency targets remain M13.9','Public release and full website closure remain separate gates']))
 print('PASS M13.7 exact Files/filter/provider tasks, source and VMware media')
if __name__=='__main__':main()
