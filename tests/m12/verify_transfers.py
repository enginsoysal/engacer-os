"""Qualify matching M12.7 command/transfer behavior, source and released media."""
import hashlib,json,re,shutil,os
from pathlib import Path
import verify_components as common
ROOT=common.ROOT;WORK=ROOT/'build/m12/stage7';OUT=ROOT/'evidence/M12/7'
load=common.load;sha=common.sha;write=common.write

def fat_state(path):
    text=path.read_text();parts={}
    for section in ('bss','data'):
        values=re.findall(r'^\s*[0-9a-f]+\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+.*kernel_storage_fat32-kernel.o:\(\.'+section+r'\)$',text,re.M)
        assert len(values)<=1;parts[section]=int(values[0],16) if values else 0
    return dict(bytes=sum(parts.values()),sections=parts,map_sha256=sha(path))

def main():
    assert not (OUT/'publication-results.json').exists()
    meta=load(ROOT/'dist/m12stage7-build-manifest.json');starter=load(ROOT/'dist/m12stage7-starter-manifest.json')
    native=load(WORK/'transfers-native/results.json');bios=load(WORK/'bios/results.json');vmware=load(WORK/'vmware-results/results.json');motion=load(WORK/'motion/results.json');syntax=load(WORK/'syntax-results.json')
    assert all(row['passed'] for row in (native,bios,vmware,motion,syntax))
    assert len(syntax['checks'])==4
    for path,digest in syntax['source_sha256'].items():assert meta['source_sha256'][path]==digest
    iso=meta['artifacts']['EngacerOS-M12STAGE7.iso']['sha256']
    assert meta['release_version']=='0.12.7' and meta['qualification_scope']=='M12-STAGE7-VM-v1'
    for row in (native,bios,vmware,motion,starter):assert row['build_id']==meta['build_id']
    for row in (native,bios,vmware,motion):assert row['iso_sha256']==iso
    assert vmware['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive'])
    assert vmware['existing_vm_inventory_unchanged'] and len(vmware['checks'])==len(bios['checks'])==3
    assert len(native['checks'])>=12 and len(native['profiles'])==2
    assert 0<native['cancelled_usb_work_bytes']<128*1024**2 and native['partial_copy_confirmed_files']>=1
    assert native['removed_source_error'] in (3,9)
    assert native['resources']['retained_pages']==0
    assert native['resources']['before'][0]==native['resources']['after'][0]
    assert native['resources']['before'][3]==native['resources']['after'][3]
    os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE7'
    import files_observe as observed
    fixture=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage7-transfers'/native['owned_fixture']/'owned.img'
    assert observed.ui.s.s.document(fixture,'/Users/Owner/Documents/Welcome.txt')==(ROOT/'distros/packages/m12-desktop-guide/content.txt').read_bytes()
    assert observed.ui.s.s.document(fixture,'/Users/Owner/Desktop/Source/Export.txt')==b'Native original 123'
    try:observed.ui.s.s.document(fixture,'/Users/Owner/Desktop/Source/Large.bin',limit=64*1024**2)
    except AssertionError as error:assert str(error).startswith('Expected persistent file not found:')
    else:raise AssertionError('The cancelled partial tree published its unfinished file')
    for profile in motion['profiles']:
        assert len(profile['comparisons'])==4 and all(v['cached_equals_full_viewport'] for v in profile['comparisons'])
        assert profile['managed_bytes_before']==profile['managed_bytes_after']
        assert profile['all_cpus_halted_when_idle'] and profile['idle_paints_unchanged'] and profile['cached_copy_frames']>0
    assert len(motion['profiles'])==3
    for group,names in [('transfers-native',['install','disk-1','disk-2']),('bios',['install','disk-only-1','disk-only-2']),('vmware-results',['install','disk-only-1','disk-only-2'])]:
        for name in names:assert 'M7_DESKTOP_READY build='+meta['build_id'] in (WORK/group/(name+'.log')).read_text(encoding='utf-8')
    for label,width,height in [('compact-actions',1280,800),('commands-150',1920,1200),('commands-4k',3840,2160)]:
        capture=load(WORK/f'transfers-native/{label}-capture.json');assert (capture['width'],capture['height'])==(width,height)
    for label in ('usb-transfer-progress','native-transfer-progress','conflict-review','usb-conflict','removed-source-result','usb-export-refusal','compact-dark-actions'):
        assert (WORK/f'transfers-native/{label}.png').is_file()
    common.git_inputs(meta['source_sha256']);common.git_inputs(syntax['source_sha256'])
    for folder in ('boot','kernel','include','runtime','user'):
        assert {p.relative_to(ROOT).as_posix() for p in (ROOT/folder).rglob('*') if p.is_file()}<=meta['source_sha256'].keys()
    for name,record in meta['artifacts'].items():assert sha(ROOT/'dist'/name)==record['sha256']
    assert meta['font']==load(ROOT/'evidence/M12/6/candidate-manifest.json')['font']
    previous=load(ROOT/'evidence/M12/6/resources.json')['current'];current=common.desktop_state(ROOT/'dist/EngacerOS-M12STAGE7-installed-kernel.map')
    fat_before=fat_state(ROOT/'dist/EngacerOS-M12STAGE6-installed-kernel.map');fat_after=fat_state(ROOT/'dist/EngacerOS-M12STAGE7-installed-kernel.map')
    baseline=load(ROOT/'evidence/M11/6/resources.json')['fixed_desktop']['FINAL'];assert current['bytes']-baseline['bytes']+fat_after['bytes']-fat_before['bytes']<256*1024
    for stage in range(1,7):
        for name,row in load(ROOT/f'evidence/M12/{stage}/candidate-manifest.json')['artifacts'].items():assert sha(ROOT/'dist'/name)==row['sha256']
        oldstarter=load(ROOT/f'evidence/M12/{stage}/starter-manifest.json');assert sha(ROOT/'dist'/oldstarter['archive'])==oldstarter['sha256']
    for row in load(ROOT/'evidence/M12/0/preserved-baseline.json')['artifacts']:assert sha(ROOT/'dist'/row['name'])==row['sha256']
    OUT.mkdir(parents=True,exist_ok=True)
    for source,name in [('transfers-native','native'),('bios','bios'),('vmware-results','vmware'),('motion','motion')]:
        target=OUT/name;target.mkdir(exist_ok=True)
        for path in (WORK/source).iterdir():
            if path.is_file() and path.suffix in ('.json','.png','.log') and path.name!='failure.log':
                if path.suffix=='.png':shutil.copyfile(path,target/path.name)
                else:(target/path.name).write_bytes(path.read_bytes().replace(str(ROOT).encode(),b'<project-root>'))
    for source,name in [('dist/m12stage7-build-manifest.json','candidate-manifest.json'),('dist/m12stage7-starter-manifest.json','starter-manifest.json'),('build/m12/stage7/syntax-results.json','syntax-results.json')]:shutil.copyfile(ROOT/source,OUT/name)
    shutil.copyfile(WORK/'transfers-native/usb-transfer-progress.png',OUT/'feature.png')
    diagnostics=OUT/'diagnostics';diagnostics.mkdir(exist_ok=True)
    for path in (WORK/'diagnostics').iterdir():
        if path.is_file() and path.suffix in ('.json','.txt','.png'):(diagnostics/path.name).write_bytes(path.read_bytes().replace(str(ROOT).encode(),b'<project-root>'))
    write(OUT/'resources.json',dict(passed=True,previous=previous,current=current,added_fixed_desktop_bytes=current['bytes']-previous['bytes'],fat32_before=fat_before,fat32_current=fat_after,added_fixed_fat32_bytes=fat_after['bytes']-fat_before['bytes'],managed=native['resources'],font=meta['font'],icon_raster_cache_bytes=0,icon_temporary_row_bytes=512,display_profiles=native['profiles'],motion=motion['profiles'],scope='Fixed shell and FAT32 cooperative reader state are measured separately from managed framebuffer pages. No additional data buffer, growing queue, per-window framebuffer or idle animation. Configured guest RAM is not consumption.'))
    harness={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tests/m12').iterdir() if p.suffix in ('.py','.c')}
    write(OUT/'acceptance-results.json',dict(passed=True,stage='M12.7',version='0.12.7',qualification='M12-STAGE7-VM-v1',build_id=meta['build_id'],iso_sha256=iso,vmware_zip_sha256=starter['sha256'],source_inputs_verified=len(meta['source_sha256']),artifacts_verified=len(meta['artifacts'])+1,native_checks=native['checks'],cached_full_comparisons=12,bios_checks=bios['checks'],vmware_checks=vmware['checks'],resources='resources.json',feature_provenance='Actual owned QEMU SATA/UEFI installed 1280x800 guest, usb-transfer-progress.png; real source/destination and bounded verified USB import',feature_sha256=sha(OUT/'feature.png'),harness_sha256=harness,limits=['USB imports are cooperative, one-file and bounded to 64 MiB; USB export remains synchronous create-only and cannot be cancelled mid-file.','USB folder import, Cut/Move, replacing USB files and sorting remain unavailable.','The menu helper footer fitting remains M12.14; HiDPI drawn cursor versus hit coordinate isolation remains M12.16.','The earlier M12.2 concurrent BIOS/AHCI timeout remains open; stress reliability is not qualified.','Final controller/device/original-application regression remains M12.18; physical/ARM, vendor GPU 3D and universal Windows compatibility remain unqualified.','Agent visual/scenario review is not a human study; public release/site/download proof closes separately.']))
    print('PASS: matching M12.7 source/media, genuine transfer/cancellation/conflict bytes, independent boots and bounded resources.')

if __name__=='__main__':main()
