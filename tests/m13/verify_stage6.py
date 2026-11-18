"""Bind exact M13.6 native app-launch, grouped taskbar and provider journeys."""
import hashlib,json,shutil,subprocess
from close_stage import verify_inputs_at_commit
import verify_stage2 as base
ROOT=base.ROOT;rules=base.rules;read=base.read;write=base.write;sha=base.sha

def copy_case(source,dest,build_id):
 dest.mkdir(parents=True,exist_ok=True)
 for p in source.iterdir():
  if not p.is_file() or p.suffix not in ('.json','.png','.log'):continue
  if 'failure' in p.name or p.name.startswith('initial-') or p.name=='task-phase-original.json':continue
  if source.name.startswith('start-') and p.name.startswith('start-dark'):
   target=ROOT/'evidence/M13/6/diagnostics'/(source.name+'-cancelled-dark-preview'+p.name[len('start-dark'):]);shutil.copyfile(p,target);continue
  if p.name.endswith('-capture.json'):
   capture=read(p);assert capture.get('build_id',build_id)==build_id,(p,capture)
  if p.suffix=='.png':shutil.copyfile(p,dest/p.name)
  else:(dest/p.name).write_bytes(p.read_bytes().replace(str(ROOT).encode(),b'<project-root>'))

def main():
 out=ROOT/'evidence/M13/6';assert not (out/'publication-results.json').exists();work=ROOT/'build/m13/stage6';meta=read(ROOT/'dist/m13stage6-build-manifest.json');starter=read(ROOT/'dist/m13stage6-starter-manifest.json');iso=meta['artifacts']['EngacerOS-M13STAGE6.iso']['sha256']
 profiles={n:read(work/n/'results.json') for n in ('ordinary','compact','1024','150','4k')};starts={n:read(work/('start-'+n)/'results.json') for n in profiles};themes={n:read(work/('themes-'+n)/'results.json') for n in profiles};tasks={n:read(work/n/'results.json') for n in ('taskbar-native','tray-native','alignment','vmware-results')}
 assert meta['release_version']=='0.13.6' and meta['qualification_scope']=='M13-STAGE6-VM-v1'
 for r in [*profiles.values(),*starts.values(),*themes.values(),*tasks.values()]:assert r['passed'] and r['build_id']==meta['build_id'] and r['iso_sha256']==iso
 for n,r in profiles.items():assert r['resources']['retained_task_delta_pages']==0 and starts[n]['resources']['retained_pages']==0 and len(starts[n]['pinned_tiles'])==6 and all(t[3]==88 for t in starts[n]['pinned_tiles'])
 assert all(tasks[n]['resources']['retained_pages']==0 for n in ('taskbar-native','tray-native','alignment'))
 taskbar=tasks['taskbar-native'];continuation=taskbar['continuation'];original=read(out/'diagnostics/initial-taskbar-order.json')
 phase_ref=verify_inputs_at_commit(continuation['native_task_phase_source'],meta['source_sha256'])
 phase_harness=subprocess.check_output(['git','show',phase_ref+':tests/m13/taskbar_native6.py'],cwd=ROOT)
 assert hashlib.sha256(phase_harness).hexdigest()==original['harness_sha256']
 assert not original['observation']['passed'] and original['observation']['build_id']==meta['build_id'] and len(original['observation']['checks'])==6
 assert len(continuation['boot_checks'])==2 and all(r['pins']==[1,7,2,4,8,9,14,16] and r['minimize_restore'] and r['sha256']==taskbar['preferences_sha256'] for r in continuation['boot_checks'])
 for n in profiles:
  for frame in ('pinned','folder-result','restart-review','start-light','start-high-contrast'):
   capture=read(work/('start-'+n)/(frame+'-capture.json'));assert (capture['width'],capture['height'])==tuple(starts[n]['physical']),(n,frame,capture)
 for n,r in themes.items():
  assert r['resources']['retained_pages']==0 and [t['theme'] for t in r['themes']]==['dark','high-contrast','light']
  assert [t['dark'] for t in r['themes']]==[1,1,0] and [t['high_contrast'] for t in r['themes']]==[False,True,False]
  assert all(t['after_settings_close'] for t in r['themes'])
  for frame in ('dark','high-contrast','light'):
   capture=read(work/('themes-'+n)/(frame+'-capture.json'));assert (capture['width'],capture['height'])==tuple(r['physical'])
 vm=tasks['vmware-results'];assert vm['existing_vm_inventory_unchanged'] and vm['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive']) and starter['passed']
 rules.git_inputs(meta['source_sha256'])
 for n,r in meta['artifacts'].items():assert sha(ROOT/'dist'/n)==r['sha256']
 old=read(ROOT/'evidence/M13/5/acceptance-results.json');assert sha(ROOT/'dist/EngacerOS-M13STAGE5.iso')==old['iso_sha256'] and sha(ROOT/'dist/EngacerOS-M13STAGE5-VMware.zip')==old['vmware_zip_sha256']
 current=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE6-installed-kernel.map');previous=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE5-installed-kernel.map');assert current['bytes']<=previous['bytes']+1024
 setup=base.fixed_setup(ROOT/'dist/EngacerOS-M13STAGE6-kernel.map');previous_setup=base.fixed_setup(ROOT/'dist/EngacerOS-M13STAGE5-kernel.map');assert setup['bytes']==previous_setup['bytes']
 font=read(ROOT/'build/m13-native/font73-manifest.json');assert font['coverage_bytes']==251248 and font['header_sha256']==read(ROOT/'third_party/inter/raster-lock12.json')['header_sha256'];assert read(work/'host-results.json')['passed']
 out.mkdir(parents=True,exist_ok=True)
 for n in [*profiles,*['start-'+n for n in starts],*['themes-'+n for n in themes],*tasks]:copy_case(work/n,out/n,meta['build_id'])
 shutil.copyfile(work/'start-ordinary/pinned.png',out/'feature.png');shutil.copyfile(work/'host-results.json',out/'host-results.json')
 write(out/'resources.json',dict(passed=True,fixed_desktop=current,baseline_fixed_desktop=previous,fixed_desktop_delta_bytes=current['bytes']-previous['bytes'],fixed_installer=setup,baseline_fixed_installer=previous_setup,font=font,profiles={n:r['resources'] for n,r in profiles.items()},start_profiles={n:r['resources'] for n,r in starts.items()},applied_theme_profiles={n:r['resources'] for n,r in themes.items()},alignment=tasks['alignment']['resources'],taskbar=tasks['taskbar-native']['resources'],tray=tasks['tray-native']['resources'],scope='Fixed state, immutable font masks, framebuffer/configured guest RAM and managed peak/current/retained pages are separate; no indexing worker or per-keystroke process. Motion targets remain M13.9.'))
 accepted=dict(passed=True,stage='M13.6',version='0.13.6',qualification='M13-STAGE6-VM-v1',build_id=meta['build_id'],iso_sha256=iso,vmware_zip_sha256=starter['sha256'],source_inputs_verified=len(meta['source_sha256']),native_checks=[c for r in [*profiles.values(),*starts.values(),tasks['taskbar-native'],tasks['tray-native'],tasks['alignment'],*themes.values()] for c in r['checks'] if not c.startswith('Real light/dark/high-contrast Start frames')],vmware_checks=vm['checks'],harness_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in [*(ROOT/'tests/m13').glob('*.py'),*(ROOT/'tests/m13').glob('*.mjs'),*(ROOT/'tests/m13').glob('*.c')]},resources='resources.json',theme_qualification='Original dark-labelled captures were cancelled previews, retained in diagnostics. Five fresh applied-theme tasks verify actual Dark/HC/Light surfaces and independent saved values after closing Settings.',limits=['Named Start/taskbar/tray display profiles and exact SATA/UEFI VMware starter, not the older fourteen-controller media or final M13.12 integration','No Wi-Fi/Bluetooth/battery provider, universal physical hardware, vendor GPU 3D or general Windows compatibility claim','Motion feedback targets remain M13.9; agent scenario/visual review is separate from a human novice study','Public delivery remains a separate gate'])
 write(out/'acceptance-results.json',accepted);print('PASS M13.6 exact Start, grouped taskbar, provider tray and independent VMware startup')
if __name__=='__main__':main()
