"""Qualify exact M12.18 keyboard, semantics, display, ownership and persistence."""
import json,os,shutil
from PIL import Image
import verify_components as common
ROOT=common.ROOT;WORK=ROOT/'build/m12/stage18';OUT=ROOT/'evidence/M12/18'
load=common.load;sha=common.sha;write=common.write

def public(data):
    for path,label in ((str(ROOT),'<project-root>'),(os.environ.get('USERPROFILE',''),'<user-home>')):
        if path:
            for spelling in (path,path.replace('\\','/')):
                for variant in (spelling,json.dumps(spelling)[1:-1]):data=data.replace(variant.encode(),label.encode())
    return data

def main():
    assert not (OUT/'publication-results.json').exists()
    meta=load(ROOT/'dist/m12stage18-build-manifest.json');starter=load(ROOT/'dist/m12stage18-starter-manifest.json');groups=['setup-profiles','setup-native-ordinary','setup-native-compact','settings-native','settings-invalid','feedback-native','feedback-busy','desktop-native','files-native','presentation-native','transfers-native','dialogs-native','start-native','taskbar-native','multitask-native','restore-native','tray-native','tray-network','tray-optional','setup-safety','setup-minimal','usb-negative','usb-quota','bios-stress','website-observations','access-native','access-profiles','access-ownership','access-invalid','access-effects','access-firstuse','access-host','access-guards','performance-native','performance-interrupt','raster-host','bios','matrix-summary','motion','taskbar-host','pack-host','recovery'];reports={name:load(WORK/name/'results.json') for name in groups};native=reports['access-native'];profiles=reports['access-profiles'];iso=meta['artifacts']['EngacerOS-M12STAGE18.iso']['sha256']
    assert meta['release_version']=='0.12.18' and meta['qualification_scope']=='M12-STAGE18-VM-v1'
    for name,row in reports.items():
        assert row['passed'],name
        if name not in ('website-observations','taskbar-host','pack-host','access-host','access-guards','raster-host'):assert row['build_id']==meta['build_id'],name
        if 'iso_sha256' in row:assert row['iso_sha256']==iso,name
        if 'resources' in row:
            r=row['resources'];assert r['retained_pages']==0 and r['after'][0]<=r['before'][0] and r['before'][3]==r['after'][3],name
    assert len(reports['bios-stress']['cases'])==12 and reports['bios-stress']['concurrent_guests']==4
    assert len(reports['matrix-summary']['profiles'])==14
    harness=sha(ROOT/'tests/m12/final_vmware18.py')
    assert all(p['harness_sha256']==harness for p in reports['matrix-summary']['profiles'])
    assert len(reports['matrix-summary']['original_payload_sha256'])==106
    hardware=[]
    for label in ('uefi','bios','low-memory','4k-hub','large-usb'):
        row=load(WORK/'hardware'/label/'results.json');assert row['passed'] and row['build_id']==meta['build_id'] and row['iso_sha256']==iso
        assert len(row['checks'])>=6 and row['resources']['retained_pages']==0;hardware.append(row)
    known=load(WORK/'known-uefi64-boot-usb/results.json');assert known['build_id']==meta['build_id'] and known['iso_sha256']==iso and known['expected_behavior_verified'] and not known['qualified'] and known['expected_refusal_recorded'] and not known['passed']
    assert len(reports['setup-profiles']['profiles'])==3
    assert len(native['checks'])>=3
    assert 'M7_DESKTOP_READY build='+meta['build_id'] in (WORK/'access-native/native.log').read_text(encoding='utf-8')
    assert [p['name'] for p in profiles['profiles']]==['compact-light','compact-dark','compact-150','150','4k']
    assert [p['scale'] for p in profiles['profiles']]==[2,2,3,3,4]
    for row in profiles['profiles']:
        assert 'M7_DESKTOP_READY build='+meta['build_id'] in (WORK/'access-profiles'/(row['name']+'.log')).read_text(encoding='utf-8')
        for kind in ('appearance','display','input','system','accessibility'):
            with Image.open(WORK/'access-profiles'/f'{kind}-{row["name"]}.png') as image:assert list(image.size)==row['physical']
        assert row['retained_pages']==0
    assert len(reports['access-invalid']['cases'])==6 and len(reports['access-ownership']['checks'])>=2
    assert [p['flags'] for p in reports['access-effects']['profiles']]==[0,2,1,3]
    assert len(reports['access-firstuse']['checks'])>=1 and len(reports['access-guards']['checks'])==6
    assert native['preferences_sha256']=='72aaf3b4c9b2f0025562312690afb073cfbef51edf64fb8a8ade0912fc673b34'
    assert native['accessibility_record_hex']=='55413136010000000300000000000000'
    assert reports['raster-host']['pixel_cases']==3073 and reports['raster-host']['current_visits']*5<reports['raster-host']['baseline_visits'] and reports['raster-host']['guard_bytes_unchanged']
    assert reports['performance-native']['accessibility_record_hex']=='55413136010000000000000000000000'
    assert [p['scale'] for p in reports['performance-interrupt']['profiles']]==[2,3,4] and all(p['viewport_pixels_restored'] and p['retained_pages']==0 for p in reports['performance-interrupt']['profiles'])
    assert len(reports['bios']['checks'])==3 and len(reports['matrix-summary']['profiles'])==14
    assert all(p['existing_vm_inventory_unchanged'] for p in reports['matrix-summary']['profiles']) and reports['matrix-summary']['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive'])
    assert len(reports['motion']['profiles'])==3 and sum(len(p['comparisons']) for p in reports['motion']['profiles'])==12 and len(reports['recovery']['checks'])==2
    assert reports['taskbar-host']['checks']>290000 and reports['pack-host']['roundtrip_pages']>500 and reports['pack-host']['malformed_and_fuzz_cases']>10000 and reports['pack-host']['guard_bytes_unchanged']
    for name in ('taskbar-host','pack-host','access-host','access-guards','raster-host'):
        for path,digest in reports[name]['source_sha256'].items():assert sha(ROOT/path)==digest
    for path,digest in reports['pack-host']['payload_sha256'].items():assert sha(ROOT/path)==digest
    syntax=load(WORK/'syntax-results.json');assert syntax['passed'] and len(syntax['checks'])==8
    for path,digest in syntax['source_sha256'].items():assert meta['source_sha256'][path]==digest
    common.git_inputs(meta['source_sha256'])
    for name,row in meta['artifacts'].items():assert sha(ROOT/'dist'/name)==row['sha256']
    previous=load(ROOT/'evidence/M12/17/resources.json')['current'];current=common.desktop_state(ROOT/'dist/EngacerOS-M12STAGE18-installed-kernel.map');baseline=load(ROOT/'evidence/M11/6/resources.json')['fixed_desktop']['FINAL'];assert current['bytes']-baseline['bytes']<256*1024 and current['bytes']==previous['bytes'] and meta['font']==load(ROOT/'evidence/M12/17/candidate-manifest.json')['font']
    for stage in range(1,18):
        for name,row in load(ROOT/f'evidence/M12/{stage}/candidate-manifest.json')['artifacts'].items():assert sha(ROOT/'dist'/name)==row['sha256']
        old=load(ROOT/f'evidence/M12/{stage}/starter-manifest.json');assert sha(ROOT/'dist'/old['archive'])==old['sha256']
    OUT.mkdir(parents=True,exist_ok=True)
    for group in groups:
        target=OUT/group;target.mkdir(exist_ok=True)
        for path in (WORK/group).rglob('*'):
            if path.is_file() and path.suffix in ('.json','.png','.log'):
                dest=target/path.relative_to(WORK/group);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(path.read_bytes() if path.suffix=='.png' else public(path.read_bytes()))
    for group in ('hardware','known-uefi64-boot-usb','matrix-results'):
        for path in (WORK/group).rglob('*'):
            if path.is_file() and path.suffix in ('.json','.png','.log'):
                dest=OUT/group/path.relative_to(WORK/group);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(path.read_bytes() if path.suffix=='.png' else public(path.read_bytes()))
    diagnostics=OUT/'diagnostics';diagnostics.mkdir(exist_ok=True)
    for path in (WORK/'diagnostics').rglob('*'):
        if path.is_file() and path.suffix in ('.json','.png'):
            target=diagnostics/path.relative_to(WORK/'diagnostics');target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(path.read_bytes() if path.suffix=='.png' else public(path.read_bytes()))
    for source,name in [('dist/m12stage18-build-manifest.json','candidate-manifest.json'),('dist/m12stage18-starter-manifest.json','starter-manifest.json'),('build/m12/stage18/syntax-results.json','syntax-results.json')]:shutil.copyfile(ROOT/source,OUT/name)
    shutil.copyfile(WORK/'files-native/native-4k.png',OUT/'feature.png');write(OUT/'resources.json',dict(passed=True,previous=previous,current=current,added_fixed_desktop_bytes=current['bytes']-previous['bytes'],managed=native['resources'],display_profiles=profiles['profiles'],font=meta['font'],raster=reports['raster-host'],interrupted_motion=reports['performance-interrupt']['profiles'],scope='Final high-contrast boundaries reuse existing state and the prior raster span optimization is retained. Native default-effect motion and interrupted moves are separately measured. No new worker, framebuffer cache or idle scanner. Fixed bytes, peak and completed retention are separate.'))
    host_groups={'taskbar-host','pack-host','access-host','access-guards','raster-host','website-observations'}
    checks=sum((row.get('checks',[]) for name,row in reports.items() if name not in host_groups and isinstance(row.get('checks'),list)),[])
    checks += [profile['profile']+': '+check for profile in hardware for check in profile['checks']]
    write(OUT/'acceptance-results.json',dict(passed=True,stage='M12.18',version='0.12.18',qualification='M12-STAGE18-VM-v1',build_id=meta['build_id'],iso_sha256=iso,vmware_zip_sha256=starter['sha256'],source_inputs_verified=len(meta['source_sha256']),artifacts_verified=len(meta['artifacts'])+1,native_checks=checks,bios_checks=reports['bios']['checks'],vmware_checks=reports['matrix-summary']['checks'],cached_full_comparisons=12,resources='resources.json',feature_provenance='Actual native physical 3840x2160/200% Files window browsing the real owned USB Games folder after installation, not a browser mockup',feature_sha256=sha(OUT/'feature.png'),harness_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tests/m12').iterdir() if p.suffix in ('.py','.c')},limits=['Named VM profiles only; no universal hardware, GPU 3D or expanded foreign Windows compatibility.','Setup review is automated scenario verification, not a participant usability study.','Named controller/original-app/device/display/desktop profiles are qualified separately. External screen reader/speech, universal physical devices and GPU 3D are not claimed; the 64-MiB boot-attached USB topology remains explicitly recorded by its final outcome.','Public release and complete website verification close separately.']))
    print('PASS: matching M12.18 final native controller, device, desktop, accessibility, source/media and bounded-resource qualification')

if __name__=='__main__':main()
