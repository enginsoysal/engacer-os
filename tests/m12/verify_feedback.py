"""Qualify exact M12.14 feedback media, actionable refusals and preserved ownership."""
import json,os,shutil
from PIL import Image
import verify_components as common
ROOT=common.ROOT;WORK=ROOT/'build/m12/stage14';OUT=ROOT/'evidence/M12/14'
load=common.load;sha=common.sha;write=common.write

def public(data):
    for path,label in ((str(ROOT),'<project-root>'),(os.environ.get('USERPROFILE',''),'<user-home>')):
        if path:
            for spelling in (path,path.replace('\\','/')):
                for variant in (spelling,json.dumps(spelling)[1:-1]):data=data.replace(variant.encode(),label.encode())
    return data

def main():
    assert not (OUT/'publication-results.json').exists()
    meta=load(ROOT/'dist/m12stage14-build-manifest.json');starter=load(ROOT/'dist/m12stage14-starter-manifest.json');groups=['feedback-native','feedback-profiles','feedback-busy','bios','vmware-results','motion','taskbar-host','pack-host','recovery'];reports={name:load(WORK/name/'results.json') for name in groups};native=reports['feedback-native'];profiles=reports['feedback-profiles'];iso=meta['artifacts']['EngacerOS-M12STAGE14.iso']['sha256']
    assert meta['release_version']=='0.12.14' and meta['qualification_scope']=='M12-STAGE14-VM-v1'
    for name,row in reports.items():
        assert row['passed'],name
        if name not in ('taskbar-host','pack-host'):assert row['build_id']==meta['build_id'],name
        if 'iso_sha256' in row:assert row['iso_sha256']==iso,name
        if 'resources' in row:
            r=row['resources'];assert r['retained_pages']==0 and r['before'][0]==r['after'][0] and r['before'][3]==r['after'][3],name
    assert len(native['checks'])>=6
    assert 'M7_DESKTOP_READY build='+meta['build_id'] in (WORK/'feedback-native/native.log').read_text(encoding='utf-8')
    assert [p['name'] for p in profiles['profiles']]==['compact','compact-dark','150','4k'] and [p['scale'] for p in profiles['profiles']]==[2,2,3,4]
    for row in profiles['profiles']:
        assert row['retained_pages']==0
        assert 'M7_DESKTOP_READY build='+meta['build_id'] in (WORK/'feedback-profiles'/(row['name']+'.log')).read_text(encoding='utf-8')
        for kind in ('menu','search','notice'):
            with Image.open(WORK/'feedback-profiles'/f'{kind}-{row["name"]}.png') as image:assert list(image.size)==row['physical']
    assert len(reports['feedback-busy']['checks'])>=2 and len(profiles['checks'])>=2
    assert len(reports['bios']['checks'])==len(reports['vmware-results']['checks'])==3
    assert reports['vmware-results']['existing_vm_inventory_unchanged'] and reports['vmware-results']['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive'])
    assert len(reports['motion']['profiles'])==3 and sum(len(p['comparisons']) for p in reports['motion']['profiles'])==12 and len(reports['recovery']['checks'])==2
    assert reports['taskbar-host']['checks']>290000 and reports['pack-host']['roundtrip_pages']>500 and reports['pack-host']['malformed_and_fuzz_cases']>10000 and reports['pack-host']['guard_bytes_unchanged']
    for name in ('taskbar-host','pack-host'):
        for path,digest in reports[name]['source_sha256'].items():assert sha(ROOT/path)==digest
    for path,digest in reports['pack-host']['payload_sha256'].items():assert sha(ROOT/path)==digest
    syntax=load(WORK/'syntax-results.json');assert syntax['passed'] and len(syntax['checks'])==8
    for path,digest in syntax['source_sha256'].items():assert meta['source_sha256'][path]==digest
    common.git_inputs(meta['source_sha256'])
    for name,row in meta['artifacts'].items():assert sha(ROOT/'dist'/name)==row['sha256']
    previous=load(ROOT/'evidence/M12/13/resources.json')['current'];current=common.desktop_state(ROOT/'dist/EngacerOS-M12STAGE14-installed-kernel.map');baseline=load(ROOT/'evidence/M11/6/resources.json')['fixed_desktop']['FINAL'];assert current['bytes']-baseline['bytes']<256*1024 and 0<=current['bytes']-previous['bytes']<=256 and meta['font']==load(ROOT/'evidence/M12/13/candidate-manifest.json')['font']
    for stage in range(1,14):
        for name,row in load(ROOT/f'evidence/M12/{stage}/candidate-manifest.json')['artifacts'].items():assert sha(ROOT/'dist'/name)==row['sha256']
        old=load(ROOT/f'evidence/M12/{stage}/starter-manifest.json');assert sha(ROOT/'dist'/old['archive'])==old['sha256']
    OUT.mkdir(parents=True,exist_ok=True)
    for group in groups:
        target=OUT/group;target.mkdir(exist_ok=True)
        for path in (WORK/group).iterdir():
            if path.is_file() and path.suffix in ('.json','.png','.log'):(target/path.name).write_bytes(path.read_bytes() if path.suffix=='.png' else public(path.read_bytes()))
    diagnostics=OUT/'diagnostics';diagnostics.mkdir(exist_ok=True)
    for path in (WORK/'diagnostics').iterdir():
        if path.suffix in ('.json','.png'):(diagnostics/path.name).write_bytes(path.read_bytes() if path.suffix=='.png' else public(path.read_bytes()))
    for source,name in [('dist/m12stage14-build-manifest.json','candidate-manifest.json'),('dist/m12stage14-starter-manifest.json','starter-manifest.json'),('build/m12/stage14/syntax-results.json','syntax-results.json')]:shutil.copyfile(ROOT/source,OUT/name)
    shutil.copyfile(WORK/'feedback-native/appearance.png',OUT/'feature.png');write(OUT/'resources.json',dict(passed=True,previous=previous,current=current,added_fixed_desktop_bytes=current['bytes']-previous['bytes'],managed=native['resources'],display_profiles=profiles['profiles'],font=meta['font'],scope='Reuses existing notices, global dialog ownership and transfer state; no new worker, framebuffer cache or idle scanner. Fixed bytes, peak and completed retention are separate.'))
    checks=sum((reports[name]['checks'] for name in ('feedback-native','feedback-profiles','feedback-busy')),[])
    write(OUT/'acceptance-results.json',dict(passed=True,stage='M12.14',version='0.12.14',qualification='M12-STAGE14-VM-v1',build_id=meta['build_id'],iso_sha256=iso,vmware_zip_sha256=starter['sha256'],source_inputs_verified=len(meta['source_sha256']),artifacts_verified=len(meta['artifacts'])+1,native_checks=checks,bios_checks=reports['bios']['checks'],vmware_checks=reports['vmware-results']['checks'],cached_full_comparisons=12,resources='resources.json',feature_provenance='Actual installed native QEMU SATA/UEFI blocked-save recovery and owner-scoped dialog; not a browser mockup',feature_sha256=sha(OUT/'feature.png'),harness_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tests/m12').iterdir() if p.suffix in ('.py','.c')},limits=['Named VM profiles only; no universal hardware, GPU 3D or expanded foreign Windows compatibility.','Feedback review is automated scenario verification, not a participant usability study.','M12.16 cursor/scale, M12.17 renderer and M12.18 final controller/original-app/site-sharing observations remain open.','Public release and complete website verification close separately.']))
    print('PASS: matching M12.14 native feedback, owner preservation, persistence and bounded resources')

if __name__=='__main__':main()
