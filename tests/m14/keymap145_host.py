"""Compare own translation with a read-only explicit existing US Windows layout."""
import ctypes as c
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools

def main():
 out=ROOT/'build/m14-native/stage5/keymap-host';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-ffreestanding','-fno-builtin','-fno-stack-protector','-I',ROOT/'include','-c',ROOT/'tests/m14/keymap145_host.c','-o',out/'keymap.obj'])
 command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'keymap.dll'),out/'keymap.obj'])
 own=c.CDLL(str(out/'keymap.dll'));own.translate145.argtypes=[c.c_uint]*3;own.translate145.restype=c.c_uint
 reference=c.WinDLL('user32');reference.GetKeyboardLayoutList.argtypes=[c.c_int,c.POINTER(c.c_void_p)];layouts=(c.c_void_p*32)();count=reference.GetKeyboardLayoutList(32,layouts);assert 0x04090409 in list(layouts)[:count], 'Existing explicit US reference required; do not change host layouts'
 reference.MapVirtualKeyExW.argtypes=[c.c_uint,c.c_uint,c.c_void_p];reference.MapVirtualKeyExW.restype=c.c_uint
 own.character145.argtypes=[c.c_uint];own.character145.restype=c.c_uint
 reference.VkKeyScanExW.argtypes=[c.c_wchar,c.c_void_p];reference.VkKeyScanExW.restype=c.c_short
 assertions=0;differences=[]
 for ch in range(32,127):
  assert own.character145(ch)==reference.VkKeyScanExW(chr(ch),c.c_void_p(0x04090409))&255,chr(ch)
  assertions+=1
 for kind in range(5):
  codes=range(256) if kind in(0,2,4)else [p|k for p in(0,0xe000,0xe100)for k in range(256)]
  for code in codes:
   expected=reference.MapVirtualKeyExW(code,kind,c.c_void_p(0x04090409));actual=own.translate145(code,kind,0)
   if actual!=expected:differences.append((hex(code),kind,hex(expected),hex(actual)))
   assertions+=1
 assert not differences,differences
 # These physical keys follow the native Dvorak layout, not host locale changes.
 for scan,logical in [(0x10,0xde),(0x11,0xbc),(0x12,0xbe),(0x1f,ord('O')),(0x33,ord('W')),(0x34,ord('V')),(0x35,ord('Z'))]:
  assert own.translate145(scan,3,1)==logical
  assert own.translate145(logical,0,1)==scan
  assertions+=2
 for layout in(0,1):
  assert own.translate145(8,0,layout)==14 and own.translate145(0xe01d,3,layout)==0xa3
  assert not own.translate145(0xffffffff,4,layout) and not own.translate145(8,5,layout)
  assertions+=4
 result=dict(passed=True,scope='Host factual US mapping and native Dvorak core; not native application qualification',existing_reference_layout='04090409',assertions=assertions,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in('include/engine/keymap145.h','include/engine/keymap-us145.inc','tests/m14/keymap145_host.c')})
 (out/'results.json').write_bytes((json.dumps(result,indent=2)+'\n').encode());print(json.dumps(result))

if __name__=='__main__':main()
