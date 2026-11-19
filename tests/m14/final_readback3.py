"""Verify the closing text sync without rewriting the accepted full-crawl receipt."""
import argparse,hashlib,importlib.util,json,posixpath,re,subprocess,sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import unquote,urlsplit
from urllib.request import Request,urlopen

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tests/m13'))
from close_stage import verify_inputs_at_commit
spec=importlib.util.spec_from_file_location('final_audit143',ROOT/'website/brix/audit.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)

def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--source',required=True);parser.add_argument('--workflow',required=True);args=parser.parse_args()
    ref=git('rev-parse',args.source+'^{commit}').decode().strip()
    out=ROOT/'evidence/M14/3'
    closed=json.loads((out/'publication-results.json').read_text(encoding='utf-8'))
    assert closed['passed'] and closed['pages_checked']>=closed['exact_source_articles_verified']>=335
    workflow=json.loads(subprocess.check_output(['gh','run','view',args.workflow,'--json','databaseId,headSha,status,conclusion'],cwd=ROOT))
    assert workflow['headSha']==ref and workflow['status']=='completed' and workflow['conclusion']=='success'
    meta=json.loads((ROOT/'dist/m14stage3-build-manifest.json').read_text(encoding='utf-8'))
    verify_inputs_at_commit(ref,meta['source_sha256'])
    verify_inputs_at_commit(closed['release_source_commit'],meta['source_sha256'])
    progress=json.loads(git('show',ref+':docs/milestones/m14-progress.json'))
    assert progress['current_native_download']=='M14.3'
    stage=next(row for row in progress['stages'] if row['id']=='M14.3')
    assert stage['status']=='complete' and stage['publication_evidence']=='evidence/M14/3/publication-results.json'
    payload=json.loads((ROOT/'build/brix/m143-closing-content.json').read_text(encoding='utf-8'))
    posts={next(m['value'] for m in post['meta'] if m['key']=='engine_source_path'):post for post in payload['page']['blog']['posts']}
    changed=git('diff','--name-only',closed['source_commit'],ref).decode().splitlines()
    paths=[p for p in changed if p.endswith('.md') and p in posts]
    assert len(paths)>=8
    tracked=set(git('ls-tree','-r','--name-only',ref).decode().splitlines())
    relative_links=0
    for path in paths:
        text=git('show',ref+':'+path).decode('utf-8')
        for href in re.findall(r'\]\(([^)]+)\)',text):
            href=href.strip('<>');parsed=urlsplit(href)
            if parsed.scheme or not parsed.path:continue
            target=posixpath.normpath(posixpath.join(posixpath.dirname(path),unquote(parsed.path)))
            assert target in tracked,(path,target)
            relative_links+=1
    def one(path):
        url=audit.SITE+'/blog/'+posts[path]['slug']
        with urlopen(Request(url,headers={'User-Agent':'EngacerOS-final-source-readback'}),timeout=45) as response:
            raw=response.read();assert response.status==200
        page=audit.Page();page.feed(raw.decode('utf-8'))
        edit=git('log','-1','--format=%H',ref,'--',path).decode().strip()
        source='https://github.com/enginsoysal/engacer-os/blob/'+edit+'/'+path
        assert source in page.links,(path,'Current exact-source link missing')
        assert page.lang.startswith('en')
        if path=='website/README.md':assert 'Current native delivery is M14.3' in page.text and 'Historical portal records' in page.text
        if path=='docs/handbook/vmware-storage.md':
            assert page.title==['VMware disks and installation storage'] or 'VMware disks and installation storage' in ''.join(page.title)
            assert '(historical)' not in ''.join(page.title).lower()
            assert 'Current M14.3 installer' in page.text and 'Historical M4.5 console troubleshooting' in page.text
        if path in ('CONTRIBUTING.md','tools/README.md','distros/README.md'):
            assert 'M14.3' in page.text or 'Current M14 desktop recipes' in page.text
        if path=='docs/architecture/loader-m141.md':assert '2,048 pages' in page.text
        if path in ('README.md','docs/roadmap/status.md','docs/handbook/index.md'):assert 'Complete actual website verification passes' in page.text
        return dict(path=path,url=url,status=200,source=source,source_sha256=hashlib.sha256(git('show',ref+':'+path)).hexdigest(),observed_html_sha256=hashlib.sha256(raw).hexdigest())
    with ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(one,paths))
    home=audit.fetch(audit.SITE+'/');assert home['status']==200 and not home.get('soft_404')
    assert any('/releases/' not in link and '/blog/downloads' in link for link in home['links'])
    latest=json.loads(subprocess.check_output(['gh','api','repos/enginsoysal/engacer-os/releases/latest'],cwd=ROOT))
    assert latest['tag_name']=='m143-v0.14.3' and len(latest['assets'])==20
    result=dict(passed=True,stage='M14.3',checked_at=datetime.now(timezone.utc).isoformat(),source_commit=ref,full_crawl_source=closed['source_commit'],build_id=meta['build_id'],frozen_native_inputs_verified=len(meta['source_sha256']),changed_published_articles_verified=rows,changed_source_relative_links_verified=relative_links,workflow=workflow,latest_release=latest['tag_name'],home_status=200,scope='Closing documentation text/source updates after the accepted complete current-source crawl; native media and public layout/navigation are unchanged')
    (out/'final-source-readback.json').write_bytes((json.dumps(result,indent=2)+'\n').encode('utf-8'))
    print('PASS final current-source sync:',len(rows),'changed articles;',relative_links,'source links; all',len(meta['source_sha256']),'native inputs unchanged')

if __name__=='__main__':main()
