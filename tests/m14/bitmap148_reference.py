"""Observe Windows GDI+ pixel ownership; supporting reference, not guest proof."""
import ctypes as c,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 dll=c.WinDLL('gdiplus.dll')
 class Input(c.Structure):
  _fields_=[('version',c.c_uint),('callback',c.c_void_p),('thread',c.c_int),('codecs',c.c_int)]
 def api(name,args):
  fn=getattr(dll,name);fn.argtypes=args;fn.restype=c.c_uint;return fn
 startup=api('GdiplusStartup',[c.POINTER(c.c_size_t),c.POINTER(Input),c.c_void_p])
 shutdown=dll.GdiplusShutdown;shutdown.argtypes=[c.c_size_t];shutdown.restype=None
 create=api('GdipCreateBitmapFromScan0',[c.c_int,c.c_int,c.c_int,c.c_uint,c.c_void_p,c.POINTER(c.c_void_p)])
 dispose=api('GdipDisposeImage',[c.c_void_p]);get=api('GdipBitmapGetPixel',[c.c_void_p,c.c_int,c.c_int,c.POINTER(c.c_uint)])
 setpixel=api('GdipBitmapSetPixel',[c.c_void_p,c.c_int,c.c_int,c.c_uint])
 token=c.c_size_t();assert startup(c.byref(token),c.byref(Input(1,None,0,0)),None)==0
 observations=[]
 try:
  for fmt in [0x21808,0x22009,0x26200a,0xe200b]:
   image=c.c_void_p();assert create(7,3,0,fmt,None,c.byref(image))==0
   try:
    color=c.c_uint();assert get(image,6,2,c.byref(color))==0;initial=color.value
    assert setpixel(image,6,2,0x80402010)==0 and get(image,6,2,c.byref(color))==0
    expected=0x803f1f0f if fmt==0xe200b else 0x80402010 if fmt==0x26200a else 0xff402010
    assert color.value==expected,(fmt,color.value,expected)
    observations.append(dict(format=fmt,initial=initial,roundtrip=color.value))
   finally:assert dispose(image)==0
  sample=(c.c_uint*1)();image=c.c_void_p();assert create(1,1,4,0xe200b,sample,c.byref(image))==0
  try:
   for alpha in [0,1,2,127,128,254,255]:
    for channel in range(256):
     value=(alpha<<24)|(channel<<16)|(channel<<8)|channel
     assert setpixel(image,0,0,value)==0
     expected=(channel*alpha+127)//255
     assert sample[0]==((alpha<<24)|(expected<<16)|(expected<<8)|expected),(alpha,channel,hex(sample[0]),expected)
     color=c.c_uint();assert get(image,0,0,c.byref(color))==0
     # Observe the platform's premultiplied readback; that format is deferred.
  finally:assert dispose(image)==0
  pixels=(c.c_uint*6)(0xff112233,0xff445566,0xff778899,0xffaabbcc,0xff123456,0xff654321)
  image=c.c_void_p();assert create(3,2,-12,0x26200a,c.byref(pixels,12),c.byref(image))==0
  try:
   color=c.c_uint();assert get(image,0,1,c.byref(color))==0 and color.value==pixels[0]
   assert setpixel(image,2,0,0x80abcdef)==0 and pixels[5]==0x80abcdef
  finally:assert dispose(image)==0
 finally:shutdown(token)
 out=ROOT/'build/m14-native/stage8/bitmap-reference.json';out.write_text(json.dumps(dict(passed=True,scope=__doc__,formats=observations,premultiplied_readback_qualified=False,negative_stride_borrowed_writeback=True),indent=2)+'\n',encoding='utf-8')
 print(out.read_text())
if __name__=='__main__':main()
