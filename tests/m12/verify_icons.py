"""Qualify matching M12.2 native icon, source, media and resource evidence."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import verify_components as common

ROOT=common.ROOT;WORK=ROOT/'build/m12/stage2';OUT=ROOT/'evidence/M12/2'
load=common.load;sha=common.sha;write=common.write

def artwork():
    spec=importlib.util.spec_from_file_location('m122_original_icons',ROOT/'tools/design/icons12.py')
    generator=importlib.util.module_from_spec(spec);spec.loader.exec_module(generator)
    isolated=WORK/'generation-check';(isolated/'include/engine/ui').mkdir(parents=True,exist_ok=True)
    generator.ROOT=isolated;generator.main()
    paths=[Path('include/engine/ui/icons12_data.h'),*[p.relative_to(isolated) for p in (isolated/'docs/architecture/figures/m12-icons').iterdir()]]
    for path in paths:assert sha(ROOT/path)==sha(isolated/path),path
    return dict(passed=True,original_icons=len(generator.ICONS),generated_files=len(paths),shared_geometry_bytes=sum(len(s) for _,s in generator.ICONS)*7,offset_bytes=(len(generator.ICONS)+1)*2,palette_bytes=2*len(generator.PALETTES[0])*4,sha256={p.as_posix():sha(ROOT/p) for p in paths})

def main():
    meta=load(ROOT/'dist/m12stage2-build-manifest.json');starter=load(ROOT/'dist/m12stage2-starter-manifest.json')
    native=load(WORK/'icons-native/results.json');files=load(WORK/'icons-files/results.json')
    bios=load(WORK/'bios/results.json');vmware=load(WORK/'vmware-results/results.json');motion=load(WORK/'motion/results.json');host=load(WORK/'host-results.json')
    assert all(p['passed'] for p in (starter,native,files,bios,vmware,motion,host))
    assert meta['release_version']=='0.12.2' and meta['qualification_scope']=='M12-STAGE2-VM-v1'
    iso=meta['artifacts']['EngacerOS-M12STAGE2.iso']['sha256']
    for report in (starter,native,files,bios,vmware,motion):assert report['build_id']==meta['build_id']
    for report in (native,files,bios,vmware,motion):assert report['iso_sha256']==iso
    assert vmware['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive'])
    assert vmware['existing_vm_inventory_unchanged'] and len(vmware['checks'])==3 and len(bios['checks'])==3
    assert len(native['profiles'])==6 and len(native['checks'])==5
    assert [(p['scale'],p['dark']) for p in native['profiles']]==[(2,0),(2,1),(3,0),(3,1),(4,0),(4,1)]
    for profile in native['profiles']:
        assert {a['app'] for a in profile['apps']}==set(range(1,20))
        assert all(a['max_channel_difference']<=1 for a in profile['apps'])
        assert profile['no_application_launch'] and profile['retained_pages']==0
        assert profile['managed_before_bytes']==profile['managed_after_bytes']
    assert len(files['comparisons'])==12 and len(files['checks'])==3
    assert all(row['max_channel_difference']<=1 for row in files['comparisons'])
    assert len(motion['profiles'])==3
    for profile in motion['profiles']:
        assert len(profile['comparisons'])==4 and all(p['cached_equals_full_viewport'] for p in profile['comparisons'])
        assert profile['managed_bytes_before']==profile['managed_bytes_after']
        assert profile['all_cpus_halted_when_idle'] and profile['idle_paints_unchanged'] and profile['cached_copy_frames']>0
    for name,width,height in [('installed-desktop',1280,800),('native-150',1920,1200),('native-4k',3840,2160)]:
        capture=load(WORK/f'icons-native/{name}-capture.json');assert (capture['width'],capture['height'])==(width,height)
    assert host['icons']==57 and host['temporary_row_bytes']==512 and host['raster_cache_bytes']==0
    common.git_inputs(meta['source_sha256']);common.git_inputs(host['source_sha256'])
    for folder in ('boot','kernel','include','runtime','user'):
        assert {p.relative_to(ROOT).as_posix() for p in (ROOT/folder).rglob('*') if p.is_file()}<=meta['source_sha256'].keys()
    for name,row in meta['artifacts'].items():assert sha(ROOT/'dist'/name)==row['sha256']
    reference=load(ROOT/'evidence/M12/1/resources.json')['current'];current=common.desktop_state(ROOT/'dist/EngacerOS-M12STAGE2-installed-kernel.map')
    assert current['bytes']==reference['bytes']==544164
    font=load(ROOT/'build/m12/font73-manifest.json');assert font['coverage_bytes']==251248
    text=(ROOT/'dist/EngacerOS-M12STAGE2-installed-kernel.map').read_text()
    symbols={}
    for name,size in [('icon12_offsets',116),('icon12_shapes',2191),('icon12_palettes',136)]:
        matches=re.findall(r'^\s*[0-9a-f]+\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+'+name+r'$',text,re.M)
        assert len(matches)==1 and int(matches[0],16)==size;symbols[name]=size
    telemetry=[]
    for name,size in [('icon12_draws',8),('icon12_pixels',8),('icon12_fallbacks',8),('icon12_max_physical',4)]:
        matches=re.findall(r'^\s*([0-9a-f]+)\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+'+name+r'$',text,re.M)
        assert len(matches)==1 and int(matches[0][1],16)==size
        telemetry.append((int(matches[0][0],16),size))
    telemetry_span=max(a+s for a,s in telemetry)-min(a for a,s in telemetry)
    for row in load(ROOT/'evidence/M12/0/preserved-baseline.json')['artifacts']:assert sha(ROOT/'dist'/row['name'])==row['sha256']
    original=load(ROOT/'evidence/M12/1/candidate-manifest.json')
    for name,row in original['artifacts'].items():assert sha(ROOT/'dist'/name)==row['sha256']
    assert sha(ROOT/'dist/EngacerOS-M12STAGE1-VMware.zip')==load(ROOT/'evidence/M12/1/starter-manifest.json')['sha256']
    generated=artwork();OUT.mkdir(parents=True,exist_ok=True)
    for source,dest in [('icons-native','native'),('icons-files','files'),('bios','bios'),('vmware-results','vmware'),('motion','motion')]:common.copy_report(WORK/source,OUT/dest)
    for name in ('light','dark'):shutil.copyfile(WORK/f'icons-{name}.png',OUT/f'host-icons-{name}.png')
    shutil.copyfile(WORK/'icons-native/ordinary-light-all-apps-0.png',OUT/'feature.png')
    for source,dest in [('dist/m12stage2-build-manifest.json','candidate-manifest.json'),('dist/m12stage2-starter-manifest.json','starter-manifest.json'),('build/m12/stage2/host-results.json','host-results.json')]:shutil.copyfile(ROOT/source,OUT/dest)
    diagnostics=OUT/'diagnostics';diagnostics.mkdir(exist_ok=True)
    for file in (WORK/'diagnostics').iterdir():
        if file.is_file() and file.suffix in ('.json','.txt'):(diagnostics/file.name).write_bytes(file.read_bytes().replace(str(ROOT).encode(),b'<project-root>'))
    write(OUT/'artwork-results.json',generated)
    write(OUT/'resources.json',dict(passed=True,scope='Fixed desktop state, shared icon art, transient row and managed framebuffers are distinct; configured RAM is not consumption',previous=reference,current=current,added_fixed_desktop_bytes=0,icon_read_only_symbols=symbols,icon_read_only_total_bytes=sum(symbols.values()),icon_telemetry_payload_bytes=sum(s for a,s in telemetry),icon_telemetry_storage_span_bytes=telemetry_span,temporary_row_bytes=512,raster_cache_bytes=0,managed=native['profiles'],motion=motion['profiles'],font_coverage_bytes=251248))
    harness={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tests/m12').iterdir() if p.suffix in ('.py','.c')}
    write(OUT/'acceptance-results.json',dict(passed=True,stage='M12.2',version='0.12.2',qualification='M12-STAGE2-VM-v1',build_id=meta['build_id'],iso_sha256=iso,vmware_zip_sha256=starter['sha256'],source_inputs_verified=len(meta['source_sha256']),artifacts_verified=len(meta['artifacts'])+1,original_icons=57,native_app_comparisons=114,native_file_usb_comparisons=12,cached_full_comparisons=12,native_checks=native['checks'],file_checks=files['checks'],bios_checks=bios['checks'],vmware_checks=vmware['checks'],resources='resources.json',artwork='artwork-results.json',feature_provenance='Actual owned QEMU SATA/UEFI installed guest at 1280x800; ordinary-light-all-apps-0.png',feature_sha256=sha(OUT/'feature.png'),harness_sha256=harness,limits=['An earlier M12.2 candidate had an initial concurrent BIOS AHCI timeout; its fresh repeat passed. The corrected palette candidate has separate matching evidence. Trigger is not isolated and stress reliability is not qualified; original failed evidence is retained.','Full controller/device/original-application regression remains M12.18; physical/ARM, vendor GPU 3D and universal Windows compatibility remain unqualified.','Agent visual/scenario review, not a human usability study. Public release, website and download proof are separate gates.']))
    print('PASS: matching M12.2 source/media; 114 native app, 12 file/USB and 12 cached/full comparisons; bounded shared art, rows and resources.')

if __name__=='__main__':main()
