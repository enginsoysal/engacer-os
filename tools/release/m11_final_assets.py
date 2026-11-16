"""Prepare the complete final release only after matching native acceptance."""
import hashlib,json,shutil,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/build'))
from m8 import privacy_input

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8'))

def main():
 dist=ROOT/'dist';meta=load(dist/'m11final-build-manifest.json');starter=load(dist/'m11final-starter-manifest.json');accepted=load(ROOT/'evidence/M11/6/acceptance-results.json')
 assert accepted['passed'] and accepted['qualification']=='M11-FINAL-VM-v1'
 assert accepted['build_id']==meta['build_id']==starter['build_id'] and accepted['vmware_zip_sha256']==starter['sha256']
 assets=[dist/name for name in meta['artifacts']]
 for p in assets:assert sha(p)==meta['artifacts'][p.name]['sha256']
 archive=dist/starter['archive'];assert sha(archive)==starter['sha256'];assets.append(archive)
 assets += [dist/'m11final-build-manifest.json',dist/'m11final-starter-manifest.json']
 notice=dist/'EngacerOS-M11FINAL-THIRD-PARTY-NOTICES.txt'
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None;notice.write_bytes(z.read('EngacerOS/THIRD-PARTY-NOTICES.txt'))
 assets.append(notice)
 for source,name in [('third_party/7zip/7z2606-src.tar.xz','7z2606-src.tar.xz'),('third_party/libmspack/COPYING.LIB','COPYING.LIB')]:
  p=dist/name;shutil.copyfile(ROOT/source,p);assert sha(p)==sha(ROOT/source);assets.append(p)
 assert len(assets)==19 and len({p.name for p in assets})==19
 checks=dist/'M11FINAL-SHA256SUMS.txt';checks.write_bytes(''.join(sha(p)+'  '+p.name+'\n' for p in sorted(assets)).encode());assets.append(checks)
 for p in assets:
  data=privacy_input(p.read_bytes());assert b'C:\\Users\\' not in data and b'C:/Users/' not in data,p.name
 result={'build_id':meta['build_id'],'qualification':accepted['qualification'],'assets':[{'name':p.name,'sha256':sha(p),'size':p.stat().st_size} for p in sorted(assets)]}
 out=ROOT/'build/m11/release';out.mkdir(parents=True,exist_ok=True);(out/'assets.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
 print('Prepared 20 matching final release assets, including complete 19-file checksums.')
if __name__=='__main__':main()
