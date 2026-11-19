"""Read-only original-package/PE inventory. Never execute a downloaded program."""
import hashlib,json,os,re,struct,subprocess,zipfile
from pathlib import Path
from urllib.request import Request,urlopen
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[2]
SCRATCH=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0'
OUT=ROOT/'evidence/M14/0'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def get(url):
 with urlopen(Request(url,headers={'User-Agent':'EngacerOS-M14-static-inventory'}),timeout=90) as r:return r.read(),r.url

def pe(path):
 b=path.read_bytes()
 def u(fmt,at):return struct.unpack_from('<'+fmt,b,at)[0]
 if len(b)<64 or b[:2]!=b'MZ':return None
 at=u('I',60)
 if at+24>len(b) or b[at:at+4]!=b'PE\0\0':return None
 machine=u('H',at+4);count=u('H',at+6);opt=at+24;magic=u('H',opt);wide=magic==0x20b
 if magic not in (0x10b,0x20b):return None
 dd=opt+(112 if wide else 96);sections=[]
 for i in range(count):
  s=opt+u('H',at+20)+i*40;sections.append((u('I',s+12),max(u('I',s+8),u('I',s+16)),u('I',s+20),u('I',s+16)))
 def rva(r):
  if r<u('I',opt+60):return r
  for start,size,offset,raw in sections:
   if start<=r<start+size:
    assert r-start<raw,'RVA has no original file bytes'
    return offset+r-start
  raise ValueError('Unmapped RVA')
 def string(r):
  start=rva(r);end=b.index(b'\0',start,min(len(b),start+4096));return b[start:end].decode('ascii',errors='replace')
 def directory(n):return (u('I',dd+n*8),u('I',dd+n*8+4)) if n<u('I',dd-4) else (0,0)
 imports=[]
 for delayed in (False,True):
  address,size=directory(13 if delayed else 1)
  if not address:continue
  base=rva(address);step=32 if delayed else 20
  for index in range(256):
   d=base+index*step
   if not any(b[d:d+step]):break
   if delayed:
    assert u('I',d)&1,'Legacy VA delay descriptors require explicit handling';name=u('I',d+4);thunk=u('I',d+16)
   else:name=u('I',d+12);thunk=u('I',d) or u('I',d+16)
   names=[];position=rva(thunk)
   for k in range(65536):
    value=u('Q' if wide else 'I',position+k*(8 if wide else 4))
    if not value:break
    names.append('#'+str(value&65535) if value&(1<<(63 if wide else 31)) else string(value+2))
   imports.append(dict(dll=string(name).lower(),delayed=delayed,symbols=names))
 return dict(file=path.name,sha256=sha(path),bytes=len(b),machine=hex(machine),architecture={0x8664:'x64',0x14c:'x86',0xaa64:'arm64'}.get(machine,'other'),format='PE32+' if wide else 'PE32',subsystem=u('H',opt+68),image_bytes=u('I',opt+56),static_tls=bool(directory(9)[0]),exception_directory=bool(directory(3)[0]),clr_directory=bool(directory(14)[0]),imports=imports)

