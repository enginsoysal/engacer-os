"""Independently verify published M12 assets and the downloaded VMware archive."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[2]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', type=int, required=True)
    stage = parser.parse_args().stage
    assert 1 <= stage <= 18
    tag = f'm12{stage}-v0.12.{stage}'
    out = ROOT / f'evidence/M12/{stage}'
    expected = json.loads((ROOT / f'build/m12/stage{stage}/release-assets.json').read_text())
    raw = subprocess.check_output(['gh', 'api', f'repos/enginsoysal/engacer-os/releases/tags/{tag}'], cwd=ROOT)
    release = json.loads(raw)
    assert not release['draft'] and not release['prerelease']
    assets = {a['name']: a for a in release['assets']}
    assert len(assets) == len(expected['assets']) == 20
    results = []
    for row in expected['assets']:
        actual = assets[row['name']]
        assert actual['size'] == row['size']
        assert actual['digest'] == 'sha256:' + row['sha256']
        request = urllib.request.Request(actual['browser_download_url'], method='HEAD', headers={'User-Agent': 'EngacerOS-public-release-verifier'})
        with urllib.request.urlopen(request, timeout=60) as response:
            assert response.status == 200
            if response.headers.get('Content-Length'):
                assert int(response.headers['Content-Length']) == row['size']
        results.append(dict(**row, url=actual['browser_download_url'], public_head=200))
    name = f'EngacerOS-M12STAGE{stage}-VMware.zip'
    target = ROOT / f'build/m12/stage{stage}/downloaded-{name}'
    request = urllib.request.Request(assets[name]['browser_download_url'], headers={'User-Agent': 'EngacerOS-public-release-verifier'})
    with urllib.request.urlopen(request, timeout=120) as response, target.open('wb') as dest:
        while chunk := response.read(1024 * 1024):
            dest.write(chunk)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    assert assets[name]['digest'] == 'sha256:' + digest
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        iso = archive.read(f'EngacerOS/EngacerOS-M12STAGE{stage}.iso')
        assert assets[f'EngacerOS-M12STAGE{stage}.iso']['digest'] == 'sha256:' + hashlib.sha256(iso).hexdigest()
        assert len(archive.namelist()) == 9
    latest = json.loads(subprocess.check_output(['gh', 'api', 'repos/enginsoysal/engacer-os/releases/latest'], cwd=ROOT))
    assert latest['tag_name'] == tag
    out.mkdir(parents=True, exist_ok=True)
    (out / 'github-release.json').write_bytes(raw)
    report = dict(passed=True, stage=f'M12.{stage}', build_id=expected['build_id'], checked_at=datetime.now(timezone.utc).isoformat(), release=release['html_url'], latest=tag, artifacts=results, downloaded_zip_sha256=digest, downloaded_zip_crc=True, downloaded_iso_sha256=hashlib.sha256(iso).hexdigest())
    (out / 'downloads.json').write_bytes((json.dumps(report, indent=2) + '\n').encode())
    print('PASS: 20 public asset digests/HEADs, independently downloaded ZIP CRC and embedded ISO, latest release.')

if __name__ == '__main__':
    main()
