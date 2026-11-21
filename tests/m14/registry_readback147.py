"""Independent read-only decoding of committed native MSI registry effects."""
import ctypes as c,hashlib,struct
from fixture1 import StoppedDisk,library

def check_registry147(disk,journal,removed=False):
 writes=[]
 class ReadOnly(StoppedDisk):
  def write(self,*args):writes.append(1);return 1
  def flush(self,*args):return 0
 mounted=ReadOnly(disk,library())
 def text(raw):return raw.split(b'\0')[0].decode('utf-8')
 def read(entry):
  assert entry.size<=3600;buffer=c.create_string_buffer(entry.size);got=c.c_uint();assert mounted.lib.v6_verify(c.byref(mounted.volume),entry.path)==0;assert mounted.lib.v6_read(c.byref(mounted.volume),entry.path,0,buffer,entry.size,c.byref(got))==0 and got.value==entry.size;return buffer.raw
 try:
  actual={}
  for entry in mounted.volume.entries:
   path=entry.path
   if entry.kind==1 and path.startswith(b'/Data/Windows/') and b'/Registry/'in path and path.rsplit(b'/',1)[-1].startswith(b'v'):
    raw=read(entry);assert 1552<=len(raw)<=3600;magic,kind,n=struct.unpack_from('<QII',raw);assert magic==0x315652454734314d and n<=2048 and len(raw)==1552+n;identity=(text(raw[16:272]),text(raw[272:1040]),text(raw[1040:1296]));assert identity not in actual;actual[identity]=(kind,raw[1552:])
  assert len(journal)>=1024 and journal[72:104]==hashlib.sha256(journal[:72]+bytes(32)+journal[104:]).digest();checked=[];at=1024
  while at<len(journal):
   kind,n=struct.unpack_from('<II',journal,at);assert n>=8 and not n%8 and at+n<=len(journal)
   if kind==2:
    root,view,aftertype,beforetype,afterbytes,beforebytes,keybytes,namebytes,exists,reserved=struct.unpack_from('<10I',journal,at+8);pos=at+48;key=text(journal[pos:pos+keybytes]);name=text(journal[pos+keybytes:pos+keybytes+namebytes]);data=pos+keybytes+namebytes;owner='/Users/Owner'if root==1 else'/Machine/'+str(view);identity=(owner,key.lower(),name.lower())
    if removed and not exists:assert identity not in actual,(identity,'Unexpected registry value survived removal');expected=b'';value_type=None
    else:
     expected=journal[data+afterbytes:data+afterbytes+beforebytes]if removed else journal[data:data+afterbytes];value_type=beforetype if removed else aftertype;assert actual.get(identity)==(value_type,expected),(identity,'Durable bytes differ from immutable ownership')
    checked.append(dict(owner=owner,key=key,name=name,type=value_type,bytes=len(expected),sha256=hashlib.sha256(expected).hexdigest(),absent=removed and not exists))
   at+=n
  assert at==len(journal) and not writes;return dict(phase='removed'if removed else'installed',checked=checked,write_callbacks_refused=True)
 finally:mounted.close()
