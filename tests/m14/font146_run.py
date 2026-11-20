"""Actual native framebuffer pixels versus fresh original Inter coverage."""
import argparse
import hashlib
import json
import os
import re
import struct
import traceback
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
from window144_native import ui, c, f, t, clone, library, StoppedDisk, task, output, wait
from original_window_trace4 import views, wait_for
from font146_build import build

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', choices=['compact', 'ordinary', '4k'], default='compact')
    parser.add_argument('--cycles', type=int, default=1)
    args = parser.parse_args()
    assert 1 <= args.cycles <= 21
    suffix = '' if args.profile == 'compact' else '-' + args.profile
    out = ROOT / 'build/m14-native/stage6' / ('font-native' + suffix)
    out.mkdir(parents=True, exist_ok=True)
    c.OUT = out
    meta = json.loads(ui.manifest_path12().read_text())
    base = json.loads((ROOT / 'build/m14-native/stage6' / ('apps' + suffix) / 'results.json').read_text())
    assert base['passed'] and base['build_id'] == meta['build_id']
    source = Path(os.environ['LOCALAPPDATA']) / ('EngineOS/Tests/M6/m146-window-apps' + suffix) / base['owned_fixture'] / 'owned.img'
    work, disk, cloned = clone(ui, source, 'm146-font-pixels-' + args.profile)
    fixture = build(args.profile)
    mounted = StoppedDisk(disk, library())
    try:
        mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe', fixture.read_bytes())
    finally:
        mounted.close()
    report = dict(passed=False, build_id=meta['build_id'], profile=args.profile,
                  scope='Owned native GDI-to-compositor Unicode pixels and lifetime; not original-app font API qualification',
                  fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest(), clone=cloned, cycles=[])
    try:
        resolution, ram = {'compact': ((1280, 800), 128), 'ordinary': ((1920, 1080), 512), '4k': ((3840, 2160), 1024)}[args.profile]
        boot = ui.guest(work / 'font', disk, media='installed', ready='M7_DESKTOP_READY', resolution=resolution, ram=ram)
        ui.s.normal_boot(boot)
        with boot as g:
            p = ui.Pointer(g)
            p.drain()
            c.key(g, 'esc')
            t.close_all(g, p)
            front = t.launch(g, p, 'windows apps', 19)
            task(g, p, 12005)
            before = f.stats(g)[0]
            for cycle in range(args.cycles):
                at = len(g.log())
                p.desktop(12100, True, settle=False)
                g.wait('M8_CPL3_CREATED', at)
                wait(g, 'M146_FONT_READY')
                root = wait_for(g, lambda: next((v for v in views(g) if v['class_name'] == 'UnicodePixels146' and v['visible']), None))
                p.move(resolution[0] - 8, resolution[1] - 8)
                p.drain()
                if cycle == 0:
                    c.shot(g, 'native-unicode-pixels')
                    image = Image.open(out / 'native-unicode-pixels.png').convert('RGB')
                    assert image.size == resolution
                    scale = c.flag(g, 'scale73')
                    physical_size = 16 * scale // 2
                    font = ImageFont.truetype(str(ROOT / 'third_party/inter/Inter.ttf'), physical_size)
                    font.set_variation_by_axes([min(32, max(14, physical_size)), 400])
                    ascent = font.getmetrics()[0]
                    report['physical_dimensions'] = list(image.size)
                    report['scale_half_units'] = scale
                    report['pixel_rows'] = []
                    for row, (text, painted) in enumerate([('Aé€ĞıŞÆ?', 'Aé€ĞıŞÆ?'), ('😀 A', '? A')]):
                        width, height = 200 * scale // 2, 40 * scale // 2
                        alpha = Image.new('L', (width, height))
                        draw = ImageDraw.Draw(alpha)
                        pen = 0
                        for char in painted:
                            draw.text((pen, ascent), char, font=font, fill=255, anchor='ls')
                            pen += round(font.getlength(char))
                        expected_channel = ImageOps.invert(alpha)
                        expected = Image.merge('RGB', (expected_channel, expected_channel, expected_channel))
                        x = (root['bounds'][0] + 1 + 20) * scale // 2
                        y = (root['bounds'][1] + 40 + root['menu_height'] + 20 + row * 40) * scale // 2
                        actual = image.crop((x, y, x + width, y + height))
                        expected.save(out / ('expected-row-' + str(row) + '.png'))
                        actual.save(out / ('actual-row-' + str(row) + '.png'))
                        assert actual.tobytes() == expected.tobytes(), ('Native glyph pixels differ', row, args.profile)
                        report['pixel_rows'].append(dict(text=text, actual_painted=painted,
                                                        exact_rgb_sha256=hashlib.sha256(actual.tobytes()).hexdigest(),
                                                        physical_font_size=physical_size, checked_pixels=width * height))
                        if row == 0:
                            match = re.search(r'M146_FONT_METRICS (\d+) (\d+)', output(g))
                            assert match and int(match[1]) == (pen * 2 + scale - 1) // scale
                            report['reported_logical_extent'] = list(map(int, match.groups()))
                    area = re.search(r'M146_WORK_AREA (\d+) (\d+)', output(g))
                    assert area
                    report['reported_work_area'] = list(map(int, area.groups()))
                    expected_area = [resolution[0] * 2 // scale, resolution[1] * 2 // scale - 60]
                    assert report['reported_work_area'] == expected_area, ('Physical/logical coordinate mismatch', report['reported_work_area'], expected_area)
                p.desktop(49002, True)
                g.wait('M8_JOB_DONE', at)
                p.drain()
                state, command, status = struct.unpack('<3I', ui.memory(g, ui.symbol('info8', installed=True)[0], 12))
                assert state == 2 and not status and 'M146_FONT_LIFETIME_PASS' in output(g), (state, command, status, output(g))
                retained = f.stats(g)[0] - before
                assert retained == 0 and ui.integer(g, 'ui_resident144', True) == 0
                assert len(t.records(g)) == 1 and t.records(g)[0]['token'] == front['token']
                report['cycles'].append(dict(cycle=cycle + 1, retained_pages=retained, normal_owned_window_close=True))
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
