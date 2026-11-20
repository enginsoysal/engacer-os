"""Original 7-Zip Browse/Cancel/Unicode selection diagnostic; not acceptance."""
import hashlib
import json
from pathlib import Path
from window144_native import ui, c, f, output
from original_window_trace4 import views, wait_for

ROOT = Path(__file__).resolve().parents[2]


def dialog_task(g, p, report):
    modal = next(v for v in views(g) if v['class_name'] == '#32770' and v['visible'])
    report['original_dialog_visible'] = True

    def click_browse():
        table = {v['handle']: v for v in views(g)}
        node = next(v for v in table.values() if v['parent'] == modal['handle'] and
                    v['class_name'] == 'Button' and v['title'] == '...')
        x, y, w, h = node['bounds']
        x += w // 2
        y += h // 2
        while node['parent']:
            node = table[node['parent']]
            border = 1 if node['style'] & 0x800000 else 0
            x += node['bounds'][0] + border
            y += node['bounds'][1] + (border if node['parent'] else 40 + node['menu_height'])
        scale = c.flag(g, 'scale73') / 2
        p.move(int(x * scale), int(y * scale))
        p.down(True)
        p.down(False)
        p.drain()

    def picker_active():
        text = output(g)
        if 'Not implemented:' in text or 'is not implemented' in text:
            raise AssertionError(text)
        return c.flag(g, 'file_dialog_state11') == 10 and c.flag(g, 'picker12') == 8

    click_browse()
    wait_for(g, picker_active)
    c.shot(g, 'original-native-browse')
    p.desktop(54010, True)
    wait_for(g, lambda: not c.flag(g, 'file_dialog_state11'))
    assert any(v['handle'] == modal['handle'] and v['visible'] for v in views(g))
    report['common_dialog_cancel_returns_to_original'] = True
    click_browse()
    wait_for(g, picker_active)
    c.key(g, 'ctrl', 'a')
    c.key(g, 'ctrl', 'v')
    c.key(g, 'end')
    for _ in range(4):
        c.key(g, 'backspace')
    c.type_text(g, '.7z')
    c.key(g, 'home')
    c.type_text(g, 'chosen-')
    raw = ui.memory(g, *ui.symbol('picker12', installed=True))
    expected = 'chosen-m146-é.7z'
    assert expected.encode() + b'\0' in raw
    c.shot(g, 'original-native-unicode-selection')
    p.desktop(54011, True)
    wait_for(g, lambda: not c.flag(g, 'file_dialog_state11'))
    wait_for(g, lambda: any(expected in v['title'] for v in views(g)))
    report['original_received_unicode_selected_name'] = expected
    report['original_selected_path_does_not_create_file'] = not any(
        path.endswith('/' + expected) for path in f.entries(g))
    assert report['original_selected_path_does_not_create_file']
    c.shot(g, 'original-received-selected-path')


def main():
    canonical = ROOT / 'tests/m14/original_add146_run.py'
    source = canonical.read_bytes().decode('utf-8')
    source = source.replace("'original-add-probe'", "'original-picker-probe'")
    source = source.replace('m146-original-add-probe', 'm146-original-picker-probe')
    before = "c.shot(g,'original-add-selected')"
    assert source.count(before) == 1
    source = source.replace(before, "c.key(g,'ctrl','c');" + before)
    before = "c.shot(g,'original-add-result');report['scope']="
    assert source.count(before) == 1
    source = source.replace(before, "dialog_task146(g,p,report);" + before)
    receipt = dict(canonical_sha256=hashlib.sha256(canonical.read_bytes()).hexdigest(),
                   executed_sha256=hashlib.sha256(source.encode()).hexdigest(),
                   adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   scope='Original common-dialog diagnostic only; no archive/lifecycle or release qualification')
    out = ROOT / 'build/m14-native/stage6/original-picker-probe'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'observer.json').write_bytes((json.dumps(receipt, indent=2) + '\n').encode())
    namespace = dict(__file__=str(canonical), __name__='original_picker_probe146', dialog_task146=dialog_task)
    exec(compile(source, str(canonical), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
