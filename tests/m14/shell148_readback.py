"""Inspect one stopped owned fixture link with the original Windows metadata reader."""
import hashlib
from pathlib import Path
from shell148_reference import read,read_icon,ROOT
def validate(disk,stopped,library,out):
 mounted=stopped(disk,library())
 try:
  matches=[e for e in mounted.volume.entries if e.kind==1 and e.path==b'/Users/Owner/AppData/Temp/NativeShellLink148.lnk'];assert len(matches)==1
  entry=matches[0];assert 76<entry.size<=4096;mounted.file.seek(mounted.offset+entry.first*4096);data=mounted.file.read(entry.size);assert len(data)==entry.size
 finally:mounted.close()
 path=Path(out)/'native-shell-link.lnk';path.write_bytes(data);metadata=read(path);icon=read_icon(path);target=r'C:\Program Files\7-Zip\7zFM.exe'
 assert metadata==dict(target=target,working_directory=r'C:\Users\Owner\Documents',arguments='--native 148',description='Owned shortcut '+chr(0xe4),show=3),metadata
 assert icon==dict(path=target,index=7),icon
 inputs=[Path(__file__),ROOT/'tests/m14/shell148_reference.py',ROOT/'tests/m14/link147_reader.py',ROOT/'tests/m14/link147_host.py']
 return dict(passed=True,scope=__doc__,native_file_bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),metadata=metadata,icon=icon,reader_source_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in inputs})
