"""Close only matching M14.3 source, native tasks and exact VMware media."""
import hashlib,json,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tests/m12'))
from verify_components import git_inputs,desktop_state,copy_report

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data):p.write_bytes((json.dumps(data,indent=2)+'\n').encode('utf-8'))

def main():
    out=ROOT/'evidence/M14/3';out.mkdir(parents=True,exist_ok=True)
    assert not (out/'publication-results.json').exists(),'Accepted stage is immutable'
    work=ROOT/'build/m14-native/stage3'
    meta=read(ROOT/'dist/m14stage3-build-manifest.json')
    starter=read(ROOT/'dist/m14stage3-starter-manifest.json')
    assert meta['qualification_scope']=='M14-STAGE3-VM-v1' and meta['release_version']=='0.14.3'
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
        assert r['metadata_pages_while_blocked']==[28,32,32,32]
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
    fixed=desktop_state(ROOT/'dist/EngacerOS-M14STAGE3-installed-kernel.map')
    assert fixed['bytes']==557516
    host={name:read(work/name/'results.json') for name in ('http-host','download-stream')}
    assert all(r['passed'] for r in host.values()) and host['http-host']['mutation_cases']==5000
    assert host['download-stream']['source_sha256']==sha(ROOT/'kernel/storage/volume6.c')
    for path,digest in host['http-host']['source_sha256'].items():assert sha(ROOT/path)==digest
    file_names=('path-native','files-native','registry-native','environment-native','file-metadata-native','find-native','state-lifetime')
    files={name:read(work/name/'results.json') for name in file_names}
    for name,r in files.items():
        assert r['passed'] and r['build_id']==meta['build_id'],name
        if name!='state-lifetime':assert len(r['samples'])==20 and all(v['retained_pages']==0 for v in r['samples']),name
    assert files['files-native']['independent_start_saved_bytes_verified']
    assert files['file-metadata-native']['same_identity_after_restart_and_removal']
    assert files['file-metadata-native']['original_removal_and_reinstallation']
    assert files['environment-native']['temporary_files_remaining']==[]
    assert files['environment-native']['protected_root_and_query_only_directory_verified']
    state=files['state-lifetime'];assert [r['name'] for r in state['cases']]==['normal-exit','cancel','unhandled-fault']
    for case in state['cases']:
        assert len(case['samples'])==21 and [r['retained_pages'] for r in case['samples']]==[4]+[0]*20
        assert case['desktop_responsive'] and case['acknowledged_registry_survives_restart']
        assert all(r['shared_resident_pages']==dict(file=0,registry=0) for r in case['samples'])
        if case['name']=='cancel':assert all(r['halted_cpus_while_blocked']==2 for r in case['samples'])
        assert case['unflushed_data_committed']==(case['name']=='normal-exit')
    file_host={name:read(work/name/'results.json') for name in ('unicode-host','path-host','find-host')}
    assert all(r['passed'] for r in file_host.values())
    assert file_host['find-host']['independent_random_cases']==10000 and file_host['find-host']['malformed_input_cases']==10
    for name,r in file_host.items():
        for path,digest in r.get('source_sha256',{}).items():assert sha(ROOT/path)==digest,(name,path)
    observers={}
    for case in ('threads','tls','last-thread','processes','named-sync','named-sync-cancel','cancel','msi-cancel','exceptions','exception-nested','exception-invalid','unwind','unwind-chain','unwind-invalid','inspection','probes'):
        r=read(work/'regression-observers'/(case+'.json'));assert r['passed'] and r['build_id']==meta['build_id'] and r['case']==case
        for path,record in r['observer_sources'].items():assert sha(ROOT/path)==record['canonical_sha256'],path
        observers[case]=r
    write(out/'runtime-observer-sources.json',observers)
    for name in (*profiles,*journeys,*runtime,*host,*files,*file_host):copy_report(work/name,out/name)
    shutil.copyfile(work/'apps/browser-choices.png',out/'feature.png')
    resources=dict(passed=True,stage='M14.3',build_id=meta['build_id'],desktop_fixed=fixed,font_coverage_bytes=font['coverage_bytes'],protected_worker_physical_page_quota=10000,protected_worker_virtual_page_quota=32768,module_quota=32,image_limit_bytes=32*1024**2,one_time_transition_stack_bytes=16384,probe_peak_owned_pages=max(r['peak_owned_pages'] for r in samples),probe_retained_pages=0,profiles={name:r['resources'] for name,r in profiles.items()},limits=['Synthetic loader probes are not original GUI app performance','Observer wall times and quanta are not measured Windows CPU time','M14.35 remains the whole-system performance and optimization gate'])
    resources['runtime']={
        'live_process_limit':4,'threads_per_process_limit':16,
        'root_metadata_pages_observed':28,'child_metadata_pages_observed':32,
        'shared_object_limit':128,'created_object_limit_per_process':32,
        'synchronization_grants_per_process':64,'handles_per_wait':32,
        'shared_registry_pages_unused':0,'shared_registry_pages_observed_blocked':1,
        'four_process_cancel_peak_group_owned_pages':max(r['peak_group_owned_pages'] for r in runtime['named-sync-cancel']['samples']),
        'four_process_cancel_retained_pages_after_initialization':0,
        'four_process_blocked_halted_cpus_observed':2,
        'scope':'Component and protected ownership accounting; not total OS RAM, original GUI performance or a Windows speed comparison'
    }
    resources['files_settings']={'selected_unicode_table_bytes':3344,'shared_file_objects':128,'file_grants_per_process':32,'dirty_data_global_limit_bytes':8388608,'file_logical_limit_bytes':67108864,'registry_keys_per_user':64,'registry_values_per_user':128,'registry_value_data_limit_bytes':2048,'environment_max_utf16_units':8192,'find_handles_per_process':16,'zero_retention_cycles':20,'scope':'Bounded component accounting; not a total OS RAM or original GUI speed benchmark'}
    write(out/'resources.json',resources)
    result=dict(passed=True,stage='M14.3',qualification='M14-STAGE3-VM-v1',build_id=meta['build_id'],iso_sha256=meta['artifacts']['EngacerOS-M14STAGE3.iso']['sha256'],vmware_zip_sha256=starter['sha256'],compiled_source_inputs=len(meta['source_sha256']),native_groups=list(profiles)+list(journeys)+list(runtime)+list(files),host_groups=list(host)+list(file_host),original_payload_count=106,limits=['Selected bounded Unicode/path/sharing/registry/environment profile; not general NTFS/network namespaces or complete Windows filesystem/ACL semantics','Original selected Notepad++/Sumatra images are mapped and inspected only; no app code is executed in inspection','The included original 7-Zip console/MSI profile remains distinct from general Windows GUI or reusable MSI compatibility','Firefox is a verified optional installer download; Firefox installation/execution are unavailable','Native concurrency and selected C exception/unwind profile only; C++ personalities, dynamic function tables and arbitrary application compatibility remain unavailable','Named virtual profiles only; no universal physical hardware or GPU gaming qualification','No new long-duration stability soak or faster-than-Windows claim'],harness_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tests/m14').iterdir() if p.suffix in ('.py','.c','.mjs')})
    write(out/'acceptance-results.json',result)
    print('PASS M14.3 exact-source/native/media acceptance:',meta['build_id'])

if __name__=='__main__':main()
