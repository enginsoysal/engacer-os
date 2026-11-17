"""Publish a qualified M13 stage; resume matching drafts, never replace public media.

Default is validation only. --publish executes the owner's authorized delivery.
Website Save/readback and close_stage remain separate gates before the next build.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];REPO='enginsoysal/engacer-os'

def read(path):return json.loads(path.read_text(encoding='utf-8'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def run(*args):return subprocess.check_output(list(args),cwd=ROOT).decode('utf-8')

def api_json(path,missing=False,paginate=False):
    args=['gh','api',path]+(['--paginate','--slurp'] if paginate else [])
    result=subprocess.run(args,cwd=ROOT,capture_output=True)
    if result.returncode:
        if missing and b'HTTP 404' in result.stderr:return None
        raise RuntimeError('Release API read failed; no release is created or replaced: '+result.stderr.decode('utf-8',errors='replace'))
    return json.loads(result.stdout)

def lookup_release(tag,request=api_json):
    """Authenticated tag lookup can hide drafts; resolve their exact listed ID.

    Only a successful complete listing can establish absence. Permission/network
    failures never authorize creation, and a public release remains immutable.
    """
    base=f'repos/{REPO}/releases'
    release=request(base+'/tags/'+tag,missing=True)
    if release is None:
        pages=request(base+'?per_page=100',paginate=True)
        matches=[row for page in pages for row in page if row['tag_name']==tag]
        assert len(matches)<=1,'Duplicate matching release records'
        if not matches:return None
        release=request(base+'/'+str(matches[0]['id']))
        assert release['id']==matches[0]['id'],'Listed release identity changed'
    assert release['tag_name']==tag,'Release tag changed'
    return release

def check_release(release,expected,reference,body,draft):
    assert release['draft']==draft and not release['prerelease'],'Unexpected release visibility'
    assert release['target_commitish']==reference,'Release targets different source'
    assert release['body'].replace('\r\n','\n')==body.replace('\r\n','\n'),'Release notes differ'
    records={a['name']:a for a in expected};assert len(records)==20
    names=set()
    for asset in release['assets']:
        name=asset['name'];assert name not in names and name in records,'Unexpected or duplicate asset';names.add(name)
        row=records[name];assert asset['size']==row['size'] and asset['digest']=='sha256:'+row['sha256'],name
    if not draft:assert len(names)==20,'Incomplete public release'
    return [row['name'] for row in expected if row['name'] not in names]

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--stage',type=int,required=True);p.add_argument('--publish',action='store_true');stage=p.parse_args();number=stage.stage;assert 1<=number<=12
    work=ROOT/f'build/m13/stage{number}';evidence=ROOT/f'evidence/M13/{number}';tag=f'm13{number}-v0.13.{number}'
    assert not (evidence/'publication-results.json').exists(),'This stage is already closed and immutable'
    previous=ROOT/('evidence/M13/0/closure-publication.json' if number==1 else f'evidence/M13/{number-1}/publication-results.json')
    assert read(previous)['passed']
    accepted=read(evidence/'acceptance-results.json');visual=read(evidence/'visual-review.json');assets=read(work/'release-assets.json');notes=read(work/'release-notes.json');body=(work/'release-notes.md').read_text(encoding='utf-8')
    assert accepted['passed'] and visual['passed'] and accepted['stage']==f'M13.{number}'
    assert accepted['build_id']==visual['build_id']==assets['build_id'] and assets['qualification']==f'M13-STAGE{number}-VM-v1'
    assert len(assets['assets'])==len({a['name'] for a in assets['assets']})==20
    assert notes['encoding']=='UTF-8' and sha(work/'release-notes.md')==notes['sha256']
    reference=run('git','rev-parse','HEAD').strip();assert reference==notes['source_commit']
    assert not run('git','status','--porcelain','--untracked-files=no').strip(),'Commit source, evidence and manuals first'
    assert json.loads(run('gh','repo','view','--json','nameWithOwner'))['nameWithOwner']==REPO
    sys.path.insert(0,str(ROOT/'tests/m12'));from verify_components import git_inputs
    git_inputs(read(ROOT/f'dist/m13stage{number}-build-manifest.json')['source_sha256'])
    for row in assets['assets']:
        path=ROOT/'dist'/row['name'];assert path.name==row['name'] and path.is_file() and path.stat().st_size==row['size'] and sha(path)==row['sha256']
    if not stage.publish:print('PASS: committed qualified source, UTF-8 notes and twenty assets; no external change.');return
    release=lookup_release(tag)
    if release is None:
        run('gh','release','create',tag,'--draft','--target',reference,'--title',body.splitlines()[0].removeprefix('# '),'--notes-file',str(work/'release-notes.md'))
        release=lookup_release(tag)
        assert release is not None,'Created draft is not readable; stop before uploads'
    endpoint=f'repos/{REPO}/releases/'+str(release['id'])
    missing=check_release(release,assets['assets'],reference,body,True)
    if missing:run('gh','release','upload',tag,*[str(ROOT/'dist'/name) for name in missing])
    release=json.loads(run('gh','api',endpoint));assert not check_release(release,assets['assets'],reference,body,True),'Incomplete draft'
    run('gh','release','edit',tag,'--draft=false','--latest')
    release=json.loads(run('gh','api',endpoint));check_release(release,assets['assets'],reference,body,False)
    target=json.loads(run('gh','api',f'repos/{REPO}/git/ref/tags/{tag}'));assert target['object']['type']=='commit' and target['object']['sha']==reference
    (evidence/'github-tag.json').write_bytes((json.dumps(target,indent=2)+'\n').encode())
    print('Published '+release['html_url']+' with twenty matching immutable assets. Run independent download and complete website verification next.')

if __name__=='__main__':main()
