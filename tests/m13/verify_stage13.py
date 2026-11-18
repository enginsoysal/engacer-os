"""Bind the owner-revised M13.13 duration scope and separate completion tasks."""
import hashlib
import json
import os
from pathlib import Path
from PIL import Image, ImageChops

import verify_stage2 as base
from close_stage import verify_inputs_at_commit

ROOT = base.ROOT
read, sha, write = base.read, base.sha, base.write


def main():
    out = ROOT / 'evidence/M13/13'
    assert not (out / 'publication-results.json').exists(), 'Closed releases are immutable'
    work = ROOT / 'build/m13/stage13'
    meta = read(ROOT / 'dist/m13stage13-build-manifest.json')
    starter = read(ROOT / 'dist/m13stage13-starter-manifest.json')
    iso = meta['artifacts']['EngacerOS-M13STAGE13.iso']['sha256']
    assert meta['release_version'] == '0.13.13'
    pointer = read(work / 'workday/current.json')
    observed_source = ROOT / pointer['report']
    assert observed_source.resolve().is_relative_to((work / 'workday').resolve())
    observed = read(observed_source)
    owner = read(out / 'owner-duration-scope.json')
    assert owner['minimum_observed_seconds'] == 5400
    assert owner['observed_seconds'] == observed['elapsed_seconds'] >= 5400
    assert owner['eight_hour_gate_passed'] is False and owner['two_hour_idle_gate_passed'] is False
    assert not observed['passed'] and 'error' not in observed
    assert observed['status'] == 'uninterrupted-idle'
    assert observed['build_id'] == meta['build_id'] and observed['iso_sha256'] == iso
    assert observed['starter_sha256'] == starter['sha256']
    assert observed['harness_sha256'] == sha(ROOT / 'tests/m13/workday13.py')
    for name, digest in observed['dependencies_sha256'].items():
        assert sha(ROOT / name) == digest, name
    observed_frames = {frame['png']: frame for frame in observed['frames']}
    for frame in observed_frames.values():
        assert sha(observed_source.parent / frame['png']) == frame['sha256']
    samples = [frame for frame in observed_frames.values() if frame['png'].startswith('uninterrupted-idle-')]
    assert len(samples) >= 89
    clock_hashes = set()
    with Image.open(observed_source.parent / 'retained-draft-seed.png') as image:
        body = image.convert('RGB').crop((194, 216, 846, 440))
    for sample in samples:
        with Image.open(observed_source.parent / sample['png']) as image:
            image = image.convert('RGB')
            clock_hashes.add(hashlib.sha256(image.crop((image.width-250, image.height-60, image.width, image.height)).tobytes()).hexdigest())
            difference = ImageChops.difference(body, image.crop((194, 216, 846, 440))).convert('L')
            assert difference.width * difference.height - difference.histogram()[0] <= 100
    assert len(clock_hashes) >= 80, 'Require actual visible clock/presentation progress'
    gaps = [b['monotonic'] - a['monotonic'] for a, b in zip(samples, samples[1:])]
    assert gaps and max(gaps) <= 90
    # The owner stopped the original gate early. Its incomplete report is never
    # relabelled. A separate fresh diagnostic completes final Save/data/starts.
    source = ROOT / read(work / 'preflight/current.json')['report']
    assert source.resolve().is_relative_to((work / 'preflight').resolve())
    day = read(source)
    assert day['passed'] is False and day['diagnostic_only'] is True
    assert day['preflight_successful'] and day['status'] == 'diagnostic-preflight-complete' and 'error' not in day
    assert day['build_id'] == meta['build_id'] and day['iso_sha256'] == iso
    assert day['starter_sha256'] == starter['sha256']
    assert len(day['cycles']) >= 1
    assert all(c['retained_managed_bytes'] == 0 and c['visible_and_serial'] and c['dirty_body_changed_pixels'] <= 100 for c in day['cycles'])
    assert all(l['visible'] and l['serial_event'] and l['changed_central_pixels'] >= 10000 for l in day['launches'])
    baseline = day['resources'][0]
    assert day['managed_peak_budget_bytes'] == baseline['peak_bytes'] + 8 * 1024 ** 2
    assert all(r['current_bytes'] == baseline['current_bytes'] and r['allocation_failures'] == baseline['allocation_failures'] and r['peak_bytes'] <= day['managed_peak_budget_bytes'] for r in day['resources'])
    assert len(day['resources']) == len(day['cycles']) + 1
    assert day['existing_vm_inventory_unchanged']
    assert len(day['independent_starts']) == 2
    assert all(r['no_iso'] and r['ordinary_firmware'] and r['actual_native_readback'] for r in day['independent_starts'])
    draft = b'engacer stability saved baseline retained unsaved text'
    assert day['saved_document_sha256'] == hashlib.sha256(draft).hexdigest()
    assert day['harness_sha256'] == sha(ROOT / 'tests/m13/workday13.py')
    for name, digest in day['dependencies_sha256'].items():
        assert sha(ROOT / name) == digest, name
    # A visible-launch retry replaces its same-name provisional PNG. Bind every
    # retained final image; keep earlier hashes as superseded observations, not
    # as independently preserved screenshots. The frozen observer stays intact.
    final_frames = {frame['png']: frame for frame in day['frames']}
    superseded = [frame for frame in day['frames'] if frame is not final_frames[frame['png']]]
    for frame in final_frames.values():
        assert sha(source.parent / frame['png']) == frame['sha256']
    native = (source.parent / 'native.log').read_text(encoding='utf-8')
    assert 'M6_INSTALL_PASS' in native and 'M7_DOCUMENT_SAVED' in native
    # The timer starts after the first complete ordinary resource cycle.
    tail = native[native.index('M7_DESKTOP_STATS current=', native.index('M7_DOCUMENT_SAVED')):]
    assert not any(token in tail for token in ['ENGINE_OS_KERNEL_ENTRY', 'M6_WIZARD_READY', 'M75_USER_RESTART', 'KERNEL_PANIC', 'KERNEL_REJECT:', 'LOADER_REJECT:'])
    for number in range(2):
        log = (source.parent / ('disk-only-' + str(number) + '.log')).read_text(encoding='utf-8')
        assert 'M6_INSTALLED_VOLUME' in log and draft.decode() in log

    reports = {}
    for name in ['ordinary', 'active-idle-constrained', 'active-idle-4k', 'screensaver-native', 'screensaver-persistence', 'screensaver-invalid', 'settings-write-failure', 'vmware-results']:
        row = read(work / name / 'results.json')
        assert row['passed'] and row['build_id'] == meta['build_id'] and row['iso_sha256'] == iso, name
        reports[name] = row
    for name, resolution, ram in [('active-idle-constrained', [1024, 768], 128), ('active-idle-4k', [3840, 2160], 1024)]:
        row = reports[name]
        assert row['physical'] == resolution and row['configured_guest_mib'] == ram
        assert len(row['cycles']) == 3
        assert all(c['real_idle_seconds'] >= 300 and c['saved_file_unchanged'] and c['same_window_owner'] and c['retained_pages'] == 0 and c['ordinary_input_after_idle'] for c in row['cycles'])
        assert row['resources']['retained_task_delta_pages'] == 0 and row['resources']['all_cpus_halted_when_idle']
    assert len(reports['screensaver-native']['checks']) == 7
    assert 58 <= reports['screensaver-native']['actual_idle_feature_seconds'] <= 70
    assert len(reports['screensaver-persistence']['cases']) == 2
    assert len(reports['screensaver-invalid']['cases']) == 7
    assert reports['settings-write-failure']['injected_fault']['once']
    assert 'Cancel changes' in reports['settings-write-failure']['message']
    vm = reports['vmware-results']
    assert vm['starter_sha256'] == starter['sha256'] and vm['existing_vm_inventory_unchanged']
    assert len(vm['checks']) == 4 and vm['visible_preview_wake_observations']
    recovery_sources = [p for p in (work / 'recovery').glob('*/results.json') if read(p).get('passed')]
    assert len(recovery_sources) == 1, 'Choose one unambiguous completed labelled recovery run'
    recovery = read(recovery_sources[0])
    assert recovery['build_id'] == meta['build_id'] and recovery['iso_sha256'] == iso and recovery['starter_sha256'] == starter['sha256']
    assert recovery['labelled_simulated_timeout'] and recovery['visible_responsiveness'] and recovery['existing_vm_inventory_unchanged']
    assert recovery['fifo_quarantines'] == 1 and recovery['framebuffer_recoveries'] == 1
    assert len(recovery['warm_resets']) == 3 and all(r['fresh_boot'] and r['visible_launch'] and not r['full_power_cycle'] for r in recovery['warm_resets'])

    verify_inputs_at_commit('HEAD', meta['source_sha256'])
    base.rules.git_inputs(meta['source_sha256'])
    for name, artifact in meta['artifacts'].items():
        assert sha(ROOT / 'dist' / name) == artifact['sha256']
    assert sha(ROOT / 'dist' / starter['archive']) == starter['sha256']
    previous = read(ROOT / 'dist/m13stage12-build-manifest.json')
    changed = [name for name, digest in meta['source_sha256'].items() if previous['source_sha256'].get(name) != digest]
    assert sorted(changed) == ['distros/engacer-desktop-m13.json', 'tools/build/m13.py']
    fixed = base.rules.desktop_state(ROOT / 'dist/EngacerOS-M13STAGE13-installed-kernel.map')
    setup = base.fixed_setup(ROOT / 'dist/EngacerOS-M13STAGE13-kernel.map')
    assert fixed['bytes'] == 557516 and setup['bytes'] == 48412
    font = read(ROOT / 'build/m13-native/font73-manifest.json')
    assert font['coverage_bytes'] == 251248

    def public(raw):
        for path in [str(ROOT), os.environ.get('USERPROFILE', '')]:
            if path:
                for spelling in [path, path.replace('\\', '/')]:
                    for variant in [spelling, json.dumps(spelling)[1:-1]]:
                        raw = raw.replace(variant.encode(), b'<redacted-local-root>')
        return raw

    for name, folder in [('owner-shortened-observation', observed_source.parent), ('functional-completion', source.parent), ('recovery', recovery_sources[0].parent), *[(name, work / name) for name in reports]]:
        dest = out / 'native' / name
        dest.mkdir(parents=True, exist_ok=True)
        for path in folder.iterdir():
            if path.suffix not in ['.json', '.png', '.log'] or path.name in ['vmware.log', 'failure.log']:
                continue
            raw = path.read_bytes()
            (dest / path.name).write_bytes(raw if path.suffix == '.png' else public(raw))
    write(out / 'resources.json', dict(passed=True, fixed_desktop=fixed, fixed_installer=setup, font_coverage_bytes=251248, workday_baseline=baseline, peak_budget_bytes=day['managed_peak_budget_bytes'], measured_peak_bytes=max(r['peak_bytes'] for r in day['resources']), retained_managed_bytes=0, new_allocation_failures=0, supplementary={name: row.get('resources') for name, row in reports.items() if 'resources' in row}))
    write(out / 'capture-retention.json', dict(scope='All final retained PNGs are SHA-256 verified. Same-name provisional launch-retry frames were superseded in the frozen observer and their earlier hashes are metadata only, not preserved image evidence.', final_images=len(final_frames), superseded_provisional_observations=superseded))
    accepted = dict(passed=True, stage='M13.13', version='0.13.13', qualification='M13-STAGE13-VM-v1', duration_scope='owner_revised_90_minutes', build_id=meta['build_id'], iso_sha256=iso, vmware_zip_sha256=starter['sha256'], source_inputs_verified=len(meta['source_sha256']), actual_observed_seconds=observed['elapsed_seconds'], minimum_observed_seconds=5400, eight_hour_gate_passed=False, two_hour_idle_gate_passed=False, visible_idle_samples=len(samples), unique_clock_captures=len(clock_hashes), maximum_recorded_capture_gap_seconds=max(gaps), active_cycles=len(day['cycles']), visible_launches=len(day['launches']), functional_completion_separate_from_duration=True, native_checks=['Owner-revised ninety-minute minimum met by actual frozen enabled-device VMware observation; retained dirty text and independently hashed clock progression in every recorded idle sample'] + day['checks'] + [check for row in reports.values() for check in row.get('checks', [])], vmware_checks=vm['checks'], resources='resources.json', harness_sha256={p.relative_to(ROOT).as_posix(): sha(p) for p in [Path(__file__), ROOT / 'tests/m13/workday13.py', ROOT / 'tests/m13/recovery13.py', ROOT / 'tests/m13/active_idle13.py', ROOT / 'tests/m13/vmware_stage13.py']}, limits=['Owner explicitly shortened the duration requirement to ninety minutes; the original eight-hour/two-hour gate was interrupted and did not pass', 'The long observation has preserved reports/screenshots; its early stop does not supply completed interval maxima or a final native session log. Saved-data finalization and independent boots are separately tested on a fresh exact candidate', 'Three warm resets follow a labelled injected display timeout; this does not establish the cause of historical natural M13.7/M13.8 freezes or reproduce their reset chain', 'Separate constrained/physical-4K native tasks last fifteen real idle minutes each', 'Native source remains identical to M13.12; its fourteen-controller integration matrix is historical evidence, not a repeated M13.13 matrix', 'No universal stability, vendor GPU 3D, universal Windows/MSI support, physical device study or human novice study is claimed'])
    write(out / 'acceptance-results.json', accepted)
    print('PASS owner-revised M13.13: actual ninety-minute-plus observation, separate saved-data/independent starts, labelled recovery, constrained/4K and screensaver regression; not an eight-hour pass')


if __name__ == '__main__':
    main()
