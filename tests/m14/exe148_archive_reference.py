"""Read/hash the pinned original PE resource archive with an independent host decoder; never execute or deploy it."""
import hashlib,json,lzma,os,struct,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ORIGINAL='1eee71cccd2ea6e94d5bcea54ee2f759844da3e1a0ee2f6045035b1d17b94381'
def main():
 path=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/SumatraPDF-3.6.1-64-install.exe';data=path.read_bytes();assert len(data)==11075960 and hashlib.sha256(data).hexdigest()==ORIGINAL
 def u16(at):assert 0<=at<=len(data)-2;return struct.unpack_from('<H',data,at)[0]
 def u32(at):assert 0<=at<=len(data)-4;return struct.unpack_from('<I',data,at)[0]
 assert data[:2]==b'MZ';pe=u32(60);assert data[pe:pe+4]==b'PE\0\0'and u16(pe+4)==0x8664 and u16(pe+24)==0x20b
 count=u16(pe+6);assert 0<count<=96;section_table=pe+24+u16(pe+20);sections=[]
 for index in range(count):
  at=section_table+index*40;sections.append((u32(at+12),u32(at+16),u32(at+20)))
 def offset(rva,length):
  matches=[raw+rva-base for base,size,raw in sections if base<=rva and rva-base+length<=size];assert len(matches)==1 and matches[0]+length<=len(data);return matches[0]
 resource_rva=u32(pe+24+112+16);resource_bytes=u32(pe+24+112+20);resource=offset(resource_rva,resource_bytes);leaves=[]
 def walk(relative,depth,identity):
  assert depth<=3 and relative+16<=resource_bytes;at=resource+relative;entries=u16(at+12)+u16(at+14);assert entries<=256 and relative+16+entries*8<=resource_bytes
  for i in range(entries):
   name=u32(at+16+i*8);child=u32(at+20+i*8);key=name if not name&0x80000000 else 'named'
   if child&0x80000000:walk(child&0x7fffffff,depth+1,identity+[key])
   else:
    assert child+16<=resource_bytes;entry=resource+child;rva=u32(entry);size=u32(entry+4);start=offset(rva,size);leaves.append((identity+[key],start,size))
 # The matching resource header identifies DLL_PAK as RCDATA 1; the separate
 # embedded manual also uses this archive format and must not be confused with it.
 walk(0,0,[]);archives=[(identity,start,size)for identity,start,size in leaves if identity[:2]==[10,1]and data[start:start+4]==b'LzSA'];assert len(archives)==1
 identity,start,size=archives[0];archive=data[start:start+size];assert len(archive)>=12;files=struct.unpack_from('<I',archive,4)[0];assert 0<files<=32;at=8;metadata=[]
 for i in range(files):
  assert at+25<=len(archive);length,packed,expanded,crc=struct.unpack_from('<4I',archive,at);assert 25<=length<=1024 and at+length<=len(archive)and 0<expanded<=64*1024**2 and packed>0
  raw_name=archive[at+24:at+length];assert raw_name[-1:]==b'\0'and b'\0'not in raw_name[:-1];name=raw_name[:-1].decode('utf-8');metadata.append((name,packed,expanded,crc));at+=length
 assert at+4<=len(archive)and zlib.crc32(archive[:at])==struct.unpack_from('<I',archive,at)[0];at+=4;rows=[]
 for name,packed,expanded,expected_crc in metadata:
  assert at+packed<=len(archive);block=archive[at:at+packed];at+=packed;method=block[0]
  if method==255:decoded=block[1:]
  else:
   assert method in[0,1]and len(block)>=6;properties=block[1];lc=properties%9;rest=properties//9;lp=rest%5;pb=rest//5;dictionary=int.from_bytes(block[2:6],'little');assert lc+lp<=4 and pb<=4 and 4096<=dictionary<=64*1024**2
   filters=([dict(id=lzma.FILTER_X86)]if method else[])+[dict(id=lzma.FILTER_LZMA1,dict_size=dictionary,lc=lc,lp=lp,pb=pb)]
   decoder=lzma.LZMADecompressor(format=lzma.FORMAT_RAW,filters=filters);decoded=decoder.decompress(block[6:],max_length=expanded+1);assert decoder.eof and not decoder.unused_data
  assert len(decoded)==expanded and zlib.crc32(decoded)==expected_crc
  rows.append(dict(name=name,bytes=len(decoded),sha256=hashlib.sha256(decoded).hexdigest(),crc32=expected_crc,compression_method=method))
 assert at==len(archive);native=json.loads((ROOT/'build/m14-native/stage8/payload-readback.json').read_text());assert native['passed'];expected={r['name']:r for r in native['payloads']if r['name']!='SumatraPDF.exe'};assert {r['name']for r in rows}==set(expected)
 for row in rows:
  for key in ['bytes','sha256','crc32']:assert row[key]==expected[row['name']][key],(row['name'],key)
 report=dict(passed=True,scope=__doc__,original_sha256=ORIGINAL,resource_identity=identity,resource_file_offset=start,resource_bytes=size,archive_header_crc_verified=True,payloads=rows,native_outputs_match_independent_archive=True,format_source='https://github.com/sumatrapdfreader/sumatrapdf/blob/3.6.1rel/src/utils/LzmaSimpleArchive.cpp',observer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
 (ROOT/'build/m14-native/stage8/archive-reference.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,payloads=rows),indent=2))
if __name__=='__main__':main()
