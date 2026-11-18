"""Bind exact M13.11 personalization/feature tasks; stability is M13.13."""
import re
import verify_stage2 as base
ROOT=base.ROOT;read=base.read;write=base.write;sha=base.sha;rules=base.rules


def input_state(path):
    text=path.read_text(encoding='utf-8');values=re.findall(r'^\s*[0-9a-f]+\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+.*kernel_input_layout10-kernel.o:\(\.bss\)$',text,re.M)
    assert len(values)==1
    return int(values[0],16)


def main():
    out=ROOT/'evidence/M13/11';out.mkdir(parents=True,exist_ok=True);assert not (out/'publication-results.json').exists()
    work=ROOT/'build/m13/stage11';meta=read(ROOT/'dist/m13stage11-build-manifest.json');starter=read(ROOT/'dist/m13stage11-starter-manifest.json');iso=meta['artifacts']['EngacerOS-M13STAGE11.iso']['sha256']
    names=('ordinary','compact','1024','150','4k');profiles={n:read(work/n/'results.json') for n in names};personal={n:read(work/('personalization-'+n)/'results.json') for n in names}
    labels=('screensaver-native','screensaver-invalid','settings-native','apps-ordinary','settings-write-failure','search-ordinary');tasks={n:read(work/n/'results.json') for n in labels};vm=read(work/'vmware-results/results.json')
    reports=[*profiles.values(),*personal.values(),*tasks.values(),vm]
    for r in reports:assert r['passed'] and r['build_id']==meta['build_id'] and r['iso_sha256']==iso
    for name in names:
        r=profiles[name];expected={'ordinary':(1920,1080,2),'compact':(1280,800,2),'1024':(1024,768,2),'150':(1920,1200,3),'4k':(3840,2160,4)}[name]
        assert tuple(r['physical'])==expected[:2] and r['scale_units']==expected[2] and r['resources']['retained_task_delta_pages']==0
        p=personal[name];assert p['themes']==['light','dark','high-contrast'] and len(p['checks'])==3 and p['resources']['retained_pages']==0
        for capture in (work/('personalization-'+name)).glob('*-capture.json'):
            image=read(capture);assert (image['width'],image['height'])==expected[:2]
        for theme in p['themes']:
            assert sha(work/('personalization-'+name)/(theme+'-reduced-motion-before.png'))==sha(work/('personalization-'+name)/(theme+'-reduced-motion.png'))
    for name,task in tasks.items():
        if 'resources' in task:assert task['resources']['retained_pages']==0
        else:assert name=='screensaver-invalid'  # Independent stopped-image semantic cases; no within-session retention claim.
    saver=tasks['screensaver-native'];assert len(saver['checks'])==7 and 58<=saver['actual_idle_feature_seconds']<=70
    assert {43101,43102,43103}<=set(saver['restored_window_controls']) and saver['saved_record_hex']=='4553323101000000000000005802000002000000'
    invalid=tasks['screensaver-invalid'];assert {c['name'] for c in invalid['cases']}=={'magic','version','enabled','timeout','style','short','long'}
    assert all(c['valid_filesystem_banks']>=1 and c['replacement_hex']=='4553323101000000000000003c00000000000000' for c in invalid['cases'])
    assert len(tasks['settings-native']['checks'])==6 and len(tasks['search-ordinary']['checks'])==7
    apps=tasks['apps-ordinary'];assert len(apps['frames'])==57 and {x['app'] for x in apps['frames']}==set(range(1,20)) and {x['theme'] for x in apps['frames']}=={'light','dark','high-contrast'}
    failure=tasks['settings-write-failure'];assert failure['injected_fault']['once'] and 'Cancel changes' in failure['message'] and len(failure['message'].encode('ascii'))<96 and len(failure['checks'])==2
    assert vm['existing_vm_inventory_unchanged'] and len(vm['checks'])==4 and vm['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive'])
    rules.git_inputs(meta['source_sha256'])
    for name,r in meta['artifacts'].items():assert sha(ROOT/'dist'/name)==r['sha256']
    previous=read(ROOT/'evidence/M13/10/acceptance-results.json');assert sha(ROOT/'dist/EngacerOS-M13STAGE10.iso')==previous['iso_sha256'] and sha(ROOT/'dist/EngacerOS-M13STAGE10-VMware.zip')==previous['vmware_zip_sha256']
    current=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE11-installed-kernel.map');older=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE10-installed-kernel.map');desktop_delta=current['bytes']-older['bytes'];assert 0<=desktop_delta<=256
    input_current=input_state(ROOT/'dist/EngacerOS-M13STAGE11-installed-kernel.map');input_old=input_state(ROOT/'dist/EngacerOS-M13STAGE10-installed-kernel.map');assert 0<=input_current-input_old<=128
    setup=base.fixed_setup(ROOT/'dist/EngacerOS-M13STAGE11-kernel.map');assert setup['bytes']==base.fixed_setup(ROOT/'dist/EngacerOS-M13STAGE10-kernel.map')['bytes']
    font=read(ROOT/'build/m13-native/font73-manifest.json');assert font['coverage_bytes']==251248 and font['header_sha256']==read(ROOT/'third_party/inter/raster-lock12.json')['header_sha256']
    write(out/'resources.json',dict(passed=True,fixed_desktop=current,previous_fixed=older,fixed_delta_bytes=desktop_delta,input_module_bss_bytes=input_current,previous_input_module_bss_bytes=input_old,input_module_delta_bytes=input_current-input_old,fixed_installer=setup,font=font,profiles={n:r['resources'] for n,r in profiles.items()},personalization_profiles={n:r['resources'] for n,r in personal.items()},tasks={n:r['resources'] for n,r in tasks.items() if 'resources' in r},scope='Fixed desktop and physical-input module state include linker alignment. Native code, framebuffer/shadow buffers and managed peak/retained pages are separate; guest configured RAM is not OS consumption. No added framebuffer, heap cache, worker or idle polling loop.'))
    for label in [*names,*['personalization-'+n for n in names],*labels,'vmware-results']:
        dest=out/'native'/label;dest.mkdir(parents=True,exist_ok=True)
        for path in (work/label).iterdir():
            if path.suffix not in ('.json','.png','.log') or path.name=='failure.log':continue
            data=path.read_bytes()
            if path.suffix!='.png':data=data.replace(str(ROOT).encode(),b'<project-root>')
            (dest/path.name).write_bytes(data)
    accepted=dict(passed=True,stage='M13.11',version='0.13.11',qualification='M13-STAGE11-VM-v1',build_id=meta['build_id'],iso_sha256=iso,vmware_zip_sha256=starter['sha256'],source_inputs_verified=len(meta['source_sha256']),native_checks=[c for r in reports[:-1] for c in r['checks']],vmware_checks=vm['checks'],app_frame_count=57,resources='resources.json',harness_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in [*(ROOT/'tests/m13').glob('*.py'),*(ROOT/'tests/m13').glob('*.mjs'),*(ROOT/'tests/m13').glob('*.c')]},limits=['One-minute real idle activation, preview/wake and controlled error tasks qualify feature behavior, not stability; all natural-freeze, duration and reset-chain work is exclusively M13.13','All five display profiles and three themes cover shared controls and personalization; nineteen app frames cover three themes at ordinary size, not every app/theme/scale combination','Screensaver is an optional Off-by-default Settings feature, not a standalone removable app or new distribution schema field','Whole-product/controller/original-MSI integration remains M13.12; no universal hardware, vendor GPU 3D or general Windows compatibility claim','Agent visual review is not a human novice study; matching public release/site closure is separate'])
    write(out/'acceptance-results.json',accepted);print('PASS exact M13.11 personalization, physical input wake, preferences, resources and VMware functional qualification')


if __name__=='__main__':main()
