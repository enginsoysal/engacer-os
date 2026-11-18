"""Bind exact M13.10 secondary-surface tasks; stability remains M13.13."""
import shutil
import verify_stage2 as base
ROOT=base.ROOT;read=base.read;write=base.write;sha=base.sha;rules=base.rules


def main():
    out=ROOT/'evidence/M13/10';out.mkdir(parents=True,exist_ok=True)
    assert not (out/'publication-results.json').exists()
    work=ROOT/'build/m13/stage10'
    meta=read(ROOT/'dist/m13stage10-build-manifest.json');starter=read(ROOT/'dist/m13stage10-starter-manifest.json')
    iso=meta['artifacts']['EngacerOS-M13STAGE10.iso']['sha256']
    names=('ordinary','compact','1024','150','4k')
    profiles={name:read(work/name/'results.json') for name in names}
    search={name:read(work/('search-'+name)/'results.json') for name in names}
    cursors={name:read(work/('cursors-'+name)/'results.json') for name in names}
    secondary={name:read(work/('secondary-'+name)/'results.json') for name in names}
    apps={name:read(work/('apps-'+name)/'results.json') for name in names}
    tasks={name:read(work/name/'results.json') for name in ('dialogs-native','settings-native','feedback-native','transfers-native','settings-write-failure')}
    vm=read(work/'vmware-results/results.json')
    reports=[*profiles.values(),*search.values(),*cursors.values(),*secondary.values(),*apps.values(),*tasks.values(),vm]
    for report in reports:
        assert report['passed'] and report['build_id']==meta['build_id'] and report['iso_sha256']==iso
    for name in names:
        assert profiles[name]['resources']['retained_task_delta_pages']==0
        for rows in (search,cursors,secondary,apps):assert rows[name]['resources']['retained_pages']==0
        assert len(search[name]['checks'])>=7 and len(cursors[name]['observations'])==10
        assert len(secondary[name]['themes'])==3 and len(secondary[name]['independent_file_sha256'])==3
        expected=57 if name=='ordinary' else 19
        assert len(apps[name]['frames'])==expected
        assert {frame['app'] for frame in apps[name]['frames']}==set(range(1,20))
        assert {frame['theme'] for frame in apps[name]['frames']}==({'light','dark','high-contrast'} if name=='ordinary' else {'light'})
        for label in ('search-'+name,'secondary-'+name,'apps-'+name):
            for capture in (work/label).glob('*-capture.json'):
                image=read(capture);assert [image['width'],image['height']]==profiles[name]['physical']
    assert len(tasks['dialogs-native']['checks'])==12 and not tasks['dialogs-native']['development_only']
    for name,task in tasks.items():
        assert task['resources']['retained_pages']==0,name
    failure=tasks['settings-write-failure'];assert len(failure['message'].encode('ascii'))<96 and 'Cancel preview' in failure['message']
    assert len(failure['checks'])==1 and failure['injected_fault']['once']
    assert len(tasks['settings-native']['checks'])>=6 and len(tasks['feedback-native']['checks'])>=6
    assert tasks['transfers-native']['checks'] and tasks['transfers-native']['profiles']
    assert vm['existing_vm_inventory_unchanged'] and vm['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive'])
    previous=read(ROOT/'evidence/M13/9/acceptance-results.json')
    assert sha(ROOT/'dist/EngacerOS-M13STAGE9.iso')==previous['iso_sha256']
    assert sha(ROOT/'dist/EngacerOS-M13STAGE9-VMware.zip')==previous['vmware_zip_sha256']
    rules.git_inputs(meta['source_sha256'])
    for name,record in meta['artifacts'].items():assert sha(ROOT/'dist'/name)==record['sha256']
    current=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE10-installed-kernel.map')
    older=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE9-installed-kernel.map')
    assert current['bytes']==older['bytes']
    setup=base.fixed_setup(ROOT/'dist/EngacerOS-M13STAGE10-kernel.map')
    assert setup['bytes']==base.fixed_setup(ROOT/'dist/EngacerOS-M13STAGE9-kernel.map')['bytes']
    font=read(ROOT/'build/m13-native/font73-manifest.json')
    assert font['coverage_bytes']==251248 and font['header_sha256']==read(ROOT/'third_party/inter/raster-lock12.json')['header_sha256']
    write(out/'resources.json',dict(passed=True,fixed_desktop=current,previous_fixed=older,fixed_delta_bytes=0,
          fixed_installer=setup,font=font,profiles={name:report['resources'] for name,report in profiles.items()},
          app_profiles={name:report['resources'] for name,report in apps.items()},
          task_resources={name:report['resources'] for name,report in tasks.items()},
          scope='No additional fixed desktop state, bitmap, framebuffer, cache, timer or idle worker. Managed peak and retained allocations are separate from configured guest RAM, native code and framebuffer bytes.'))
    labels=[*names,*['search-'+n for n in names],*['cursors-'+n for n in names],
            *['secondary-'+n for n in names],*['apps-'+n for n in names],*tasks,'vmware-results']
    for label in labels:
        dest=out/'native'/label;dest.mkdir(parents=True,exist_ok=True)
        for path in (work/label).iterdir():
            if path.suffix not in ('.json','.png','.log') or path.name=='failure.log':continue
            data=path.read_bytes()
            if path.suffix!='.png':data=data.replace(str(ROOT).encode(),b'<project-root>')
            (dest/path.name).write_bytes(data)
    accepted=dict(passed=True,stage='M13.10',version='0.13.10',qualification='M13-STAGE10-VM-v1',
        build_id=meta['build_id'],iso_sha256=iso,vmware_zip_sha256=starter['sha256'],
        source_inputs_verified=len(meta['source_sha256']),
        native_checks=[check for report in reports[:-1] for check in report['checks']],vmware_checks=vm['checks'],
        app_frame_count=sum(len(report['frames']) for report in apps.values()),
        resources='resources.json',harness_sha256={path.relative_to(ROOT).as_posix():sha(path) for path in
          [*(ROOT/'tests/m13').glob('*.py'),*(ROOT/'tests/m13').glob('*.mjs'),*(ROOT/'tests/m13').glob('*.c')]},
        limits=['Scoped secondary-surface, supported app-frame and functional startup qualification; stability investigation and duration/reset-chain tests are exclusively M13.13',
                'All nineteen app windows in Light at five profiles; all nineteen also in Dark/High contrast at ordinary size; shared controls/dialogs independently cover all themes at every profile',
                'Controlled injected write refusal is a functional recovery-message test, not natural-freeze or stability evidence',
                'No new motion/FPS qualification; historical M13.9 processing measurements do not certify physical scanout of these media',
                'Exact enabled-device SATA/UEFI starter and named QEMU profiles; final whole-product controller/application integration remains M13.12',
                'No universal hardware, vendor GPU 3D, general Windows compatibility or human novice-study claim',
                'Matching public release, manuals and actual website closure remain separate gates'])
    write(out/'acceptance-results.json',accepted)
    print('PASS exact M13.10 secondary surfaces, app frames, error recovery, resources and VMware tasks; stability remains M13.13')


if __name__=='__main__':main()
