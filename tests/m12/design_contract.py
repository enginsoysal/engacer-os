"""Check ordered delivery gates, concept provenance and readable theme pairs."""
import hashlib
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]

def luminance(value):
    channels = [int(value[i:i+2], 16) / 255 for i in (1, 3, 5)]
    channels = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in channels]
    return sum(c * w for c, w in zip(channels, (.2126, .7152, .0722)))

def main():
    progress = json.loads((ROOT / 'docs/milestones/m12-progress.json').read_text(encoding='utf-8'))
    tokens = json.loads((ROOT / 'docs/architecture/m12-tokens.json').read_text(encoding='utf-8'))
    inventory = (ROOT / 'docs/architecture/m12-inventory.md').read_text(encoding='utf-8')
    inventory_sources = sorted(set(re.findall(r'`([^`]+\.(?:c|h|inc))`', inventory)))
    for name in inventory_sources:
        assert (ROOT / name).exists() if '/' in name else list((ROOT / 'kernel').rglob(name)), name
    stages = progress['stages']
    assert [s['id'] for s in stages] == [f'M12.{n}' for n in range(19)]
    for n, stage in enumerate(stages):
        assert stage['requires'] == (f'M12.{n-1}' if n else None)
        assert all(stage.get(k) for k in ('title', 'deliverable', 'how_and_why', 'acceptance'))
        assert stage['publication'] == 'required_before_next_stage'
    contrast = []
    for name, theme in tokens['themes'].items():
        for foreground, background in [('ink', 'paper'), ('ink', 'surface'), ('muted', 'surface'), ('ink', 'selection'), ('on_accent', 'accent')]:
            a, b = sorted((luminance(theme[foreground]), luminance(theme[background])))
            ratio = (b + .05) / (a + .05)
            contrast.append(dict(theme=name, foreground=foreground, background=background, ratio=round(ratio, 3)))
            assert ratio >= 4.5, contrast[-1]
    concepts = []
    for name in ('overview', 'files-usb', 'usb-empty', 'settings', 'transfer', 'setup'):
        path = ROOT / f'docs/architecture/figures/m12/{name}.svg'
        raw = path.read_bytes()
        svg = ET.fromstring(raw)
        assert svg.attrib['width'] == '1280' and svg.attrib['height'] == '800'
        assert 'M12.0 DESIGN CONCEPT' in raw.decode('utf-8')
        assert not any(node.tag.endswith(('image', 'script', 'foreignObject')) for node in svg.iter())
        concepts.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(raw).hexdigest()))
    report = dict(schema=1, scope='M12.0 design contract; no native runtime or human study claimed', passed=True, ordered_stages=len(stages), inventory_sources=inventory_sources, contrast=contrast, concepts=concepts, visual_review='See separate visual-review.json; this script cannot certify visual quality.')
    destination = ROOT / 'evidence/M12/0/design-results.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('PASS: 19 ordered stages, 15 contrast pairs and six original labeled concepts. Visual review remains separate.')

if __name__ == '__main__':
    main()
