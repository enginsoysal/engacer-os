"""Close design-only M12.0 from explicit checks and independent public evidence."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'evidence/M12/0'

def load(name):
    return json.loads((OUT / name).read_text(encoding='utf-8-sig'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8')

def main():
    design = load('design-results.json')
    visual = load('visual-review.json')
    site = load('website-readback.json')
    browser = load('public-browser-verification.json')
    downloads = load('design-downloads.json')
    release = load('github-release.json')
    baseline = load('preserved-baseline.json')
    workflows = load('publication-workflows.json')
    assert all(r['passed'] for r in (design, visual, site, downloads, baseline))
    assert not visual['native_runtime'] and not visual['human_usability_study']
    assert design['ordered_stages'] == 19 and len(design['contrast']) == 15
    for concept in design['concepts']:
        assert sha(ROOT / concept['path']) == concept['sha256']
    for artifact in baseline['artifacts']:
        assert sha(ROOT / 'dist' / artifact['name']) == artifact['sha256']
    assets = {a['name']: a for a in release['assets']}
    for artifact in downloads['artifacts']:
        public = assets[artifact['name']]
        assert public['digest'] == 'sha256:'+artifact['sha256']
        assert public['size'] == artifact['size']
        assert sha(ROOT / 'build/brix' / (artifact['name'].removesuffix('.zip')+'-downloaded.zip')) == artifact['sha256']
    assert release['isPrerelease'] and release['tagName'] == 'm120-v0.12.0-design'
    assert browser['gallery_six_links'] and browser['mobile_menu']
    assert browser['native_editor_save'].startswith('Saved')
    assert browser['source_commit'] == site['source_commit']
    assert all(i['loaded'] for i in browser['desktop']['images'])
    for layout in (browser['desktop'], browser['mobile']):
        assert layout['document'] <= layout['viewport']
    successful = [r for r in workflows if r['headSha'] == site['source_commit'] and r['status'] == 'completed' and r['conclusion'] == 'success']
    assert successful, 'No successful publication for these source bytes'
    tap = (OUT / 'publisher-tests.txt').read_text(encoding='utf-8-sig')
    count = int(re.search(r'^# tests (\d+)$', tap, re.M)[1])
    assert count >= 19 and re.search(r'^# fail 0$', tap, re.M)
    assert not subprocess.check_output(['git','diff','HEAD','--','boot','kernel','include','runtime','user'], cwd=ROOT)
    latest = subprocess.check_output(['gh','api','repos/enginsoysal/engacer-os/releases/latest','--jq','.tag_name'], cwd=ROOT, text=True).strip()
    assert latest == 'm116-v0.11.6'
    write('acceptance-results.json', dict(passed=True, stage='M12.0', qualification='M12-DESIGN-v1', native_runtime=False, new_iso=False,
          ordered_stages=19, text_contrast_pairs=15, original_concepts=6, publisher_tests=count,
          visual_review='Agent review; not a human usability study', preserved_native_baseline=baseline['build_id'], design_archives=downloads['artifacts']))
    write('publication-results.json', dict(passed=True, stage='M12.0', qualification='M12-DESIGN-v1', source_commit=site['source_commit'],
          website=browser['website'], github_release=release['url'], workflow_ids=[r['databaseId'] for r in successful],
          current_native_download=latest, design_only=True, new_iso=False, pages_checked=site['pages_checked'], unique_links=site['unique_links'],
          full_audit='website-audit.json', fresh_readback='website-readback.json', browser_readback='public-browser-verification.json',
          downloads='design-downloads.json', diagnostics=[
              {'run':43877002152,'outcome':'Failed: server 502; later successful sync retained separately'},
              {'run':43878853754,'outcome':'Failed: server 429; publisher rate/backoff corrected'},
              {'run':43878959449,'outcome':'Failed: request timeout; bounded safe retries added'},
              {'run':43879309866,'outcome':'Cancelled as superseded by documented publication correction'}]))
    print('PASS: M12.0 design and public delivery; M11.6 remains the native ISO.')

if __name__ == '__main__':
    main()
