"""Retain failed reads while refreshing the current publication and crawl closure."""
import argparse
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import re
import time
from urllib.parse import urldefrag, urlsplit, parse_qs

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('site_audit', ROOT / 'website/brix/audit.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--audit', type=Path, required=True)
    parser.add_argument('--payload', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--stage', type=int, default=0)
    args = parser.parse_args()
    assert 0 <= args.stage <= 12
    report = json.loads(args.audit.read_text(encoding='utf-8'))
    payload = json.loads(args.payload.read_text(encoding='utf-8'))
    results = {r['url']: r for r in report['pages']}
    initial_errors = list(report['page_errors'])
    expected_sources = {}
    required = {audit.SITE+'/', *[audit.SITE+'/blog/'+slug for slug in ('documentation','documentation-archive','downloads','guide-start','guide-install','guide-use','guide-customize','guide-project')]}
    critical_paths = {'docs/milestones/m13.md', 'docs/architecture/desktop-m13.md',
                      'docs/architecture/website-m13.md', 'docs/roadmap/status.md', 'website/README.md'}
    if args.stage:
        suffix = f'm13{args.stage}'
        critical_paths.update({f'docs/milestones/m13-{args.stage}.md',
                              f'docs/handbook/install-{suffix}.md',
                              f'docs/releases/{suffix}-v0.13.{args.stage}.md'})
    seen_critical = set()
    for post in payload['page']['blog']['posts']:
        meta = {item['key']:item['value'] for item in post['meta']}
        path = meta['engine_source_path']
        if path in critical_paths:
            seen_critical.add(path)
        url = audit.SITE+'/blog/'+post['slug']
        required.add(url)
        expected_sources[url] = ('https://github.com/enginsoysal/engacer-os/blob/'+meta['engine_source_commit']+'/'+path
                                 if path.endswith('.md') else 'https://github.com/enginsoysal/engacer-os/tree/'+payload['source_commit'])
    assert seen_critical == critical_paths, 'A current stage article is missing from the publication payload'
    pending = required | {r['url'] for r in initial_errors}
    attempts = []
    while pending:
        url = sorted(pending)[0]
        pending.remove(url)
        assert len(results) < 600
        for attempt in range(3):
            row = audit.fetch(url)
            attempts.append({'url': url, 'attempt': attempt+1, 'status': row['status'], 'error': row.get('error')})
            if row['status'] == 200 and not row.get('soft_404'):
                break
            if attempt < 2:
                time.sleep(2*(attempt+1))
        results[url] = row
        for href in row.get('links', []):
            parsed = urlsplit(href)
            query = parse_qs(parsed.query)
            paging = set(query) == {'page'} and len(query['page']) == 1 and query['page'][0].isdigit() and 1 <= int(query['page'][0]) <= 100
            normalized = urldefrag(href)[0]
            if parsed.netloc == 'engaceros.brixcanvas.com' and (not parsed.query or paging) and not parsed.path.startswith(('/api/', '/_next/')) and normalized not in results:
                pending.add(normalized)
    links = sorted({u for row in results.values() for u in row.get('links', [])})
    errors = [r for r in results.values() if r['status'] != 200 or r.get('soft_404')]
    stale = [u for u in links if urlsplit(u).netloc in audit.OLD_HOSTS or re.search(r'github(?:usercontent)?\.com/enginsoysal/codename-engine-os(?:/|$)', u)]
    branding = []
    for row in results.values():
        if row['status'] != 200:
            continue
        for key, value in {'title': row['title'], **row['meta']}.items():
            if key in ('title','og:title','twitter:title','og:site_name','canonical','og:url') and re.search(r'(?i)\bEngine OS\b|(?:engineos|engacer)\.brixcanvas\.com|github\.com/enginsoysal/codename-engine-os', value):
                branding.append({'url': row['url'], 'field': key, 'value': value})
        if not row['lang'].startswith('en'):
            branding.append({'url': row['url'], 'field': 'lang', 'value': row['lang']})
    provenance_errors = [{'url': url, 'expected': expected} for url, expected in expected_sources.items() if expected not in results[url].get('links', [])]
    report.update(passed=not errors and not stale and not branding and not provenance_errors,
                  checked_at=datetime.now(timezone.utc).isoformat(),
                  source_commit=payload['source_commit'], exact_source_articles_verified=len(expected_sources), initial_page_errors=initial_errors,
                  fresh_readback_attempts=attempts, pages=list(results.values()),
                  pages_checked=len(results), unique_links=len(links),
                  page_errors=errors, stale_links=stale, branding_errors=branding, provenance_errors=provenance_errors)
    args.output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    assert report['passed'], errors or stale or branding or provenance_errors
    print(f"PASS: {len(results)} pages, {len(links)} links; {len(initial_errors)} earlier errors retained, {len(attempts)} fresh reads.")

if __name__ == '__main__':
    main()
