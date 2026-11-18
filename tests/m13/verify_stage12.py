"""Bind final whole-product tasks to immutable M13.12 source and media."""
import hashlib,json,os,shutil
from pathlib import Path
import verify_stage2 as base
from close_stage import verify_inputs_at_commit
ROOT=base.ROOT;read=base.read;write=base.write;sha=base.sha;rules=base.rules


def main():
    out=ROOT/'evidence/M13/12';assert not (out/'publication-results.json').exists();out.mkdir(parents=True,exist_ok=True)
    work=ROOT/'build/m13/stage12';meta=read(ROOT/'dist/m13stage12-build-manifest.json');starter=read(ROOT/'dist/m13stage12-starter-manifest.json');iso=meta['artifacts']['EngacerOS-M13STAGE12.iso']['sha256']
    assert meta['qualification_scope']=='M13-STAGE12-VM-v1' and meta['release_version']=='0.13.12'
    for group,count in [('ordinary',9),('small',12),('large',14),('matrix',14)]:
        row=read(work/('queue-'+group)/'results.json');assert row['passed'] and row['build_id']==meta['build_id'] and len(row['steps'])==count and all(s['exit_code']==0 for s in row['steps']),group
    profiles=['ordinary','compact','1024','150','4k']
    names=profiles+['personalization-'+n for n in profiles]+['screensaver-native','screensaver-persistence','screensaver-invalid','settings-native','search-ordinary','settings-write-failure','dialogs-native','feedback-native','transfers-native','desktop-native','files-ordinary','usb-native','setup-safety','progress-recovery','startup-failure','4kn-refusal','apps-ordinary','apps-1024','apps-4k','windows-4k','start-ordinary','taskbar-native','tray-native','progress-compact','progress-4k','vmware-results']
    reports={name:read(work/name/'results.json') for name in names}
    for name,row in reports.items():
        assert row['passed'] and row['build_id']==meta['build_id'] and row['iso_sha256']==iso,name
        if 'resources' in row:
            r=row['resources'];assert r.get('retained_pages',r.get('retained_task_delta_pages'))==0,(name,r)
    for name in profiles:
        r=reports[name];expected={'ordinary':(1920,1080,2),'compact':(1280,800,2),'1024':(1024,768,2),'150':(1920,1200,3),'4k':(3840,2160,4)}[name]
        assert tuple(r['physical'])==expected[:2] and r['scale_units']==expected[2]
        personal=reports['personalization-'+name];assert personal['themes']==['light','dark','high-contrast'] and len(personal['checks'])==3
        for theme in personal['themes']:assert sha(work/('personalization-'+name)/(theme+'-reduced-motion-before.png'))==sha(work/('personalization-'+name)/(theme+'-reduced-motion.png'))
    assert len(reports['screensaver-native']['checks'])==7 and 58<=reports['screensaver-native']['actual_idle_feature_seconds']<=70
    assert len(reports['screensaver-invalid']['cases'])==7 and len(reports['screensaver-persistence']['cases'])==2
    assert len(reports['settings-native']['checks'])==6 and len(reports['search-ordinary']['checks'])==7
    assert reports['settings-write-failure']['injected_fault']['once'] and 'Cancel changes' in reports['settings-write-failure']['message']
    assert len(reports['apps-ordinary']['frames'])==57 and len(reports['apps-1024']['frames'])==19 and len(reports['apps-4k']['frames'])==19
    labels=[c+'-'+f for c in ['sata','ide','lsilogic','lsisas1068','pvscsi','nvme'] for f in ['efi','bios']]+['buslogic-bios','sata-efi-starter']
    matrix={label:read(work/'matrix-results'/label/'results.json') for label in labels}
    for label,row in matrix.items():
        assert row['passed'] and row['build_id']==meta['build_id'] and row['iso_sha256']==iso,label
        assert row['existing_vm_inventory_unchanged'] and row['all_shipped_devices_enabled'] and row['same_vm_reused'] and not row['boot_order_forced']
        assert row['harness_sha256']==sha(ROOT/'tests/m13/vmware_matrix12.py') and len(row['checks'])>=(4 if label.endswith('starter') else 3)
    exact=matrix['sata-efi-starter'];assert exact['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive']) and len(exact['original_payload_sha256'])==106
    vm=reports['vmware-results'];assert vm['existing_vm_inventory_unchanged'] and len(vm['checks'])==4 and vm['starter_sha256']==starter['sha256']
    verify_inputs_at_commit('HEAD',meta['source_sha256']);rules.git_inputs(meta['source_sha256'])
    for name,row in meta['artifacts'].items():assert sha(ROOT/'dist'/name)==row['sha256']
    old=read(ROOT/'evidence/M13/11/acceptance-results.json');assert sha(ROOT/'dist/EngacerOS-M13STAGE11.iso')==old['iso_sha256'] and sha(ROOT/'dist/EngacerOS-M13STAGE11-VMware.zip')==old['vmware_zip_sha256']
    fixed=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE12-installed-kernel.map');previous=rules.desktop_state(ROOT/'dist/EngacerOS-M13STAGE11-installed-kernel.map');assert fixed['bytes']==previous['bytes']
    setup=base.fixed_setup(ROOT/'dist/EngacerOS-M13STAGE12-kernel.map');assert setup['bytes']==base.fixed_setup(ROOT/'dist/EngacerOS-M13STAGE11-kernel.map')['bytes']
    font=read(ROOT/'build/m13-native/font73-manifest.json');assert font['coverage_bytes']==251248 and font['header_sha256']==read(ROOT/'third_party/inter/raster-lock12.json')['header_sha256']
    write(out/'resources.json',dict(passed=True,fixed_desktop=fixed,previous_fixed=previous,fixed_delta_bytes=0,fixed_installer=setup,font=font,tasks={n:r['resources'] for n,r in reports.items() if 'resources' in r},scope='Fixed state, code, configured guest RAM, framebuffer/shadow and managed peak/retained pages are separate. No added native state, cache, worker or idle polling loop.'))
    def public(data):
        for path,label in [(str(ROOT),'<project-root>'),(os.environ.get('USERPROFILE',''),'<user-home>')]:
            if path:
                for spelling in [path,path.replace('\\','/')]:
                    for variant in [spelling,json.dumps(spelling)[1:-1]]:data=data.replace(variant.encode(),label.encode())
        return data
    for label,source in [(n,work/n) for n in names]+[('matrix/'+n,work/'matrix-results'/n) for n in labels]:
        dest=out/'native'/label;dest.mkdir(parents=True,exist_ok=True)
        for path in source.iterdir():
            if path.suffix not in ['.json','.png','.log'] or path.name=='failure.log':continue
            raw=path.read_bytes();(dest/path.name).write_bytes(raw if path.suffix=='.png' else public(raw))
    checks=[c for n,r in reports.items() if n!='vmware-results' for c in r.get('checks',[])];vmchecks=[label+': '+c for label,r in matrix.items() for c in r['checks']]+vm['checks']
    accepted=dict(passed=True,stage='M13.12',version='0.13.12',qualification='M13-STAGE12-VM-v1',build_id=meta['build_id'],iso_sha256=iso,vmware_zip_sha256=starter['sha256'],source_inputs_verified=len(meta['source_sha256']),native_checks=checks,vmware_checks=vmchecks,controller_profiles=14,original_payload_count=106,app_frame_count=95,resources='resources.json',harness_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in [*(ROOT/'tests/m13').glob('*.py'),*(ROOT/'tests/m13').glob('*.mjs'),*(ROOT/'tests/m13').glob('*.c')]},limits=['Long-duration stability, natural-freeze investigation and reset-chain qualification remain exclusively M13.13','Named virtual profiles only; no universal physical hardware, vendor GPU 3D or general Windows/MSI compatibility','Nineteen app frames cover three themes at ordinary size and Light at 1024/4K; shared controls and personalization cover five display profiles, not every app/theme/scale combination','Agent task and visual review is not a human novice study; matching release and actual website close separately'])
    write(out/'acceptance-results.json',accepted);print('PASS M13.12 final whole-product integration:',len(checks),'native checks,',len(vmchecks),'VMware checks, 14 controller profiles, 106 original payloads, 95 app frames')


if __name__=='__main__':main()
