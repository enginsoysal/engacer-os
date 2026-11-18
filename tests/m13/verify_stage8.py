"""Bind exact M13.8 Settings/search/feedback tasks, resources and VMware media."""
import shutil
import verify_stage2 as base
ROOT=base.ROOT;rules=base.rules;read=base.read;write=base.write;sha=base.sha


def main():
    out=ROOT/'evidence/M13/8';assert not (out/'publication-results.json').exists()
    work=ROOT/'build/m13/stage8';meta=read(ROOT/'dist/m13stage8-build-manifest.json');starter=read(ROOT/'dist/m13stage8-starter-manifest.json');iso=meta['artifacts']['EngacerOS-M13STAGE8.iso']['sha256']
    names=('ordinary','compact','1024','150','4k')
    profiles={n:read(work/n/'results.json') for n in names}
    searches={n:read(work/('search-'+n)/'results.json') for n in names}
    tasks={n:read(work/n/'results.json') for n in ('settings-native','settings-invalid','feedback-native')}
    vm=read(work/'vmware-results/results.json')
    assert meta['release_version']=='0.13.8' and meta['qualification_scope']=='M13-STAGE8-VM-v1'
    for r in [*profiles.values(),*searches.values(),*tasks.values(),vm]:
        assert r['passed'] and r['build_id']==meta['build_id'] and r['iso_sha256']==iso
    for n in names:
        r=searches[n];assert len(r['checks'])>=7 and r['resources']['retained_pages']==0
        assert profiles[n]['resources']['retained_task_delta_pages']==0
        assert r['host_observer']['mutable_guest_state_cached'] is False
        for frame in ('settings-common-frame','search-scale','search-dark-mode','search-apps','minimum-settings','minimum-search-results','applied-dark','applied-light','high-contrast-search','caption-safe-feedback','disk-only-1','disk-only-2'):
            capture=read(work/('search-'+n)/(frame+'-capture.json'))
            assert (capture['width'],capture['height'])==tuple(r['physical'])
    for name in ('settings-native','feedback-native'):assert tasks[name]['resources']['retained_pages']==0 and len(tasks[name]['checks'])>=6
    assert tasks['settings-invalid']['malformed_records'] and tasks['settings-invalid']['checks']
    assert vm['existing_vm_inventory_unchanged'] and vm['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive']) and starter['passed']
    rules.git_inputs(meta['source_sha256'])
    for n,r in meta['artifacts'].items():assert sha(ROOT/'dist'/n)==r['sha256']
    previous=read(ROOT/'evidence/M13/7/acceptance-results.json')
    assert sha(ROOT/'dist/EngacerOS-M13STAGE7.iso')==previous['iso_sha256'] and sha(ROOT/'dist/EngacerOS-M13STAGE7-VMware.zip')==previous['vmware_zip_sha256']
    current=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE8-installed-kernel.map');old=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE7-installed-kernel.map');assert current['bytes']-old['bytes']==704
    setup=base.fixed_setup(ROOT/'dist/EngacerOS-M13STAGE8-kernel.map');assert setup['bytes']==base.fixed_setup(ROOT/'dist/EngacerOS-M13STAGE7-kernel.map')['bytes']
    font=read(ROOT/'build/m13-native/font73-manifest.json');assert font['coverage_bytes']==251248 and font['header_sha256']==read(ROOT/'third_party/inter/raster-lock12.json')['header_sha256'];assert read(work/'host-results.json')['passed']
    out.mkdir(parents=True,exist_ok=True)
    for name in [*names,*['search-'+n for n in names],*tasks,'vmware-results']:
        dest=out/name;dest.mkdir(parents=True,exist_ok=True)
        for p in (work/name).iterdir():
            if p.is_file() and p.suffix in ('.json','.png','.log') and not any(mark in p.name for mark in ('failure','unavailable-item')):
                if p.suffix=='.png':shutil.copyfile(p,dest/p.name)
                else:(dest/p.name).write_bytes(p.read_bytes().replace(str(ROOT).encode(),b'<project-root>'))
    shutil.copyfile(work/'search-ordinary/settings-common-frame.png',out/'feature.png');shutil.copyfile(work/'host-results.json',out/'host-results.json')
    write(out/'resources.json',dict(passed=True,fixed_desktop=current,baseline_fixed_desktop=old,fixed_desktop_delta_bytes=704,fixed_installer=setup,font=font,profiles={n:r['resources'] for n,r in profiles.items()},search_profiles={n:r['resources'] for n,r in searches.items()},tasks={n:r.get('resources') for n,r in tasks.items()},scope='Eight bounded transient category-query records. Immutable symbol-map caching belongs only to the host observer; every mutable guest value is freshly read. Configured RAM, framebuffer, fixed state and managed peak/retained pages remain separate. No native FPS or latency claim.'))
    write(out/'acceptance-results.json',dict(passed=True,stage='M13.8',version='0.13.8',qualification='M13-STAGE8-VM-v1',build_id=meta['build_id'],iso_sha256=iso,vmware_zip_sha256=starter['sha256'],source_inputs_verified=len(meta['source_sha256']),native_checks=[c for r in [*profiles.values(),*searches.values(),*tasks.values()] for c in r['checks']],vmware_checks=vm['checks'],harness_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in [*(ROOT/'tests/m13').glob('*.py'),*(ROOT/'tests/m13').glob('*.mjs'),*(ROOT/'tests/m13').glob('*.c')]},resources='resources.json',limits=['Bounded ASCII search over supported Settings category names, descriptions and declared aliases; not arbitrary system/content search','Named Settings/display/feedback tasks and exact SATA/UEFI starter, not a fresh fourteen-controller or final M13.12 whole-product matrix','Crowded message placement protects the focused caption if no all-caption-free ordinary corner exists','No general Windows, GPU 3D or universal physical-device compatibility claim','Agent visual/scenario review is not a human novice study; actual feedback/frame timing belongs to M13.9','Matching release and full public website closure remain separate gates']))
    print('PASS M13.8 exact Settings/search/feedback tasks, source, resources and VMware media')


if __name__=='__main__':main()
