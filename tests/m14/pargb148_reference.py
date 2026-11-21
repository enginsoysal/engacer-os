"""Exhaustive own GDI+ premultiplication reference; no vendor application execution."""
import ctypes as c,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
H=c.c_void_p
class INPUT(c.Structure):_fields_=[('version',c.c_uint),('callback',H),('suppress_thread',c.c_int),('suppress_codec',c.c_int)]

def main():
 out=ROOT/'build/m14-native/stage8/pargb-reference';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools();source=ROOT/'tests/m14/pargb148_reference.c';obj=out/'pargb.obj';dll=out/'pargb.dll'
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-mgeneral-regs-only','-c',source,'-o',obj]);command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(dll),obj]);own=c.CDLL(str(dll));own.pargb_pack.argtypes=own.pargb_unpack.argtypes=[c.c_uint,c.c_uint];own.pargb_pack.restype=own.pargb_unpack.restype=c.c_uint;own.pargb_color.argtypes=[c.c_uint];own.pargb_color.restype=c.c_uint;own.pargb_over.argtypes=[c.c_uint,c.c_uint];own.pargb_over.restype=c.c_uint
 gp=c.WinDLL('gdiplus');gp.GdiplusStartup.argtypes=[c.POINTER(c.c_size_t),c.POINTER(INPUT),H];gp.GdiplusShutdown.argtypes=[c.c_size_t];gp.GdipCreateBitmapFromScan0.argtypes=[c.c_int,c.c_int,c.c_int,c.c_uint,H,c.POINTER(H)];gp.GdipDisposeImage.argtypes=[H];gp.GdipBitmapSetPixel.argtypes=[H,c.c_int,c.c_int,c.c_uint];gp.GdipBitmapGetPixel.argtypes=[H,c.c_int,c.c_int,c.POINTER(c.c_uint)];gp.GdipGetImageGraphicsContext.argtypes=[H,c.POINTER(H)];gp.GdipCreateBitmapFromGraphics.argtypes=[c.c_int,c.c_int,H,c.POINTER(H)];gp.GdipGetImagePixelFormat.argtypes=[H,c.POINTER(c.c_uint)];gp.GdipDeleteGraphics.argtypes=[H];gp.GdipCreateSolidFill.argtypes=[c.c_uint,c.POINTER(H)];gp.GdipSetSolidFillColor.argtypes=[H,c.c_uint];gp.GdipDeleteBrush.argtypes=[H];gp.GdipGraphicsClear.argtypes=[H,c.c_uint];gp.GdipFillRectangleI.argtypes=[H,H,c.c_int,c.c_int,c.c_int,c.c_int]
 token=c.c_size_t();assert not gp.GdiplusStartup(c.byref(token),INPUT(1,None,0,0),None);raw=(c.c_uint*1)();bitmap=H();assert not gp.GdipCreateBitmapFromScan0(1,1,4,0xe200b,raw,c.byref(bitmap));examples=[]
 try:
  for a in range(256):
   for value in range(256):
    r=value;g=(value*73+19)&255;b=255-value;argb=(a<<24)|(r<<16)|(g<<8)|b;assert not gp.GdipBitmapSetPixel(bitmap,0,0,argb)
    expected=(a<<24)|(own.pargb_pack(r,a)<<16)|(own.pargb_pack(g,a)<<8)|own.pargb_pack(b,a);assert raw[0]==expected,(a,value,hex(raw[0]),hex(expected))
    actual=c.c_uint();assert not gp.GdipBitmapGetPixel(bitmap,0,0,c.byref(actual));expected=(a<<24)|(own.pargb_unpack((raw[0]>>16)&255,a)<<16)|(own.pargb_unpack((raw[0]>>8)&255,a)<<8)|own.pargb_unpack(raw[0]&255,a);assert actual.value==expected
    if (a,value) in [(0,255),(1,128),(7,255),(127,255),(128,64),(255,255)]:examples.append(dict(alpha=a,input=hex(argb),stored=hex(raw[0]),readback=hex(actual.value)))
  inverse_pairs=0
  for a in range(1,256):
   for value in range(a+1):
    r=value;g=value//2;b=a-value;raw[0]=(a<<24)|(r<<16)|(g<<8)|b;actual=c.c_uint();assert not gp.GdipBitmapGetPixel(bitmap,0,0,c.byref(actual));expected=(a<<24)|(own.pargb_unpack(r,a)<<16)|(own.pargb_unpack(g,a)<<8)|own.pargb_unpack(b,a);assert actual.value==expected;(inverse_pairs:=inverse_pairs+1)
  graphics=H();assert not gp.GdipGetImageGraphicsContext(bitmap,c.byref(graphics));derived=H()
  try:
   brush=H();assert not gp.GdipCreateSolidFill(0,c.byref(brush))
   try:
    for da in range(256):
     for sa in range(256):
      dst=(da<<24)|(((da*73)&255)<<16)|(((da+19)&255)<<8)|(255-da);src=(sa<<24)|(((sa*37)&255)<<16)|(((sa+91)&255)<<8)|(255-sa);assert not gp.GdipGraphicsClear(graphics,dst);before=raw[0];assert not gp.GdipSetSolidFillColor(brush,src) and not gp.GdipFillRectangleI(graphics,brush,0,0,1,1);expected=own.pargb_over(own.pargb_color(src),before);assert raw[0]==expected,(hex(src),hex(before),hex(raw[0]),hex(expected))
   finally:assert not gp.GdipDeleteBrush(brush)
   assert not gp.GdipCreateBitmapFromGraphics(7,3,graphics,c.byref(derived));fmt=c.c_uint();assert not gp.GdipGetImagePixelFormat(derived,c.byref(fmt)) and fmt.value==0xe200b;assert not gp.GdipDisposeImage(derived)
  finally:assert not gp.GdipDeleteGraphics(graphics)
 finally:assert not gp.GdipDisposeImage(bitmap);gp.GdiplusShutdown(token)
 paths=['user/windows8/pargb148.h','tests/m14/pargb148_reference.c','tests/m14/pargb148_reference.py'];report=dict(passed=True,scope=__doc__,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in paths},own_dll_sha256=hashlib.sha256(dll.read_bytes()).hexdigest(),pack_pairs=65536,inverse_pairs=inverse_pairs,channels_per_pair=3,source_over_alpha_pairs=65536,derived_bitmap_format='0xe200b',examples=examples,visible_windows_created=0,conversion='Rounded integer premultiplication; 16-bit truncated reciprocal unpremultiplication, including lossy full-channel cases.')
 (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2))
if __name__=='__main__':main()
