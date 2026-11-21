"""Independently decode durable native registry records on one stopped owned clone."""
import argparse,ctypes as c,hashlib,json,os,re,struct
from pathlib import Path
from fixture1 import StoppedDisk,library
ROOT=Path(__file__).resolve().parents[2]
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--fixture',required=True);args=parser.parse_args();assert re.fullmatch('[0-9a-f]{32}',args.fixture)
 def digest(path):
  value=hashlib.sha256()
  with path.open('rb')as f:
   for chunk in iter(lambda:f.read(1024*1024),b''):value.update(chunk)
  return value.hexdigest()
 disk=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m147-install-native'/args.fixture/'owned.img';assert disk.is_file();before=digest(disk);writes=[]
 # Refuse every write callback, including an unexpected filesystem repair.
 class ReadOnly(StoppedDisk):
  def write(self,*args):writes.append(1);return 1
  def flush(self,*args):return 0
 mounted=ReadOnly(disk,library())
 def read(entry):
  buf=c.create_string_buffer(entry.size);got=c.c_uint();assert mounted.lib.v6_verify(c.byref(mounted.volume),entry.path)==0;assert mounted.lib.v6_read(c.byref(mounted.volume),entry.path,0,buf,entry.size,c.byref(got))==0 and got.value==entry.size;return buf.raw
 try:
  entries={entry.path:entry for entry in mounted.volume.entries if entry.kind==1};root=b'/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}';journal=read(entries[root+b'/product.bin']);native=json.loads((ROOT/'build/m14-native/stage7/install-native/results.json').read_text(encoding='utf-8'));assert native['passed']and hashlib.sha256(journal).hexdigest()==native['journal_sha256'];assert journal[72:104]==hashlib.sha256(journal[:72]+bytes(32)+journal[104:]).digest()
  def text(raw):return raw.split(b'\0')[0].decode('utf-8')
  actual={}
  for path,entry in entries.items():
   if path.startswith(b'/Data/Windows/')and b'/Registry/'in path and path.rsplit(b'/',1)[-1].startswith(b'v'):
    raw=read(entry);assert 1552<=len(raw)<=3600,(path.decode(),len(raw));magic,kind,n=struct.unpack_from('<QII',raw);assert magic==0x315652454734314d and n<=2048 and len(raw)==1552+n,(path.decode(),hex(magic),n);identity=(text(raw[16:272]),text(raw[272:1040]),text(raw[1040:1296]));assert identity not in actual;actual[identity]=(kind,raw[1552:1552+n])
  checked=[];at=1024
  while at<len(journal):
   kind,n=struct.unpack_from('<II',journal,at)
   if kind==2:
    root,view,aftertype,beforetype,afterbytes,beforebytes,keybytes,namebytes,exists,reserved=struct.unpack_from('<10I',journal,at+8);pos=at+48;key=text(journal[pos:pos+keybytes]);name=text(journal[pos+keybytes:pos+keybytes+namebytes]);expected=journal[pos+keybytes+namebytes:pos+keybytes+namebytes+afterbytes];owner='/Users/Owner'if root==1 else'/Machine/'+str(view);assert actual[(owner,key.lower(),name.lower())]==(aftertype,expected),(owner,key,name);checked.append(dict(root=root,view=view,key=key,name=name,type=aftertype,bytes=afterbytes,sha256=hashlib.sha256(expected).hexdigest()))
   at+=n
  assert len(checked)==16 and at==len(journal)
 finally:mounted.close()
 assert not writes and digest(disk)==before
 out=ROOT/'build/m14-native/stage7/install-native/registry-readback.json';out.write_bytes((json.dumps(dict(passed=True,build_id=native['build_id'],journal_sha256=native['journal_sha256'],scope=__doc__,checked=checked,write_callbacks_refused=True,whole_disk_sha_checked=before is not None,observer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n').encode());print('PASS independent durable native registry readback',len(checked))
if __name__=='__main__':main()
