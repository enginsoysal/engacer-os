"""Prepare complete stage assets only after matching native acceptance."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/build'))
from m8 import privacy_input

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', type=int, required=True)
    stage = parser.parse_args().stage
    assert 1 <= stage <= 15
    prefix = f'm14stage{stage}'
    image = f'EngacerOS-M14STAGE{stage}'
    dist = ROOT / 'dist'
    manifests = [dist / f'{prefix}-{kind}-manifest.json' for kind in ('build', 'starter')]
    meta, starter = map(load, manifests)
    accepted = load(ROOT / f'evidence/M14/{stage}/acceptance-results.json')
    assert accepted['passed'] and accepted['qualification'] == f'M14-STAGE{stage}-VM-v1'
    assert accepted['build_id'] == meta['build_id'] == starter['build_id']
    assert accepted['vmware_zip_sha256'] == starter['sha256']
    assets = [dist / name for name in meta['artifacts']]
    for path in assets:
        assert sha(path) == meta['artifacts'][path.name]['sha256']
    archive = dist / starter['archive']
    assert sha(archive) == starter['sha256']
    assets += [archive, *manifests]
    notice = dist / f'{image}-THIRD-PARTY-NOTICES.txt'
    with zipfile.ZipFile(archive) as source:
        assert source.testzip() is None
        notice.write_bytes(source.read('EngacerOS/THIRD-PARTY-NOTICES.txt'))
    assets.append(notice)
    for original, name in [('third_party/7zip/7z2606-src.tar.xz', '7z2606-src.tar.xz'), ('third_party/libmspack/COPYING.LIB', 'COPYING.LIB')]:
        path = dist / name
        shutil.copyfile(ROOT / original, path)
        assert sha(path) == sha(ROOT / original)
        assets.append(path)
    assert len(assets) == len({p.name for p in assets}) == 19
    checks = dist / f'M14STAGE{stage}-SHA256SUMS.txt'
    checks.write_bytes(''.join(sha(p) + '  ' + p.name + '\n' for p in sorted(assets)).encode())
    assets.append(checks)
    for path in assets:
        data = privacy_input(path.read_bytes())
        assert b'C:\\Users\\' not in data and b'C:/Users/' not in data, path.name
    result = dict(build_id=meta['build_id'], qualification=accepted['qualification'], assets=[dict(name=p.name, sha256=sha(p), size=p.stat().st_size) for p in sorted(assets)])
    out = ROOT / f'build/m14-native/stage{stage}'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'release-assets.json').write_bytes((json.dumps(result, indent=2) + '\n').encode())
    print('Prepared 20 matching stage assets and complete 19-file checksums.')

if __name__ == '__main__':
    main()
