"""Close a native M13 stage only from matching local and public proof."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]

def verify_inputs_at_commit(ref, records, root=ROOT):
    """Docs may advance after release; both refs must still bind every compiled byte."""
    resolved = subprocess.check_output(['git','rev-parse',ref+'^{commit}'],cwd=root).decode().strip()
    paths = list(records)
    raw = subprocess.run(['git','cat-file','--batch'],cwd=root,input=''.join(resolved+':'+p+'\n' for p in paths).encode(),capture_output=True,check=True).stdout
    at = 0
    for path in paths:
        end = raw.index(b'\n',at); header = raw[at:end].split()
        assert len(header)==3 and header[1]==b'blob', ('Missing compiled source',path)
        size=int(header[2]); body=raw[end+1:end+1+size]; at=end+size+2
        assert hashlib.sha256(body).hexdigest()==records[path], ('Compiled source differs',resolved,path)
    return resolved


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', type=int, required=True)
    stage = parser.parse_args().stage
    assert 1 <= stage <= 13
    out = ROOT / f'evidence/M13/{stage}'
    def load(name):
        return json.loads((out / name).read_text(encoding='utf-8-sig'))
    accepted = load('acceptance-results.json')
    downloads = load('downloads.json')
    site = load('website-readback.json')
    browser = load('public-browser-verification.json')
    release = load('github-release.json')
    tag = load('github-tag.json')
    visual = load('visual-review.json')
    workflows = load('publication-workflows.json')
    assert all(r['passed'] for r in (accepted, downloads, site, browser, visual))
    assert accepted['build_id'] == downloads['build_id'] == visual['build_id']
    assert downloads['downloaded_zip_sha256'] == accepted['vmware_zip_sha256']
    assert downloads['downloaded_iso_sha256'] == accepted['iso_sha256']
    assert downloads['downloaded_zip_crc'] and len(downloads['artifacts']) == 20
    assert accepted['stage'] == downloads['stage'] == f'M13.{stage}'
    assert release['tag_name'] == downloads['latest'] == f'm13{stage}-v0.13.{stage}'
    assert not release['draft'] and not release['prerelease']
    assert browser['source_commit'] == site['source_commit']
    notes_meta = json.loads((ROOT / f'build/m13/stage{stage}/release-notes.json').read_text(encoding='utf-8'))
    notes = (ROOT / f'build/m13/stage{stage}/release-notes.md').read_text(encoding='utf-8')
    assert notes_meta['encoding'] == 'UTF-8'
    assert hashlib.sha256(notes.encode('utf-8')).hexdigest() == notes_meta['sha256']
    assert release['body'].replace('\r\n', '\n') == notes.replace('\r\n', '\n')
    assert tag['ref'] == f'refs/tags/m13{stage}-v0.13.{stage}'
    assert tag['object']['type'] == 'commit' and tag['object']['sha'] == notes_meta['source_commit']
    manifest = json.loads((ROOT / f'dist/m13stage{stage}-build-manifest.json').read_text(encoding='utf-8'))
    verify_inputs_at_commit(tag['object']['sha'], manifest['source_sha256'])
    verify_inputs_at_commit(site['source_commit'], manifest['source_sha256'])
    assert browser['native_editor_save'].startswith('Saved')
    assert browser['production_search'] and browser['task_sidebar'] and browser['ordered_task_navigation']
    assert browser['current_guide'] and browser['matching_download'] and browser['mobile_menu']
    assert all(image['loaded'] for image in browser['desktop']['images'])
    for layout in (browser['desktop'], browser['mobile']):
        assert layout['document'] <= layout['viewport']
    successful = [w for w in workflows if w['headSha'] == site['source_commit'] and w['status'] == 'completed' and w['conclusion'] == 'success']
    assert successful, 'No successful publisher run for the verified current source'
    for path, digest in accepted['harness_sha256'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    tap = (out / 'publisher-tests.txt').read_text(encoding='utf-8-sig')
    count = re.search(r'(?:#|ℹ) tests (\d+)\b', tap)
    assert count and int(count[1]) >= 22 and re.search(r'(?:#|ℹ) fail 0\b', tap)
    target = out / 'publication-results.json'
    assert not target.exists(), 'Accepted publication proof is immutable'
    result = dict(passed=True, stage=f'M13.{stage}', qualification=accepted['qualification'], source_commit=site['source_commit'], release_source_commit=tag['object']['sha'], build_id=accepted['build_id'], website='https://engaceros.brixcanvas.com', github_release=release['html_url'], workflow_ids=[w['databaseId'] for w in successful], current_native_download=downloads['latest'], design_only=False, new_iso=True, pages_checked=site['pages_checked'], unique_links=site['unique_links'], full_audit='website-audit.json', fresh_readback='website-readback.json', browser_readback='public-browser-verification.json', downloads='downloads.json')
    target.write_bytes((json.dumps(result, indent=2) + '\n').encode())
    print(f'PASS: M13.{stage} matching native source/media, GitHub downloads and current public website.')

if __name__ == '__main__':
    main()
