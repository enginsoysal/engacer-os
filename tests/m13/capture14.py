"""Preserve exact physical VRAM while bounding new disposable capture storage.

Only a new UUID-named file is compressed before QEMU writes it. Existing test
fixtures, accepted evidence and the previously blocked cleanup are untouched.
"""
import hashlib,json,re,subprocess,uuid
from PIL import Image

def bind(ui):
 def raw_shot(g,out,name,installed=False):
  assert re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,95}',name)
  import struct
  boot=ui.physical_boot(g,installed);address=struct.unpack_from('<Q',boot,80)[0];stride,fmt,w,h=struct.unpack_from('<4I',boot,136)
  assert 320<=w<=4096 and 200<=h<=2160 and stride>=w*4 and stride*h<=64*1024**2
  path=g.folder/(name+'-'+uuid.uuid4().hex+'-vram.bin');assert path.parent.resolve()==g.folder.resolve()
  with path.open('xb'):pass
  subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,check=True,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
  g.qmp('human-monitor-command',{'command-line':f'pmemsave 0x{address:x} 0x{stride*h:x} "{path.as_posix()}"'})
  data=path.read_bytes();assert len(data)==stride*h and path.stat().st_file_attributes&0x800
  image=Image.frombytes('RGB',(stride//4,h),data,'raw','BGRX' if fmt==2 else 'RGBX');image.crop((0,0,w,h)).save(out/(name+'.png'))
  (out/(name+'-capture.json')).write_bytes((json.dumps(dict(source='actual native framebuffer physical bytes; no VGA cache or image resizing',width=w,height=h,stride=stride,raw_sha256=hashlib.sha256(data).hexdigest(),raw_storage='New file compressed at creation by NTFS; existing fixtures untouched'),indent=2)+'\n').encode())
 ui.raw_shot=raw_shot
