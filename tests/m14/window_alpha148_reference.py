"""Own memory-HDC Windows reference for straight-ARGB image rounding."""
import ctypes as c,json,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];H=c.c_void_p
class INPUT(c.Structure):_fields_=[('v',c.c_uint),('callback',H),('thread',c.c_int),('codecs',c.c_int)]

def main():
 p=c.WinDLL('gdiplus');g=c.WinDLL('gdi32');p.GdiplusStartup.argtypes=[c.POINTER(c.c_size_t),c.POINTER(INPUT),H];p.GdiplusShutdown.argtypes=[c.c_size_t];p.GdipCreateBitmapFromScan0.argtypes=[c.c_int,c.c_int,c.c_int,c.c_uint,H,c.POINTER(H)];p.GdipBitmapSetPixel.argtypes=[H,c.c_int,c.c_int,c.c_uint];p.GdipCreateFromHDC.argtypes=[H,c.POINTER(H)];p.GdipDrawImageI.argtypes=[H,H,c.c_int,c.c_int];p.GdipFlush.argtypes=[H,c.c_int];p.GdipDeleteGraphics.argtypes=[H];p.GdipDisposeImage.argtypes=[H];g.CreateCompatibleDC.argtypes=[H];g.CreateCompatibleDC.restype=H;g.CreateDIBSection.argtypes=[H,H,c.c_uint,c.POINTER(H),H,c.c_uint];g.CreateDIBSection.restype=H;g.SelectObject.argtypes=[H,H];g.SelectObject.restype=H;g.DeleteObject.argtypes=[H];g.DeleteDC.argtypes=[H]
 token=c.c_size_t();assert not p.GdiplusStartup(c.byref(token),INPUT(1,None,0,0),None);dc=g.CreateCompatibleDC(None);assert dc;info=c.create_string_buffer(44);struct.pack_into('<IiiHHIIiiII',info,0,40,1,-1,1,32,0,4,0,0,0,0);bits=H();dib=g.CreateDIBSection(dc,info,0,c.byref(bits),None,0);assert dib and bits;old=g.SelectObject(dc,dib);raw=c.c_uint.from_address(bits.value);source=H();graphics=H();assert not p.GdipCreateBitmapFromScan0(1,1,0,0x26200a,None,c.byref(source));assert not p.GdipCreateFromHDC(dc,c.byref(graphics));cases=0
 def draw(color,destination):
  raw.value=destination;assert not p.GdipBitmapSetPixel(source,0,0,color) and not p.GdipDrawImageI(graphics,source,0,0) and not p.GdipFlush(graphics,1);return raw.value&0xffffff
 try:
  assert draw(0x01808080,0x010101)==0x020202
  for alpha in range(256):
   for destination in [1,17,127,240]:
    for channel in [1,63,128,254]:
     r=channel;green=(channel*73)&255;b=255-channel;color=(alpha<<24)|(r<<16)|(green<<8)|b;actual=draw(color,destination*0x010101);expected=0
     for shift,component in [(16,r),(8,green),(0,b)]:expected|=min(255,(component*alpha+127)//255+(destination*(255-alpha)+127)//255)<<shift
     assert actual==expected,(hex(color),destination,hex(actual),hex(expected));cases+=1
 finally:
  assert not p.GdipDeleteGraphics(graphics) and not p.GdipDisposeImage(source);g.SelectObject(dc,old);assert g.DeleteObject(dib) and g.DeleteDC(dc);p.GdiplusShutdown(token)
 report=dict(passed=True,scope=__doc__,cases=cases,visible_windows_created=0,counterexample=dict(straight_argb='0x01808080',destination_rgb='0x010101',actual_windows_rgb='0x020202',incorrect_fused_rounding_rgb='0x010101'),conversion='Round source premultiplication first, then separately round the destination contribution.')
 out=ROOT/'build/m14-native/stage8/window-alpha-reference';out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2))
if __name__=='__main__':main()
