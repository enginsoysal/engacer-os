"""Resolve a recorded original AMD64 indirect-import return RVA without execution."""
import argparse,json,os,struct,hashlib
from pathlib import Path
def inspect(path,rva):
 b=path.read_bytes();u16=lambda at:struct.unpack_from('<H',b,at)[0];u32=lambda at:struct.unpack_from('<I',b,at)[0]
 pe=u32(0x3c);assert b[pe:pe+4]==b'PE\0\0' and u16(pe+4)==0x8664
 opt=pe+24;assert u16(opt)==0x20b
 sections=[struct.unpack_from('<IIII',b,opt+u16(pe+20)+i*40+8)for i in range(u16(pe+6))]
 def offset(r):
  for size,va,raw,at in sections:
   if va<=r<va+max(size,raw):assert r-va<raw;return at+r-va
  raise AssertionError(('RVA is not backed by original file',hex(r)))
 def string(r):return b[offset(r):].split(b'\0',1)[0].decode('ascii')
 at=offset(rva-6);assert b[at:at+2]==b'\xff\x15','Expected original RIP-relative import call'
 slot=rva+struct.unpack_from('<i',b,at+2)[0]
 desc=u32(opt+120)
 while True:
  fields=struct.unpack_from('<5I',b,offset(desc))
  if not any(fields):break
  original,_,_,name,iat=fields;index=0
  while True:
   thunk=struct.unpack_from('<Q',b,offset(original or iat)+index*8)[0]
   if not thunk:break
   if iat+index*8==slot:
    return dict(original_sha256=hashlib.sha256(b).hexdigest(),return_rva=hex(rva),iat_rva=hex(slot),dll=string(name),symbol=('ordinal:'+str(thunk&65535))if thunk>>63 else string(thunk+2),scope='Static original import identity, not API execution qualification')
   index+=1
  desc+=20
 raise AssertionError(('Import slot not found',hex(slot)))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('return_rva',type=lambda x:int(x,0));a=p.parse_args()
 path=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/SumatraPDF-3.6.1-64-install.exe'
 print(json.dumps(inspect(path,a.return_rva),indent=2))
