"""Original Browse/Cancel/Unicode selection and explicit native group cancellation.

This named journey does not qualify archive creation or normal 7zG C++ exit.
"""
import hashlib
import json
import struct
from pathlib import Path
from window144_native import ui, c, f, t, task, output
from original_window_trace4 import views, wait_for
from original_picker146_probe import dialog_task

ROOT = Path(__file__).resolve().parents[2]


def journey(g, p, report, front, before, format_before):
    dialog_task(g, p, report)
    t.focus(g, p, front)
    p.desktop(12008, True)
    assert not ui.integer(g, 'w8_active', True)
    state = ui.memory(g, ui.symbol('info8', installed=True)[0], 496)
    assert struct.unpack_from('<I', state)[0] == 3 and b'cancel' in state[304:].lower()
    assert not views(g) and ui.integer(g, 'ui_resident144', True) == 0
    assert ui.integer(g, 'mapping_resident146', True) == 0
    assert not any(ui.memory(g, ui.symbol('picker_request', installed=True)[0], 8))
    assert not c.flag(g, 'file_dialog_state11')
    format_delta = ui.integer(g, 'clipboard_resident144', True) - format_before
    assert format_delta in (0, 1)
    retained = f.stats(g)[0] - before - format_delta
    assert retained == 0, (retained, format_delta)
    report.update(native_group_cancel_releases_parent_and_original_helper=True,
                  registered_format_session_pages=format_delta,
                  retained_process_pages=retained,
                  termination_scope='Explicit native Cancel task; normal 7zG C++ cancellation is not qualified')
    assert any(row['token'] == front['token'] for row in t.records(g))
    value = task(g, p, 12005)
    assert 'Mapped original image: 7z.exe' in value and '7-Zip' in value
    report['subsequent_original_console_success'] = True
    c.shot(g, 'desktop-after-original-dialog-task')


def main():
    canonical = ROOT / 'tests/m14/original_add146_run.py'
    source = canonical.read_bytes().decode('utf-8')
    source = source.replace("'original-add-probe'", "'original-picker-native'")
    source = source.replace('m146-original-add-probe', 'm146-original-picker-native')
    before = "c.shot(g,'original-add-selected')"
    assert source.count(before) == 1
    source = source.replace(before, "c.key(g,'ctrl','c');" + before)
    before = 'before=f.stats(g)[0];at=len(g.log());'
    assert source.count(before) == 1
    source = source.replace(before, 'before=f.stats(g)[0];format_before=ui.integer(g,\'clipboard_resident144\',True);at=len(g.log());')
    before = "c.shot(g,'original-add-result');report['scope']="
    assert source.count(before) == 1
    source = source.replace(before, 'journey146(g,p,report,front,before,format_before);' + before)
    source = source.replace("report['diagnostic_completed']=True;report['passed']=False", "report['original_common_dialog_task_completed']=True")
    source = source.replace('Read-only native diagnostic of the actual original 7-Zip Add action; no archive/common-dialog compatibility qualification',
                            'Original 7-Zip common-dialog cancel/Unicode selection, explicit native group cancellation and console recovery; not archive creation or normal C++ exit qualification')
    before = ' except Exception:'
    assert source.count(before) == 1
    source = source.replace(before, "  assert ui.s.s.document(disk,folder+'/'+leaf,4096)==payload;report['source_bytes_independently_unchanged']=True;report['passed']=True\n" + before)
    receipt = dict(canonical_sha256=hashlib.sha256(canonical.read_bytes()).hexdigest(),
                   executed_sha256=hashlib.sha256(source.encode()).hexdigest(),
                   adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   picker_task_sha256=hashlib.sha256((ROOT / 'tests/m14/original_picker146_probe.py').read_bytes()).hexdigest())
    namespace = dict(__file__=str(canonical), __name__='original_picker_native146', journey146=journey)
    exec(compile(source, str(canonical), 'exec'), namespace)
    namespace['main']()
    # The canonical argument parser determines the profile-specific output path.
    import sys
    profile = sys.argv[sys.argv.index('--profile') + 1] if '--profile' in sys.argv else 'compact'
    out = ROOT / 'build/m14-native/stage6' / ('original-picker-native' + ('' if profile == 'compact' else '-' + profile))
    (out / 'observer.json').write_bytes((json.dumps(receipt, indent=2) + '\n').encode())


if __name__ == '__main__':
    main()
