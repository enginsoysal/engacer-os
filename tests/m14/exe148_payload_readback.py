"""Independent stopped-volume CRC/SHA/PE readback of the actual diagnostic installation payloads."""
import hashlib,json,os,struct,sys,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 import replay8
 loader=replay8.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  from window144_native import StoppedDisk
  from fixture1 import library
  source=json.loads((ROOT/'build/m14-native/stage8/install-click-native/results.json').read_text());assert source['diagnostic_completed']and source['original_installer_thread_completion_observed']
  disk=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m148-original-install-click'/source['owned_fixture']/'owned.img';mounted=StoppedDisk(disk,library());rows=[]
  try:
   for name in ['SumatraPDF.exe','libmupdf.dll','PdfFilter.dll','PdfPreview.dll']:
    path=('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/'+name).encode();matches=[e for e in mounted.volume.entries if e.kind==1 and e.path==path];assert len(matches)==1,name
    entry=matches[0];assert 64<entry.size<=64*1024**2;start=mounted.offset+entry.first*4096;mounted.file.seek(start);header=mounted.file.read(min(entry.size,65536));assert header[:2]==b'MZ';pe=struct.unpack_from('<I',header,60)[0];assert pe+26<=len(header)and header[pe:pe+4]==b'PE\0\0'
    machine=struct.unpack_from('<H',header,pe+4)[0];magic=struct.unpack_from('<H',header,pe+24)[0];assert machine==0x8664 and magic==0x20b,(name,machine,magic)
    mounted.file.seek(start);remaining=entry.size;sha=hashlib.sha256();crc=0
    while remaining:
     data=mounted.file.read(min(remaining,1024**2));assert data;remaining-=len(data);sha.update(data);crc=zlib.crc32(data,crc)
    assert crc==entry.crc,name
    rows.append(dict(name=name,bytes=entry.size,sha256=sha.hexdigest(),crc32=crc,machine=machine,optional_magic=magic))
   assert rows[0]['sha256']==source['original_sha256']and rows[0]['bytes']==source['original_bytes']
  finally:mounted.close()
  report=dict(passed=True,scope=__doc__,ordinary_installer_qualified=False,kernel_build_id=source['kernel_build_id'],worker_inputs=source['private_inputs'],payloads=rows,observer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),dll_reference_scope='DLL hashes are measured native output, not yet an independent extraction oracle from the original resource archive')
  (ROOT/'build/m14-native/stage8/payload-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,payloads=rows),indent=2))
 finally:sys.meta_path.remove(loader)
if __name__=='__main__':main()
