"""Own contrasting bitmap strip; preserve accepted resource generator and assertions."""
import hashlib,json,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def build():
 source=ROOT/'tests/m14/resource144_build.py';raw=source.read_bytes();text=raw.decode('utf-8')
 bitmap=struct.pack('<IiiHHIIiiII',40,8,2,1,4,0,0,0,0,4,4)+bytes.fromhex('00000000ff00ff0000ff0000ffffff00')+bytes.fromhex('0101232301012323')
 before='bitmap=dib(8,2,False);icon='
 assert text.count(before)==1
 text=text.replace(before,'bitmap=bytes.fromhex('+repr(bitmap.hex())+');icon=')
 assert "stage4/resource-fixture"in text
 text=text.replace('stage4/resource-fixture','stage5/raster-resource-fixture')
 namespace={'__name__':'owned_resource145_derived','__file__':str(source)};exec(compile(text,str(source),'exec'),namespace);out=namespace['build']()
 (out/'source-derivation.json').write_bytes((json.dumps(dict(scope='Own contrasting bitmap; accepted generator/native assertion source unchanged',canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),bitmap_sha256=hashlib.sha256(bitmap).hexdigest(),first_image_colors=['black','magenta'],second_image_colors=['green','white']),indent=2)+'\n').encode());return out

if __name__=='__main__':build()
