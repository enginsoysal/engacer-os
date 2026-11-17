"""Qualify exact M12.17 keyboard, semantics, display, ownership and persistence."""
import json,os,shutil
from PIL import Image
import verify_components as common
ROOT=common.ROOT;WORK=ROOT/'build/m12/stage17';OUT=ROOT/'evidence/M12/17'
load=common.load;sha=common.sha;write=common.write

def public(data):
    for path,label in ((str(ROOT),'<project-root>'),(os.environ.get('USERPROFILE',''),'<user-home>')):
        if path:
            for spelling in (path,path.replace('\\','/')):
                for variant in (spelling,json.dumps(spelling)[1:-1]):data=data.replace(variant.encode(),label.encode())
    return data

def main():
    assert not (OUT/'publication-results.json').exists()
    meta=load(ROOT/'dist/m12stage17-build-manifest.json');starter=load(ROOT/'dist/m12stage17-starter-manifest.json');groups=['access-native','access-profiles','access-ownership','access-invalid','access-effects','access-firstuse','access-host','access-guards','performance-native','performance-interrupt','raster-host','bios','vmware-results','motion','taskbar-host','pack-host','recovery'];reports={name:load(WORK/name/'results.json') for name in groups};native=reports['access-native'];profiles=reports['access-profiles'];iso=meta['artifacts']['EngacerOS-M12STAGE17.iso']['sha256']
    assert meta['release_version']=='0.12.17' and meta['qualification_scope']=='M12-STAGE17-VM-v1'
    for name,row in reports.items():
        assert row['passed'],name
        if name not in ('taskbar-host','pack-host','access-host','access-guards','raster-host'):assert row['build_id']==meta['build_id'],name
        if 'iso_sha256' in row:assert row['iso_sha256']==iso,name
        if 'resources' in row:
            r=row['resources'];assert r['retained_pages']==0 and r['after'][0]<=r['before'][0] and r['before'][3]==r['after'][3],name
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
    assert len(reports['bios']['checks'])==len(reports['vmware-results']['checks'])==3
    assert reports['vmware-results']['existing_vm_inventory_unchanged'] and reports['vmware-results']['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive'])
    assert len(reports['motion']['profiles'])==3 and sum(len(p['comparisons']) for p in reports['motion']['profiles'])==12 and len(reports['recovery']['checks'])==2
    assert reports['taskbar-host']['checks']>290000 and reports['pack-host']['roundtrip_pages']>500 and reports['pack-host']['malformed_and_fuzz_cases']>10000 and reports['pack-host']['guard_bytes_unchanged']
    for name in ('taskbar-host','pack-host','access-host','access-guards','raster-host'):
        for path,digest in reports[name]['source_sha256'].items():assert sha(ROOT/path)==digest
    for path,digest in reports['pack-host']['payload_sha256'].items():assert sha(ROOT/path)==digest
    syntax=load(WORK/'syntax-results.json');assert syntax['passed'] and len(syntax['checks'])==8
    for path,digest in syntax['source_sha256'].items():assert meta['source_sha256'][path]==digest
    common.git_inputs(meta['source_sha256'])
    for name,row in meta['artifacts'].items():assert sha(ROOT/'dist'/name)==row['sha256']
    previous=load(ROOT/'evidence/M12/16/resources.json')['current'];current=common.desktop_state(ROOT/'dist/EngacerOS-M12STAGE17-installed-kernel.map');baseline=load(ROOT/'evidence/M11/6/resources.json')['fixed_desktop']['FINAL'];assert current['bytes']-baseline['bytes']<256*1024 and 0<=current['bytes']-previous['bytes']<=256 and meta['font']==load(ROOT/'evidence/M12/16/candidate-manifest.json')['font']
    for stage in range(1,17):
        for name,row in load(ROOT/f'evidence/M12/{stage}/candidate-manifest.json')['artifacts'].items():assert sha(ROOT/'dist'/name)==row['sha256']
        old=load(ROOT/f'evidence/M12/{stage}/starter-manifest.json');assert sha(ROOT/'dist'/old['archive'])==old['sha256']
    OUT.mkdir(parents=True,exist_ok=True)
    for group in groups:
        target=OUT/group;target.mkdir(exist_ok=True)
        for path in (WORK/group).iterdir():
            if path.is_file() and path.suffix in ('.json','.png','.log'):(target/path.name).write_bytes(path.read_bytes() if path.suffix=='.png' else public(path.read_bytes()))
    diagnostics=OUT/'diagnostics';diagnostics.mkdir(exist_ok=True)
    for path in (WORK/'diagnostics').rglob('*'):
        if path.is_file() and path.suffix in ('.json','.png'):
            target=diagnostics/path.relative_to(WORK/'diagnostics');target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(path.read_bytes() if path.suffix=='.png' else public(path.read_bytes()))
    for source,name in [('dist/m12stage17-build-manifest.json','candidate-manifest.json'),('dist/m12stage17-starter-manifest.json','starter-manifest.json'),('build/m12/stage17/syntax-results.json','syntax-results.json')]:shutil.copyfile(ROOT/source,OUT/name)
    shutil.copyfile(WORK/'performance-interrupt/cancelled-4k.png',OUT/'feature.png');write(OUT/'resources.json',dict(passed=True,previous=previous,current=current,added_fixed_desktop_bytes=current['bytes']-previous['bytes'],managed=native['resources'],display_profiles=profiles['profiles'],font=meta['font'],raster=reports['raster-host'],interrupted_motion=reports['performance-interrupt']['profiles'],scope='The optimization adds one local span counter and zero fixed state; native default-effect motion and interrupted moves are separately measured. No new worker, framebuffer cache or idle scanner. Fixed bytes, peak and completed retention are separate.'))
    checks=sum((reports[name]['checks'] for name in ('access-native','access-profiles','access-ownership','access-invalid','access-effects','access-firstuse','performance-native','performance-interrupt')),[])
    write(OUT/'acceptance-results.json',dict(passed=True,stage='M12.17',version='0.12.17',qualification='M12-STAGE17-VM-v1',build_id=meta['build_id'],iso_sha256=iso,vmware_zip_sha256=starter['sha256'],source_inputs_verified=len(meta['source_sha256']),artifacts_verified=len(meta['artifacts'])+1,native_checks=checks,bios_checks=reports['bios']['checks'],vmware_checks=reports['vmware-results']['checks'],cached_full_comparisons=12,resources='resources.json',feature_provenance='Actual native physical 4K/200% default-effects desktop after an Escape-cancelled move restores its exact original rectangle and pixels; verified installation and independent startup, not a browser mockup',feature_sha256=sha(OUT/'feature.png'),harness_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tests/m12').iterdir() if p.suffix in ('.py','.c')},limits=['Named VM profiles only; no universal hardware, GPU 3D or expanded foreign Windows compatibility.','Setup review is automated scenario verification, not a participant usability study.','M12.18 final controller/original-app/site-sharing and high-contrast boundary observations remain open; external screen reader/speech and direct-framebuffer fallback native qualification are not claimed.','Public release and complete website verification close separately.']))
    print('PASS: matching M12.17 production raster equivalence, default-effects motion, interrupted moves, full accessibility carry and bounded resources')

if __name__=='__main__':main()
