"""Own off-screen Windows image blit, alpha, clipping and overlap observations."""
import ctypes as c,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];H=c.c_void_p
class INPUT(c.Structure):_fields_=[('v',c.c_uint),('callback',H),('thread',c.c_int),('codecs',c.c_int)]

def main():
 p=c.WinDLL('gdiplus');p.GdiplusStartup.argtypes=[c.POINTER(c.c_size_t),c.POINTER(INPUT),H];p.GdiplusShutdown.argtypes=[c.c_size_t];p.GdipCreateBitmapFromScan0.argtypes=[c.c_int,c.c_int,c.c_int,c.c_uint,H,c.POINTER(H)];p.GdipGetImageGraphicsContext.argtypes=[H,c.POINTER(H)];p.GdipDrawImageI.argtypes=[H,H,c.c_int,c.c_int];p.GdipDeleteGraphics.argtypes=[H];p.GdipDisposeImage.argtypes=[H];p.GdipBitmapGetPixel.argtypes=[H,c.c_int,c.c_int,c.POINTER(c.c_uint)];p.GdipBitmapSetPixel.argtypes=[H,c.c_int,c.c_int,c.c_uint];p.GdipGraphicsClear.argtypes=[H,c.c_uint];p.GdipSetCompositingMode.argtypes=[H,c.c_int]
 token=c.c_size_t();assert not p.GdiplusStartup(c.byref(token),INPUT(1,None,0,0),None);source=H();destination=H();graphics=H();rows=[]
 def pixel(image,x,y):
  color=c.c_uint();assert not p.GdipBitmapGetPixel(image,x,y,c.byref(color));return color.value
 try:
  assert not p.GdipCreateBitmapFromScan0(2,2,0,0x26200a,None,c.byref(source)) and not p.GdipCreateBitmapFromScan0(4,4,0,0xe200b,None,c.byref(destination))
  for x,y,color in [(0,0,0x80ff0000),(1,0,0xff0000ff),(0,1,0),(1,1,0xff00ff00)]:assert not p.GdipBitmapSetPixel(source,x,y,color)
  assert not p.GdipGetImageGraphicsContext(destination,c.byref(graphics)) and not p.GdipGraphicsClear(graphics,0x80402010) and not p.GdipDrawImageI(graphics,source,1,1)
  actual=[pixel(destination,x,y)for x,y in [(1,1),(2,1),(1,2),(2,2)]];assert actual==[0xc0bf0a05,0xff0000ff,0x803f1f0f,0xff00ff00];rows.append(dict(task='SourceOver ARGB source into PARGB destination',pixels=[hex(x)for x in actual]))
  assert not p.GdipSetCompositingMode(graphics,1) and not p.GdipDrawImageI(graphics,source,-1,-1) and pixel(destination,0,0)==0xff00ff00
 finally:
  if graphics:assert not p.GdipDeleteGraphics(graphics)
  if source:assert not p.GdipDisposeImage(source)
  if destination:assert not p.GdipDisposeImage(destination)
  graphics=H();source=H();destination=H()
 try:
  backing=(c.c_uint*3)(0xffff0000,0xff0000ff,0xff00ff00);assert not p.GdipCreateBitmapFromScan0(3,1,12,0xe200b,backing,c.byref(source)) and not p.GdipGetImageGraphicsContext(source,c.byref(graphics)) and not p.GdipDrawImageI(graphics,source,1,0)
  actual=[pixel(source,x,0)for x in range(3)];assert actual==[0xffff0000,0xffff0000,0xff0000ff];rows.append(dict(task='Overlapping self blit',pixels=[hex(x)for x in actual],borrowed_pointer_after=[hex(x)for x in backing],observer_note='Windows logical readback changes while this borrowed backing remains unchanged; raw pointer observation alone would incorrectly report no draw. Native tests assert actual bitmap readback.'))
 finally:
  if graphics:assert not p.GdipDeleteGraphics(graphics)
  if source:assert not p.GdipDisposeImage(source)
  p.GdiplusShutdown(token)
 report=dict(passed=True,scope=__doc__,cases=rows,visible_windows_created=0)
 out=ROOT/'build/m14-native/stage8/image-reference';out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2))
if __name__=='__main__':main()
