"""Close only matching M14.1 source, native tasks and exact VMware media."""
import hashlib,json,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tests/m12'))
from verify_components import git_inputs,desktop_state,copy_report

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data):p.write_bytes((json.dumps(data,indent=2)+'\n').encode('utf-8'))

def main():
    out=ROOT/'evidence/M14/1';out.mkdir(parents=True,exist_ok=True)
    assert not (out/'publication-results.json').exists(),'Accepted stage is immutable'
    work=ROOT/'build/m14-native/stage1'
    meta=read(ROOT/'dist/m14stage1-build-manifest.json')
    starter=read(ROOT/'dist/m14stage1-starter-manifest.json')
    assert meta['qualification_scope']=='M14-STAGE1-VM-v1' and meta['release_version']=='0.14.1'
    profiles={name:read(work/name/'results.json') for name in ('ordinary','compact','4k')}
    journeys={name:read(work/name/'results.json') for name in ('inspection','apps','probes','browser-download','vmware-results')}
    for name,r in {**profiles,**journeys}.items():
        assert r['passed'] and r['build_id']==meta['build_id'],name
    assert len(journeys['apps']['original_payload_sha256'])==106
    samples=journeys['probes']['samples']
    assert len(samples)==20 and all(r['retained_pages']==0 and r['peak_owned_pages']<1024 for r in samples)
    protections=[r for r in journeys['probes']['checks'] if isinstance(r,dict)]
    assert len(protections)==3 and all(r['actual_cpl3_fault_contained'] and r['repeated_retention_pages']==[4,0] and r['desktop_responsive'] for r in protections)
    assert journeys['inspection']['first_worker_initialization_pages']==4
    assert len(journeys['inspection']['checks'])==3 and all(r['retained_pages']==0 for r in journeys['inspection']['checks'])
    browser=journeys['browser-download']['checks']
    assert len(browser)==2 and browser[1]['bytes']==95924224 and browser[1]['sha256']=='6dc28633cbd77cb1d044f339185cd467dda39397e4bcca942bfb0ddb2360c681'
    assert browser[1]['installer_executed'] is False
    for name,dimensions in {'ordinary':(1920,1080,2),'compact':(1280,800,2),'4k':(3840,2160,4)}.items():
        r=profiles[name];assert tuple(r['physical'])==dimensions[:2] and r['scale_units']==dimensions[2]
        assert r['resources']['retained_task_delta_pages']==0
        capture=read(work/name/'desktop-capture.json')
        assert (capture['width'],capture['height'])==dimensions[:2]
    vm=journeys['vmware-results'];assert vm['existing_vm_inventory_unchanged'] and starter['passed']
    assert vm['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive'])
    for name,r in meta['artifacts'].items():assert sha(ROOT/'dist'/name)==r['sha256'],name
    git_inputs(meta['source_sha256'])
    font=read(ROOT/'build/m14-native/font73-manifest.json')
    assert font['coverage_bytes']==251248 and font['header_sha256']==read(ROOT/'third_party/inter/raster-lock12.json')['header_sha256']
    fixed=desktop_state(ROOT/'dist/EngacerOS-M14STAGE1-installed-kernel.map')
    assert fixed['bytes']==557516
    host={name:read(work/name/'results.json') for name in ('http-host','download-stream')}
    assert all(r['passed'] for r in host.values()) and host['http-host']['mutation_cases']==5000
    assert host['download-stream']['source_sha256']==sha(ROOT/'kernel/storage/volume6.c')
    for path,digest in host['http-host']['source_sha256'].items():assert sha(ROOT/path)==digest
    for name in (*profiles,*journeys,*host):copy_report(work/name,out/name)
    shutil.copyfile(work/'apps/browser-choices.png',out/'feature.png')
    resources=dict(passed=True,stage='M14.1',build_id=meta['build_id'],desktop_fixed=fixed,font_coverage_bytes=font['coverage_bytes'],protected_worker_physical_page_quota=10000,protected_worker_virtual_page_quota=32768,module_quota=32,image_limit_bytes=32*1024**2,one_time_transition_stack_bytes=16384,probe_peak_owned_pages=max(r['peak_owned_pages'] for r in samples),probe_retained_pages=0,profiles={name:r['resources'] for name,r in profiles.items()},limits=['Synthetic loader probes are not original GUI app performance','Observer wall times and quanta are not measured Windows CPU time','M14.15 remains the whole-system performance and optimization gate'])
    write(out/'resources.json',resources)
    result=dict(passed=True,stage='M14.1',qualification='M14-STAGE1-VM-v1',build_id=meta['build_id'],iso_sha256=meta['artifacts']['EngacerOS-M14STAGE1.iso']['sha256'],vmware_zip_sha256=starter['sha256'],compiled_source_inputs=len(meta['source_sha256']),native_groups=list(profiles)+list(journeys),host_groups=list(host),original_payload_count=106,limits=['Original selected Notepad++/Sumatra images are mapped and inspected only; no app code is executed in inspection','The included original 7-Zip console/MSI profile remains distinct from general Windows GUI or reusable MSI compatibility','Firefox is a verified optional installer download; Firefox installation/execution are unavailable','Static TLS, processes/threads/exceptions and normal process-detach semantics remain later runtime work','Named virtual profiles only; no universal physical hardware or GPU gaming qualification','No new long-duration stability soak or faster-than-Windows claim'],harness_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tests/m14').iterdir() if p.suffix in ('.py','.c','.mjs')})
    write(out/'acceptance-results.json',result)
    print('PASS M14.1 exact-source/native/media acceptance:',meta['build_id'])

if __name__=='__main__':main()
