"""Qualify matching M12.5 Files behavior, resources, sources and media."""
import hashlib,json,shutil
from pathlib import Path
import verify_components as common
ROOT=common.ROOT;WORK=ROOT/'build/m12/stage5';OUT=ROOT/'evidence/M12/5'
load=common.load;sha=common.sha;write=common.write

def main():
    assert not (OUT/'publication-results.json').exists()
    meta=load(ROOT/'dist/m12stage5-build-manifest.json');starter=load(ROOT/'dist/m12stage5-starter-manifest.json')
    native=load(WORK/'files-native/results.json');host=load(WORK/'history-host/results.json');compact=load(WORK/'files-compact/results.json')
    bios=load(WORK/'bios/results.json');vmware=load(WORK/'vmware-results/results.json');motion=load(WORK/'motion/results.json')
    assert all(r['passed'] for r in (native,host,compact,bios,vmware,motion))
    iso=meta['artifacts']['EngacerOS-M12STAGE5.iso']['sha256']
    assert meta['release_version']=='0.12.5' and meta['qualification_scope']=='M12-STAGE5-VM-v1'
    for report in (native,compact,bios,vmware,motion,starter):assert report['build_id']==meta['build_id']
    for report in (native,compact,bios,vmware,motion):assert report['iso_sha256']==iso
    assert vmware['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive'])
    assert vmware['existing_vm_inventory_unchanged'] and len(vmware['checks'])==len(bios['checks'])==3
    assert len(native['checks'])>=10 and len(native['profiles'])==2
    assert host['history_slots_per_window']==8 and host['allocations']==0
    assert compact['bounds'][2:]==[500,420] and compact['retained_pages']==0
    assert native['resources']['retained_pages']==0
    assert native['resources']['before'][0]==native['resources']['after'][0]
    assert native['resources']['before'][3]==native['resources']['after'][3]
    for profile in motion['profiles']:
        assert len(profile['comparisons'])==4 and all(v['cached_equals_full_viewport'] for v in profile['comparisons'])
        assert profile['managed_bytes_before']==profile['managed_bytes_after']
        assert profile['all_cpus_halted_when_idle'] and profile['idle_paints_unchanged'] and profile['cached_copy_frames']>0
    assert len(motion['profiles'])==3
    for group,names in [('files-native',['install','disk-1','disk-2']),('bios',['install','disk-only-1','disk-only-2']),('vmware-results',['install','disk-only-1','disk-only-2'])]:
        for name in names:assert 'M7_DESKTOP_READY build='+meta['build_id'] in (WORK/group/(name+'.log')).read_text(encoding='utf-8')
    for label,width,height in [('usb-folder-common-frame',1280,800),('native-150',1920,1200),('native-4k',3840,2160)]:
        capture=load(WORK/f'files-native/{label}-capture.json');assert (capture['width'],capture['height'])==(width,height)
    common.git_inputs(meta['source_sha256']);common.git_inputs(host['source_sha256'])
    for folder in ('boot','kernel','include','runtime','user'):
        assert {p.relative_to(ROOT).as_posix() for p in (ROOT/folder).rglob('*') if p.is_file()}<=meta['source_sha256'].keys()
    for name,record in meta['artifacts'].items():assert sha(ROOT/'dist'/name)==record['sha256']
    assert meta['font']==load(ROOT/'evidence/M12/4/candidate-manifest.json')['font']
    previous=load(ROOT/'evidence/M12/4/resources.json')['current'];current=common.desktop_state(ROOT/'dist/EngacerOS-M12STAGE5-installed-kernel.map')
    baseline=load(ROOT/'evidence/M11/6/resources.json')['fixed_desktop']['FINAL']
    assert current['bytes']-baseline['bytes']<256*1024
    for stage in (1,2,3,4):
        old=load(ROOT/f'evidence/M12/{stage}/candidate-manifest.json')
        for name,row in old['artifacts'].items():assert sha(ROOT/'dist'/name)==row['sha256']
        oldstarter=load(ROOT/f'evidence/M12/{stage}/starter-manifest.json')
        assert sha(ROOT/'dist'/oldstarter['archive'])==oldstarter['sha256']
    for row in load(ROOT/'evidence/M12/0/preserved-baseline.json')['artifacts']:assert sha(ROOT/'dist'/row['name'])==row['sha256']
    OUT.mkdir(parents=True,exist_ok=True)
    for source,name in [('files-native','native'),('files-compact','compact'),('bios','bios'),('vmware-results','vmware'),('motion','motion')]:
        target=OUT/name;target.mkdir(exist_ok=True)
        for path in (WORK/source).iterdir():
            if path.is_file() and path.suffix in ('.json','.png','.log') and not path.name.startswith('prototype-'):
                if path.suffix=='.png':shutil.copyfile(path,target/path.name)
                else:(target/path.name).write_bytes(path.read_bytes().replace(str(ROOT).encode(),b'<project-root>'))
    for source,name in [('dist/m12stage5-build-manifest.json','candidate-manifest.json'),('dist/m12stage5-starter-manifest.json','starter-manifest.json'),('build/m12/stage5/history-host/results.json','host-results.json')]:shutil.copyfile(ROOT/source,OUT/name)
    shutil.copyfile(WORK/'files-native/usb-folder-common-frame.png',OUT/'feature.png')
    diagnostics=OUT/'diagnostics';diagnostics.mkdir(exist_ok=True)
    (WORK/'diagnostics').mkdir(exist_ok=True)
    for path in (WORK/'diagnostics').iterdir():
        if path.is_file() and path.suffix in ('.json','.txt','.png'):
            (diagnostics/path.name).write_bytes(path.read_bytes().replace(str(ROOT).encode(),b'<project-root>'))
    write(OUT/'resources.json',dict(passed=True,previous=previous,current=current,added_fixed_desktop_bytes=current['bytes']-previous['bytes'],managed=native['resources'],font=meta['font'],icon_raster_cache_bytes=0,icon_temporary_row_bytes=512,display_profiles=native['profiles'],motion=motion['profiles'],scope='Fixed shell state and managed framebuffer pages are separate. No new icon cache, per-window framebuffer, idle animation or heap allocation is introduced by common Files rendering. Configured VM RAM is not consumption.'))
    harness={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tests/m12').iterdir() if p.suffix in ('.py','.c')}
    write(OUT/'acceptance-results.json',dict(passed=True,stage='M12.5',version='0.12.5',qualification='M12-STAGE5-VM-v1',build_id=meta['build_id'],iso_sha256=iso,vmware_zip_sha256=starter['sha256'],source_inputs_verified=len(meta['source_sha256']),artifacts_verified=len(meta['artifacts'])+1,native_checks=native['checks'],cached_full_comparisons=12,bios_checks=bios['checks'],vmware_checks=vmware['checks'],resources='resources.json',feature_provenance='Actual owned QEMU SATA/UEFI installed 1280x800 guest, usb-folder-common-frame.png; original native Inter/vector rendering',feature_sha256=sha(OUT/'feature.png'),harness_sha256=harness,limits=['The shared window-menu helper footer fitting is carried to M12.14.','The drawn cursor versus hit coordinates after HiDPI changes requires explicit M12.16 isolation; scripted caption clicks alone do not qualify pointer usability.','The earlier M12.2 concurrent BIOS/AHCI timeout remains open; stress reliability is not qualified.','File presentation, commands and shared dialogs continue in later stages; USB FAT32 one-file/create-only limits and existing name/window quotas remain real.','Final controller/device/original-application regression remains M12.18; physical/ARM, vendor GPU 3D and universal Windows compatibility remain unqualified.','Agent visual/scenario review is not a human usability study. Public release/site/download proof closes separately.']))
    print('PASS: matching M12.5 Files source/media, native provider/history/detach journeys and 12 cached/full comparisons, independent boots and bounded resources.')

if __name__=='__main__':main()
