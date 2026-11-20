"""Read-only direct-IAT call-site diagnosis; never execute an app or guess a name."""
import re,struct
from resource144_host import mapped

def decode(path,text):
 match=re.search(r'Unavailable Win32 API caller=0x([0-9a-f]+) main=0x([0-9a-f]+)',text)
 if not match:return None
 caller,base=(int(v,16)for v in match.groups());image,_,_=mapped(path);rva=caller-base
 result=dict(caller=f'{caller:016x}',main=f'{base:016x}',resolved=False)
 if not 6<=rva<len(image):return{**result,'reason':'Caller is outside the main image'}
 result['return_rva']=rva;slot=None
 if image[rva-6:rva-4]==b'\xff\x15':slot=rva+struct.unpack_from('<i',image,rva-4)[0]
 elif image[rva-5]==0xe8:
  thunk=rva+struct.unpack_from('<i',image,rva-4)[0]
  if 0<=thunk<len(image)-6 and image[thunk:thunk+2]==b'\xff\x25':slot=thunk+6+struct.unpack_from('<i',image,thunk+2)[0]
 if slot is None:return{**result,'reason':'No direct IAT call or simple import thunk; no symbol guessed'}
 pe=struct.unpack_from('<I',image,60)[0];directory,size=struct.unpack_from('<II',image,pe+24+120)
 def string(at):
  assert 0<=at<len(image);end=image.index(0,at,min(len(image),at+256));return bytes(image[at:end]).decode('ascii')
 for offset in range(0,min(size,20480),20):
  lookup,_,_,name,address=struct.unpack_from('<5I',image,directory+offset)
  if not name:break
  if slot<address or(slot-address)%8:continue
  for index in range(4096):
   at=(lookup or address)+index*8
   if not 0<=at<=len(image)-8:break
   value=struct.unpack_from('<Q',image,at)[0]
   if not value:break
   if slot!=address+index*8:continue
   symbol='#'+str(value&65535)if value>>63 else string(value+2)
   return{**result,'resolved':True,'iat_rva':slot,'dll':string(name).lower(),'symbol':symbol}
 return{**result,'reason':'Call slot did not identify an imported symbol'}
