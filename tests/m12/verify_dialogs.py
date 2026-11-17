"""Close only matching native M12.8 dialogs, failure cases and exact media."""
import hashlib,json,os,shutil
from pathlib import Path
from PIL import Image
import verify_components as common
ROOT=common.ROOT;WORK=ROOT/'build/m12/stage8';OUT=ROOT/'evidence/M12/8'
load=common.load;sha=common.sha;write=common.write

def public(data):
    for path,label in ((str(ROOT),'<project-root>'),(os.environ.get('USERPROFILE',''),'<user-home>')):
        if path:
            for spelling in (path,path.replace('\\','/')):
                for variant in (spelling,json.dumps(spelling)[1:-1]):data=data.replace(variant.encode(),label.encode())
    return data

def main():
    assert not (OUT/'publication-results.json').exists()
    meta=load(ROOT/'dist/m12stage8-build-manifest.json');starter=load(ROOT/'dist/m12stage8-starter-manifest.json')
    groups=['dialogs-native','dialogs-formats-smoke','dialogs-profiles','dialogs-fault','dialogs-preferences','dialogs-storage','bios','vmware-results','motion','document-host','pack-host','recovery']
    reports={name:load(WORK/name/'results.json') for name in groups}
    iso=meta['artifacts']['EngacerOS-M12STAGE8.iso']['sha256'];native=reports['dialogs-native'];profiles=reports['dialogs-profiles']
    assert meta['release_version']=='0.12.8' and meta['qualification_scope']=='M12-STAGE8-VM-v1'
    for name,row in reports.items():
        assert row['passed'],name
        if name not in ('document-host','pack-host'):assert row['build_id']==meta['build_id'],name
        if 'iso_sha256' in row:assert row['iso_sha256']==iso,name
    assert len(reports['dialogs-formats-smoke']['checks'])>=3
    assert not native['development_only'] and len(native['checks'])>=12 and native['resources']['retained_pages']==0
    assert native['resources']['before'][0]==native['resources']['after'][0] and native['resources']['before'][3]==native['resources']['after'][3]
    assert profiles['feature_journeys_passed'] and len(profiles['profiles'])==5
    assert [p['scale'] for p in profiles['profiles']]==[4,2,2,3,4]
    assert [p['logical'] for p in profiles['profiles']]==[[640,512],[800,600],[800,600],[1280,800],[1920,1080]]
    assert [(p['physical'],p['theme']) for p in profiles['profiles']]==[([1280,1024],'light'),([800,600],'light'),([800,600],'dark'),([1920,1200],'light'),([3840,2160],'light')]
    for label,size in [('minimum-height',(1280,1024)),('compact',(800,600)),('compact-dark',(800,600)),('150',(1920,1200)),('4k',(3840,2160))]:
        for kind in ('save-as','open','new-folder','replace','dirty'):
            with Image.open(WORK/'dialogs-profiles'/f'{kind}-{label}.png') as image:assert image.size==size
    assert len(reports['bios']['checks'])==len(reports['vmware-results']['checks'])==3
    assert reports['vmware-results']['existing_vm_inventory_unchanged'] and reports['vmware-results']['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive'])
    assert len(reports['motion']['profiles'])==3 and sum(len(row['comparisons']) for row in reports['motion']['profiles'])==12
    assert len(reports['recovery']['checks'])==2
    assert reports['document-host']['checks']==14 and reports['document-host']['new_kernel_payload_buffers']==0
    assert reports['dialogs-fault']['retained_pages_after_failed_save']==0
    stack=load(WORK/'diagnostics/stack-final-results.json');assert stack['passed'] and stack['guarded_kernel_stack_bytes']==16384 and stack['frames']['keyboard']<1024
    for path,digest in stack['source_sha256'].items():assert sha(ROOT/path)==digest
    assert reports['pack-host']['roundtrip_pages']>500 and reports['pack-host']['malformed_and_fuzz_cases']>10000 and reports['pack-host']['guard_bytes_unchanged']
    for name in ('document-host','pack-host'):
        for path,digest in reports[name]['source_sha256'].items():assert sha(ROOT/path)==digest
    for path,digest in reports['pack-host']['payload_sha256'].items():assert sha(ROOT/path)==digest
    syntax=load(WORK/'syntax-results.json');assert syntax['passed'] and len(syntax['checks'])==8
    for path,digest in syntax['source_sha256'].items():assert meta['source_sha256'][path]==digest
    common.git_inputs(meta['source_sha256'])
    for name,row in meta['artifacts'].items():assert sha(ROOT/'dist'/name)==row['sha256']
    previous=load(ROOT/'evidence/M12/7/resources.json')['current'];current=common.desktop_state(ROOT/'dist/EngacerOS-M12STAGE8-installed-kernel.map')
    baseline=load(ROOT/'evidence/M11/6/resources.json')['fixed_desktop']['FINAL'];assert current['bytes']-baseline['bytes']<256*1024
    assert meta['font']==load(ROOT/'evidence/M12/7/candidate-manifest.json')['font']
    for stage in range(1,8):
        for name,row in load(ROOT/f'evidence/M12/{stage}/candidate-manifest.json')['artifacts'].items():assert sha(ROOT/'dist'/name)==row['sha256']
        old=load(ROOT/f'evidence/M12/{stage}/starter-manifest.json');assert sha(ROOT/'dist'/old['archive'])==old['sha256']
    OUT.mkdir(parents=True,exist_ok=True)
    for group in groups:
        target=OUT/group;target.mkdir(exist_ok=True)
        for path in (WORK/group).iterdir():
            if path.is_file() and path.suffix in ('.json','.png','.log') and path.name!='failure.log':
                (target/path.name).write_bytes(path.read_bytes() if path.suffix=='.png' else public(path.read_bytes()))
    for source,name in [('dist/m12stage8-build-manifest.json','candidate-manifest.json'),('dist/m12stage8-starter-manifest.json','starter-manifest.json'),('build/m12/stage8/syntax-results.json','syntax-results.json')]:shutil.copyfile(ROOT/source,OUT/name)
    shutil.copyfile(WORK/'dialogs-native/save-as-initial.png',OUT/'feature.png')
    target=OUT/'diagnostics';target.mkdir(exist_ok=True)
    for path in (WORK/'diagnostics').iterdir():
        if path.is_file() and path.suffix in ('.json','.txt','.png'):(target/path.name).write_bytes(public(path.read_bytes()))
    write(OUT/'resources.json',dict(passed=True,previous=previous,current=current,added_fixed_desktop_bytes=current['bytes']-previous['bytes'],managed=native['resources'],display_profiles=profiles['profiles'],font=meta['font'],new_kernel_document_buffers=0,scope='One bounded owner picker; existing worker input pages and volume page are reused. Fixed state and peak/retained managed pages are separate; configured RAM is not consumption.'))
    write(OUT/'acceptance-results.json',dict(passed=True,stage='M12.8',version='0.12.8',qualification='M12-STAGE8-VM-v1',build_id=meta['build_id'],iso_sha256=iso,vmware_zip_sha256=starter['sha256'],source_inputs_verified=len(meta['source_sha256']),artifacts_verified=len(meta['artifacts'])+1,native_checks=native['checks']+reports['dialogs-formats-smoke']['checks'],bios_checks=reports['bios']['checks'],vmware_checks=reports['vmware-results']['checks'],cached_full_comparisons=12,resources='resources.json',feature_provenance='Actual native installed QEMU SATA/UEFI Save as dialog, not a browser mockup',feature_sha256=sha(OUT/'feature.png'),harness_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tests/m12').iterdir() if p.suffix in ('.py','.c')},limits=['Native app integration only; no Windows common-dialog ABI expansion.','Text remains supported ASCII up to 8191 bytes; BMP/ZIP format and extraction limits remain.','USB editing and arbitrary replacement are unavailable; copy into a native folder first.','M12.14 feedback, M12.16 cursor isolation and M12.18 BIOS/AHCI stress and final device/application qualification remain open.','Agent visual review is not a human study; public release and complete site proof close separately.']))
    print('PASS: exact M12.8 dialogs, native failure cases, persisted bytes, matching media and bounded resources.')
if __name__=='__main__':main()
