"""Qualify matching M12.11 multitasking media and real guest journeys only."""
import hashlib,json,os,shutil
from pathlib import Path
from PIL import Image
import verify_components as common
ROOT=common.ROOT;WORK=ROOT/'build/m12/stage11';OUT=ROOT/'evidence/M12/11'
load=common.load;sha=common.sha;write=common.write
def public(data):
    for path,label in ((str(ROOT),'<project-root>'),(os.environ.get('USERPROFILE',''),'<user-home>')):
        if path:
            for spelling in (path,path.replace('\\','/')):
                for variant in (spelling,json.dumps(spelling)[1:-1]):data=data.replace(variant.encode(),label.encode())
    return data
def main():
    assert not (OUT/'publication-results.json').exists()
    meta=load(ROOT/'dist/m12stage11-build-manifest.json');starter=load(ROOT/'dist/m12stage11-starter-manifest.json')
    groups=['multitask-native','multitask-profiles','bios','vmware-results','motion','pack-host','recovery','restore-native']
    reports={name:load(WORK/name/'results.json') for name in groups};native=reports['multitask-native'];profiles=reports['multitask-profiles']
    iso=meta['artifacts']['EngacerOS-M12STAGE11.iso']['sha256']
    assert 'M7_DESKTOP_READY build='+meta['build_id'] in (WORK/'multitask-native/native.log').read_text(encoding='utf-8')
    for name in ('compact','compact-dark','150','4k'):
        assert 'M7_DESKTOP_READY build='+meta['build_id'] in (WORK/'multitask-profiles'/(name+'.log')).read_text(encoding='utf-8')
    assert meta['release_version']=='0.12.11' and meta['qualification_scope']=='M12-STAGE11-VM-v1'
    for name,row in reports.items():
        assert row['passed'],name
        if name!='pack-host':assert row['build_id']==meta['build_id'],name
        if 'iso_sha256' in row:assert row['iso_sha256']==iso,name
    assert 'M7_DESKTOP_READY build='+meta['build_id'] in (WORK/'restore-native/native.log').read_text(encoding='utf-8')
    restore=reports['restore-native'];assert len(restore['checks'])==3 and restore['distinct_normal_bounds'] and restore['normal_before']==restore['normal_after'] and restore['normal_before'][0]!=restore['normal_before'][1] and restore['resources']['retained_pages']==0
    assert not native['development_only'] and len(native['checks'])>=6 and native['resources']['retained_pages']==0
    assert native['resources']['before'][0]==native['resources']['after'][0] and native['resources']['before'][3]==native['resources']['after'][3]
    assert [p['name'] for p in profiles['profiles']]==['compact','compact-dark','150','4k']
    assert [p['scale'] for p in profiles['profiles']]==[2,2,3,4]
    assert [p['half_available'] for p in profiles['profiles']]==[False,False,True,True]
    for row in profiles['profiles']:
        assert row['retained_pages']==0
        for kind in ('arrange','switcher','dirty-review',*(['assist','paired'] if row['half_available'] else ['minimum'])):
            with Image.open(WORK/'multitask-profiles'/f'{kind}-{row["name"]}.png') as im:assert list(im.size)==row['physical']
    assert len(reports['bios']['checks'])==len(reports['vmware-results']['checks'])==3
    assert reports['vmware-results']['existing_vm_inventory_unchanged'] and reports['vmware-results']['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive'])
    assert len(reports['motion']['profiles'])==3 and sum(len(p['comparisons']) for p in reports['motion']['profiles'])==12
    assert len(reports['recovery']['checks'])==2 and len(profiles['checks'])>=2
    assert reports['pack-host']['roundtrip_pages']>500 and reports['pack-host']['malformed_and_fuzz_cases']>10000 and reports['pack-host']['guard_bytes_unchanged']
    for name in ('pack-host',):
        for path,digest in reports[name]['source_sha256'].items():assert sha(ROOT/path)==digest
    for path,digest in reports['pack-host']['payload_sha256'].items():assert sha(ROOT/path)==digest
    syntax=load(WORK/'syntax-results.json');assert syntax['passed'] and len(syntax['checks'])==8
    for path,digest in syntax['source_sha256'].items():assert meta['source_sha256'][path]==digest
    common.git_inputs(meta['source_sha256'])
    for name,row in meta['artifacts'].items():assert sha(ROOT/'dist'/name)==row['sha256']
    previous=load(ROOT/'evidence/M12/10/resources.json')['current'];current=common.desktop_state(ROOT/'dist/EngacerOS-M12STAGE11-installed-kernel.map')
    baseline=load(ROOT/'evidence/M11/6/resources.json')['fixed_desktop']['FINAL'];assert current['bytes']-baseline['bytes']<256*1024
    assert 0<current['bytes']-previous['bytes']<=64 and meta['font']==load(ROOT/'evidence/M12/10/candidate-manifest.json')['font']
    for stage in range(1,11):
        for name,row in load(ROOT/f'evidence/M12/{stage}/candidate-manifest.json')['artifacts'].items():assert sha(ROOT/'dist'/name)==row['sha256']
        old=load(ROOT/f'evidence/M12/{stage}/starter-manifest.json');assert sha(ROOT/'dist'/old['archive'])==old['sha256']
    OUT.mkdir(parents=True,exist_ok=True)
    for group in groups:
        target=OUT/group;target.mkdir(exist_ok=True)
        for path in (WORK/group).iterdir():
            if path.is_file() and path.suffix in ('.json','.png','.log'):(target/path.name).write_bytes(path.read_bytes() if path.suffix=='.png' else public(path.read_bytes()))
    for source,name in [('dist/m12stage11-build-manifest.json','candidate-manifest.json'),('dist/m12stage11-starter-manifest.json','starter-manifest.json'),('build/m12/stage11/syntax-results.json','syntax-results.json')]:shutil.copyfile(ROOT/source,OUT/name)
    shutil.copyfile(WORK/'multitask-native/two-real-windows-side-by-side.png',OUT/'feature.png')
    write(OUT/'resources.json',dict(passed=True,previous=previous,current=current,added_fixed_desktop_bytes=current['bytes']-previous['bytes'],managed=native['resources'],display_profiles=profiles['profiles'],font=meta['font'],scope='Reused eight-token overlay, original icons and geometry; one owner token and side, no new worker, thumbnail framebuffer or idle animation. Fixed state, peak and retained pages are separate measurements.'))
    write(OUT/'acceptance-results.json',dict(passed=True,stage='M12.11',version='0.12.11',qualification='M12-STAGE11-VM-v1',build_id=meta['build_id'],iso_sha256=iso,vmware_zip_sha256=starter['sha256'],source_inputs_verified=len(meta['source_sha256']),artifacts_verified=len(meta['artifacts'])+1,native_checks=native['checks']+profiles['checks']+restore['checks'],bios_checks=reports['bios']['checks'],vmware_checks=reports['vmware-results']['checks'],cached_full_comparisons=12,resources='resources.json',feature_provenance='Actual native installed QEMU SATA/UEFI paired Files windows; not a browser mockup',feature_sha256=sha(OUT/'feature.png'),harness_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tests/m12').iterdir() if p.suffix in ('.py','.c')},limits=['Bounded eight-window switching and supported half/maximize geometry; no thumbnail buffers or new window/process limits.','Existing preference ABI and generation-scoped independent normal bounds are retained; compact unsupported halves are disabled.','M12.14 menu/conflict/Start query affordance and notice feedback, plus transfer/modal arbitration, remain open alongside M12.16 scale/cursor and M12.18 BIOS/AHCI stress/final qualification.','Agent visual review is not a human study. Public release and full site readback remain separate gates.']))
    print('PASS: exact M12.11 native multitasking, guarded geometry, matching media and bounded resources')
if __name__=='__main__':main()
