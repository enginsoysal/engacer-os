"""Record native/public-asset completion without hiding the failed homepage Save."""
import hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 out=ROOT/'evidence/M14/8'
 def read(p):return json.loads(p.read_text(encoding='utf-8'))
 a=read(out/'acceptance-results.json');d=read(out/'downloads.json');v=read(out/'visual-review.json');r=read(out/'website-readback.json');links=read(out/'website-links.json');home=read(out/'homepage-blocker.json')
 assert all(x['passed']for x in (a,d,v,r,links))
 assert not links['broken']and not r['page_errors']and not r['provenance_errors']
 assert a['build_id']==d['build_id']==v['build_id']
 assert a['campaign_tasks']==147 and a['source_inputs']==825
 assert len(a['native_groups'])==105 and len(a['host_groups'])==41
 assert len(d['artifacts'])==20 and d['downloaded_zip_crc']
 assert all(x['downloaded_bytes']==x['size']and x['downloaded_sha256']==x['sha256']for x in d['artifacts'])
 for p,digest in v['capture_sha256'].items():assert hashlib.sha256((out/p).read_bytes()).hexdigest()==digest
 manifest=read(ROOT/'dist/m14stage8-build-manifest.json')
 assert d['downloaded_iso_sha256']==manifest['artifacts']['EngacerOS-M14STAGE8.iso']['sha256']
 assert d['downloaded_zip_sha256']==a['vmware_zip_sha256']
 sys.path.insert(0,str(ROOT/'tests/m14'));from close7_scoped import verify_inputs_at_commit
 refs={ref:verify_inputs_at_commit(ref,manifest['source_sha256'])for ref in (manifest['source_commit'],'m148-v0.14.8',r['source_commit'])}
 workflows=json.loads(subprocess.check_output(['gh','run','list','--workflow','brixcanvas-docs.yml','--limit','5','--json','databaseId,headSha,status,conclusion'],cwd=ROOT))
 assert any(w['headSha']==r['source_commit']and w['status']=='completed'and w['conclusion']=='success'for w in workflows)
 (out/'publication-workflows.json').write_bytes((json.dumps(workflows,indent=2)+'\n').encode())
 release=read(out/'github-release.json');tag=read(out/'github-tag.json');notes=read(ROOT/'build/m14-native/stage8/release-notes.json')
 assert not release['draft']and release['tag_name']==d['latest']=='m148-v0.14.8'
 assert tag['object']['sha']==notes['source_commit']
 assert release['body'].replace('\r\n','\n')==(ROOT/'build/m14-native/stage8/release-notes.md').read_text(encoding='utf-8').replace('\r\n','\n')
 assert not home['passed']and home['still_contains_previous_download']and home['still_contains_old_future_plan']
 progress=read(ROOT/'docs/milestones/m14-progress.json');assert all(s['status']=='planned'for s in progress['stages']if s['id']in ['M14.'+str(n)for n in range(9,17)])
 result=dict(passed=False,stage='M14.8',status='native_released_publication_partial_owner_stop',checked_at=datetime.now(timezone.utc).isoformat(),build_id=a['build_id'],native_source_media_passed=True,campaign_tasks=147,native_groups=105,host_groups=41,public_downloads_passed=True,public_assets=20,public_article_content_passed=True,public_link_targets_passed=True,website_source_commit=r['source_commit'],public_pages=r['pages_checked'],exact_source_articles=r['exact_source_articles_verified'],public_links=r['unique_links'],known_broken_targets=0,unverified_external_references=len(links['unverified']),native_homepage_save_passed=False,full_publication_complete=False,remaining=['Native BrixCanvas homepage Save returns a website-read error; the public homepage still has the previous download badge and obsolete future-plan copy.','Reported advanced platform search/navigation remains unqualified.'],source_bindings=refs,owner_stop_after='M14.8',future_implementation_started=False,scope='Native milestone implementation and GitHub delivery are complete within their documented scope. Do not claim complete website publication or start M14.9. Preserve the combined platform report.',observer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
 target=out/'publication-results.json';assert not target.exists();target.write_bytes((json.dumps(result,indent=2)+'\n').encode())
 print('Recorded qualified native M14.8, twenty verified public assets, complete article/link checks and the unhidden homepage blocker. Stop before M14.9.')
if __name__=='__main__':main()
