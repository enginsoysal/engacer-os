"""Close research only after exact public archive, native Save and full website proof."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'evidence/M14/0'
def read(p):return json.loads((OUT/p).read_text(encoding='utf-8-sig'))
def main():
 assert not (OUT/'publication-results.json').exists(),'Closed research delivery is immutable'
 accepted=read('acceptance-results.json');downloads=read('downloads.json');release=read('github-release.json');saved=read('native-editor-save.json');browser=read('public-browser-verification.json');site=read('website-readback.json');links=read('website-links.json');source=read('publication-source.json');workflows=read('publication-workflows.json')
 assert all(r['passed'] for r in [accepted,downloads,browser,site,links,source])
 assert accepted['research_only'] and not accepted['new_iso'] and not downloads['new_iso']
 assert release['tag_name']=='m140-v0.14.0-research.2' and release['prerelease'] and not release['draft']
 assert len(release['assets'])==len(downloads['assets'])==2 and downloads['archive_crc_verified']
 assert release['target_commitish']==downloads['source_commit']
 assert all(a['digest']=='sha256:'+next(r['sha256'] for r in downloads['assets'] if r['name']==a['name']) for a in release['assets'])
 assert saved['source_commit']==browser['source_commit']==site['source_commit']==source['source_commit']
 assert saved['home'].startswith('Saved') and saved['recovery'].startswith('Saved')
 assert browser['stage']=='M14.0' and browser['current_native_stage']=='M13.13'
 assert all(browser[k] for k in ['production_search','task_sidebar','ordered_task_navigation','current_guide','matching_download','mobile_menu'])
 assert site['exact_source_articles_verified']>=336 and site['pages_checked']>=512 and not links['broken']
 assert source['document_bytes_verified']>=320
 assert any(w['headSha']==site['source_commit'] and w['conclusion']=='success' for w in workflows)
 for path,digest in accepted['harness_sha256'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest
 tap=(OUT/'publisher-tests.txt').read_text(encoding='utf-8');assert 'tests 46' in tap and 'fail 0' in tap
 latest=json.loads(subprocess.check_output(['gh','api','repos/enginsoysal/engacer-os/releases/latest'],cwd=ROOT));assert latest['tag_name']=='m1313-v0.13.13'
 result=dict(passed=True,stage='M14.0',qualification=accepted['qualification'],research_only=True,new_iso=False,current_native_download='M13.13',source_commit=site['source_commit'],research_source_commit=downloads['source_commit'],research_release=release['html_url'],website='https://engaceros.brixcanvas.com',original_containers=6,original_pe_payloads=23,independent_pe_checks=len(accepted['independent_pe_checks']),native_inputs_unchanged=accepted['native_inputs_unchanged'],pages_checked=site['pages_checked'],exact_source_articles_verified=site['exact_source_articles_verified'],unique_links=site['unique_links'],known_broken=0,unverified_external_references=len(links['unverified']),scope='Investigation/plan/measurement protocol and actual public research delivery only; original GUI app execution and performance remain future stages')
 (OUT/'publication-results.json').write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PASS M14.0 original x64 research, exact corrected archive, full actual website and unchanged current native download')
if __name__=='__main__':main()
