"""Publish and independently read back a research-only archive; never replace media."""
import hashlib,json,posixpath,re,subprocess,sys,time,zipfile
from pathlib import Path
from urllib.parse import quote,urlsplit
from urllib.request import Request,urlopen
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'evidence/M14/0';TAG='m140-v0.14.0-research.2'
def run(*args):return subprocess.check_output(list(args),cwd=ROOT)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,r):p.write_bytes((json.dumps(r,indent=2)+'\n').encode())

def main():
 accepted=json.loads((OUT/'acceptance-results.json').read_text(encoding='utf-8'));assert accepted['passed'] and accepted['research_only'] and not accepted['new_iso']
 assert not run('git','status','--porcelain','--untracked-files=no').strip(),'Commit the research source and reports first'
 ref=run('git','rev-parse','HEAD').decode().strip()
 for path,digest in accepted['harness_sha256'].items():assert sha(ROOT/path)==digest
 work=ROOT/'build/m14/stage0';work.mkdir(parents=True,exist_ok=True)
 archive=ROOT/'dist/EngacerOS-M14.0-Research-2.zip';checksum=ROOT/'dist/M14.0-Research-2-SHA256SUMS.txt'
 run('git','archive','--format=zip','--prefix=EngacerOS-M14.0-Research/','--output='+str(archive),ref,'LICENSE','docs/milestones/m14.md','docs/milestones/m14-0.md','docs/milestones/m14-progress.json','docs/architecture/windows-m14.md','docs/roadmap/m14-targets.json','docs/handbook/windows-m140.md','docs/releases/m140-v0.14.0-research.md','tools/m14','tests/m14','evidence/M14/0')
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None and not any(Path(n).suffix.lower() in ['.exe','.dll','.msi','.iso'] for n in z.namelist())
  prefix='EngacerOS-M14.0-Research/'
  for path,digest in accepted['harness_sha256'].items():assert hashlib.sha256(z.read(prefix+path)).hexdigest()==digest,('Archived observer bytes changed',path)
  assert hashlib.sha256(z.read(prefix+'evidence/M14/0/task-corpus.json')).hexdigest()==accepted['task_corpus_sha256'],'Archived corpus receipt bytes changed'
 checksum.write_bytes((sha(archive)+'  '+archive.name+'\n').encode())
 note_path='docs/releases/m140-v0.14.0-research.md';body=run('git','show',ref+':'+note_path).decode('utf-8')
 def link(m):
  label,target=m.groups()
  if urlsplit(target).scheme or target.startswith('#'):return m.group(0)
  p=posixpath.normpath(posixpath.join(posixpath.dirname(note_path),target));run('git','cat-file','-e',ref+':'+p)
  return label+'(https://github.com/enginsoysal/engacer-os/blob/'+ref+'/'+quote(p,safe='/')+')'
 notes=work/'release-notes.md';notes.write_bytes(re.sub(r'(\[[^\]]*\])\(([^)]+)\)',link,body).encode())
 sys.path.insert(0,str(ROOT/'tools/release'));from publish13 import lookup_release
 release=lookup_release(TAG)
 if release is None:
  run('gh','release','create',TAG,'--draft','--prerelease','--target',ref,'--title',body.splitlines()[0].removeprefix('# '),'--notes-file',str(notes))
  for _ in range(5):
   release=lookup_release(TAG)
   if release:break
   time.sleep(1)
 assert release and release['target_commitish']==ref and release['body'].replace('\r\n','\n')==notes.read_text(encoding='utf-8').replace('\r\n','\n')
 assets=[archive,checksum];expected={p.name:(p.stat().st_size,sha(p)) for p in assets}
 if release['draft']:
  current={a['name']:a for a in release['assets']};assert set(current)<=set(expected)
  missing=[str(p) for p in assets if p.name not in current]
  if missing:run('gh','release','upload',TAG,*missing)
  record=json.loads(run('gh','api','repos/enginsoysal/engacer-os/releases/'+str(release['id'])))
  assert {a['name'] for a in record['assets']}==set(expected)
  for a in record['assets']:assert (a['size'],a['digest'])==(expected[a['name']][0],'sha256:'+expected[a['name']][1])
  run('gh','release','edit',TAG,'--draft=false','--prerelease','--latest=false')
 release=json.loads(run('gh','api','repos/enginsoysal/engacer-os/releases/'+str(release['id'])))
 assert not release['draft'] and release['prerelease'] and len(release['assets'])==2
 downloaded=[]
 for asset in release['assets']:
  with urlopen(Request(asset['browser_download_url'],headers={'User-Agent':'EngacerOS-research-readback'}),timeout=90) as response:data=response.read()
  assert hashlib.sha256(data).hexdigest()==expected[asset['name']][1]
  target=work/asset['name'];target.write_bytes(data)
  if target.suffix=='.zip':
   with zipfile.ZipFile(target) as z:assert z.testzip() is None
  downloaded.append(dict(name=asset['name'],sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),independently_downloaded=True))
 write(OUT/'github-release.json',release)
 write(OUT/'downloads.json',dict(passed=True,stage='M14.0',source_commit=ref,research_only=True,new_iso=False,current_native_download='M13.13',release=release['html_url'],assets=downloaded,archive_crc_verified=True))
 print('PASS research-only prerelease, two immutable assets, independent downloads/ZIP CRC; native download remains M13.13')

if __name__=='__main__':main()
