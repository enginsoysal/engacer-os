"""Close only matching M14.2 source, native tasks and exact VMware media."""
import hashlib,json,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tests/m12'))
from verify_components import git_inputs,desktop_state,copy_report

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data):p.write_bytes((json.dumps(data,indent=2)+'\n').encode('utf-8'))

def main():
    out=ROOT/'evidence/M14/2';out.mkdir(parents=True,exist_ok=True)
    assert not (out/'publication-results.json').exists(),'Accepted stage is immutable'
    work=ROOT/'build/m14-native/stage2'
    meta=read(ROOT/'dist/m14stage2-build-manifest.json')
    starter=read(ROOT/'dist/m14stage2-starter-manifest.json')
    assert meta['qualification_scope']=='M14-STAGE2-VM-v1' and meta['release_version']=='0.14.2'
    profiles={name:read(work/name/'results.json') for name in ('ordinary','compact','4k')}
    journeys={name:read(work/name/'results.json') for name in ('inspection','apps','probes','browser-download','vmware-results')}
    for name,r in {**profiles,**journeys}.items():
        assert r['passed'] and r['build_id']==meta['build_id'],name
    runtime_names=('threads','tls','last-thread','processes','named-sync','named-sync-cancel','cancel','msi-cancel','exceptions','exception-nested','exception-invalid','unwind','unwind-chain','unwind-invalid')
    runtime={name:read(work/name/'results.json') for name in runtime_names}
    for name,r in runtime.items():
        assert r['passed'] and r['build_id']==meta['build_id'],name
    for name in ('threads','tls','last-thread','processes','named-sync','exceptions','exception-nested','unwind','unwind-chain'):
        samples=runtime[name].get('samples',runtime[name].get('process_samples'))
        assert len(samples)==20 and all(r['retained_pages']==0 for r in samples),name
    assert 2 in runtime['threads']['sleep_cpu_halt_observations']
    named=runtime['named-sync']
    assert named['quota_and_stale_refusal_checked'] and named['quota_object_limit']==32 and named['quota_grant_limit']==64
    assert all(r['shared_registry_pages_after_close']==0 for r in named['samples']+named['survivor_samples'])
    assert [r['retained_pages'] for r in named['survivor_samples']]==[4,0]
    assert all(r['object_survives_creator_exit'] for r in named['survivor_samples'])
    for name in ('named-sync-cancel','cancel'):
        samples=runtime[name]['samples']
        assert len(samples)==21 and [r['retained_pages'] for r in samples]==[4]+[0]*20,name
    for r in runtime['named-sync-cancel']['samples']:
        assert r['metadata_pages_while_blocked']==[41,45,45,45]
        assert r['shared_registry_pages_while_blocked']==1 and r['shared_registry_pages_after_cancel']==0
        assert r['halted_cpus_observed_while_blocked']==2
    assert all(r['all_cpus_halted_while_blocked']==2 for r in runtime['cancel']['samples'])
    process=runtime['processes']
    assert process['lifetime_epoch_checked_park'] and len(process['actual_original_archives'])==2
    assert all(r['original_child_output_matches'] for r in process['actual_original_archives'].values())
    assert [r['retained_pages'] for r in process['survivor_samples']]==[4,0]
    assert all(r['root_exit_precedes_child_exit'] for r in process['survivor_samples'])
    assert runtime['msi-cancel']['cancel']['namespace_restored'] and runtime['msi-cancel']['cancel']['committed_entries_seen']>0
    assert runtime['msi-cancel']['reinstall_and_original_execution'] and runtime['msi-cancel']['subsequent_retained_pages']==0
    assert runtime['exception-nested']['handled_faults_per_execution']==480
    assert runtime['unwind']['handled_faults_per_execution']==runtime['unwind-chain']['handled_faults_per_execution']==60
    for name,count in (('exception-invalid',3),('unwind-invalid',4)):
        assert len(runtime[name]['cases'])==count,name
        for case in runtime[name]['cases']:
            assert case['desktop_responsive'] and [r['retained_pages'] for r in case['samples']]==[4,0],(name,case)
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
    fixed=desktop_state(ROOT/'dist/EngacerOS-M14STAGE2-installed-kernel.map')
    assert fixed['bytes']==557516
    host={name:read(work/name/'results.json') for name in ('http-host','download-stream')}
    assert all(r['passed'] for r in host.values()) and host['http-host']['mutation_cases']==5000
    assert host['download-stream']['source_sha256']==sha(ROOT/'kernel/storage/volume6.c')
    for path,digest in host['http-host']['source_sha256'].items():assert sha(ROOT/path)==digest
    for name in (*profiles,*journeys,*runtime,*host):copy_report(work/name,out/name)
    shutil.copyfile(work/'apps/browser-choices.png',out/'feature.png')
    resources=dict(passed=True,stage='M14.2',build_id=meta['build_id'],desktop_fixed=fixed,font_coverage_bytes=font['coverage_bytes'],protected_worker_physical_page_quota=10000,protected_worker_virtual_page_quota=32768,module_quota=32,image_limit_bytes=32*1024**2,one_time_transition_stack_bytes=16384,probe_peak_owned_pages=max(r['peak_owned_pages'] for r in samples),probe_retained_pages=0,profiles={name:r['resources'] for name,r in profiles.items()},limits=['Synthetic loader probes are not original GUI app performance','Observer wall times and quanta are not measured Windows CPU time','M14.25 remains the whole-system performance and optimization gate'])
    resources['runtime']={
        'live_process_limit':4,'threads_per_process_limit':16,
        'root_metadata_pages_observed':41,'child_metadata_pages_observed':45,
        'shared_object_limit':128,'created_object_limit_per_process':32,
        'synchronization_grants_per_process':64,'handles_per_wait':32,
        'shared_registry_pages_unused':0,'shared_registry_pages_observed_blocked':1,
        'four_process_cancel_peak_group_owned_pages':max(r['peak_group_owned_pages'] for r in runtime['named-sync-cancel']['samples']),
        'four_process_cancel_retained_pages_after_initialization':0,
        'four_process_blocked_halted_cpus_observed':2,
        'scope':'Component and protected ownership accounting; not total OS RAM, original GUI performance or a Windows speed comparison'
    }
    write(out/'resources.json',resources)
    result=dict(passed=True,stage='M14.2',qualification='M14-STAGE2-VM-v1',build_id=meta['build_id'],iso_sha256=meta['artifacts']['EngacerOS-M14STAGE2.iso']['sha256'],vmware_zip_sha256=starter['sha256'],compiled_source_inputs=len(meta['source_sha256']),native_groups=list(profiles)+list(journeys)+list(runtime),host_groups=list(host),original_payload_count=106,limits=['Original selected Notepad++/Sumatra images are mapped and inspected only; no app code is executed in inspection','The included original 7-Zip console/MSI profile remains distinct from general Windows GUI or reusable MSI compatibility','Firefox is a verified optional installer download; Firefox installation/execution are unavailable','Native concurrency and selected C exception/unwind profile only; C++ personalities, dynamic function tables and arbitrary application compatibility remain unavailable','Named virtual profiles only; no universal physical hardware or GPU gaming qualification','No new long-duration stability soak or faster-than-Windows claim'],harness_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tests/m14').iterdir() if p.suffix in ('.py','.c','.mjs')})
    write(out/'acceptance-results.json',result)
    print('PASS M14.2 exact-source/native/media acceptance:',meta['build_id'])

if __name__=='__main__':main()