def main():
 SCRATCH.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
 repo=json.loads(subprocess.check_output(['gh','api','repos/notepad-plus-plus/notepad-plus-plus/releases/tags/v8.9.9.1']))
 assets={x['name']:x for x in repo['assets']};tag=repo['tag_name'];version=tag.removeprefix('v')
 requested=[('notepadpp',assets[f'npp.{version}.Installer.x64.exe']['browser_download_url']),('notepadpp',assets[f'npp.{version}.Installer.x64.msi']['browser_download_url']),('notepadpp',assets[f'npp.{version}.portable.x64.zip']['browser_download_url']),('sumatra','https://www.sumatrapdfreader.org/dl/rel/3.6.1/SumatraPDF-3.6.1-64-install.exe'),('sumatra','https://www.sumatrapdfreader.org/dl/rel/3.6.1/SumatraPDF-3.6.1-64.zip')]
 packages=[]
 for app,url in requested:
  name=url.rsplit('/',1)[1];target=SCRATCH/name
  if target.exists():
   old=json.loads((OUT/'binary-inventory.json').read_text(encoding='utf-8')) if (OUT/'binary-inventory.json').exists() else {}
   final=next((p['resolved_url'] for p in old.get('packages',[]) if p['file']==name and 'resolved_url' in p),url)
  else:data,final=get(url);target.write_bytes(data)
  expected=assets.get(name,{}).get('digest');digest=sha(target)
  if 'old' in locals():
   previous=next((p['sha256'] for p in old.get('packages',[]) if p['file']==name),None)
   if previous:assert previous==digest,'Previously pinned research package changed'
  if expected:assert expected=='sha256:'+digest
  packages.append(dict(app=app,file=name,requested_url=url,resolved_url=final,sha256=digest,bytes=target.stat().st_size,upstream_digest_verified=bool(expected),pe=pe(target)))
  if name.endswith('.zip'):
   folder=SCRATCH/app;folder.mkdir(exist_ok=True)
   with zipfile.ZipFile(target) as archive:
    assert archive.testzip() is None
    for member in archive.infolist():
     assert (folder/member.filename).resolve().is_relative_to(folder.resolve())
    archive.extractall(folder)
  print('Inspected original container:',name,flush=True)
 source=ROOT/'third_party/7zip/7z2606-x64.msi';lock=json.loads((ROOT/'third_party/7zip/provenance.json').read_text(encoding='utf-8'));assert sha(source)==lock['files'][source.name]['sha256']
 packages.append(dict(app='7zip',file=source.name,requested_url=lock['files'][source.name]['url'],sha256=sha(source),bytes=source.stat().st_size,upstream_digest_verified=False,project_lock_verified=True,pe=None))
 folder=SCRATCH/'7zip';folder.mkdir(exist_ok=True)
 subprocess.run(['C:/Program Files/7-Zip/7z.exe','x',str(source),'-o'+str(folder),'-y'],capture_output=True,check=True)
 msi_folder=SCRATCH/'notepadpp-msi';msi_folder.mkdir(exist_ok=True)
 subprocess.run(['C:/Program Files/7-Zip/7z.exe','x',str(SCRATCH/f'npp.{version}.Installer.x64.msi'),'-o'+str(msi_folder),'-y'],capture_output=True,check=True)
 binaries=[]
 for app in ['7zip','notepadpp','notepadpp-msi','sumatra','msi-streams']:
  for path in sorted((SCRATCH/app).rglob('*')):
   if path.is_file() and path.stat().st_size>=64 and path.open('rb').read(2)==b'MZ':
    row=pe(path)
    if row:row.update(app=app,relative_path=path.relative_to(SCRATCH/app).as_posix());binaries.append(row)
 api=(ROOT/'user/windows8/api.c').read_text(encoding='utf-8')
 registered=sorted(set(re.findall(r'API8\((\w+),\d+\)',api)))
 for row in binaries:
  names={s for imp in row['imports'] for s in imp['symbols'] if not s.startswith('#')}
  row['names_absent_from_api8_table']=sorted(names-set(registered))
  row['scope']='Static direct/delayed imports only; name presence does not establish provider match, semantics, dynamic loads or complete dependency closure'
 report=dict(passed=True,stage='M14.0',checked_at=datetime.now(timezone.utc).isoformat(),packages=packages,binaries=binaries,registered_api_names=registered,tools=dict(host_extractor_sha256=sha(Path('C:/Program Files/7-Zip/7z.exe')),inspector_sha256=sha(Path(__file__))),downloaded_apps_executed=False,native_compatibility_proven=False,performance_measurements='Not collected for unsupported GUI apps; baseline protocol and native baseline references are separate')
 (OUT/'binary-inventory.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 print('PASS original-package inventory:',len(packages),'containers;',len(binaries),'PE payloads; no downloaded app execution')

if __name__=='__main__':main()
