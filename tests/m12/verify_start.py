"""Qualify matching M12.9 Start media and real guest journeys only."""
import hashlib,json,os,shutil
from pathlib import Path
from PIL import Image
import verify_components as common
ROOT=common.ROOT;WORK=ROOT/'build/m12/stage9';OUT=ROOT/'evidence/M12/9'
load=common.load;sha=common.sha;write=common.write
def public(data):
    for path,label in ((str(ROOT),'<project-root>'),(os.environ.get('USERPROFILE',''),'<user-home>')):
        if path:
            for spelling in (path,path.replace('\\','/')):
                for variant in (spelling,json.dumps(spelling)[1:-1]):data=data.replace(variant.encode(),label.encode())
    return data
def main():
    assert not (OUT/'publication-results.json').exists()
    meta=load(ROOT/'dist/m12stage9-build-manifest.json');starter=load(ROOT/'dist/m12stage9-starter-manifest.json')
    groups=['start-native','start-profiles','bios','vmware-results','motion','search-host','pack-host','recovery']
    reports={name:load(WORK/name/'results.json') for name in groups};native=reports['start-native'];profiles=reports['start-profiles']
    iso=meta['artifacts']['EngacerOS-M12STAGE9.iso']['sha256']
    assert meta['release_version']=='0.12.9' and meta['qualification_scope']=='M12-STAGE9-VM-v1'
    for name,row in reports.items():
        assert row['passed'],name
        if name not in ('search-host','pack-host'):assert row['build_id']==meta['build_id'],name
        if 'iso_sha256' in row:assert row['iso_sha256']==iso,name
    assert len(native['checks'])>=9 and native['resources']['retained_pages']==0
    assert native['resources']['before'][0]==native['resources']['after'][0] and native['resources']['before'][3]==native['resources']['after'][3]
    assert [p['name'] for p in profiles['profiles']]==['compact','compact-dark','150','4k']
    assert [p['scale'] for p in profiles['profiles']]==[2,2,3,4]
    for row in profiles['profiles']:
        assert row['retained_pages']==0
        for kind in ('pinned','all-apps','search','context','category-dialog'):
            with Image.open(WORK/'start-profiles'/f'{kind}-{row["name"]}.png') as im:assert list(im.size)==row['physical']
    assert len(reports['bios']['checks'])==len(reports['vmware-results']['checks'])==3
    assert reports['vmware-results']['existing_vm_inventory_unchanged'] and reports['vmware-results']['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive'])
    assert len(reports['motion']['profiles'])==3 and sum(len(p['comparisons']) for p in reports['motion']['profiles'])==12
    assert len(reports['recovery']['checks'])==2 and reports['search-host']['checks']==16
    assert reports['pack-host']['roundtrip_pages']>500 and reports['pack-host']['malformed_and_fuzz_cases']>10000 and reports['pack-host']['guard_bytes_unchanged']
    for name in ('search-host','pack-host'):
        for path,digest in reports[name]['source_sha256'].items():assert sha(ROOT/path)==digest
    for path,digest in reports['pack-host']['payload_sha256'].items():assert sha(ROOT/path)==digest
    syntax=load(WORK/'syntax-results.json');assert syntax['passed'] and len(syntax['checks'])==8
    for path,digest in syntax['source_sha256'].items():assert meta['source_sha256'][path]==digest
    common.git_inputs(meta['source_sha256'])
    for name,row in meta['artifacts'].items():assert sha(ROOT/'dist'/name)==row['sha256']
    previous=load(ROOT/'evidence/M12/8/resources.json')['current'];current=common.desktop_state(ROOT/'dist/EngacerOS-M12STAGE9-installed-kernel.map')
    baseline=load(ROOT/'evidence/M11/6/resources.json')['fixed_desktop']['FINAL'];assert current['bytes']-baseline['bytes']<256*1024
    assert current['bytes']==previous['bytes'] and meta['font']==load(ROOT/'evidence/M12/8/candidate-manifest.json')['font']
    for stage in range(1,9):
        for name,row in load(ROOT/f'evidence/M12/{stage}/candidate-manifest.json')['artifacts'].items():assert sha(ROOT/'dist'/name)==row['sha256']
        old=load(ROOT/f'evidence/M12/{stage}/starter-manifest.json');assert sha(ROOT/'dist'/old['archive'])==old['sha256']
    OUT.mkdir(parents=True,exist_ok=True)
    for group in groups:
        target=OUT/group;target.mkdir(exist_ok=True)
        for path in (WORK/group).iterdir():
            if path.is_file() and path.suffix in ('.json','.png','.log'):(target/path.name).write_bytes(path.read_bytes() if path.suffix=='.png' else public(path.read_bytes()))
    for source,name in [('dist/m12stage9-build-manifest.json','candidate-manifest.json'),('dist/m12stage9-starter-manifest.json','starter-manifest.json'),('build/m12/stage9/syntax-results.json','syntax-results.json')]:shutil.copyfile(ROOT/source,OUT/name)
    shutil.copyfile(WORK/'start-native/pinned.png',OUT/'feature.png')
    write(OUT/'resources.json',dict(passed=True,previous=previous,current=current,added_fixed_desktop_bytes=current['bytes']-previous['bytes'],managed=native['resources'],display_profiles=profiles['profiles'],font=meta['font'],scope='Bounded local catalogue/pin search, no index/worker/heap/raster cache. Fixed state, peak and retained pages are separate measurements.'))
    write(OUT/'acceptance-results.json',dict(passed=True,stage='M12.9',version='0.12.9',qualification='M12-STAGE9-VM-v1',build_id=meta['build_id'],iso_sha256=iso,vmware_zip_sha256=starter['sha256'],source_inputs_verified=len(meta['source_sha256']),artifacts_verified=len(meta['artifacts'])+1,native_checks=native['checks'],bios_checks=reports['bios']['checks'],vmware_checks=reports['vmware-results']['checks'],cached_full_comparisons=12,resources='resources.json',feature_provenance='Actual native installed QEMU SATA/UEFI Start menu; not a browser mockup',feature_sha256=sha(OUT/'feature.png'),harness_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tests/m12').iterdir() if p.suffix in ('.py','.c')},limits=['Search is installed-app and pinned-folder labels only; no filesystem index or Internet search.','Existing preference ABI and catalogue identities are retained; taskbar redesign remains M12.10.','M12.14 menu/conflict/Start query affordance and notice feedback, plus transfer/modal arbitration, remain open alongside M12.16 scale/cursor and M12.18 BIOS/AHCI stress/final qualification.','Agent visual review is not a human study. Public release and full site readback remain separate gates.']))
    print('PASS: exact M12.9 Start native interaction, persisted preferences, matching media and bounded resources')
if __name__=='__main__':main()
