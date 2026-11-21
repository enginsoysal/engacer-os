"""Read-only selected original WiX call-site/import attribution; never execute PE."""
import argparse,hashlib,json,os,struct
from pathlib import Path

def inspect(return_rva):
 path=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/msi-streams/npp.8.9.9.1.Installer.x64/Wix4UtilCA_X64.bin'
 data=path.read_bytes();digest=hashlib.sha256(data).hexdigest();assert digest=='54febbd1f0a3875df16a4b88621cc0a10729b3c94b9a68639aab27d36fe39381'
 header=struct.unpack_from('<I',data,60)[0];assert data[header:header+4]==b'PE\0\0';count=struct.unpack_from('<H',data,header+6)[0];optional=header+24;assert struct.unpack_from('<H',data,optional)[0]==0x20b;sections=optional+struct.unpack_from('<H',data,header+20)[0]
 def rva(address):
  for i in range(count):
   size,start,raw,position=struct.unpack_from('<IIII',data,sections+40*i+8)
   if start<=address<start+max(size,raw):assert address-start<raw;return position+address-start
  raise ValueError('Address has no original file bytes')
 def text(address):
  start=rva(address);end=data.index(b'\0',start);return data[start:end].decode('ascii')
 table={};at=rva(struct.unpack_from('<I',data,optional+120)[0])
 while any(data[at:at+20]):
  original,_,_,name,iat=struct.unpack_from('<IIIII',data,at);pos=rva(original);i=0
  while True:
   value=struct.unpack_from('<Q',data,pos+i*8)[0]
   if not value:break
   table[iat+i*8]=(text(name),'#'+str(value&65535)if value>>63 else text(value+2));i+=1
  at+=20
 before=rva(return_rva);target=None;via=[]
 if data[before-6:before-4]==b'\xff\x15':target=return_rva+struct.unpack_from('<i',data,before-4)[0]
 elif data[before-5]==0xe8:
  thunk=return_rva+struct.unpack_from('<i',data,before-4)[0];via.append(thunk);position=rva(thunk)
  if data[position:position+3]==b'\x48\xff\x25':target=thunk+7+struct.unpack_from('<i',data,position+3)[0]
  elif data[position:position+2]==b'\xff\x25':target=thunk+6+struct.unpack_from('<i',data,position+2)[0]
  elif data[position:position+3]==b'\x48\x8d\x0d'and data[position+7:position+10]==b'\x48\xff\x25':target=thunk+14+struct.unpack_from('<i',data,position+10)[0]
 if target not in table:raise ValueError('Call does not resolve through a recognized original import thunk')
 dll,symbol=table[target];return dict(scope='Original bytes and relative call/import metadata only; no host PE execution',original_sha256=digest,return_rva=hex(return_rva),thunks=[hex(v)for v in via],iat_rva=hex(target),dll=dll,symbol=symbol)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--return-rva',required=True,type=lambda s:int(s,0));args=parser.parse_args();print(json.dumps(inspect(args.return_rva),indent=2))
