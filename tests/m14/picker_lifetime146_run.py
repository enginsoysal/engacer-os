"""Observe real pending dialogs through owner, thread and process teardown."""
import argparse
import hashlib
import json
import os
import struct
import time
import traceback
from pathlib import Path
from window144_native import ui, c, f, t, clone, library, StoppedDisk, task, output
from original_window_trace4 import views
from picker_lifetime146_build import build

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cycles', type=int, default=21)
    args = parser.parse_args()
    assert 1 <= args.cycles <= 21
    out = ROOT / 'build/m14-native/stage6/picker-lifetime-native'
    out.mkdir(parents=True, exist_ok=True)
    c.OUT = out
    meta = json.loads(ui.manifest_path12().read_text())
    base = json.loads((ROOT / 'build/m14-native/stage6/apps/results.json').read_text())
    assert base['passed'] and base['build_id'] == meta['build_id']
    source = Path(os.environ['LOCALAPPDATA']) / 'EngineOS/Tests/M6/m146-window-apps' / base['owned_fixture'] / 'owned.img'
    work, disk, cloned = clone(ui, source, 'm146-picker-lifetimes')
    fixture = build()
    mounted = StoppedDisk(disk, library())
    try:
        mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe', fixture.read_bytes())
    finally:
        mounted.close()
    report = dict(passed=False, build_id=meta['build_id'], clone=cloned,
                  scope='Owned actual displayed modal requests, timer-dispatched owner/thread/process teardown and idle/lifetime observations',
                  fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest(), cycles=[])
    try:
        boot = ui.guest(work / 'lifetimes', disk, media='installed', ready='M7_DESKTOP_READY', ram=128)
        ui.s.normal_boot(boot)
        with boot as g:
            p = ui.Pointer(g)
            p.drain()
            c.key(g, 'esc')
            t.close_all(g, p)
            front = t.launch(g, p, 'windows apps', 19)
            task(g, p, 12005)
            before = f.stats(g)[0]
            last_generation = 0
            for cycle in range(args.cycles):
                at = len(g.log())
                p.desktop(12100, True, settle=False)
                g.wait('M8_CPL3_CREATED', at)
                phases = []
                for marker, purpose, name in [('M146_OWNER_DESTROY_READY', 7, 'owner'),
                                              ('M146_THREAD_EXIT_READY', 8, 'thread'),
                                              ('M146_PROCESS_EXIT_READY', 7, 'process')]:
                    deadline = time.monotonic() + 40
                    while time.monotonic() < deadline:
                        text = output(g)
                        assert 'M146_LIFETIME_FAIL' not in text, text
                        pointer = int.from_bytes(ui.memory(g, ui.symbol('picker_request', installed=True)[0], 8), 'little')
                        generation = int.from_bytes(ui.memory(g, pointer, 8), 'little') if pointer else 0
                        if marker in text and c.flag(g, 'file_dialog_state11') == 10 and c.flag(g, 'picker12') == purpose and generation > last_generation:
                            break
                        state, command, status = struct.unpack('<3I', ui.memory(g, ui.symbol('info8', installed=True)[0], 12))
                        if state == 3:
                            raise AssertionError(('Request ended before displayed observation', marker, status, text))
                        time.sleep(.03)
                    else:
                        raise TimeoutError((marker, output(g)))
                    last_generation = generation
                    p.drain()
                    idle_observations = []
                    idle_deadline = time.monotonic() + 2
                    while time.monotonic() < idle_deadline:
                        active = int.from_bytes(ui.memory(g, ui.symbol('picker_request', installed=True)[0], 8), 'little')
                        assert active == pointer and active, ('Request ended before idle observation', name)
                        observed_generation = int.from_bytes(ui.memory(g, active, 8), 'little')
                        assert observed_generation == generation and c.flag(g, 'file_dialog_state11') == 10 and c.flag(g, 'picker12') == purpose
                        halted = g.qmp('human-monitor-command', {'command-line': 'info registers -a'}).count('HLT=1')
                        idle_observations.append(halted)
                        if len(idle_observations) >= 3 and idle_observations[-3:] == [2, 2, 2]:
                            break
                        time.sleep(.05)
                    else:
                        raise AssertionError(('No stable blocked idle interval', name, idle_observations))
                    if cycle == 0:
                        c.shot(g, 'pending-' + name)
                    phases.append(dict(phase=name, generation=generation, actual_native_picker_displayed=True, blocked_halted_cpus=halted, idle_observations=idle_observations))
                deadline = time.monotonic() + 20
                while time.monotonic() < deadline:
                    state, command, status = struct.unpack('<3I', ui.memory(g, ui.symbol('info8', installed=True)[0], 12))
                    if state == 3:
                        break
                    time.sleep(.03)
                else:
                    raise TimeoutError('Expected controlled process exit did not finish')
                assert status == 42 and 'M146_OWNER_RELEASE_PASS' in output(g) and 'M146_THREAD_RELEASE_PASS' in output(g), (status, output(g))
                p.drain()
                assert not views(g) and not c.flag(g, 'file_dialog_state11')
                assert ui.integer(g, 'ui_resident144', True) == 0
                assert not any(ui.memory(g, ui.symbol('picker_request', installed=True)[0], 8))
                retained = f.stats(g)[0] - before
                assert retained == 0, retained
                assert len(t.records(g)) == 1 and t.records(g)[0]['token'] == front['token']
                report['cycles'].append(dict(cycle=cycle + 1, phases=phases, expected_process_exit=42,
                                             owner_output_preserved=True, abandoned_thread_output_preserved=True,
                                             picker_and_window_pages_released=True, retained_pages=retained))
            value = task(g, p, 12005)
            assert 'Mapped original image: 7z.exe' in value and '7-Zip' in value
            report['subsequent_original_console_success'] = True
            (out / 'serial.log').write_bytes(g.log().encode())
        report['passed'] = True
    except Exception:
        report['error'] = ui.q.clean(traceback.format_exc())
        raise
    finally:
        (out / 'results.json').write_bytes((json.dumps(report, indent=2) + '\n').encode())
        print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
