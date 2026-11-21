"""Owned off-screen Windows GDI contract observations, never vendor execution."""
import ctypes as c,json,platform
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 g=c.WinDLL('gdi32',use_last_error=True)
 g.CreateFontIndirectW.argtypes=[c.c_void_p];g.CreateFontIndirectW.restype=c.c_void_p
 g.GetObjectW.argtypes=[c.c_void_p,c.c_int,c.c_void_p];g.DeleteObject.argtypes=[c.c_void_p]
 g.CreateCompatibleDC.argtypes=[c.c_void_p];g.CreateCompatibleDC.restype=c.c_void_p
 g.SelectObject.argtypes=[c.c_void_p,c.c_void_p];g.SelectObject.restype=c.c_void_p
 g.GetTextFaceW.argtypes=[c.c_void_p,c.c_int,c.c_void_p];g.DeleteDC.argtypes=[c.c_void_p]
 raw=c.create_string_buffer(92);c.c_int.from_buffer(raw).value=-16;h=g.CreateFontIndirectW(raw);assert h
 rows=[]
 try:
  assert g.GetObjectW(h,0,None)==92
  for size in (0,1,4,28,91,92):
   b=c.create_string_buffer(b'\xa5'*128);result=g.GetObjectW(h,size,b);assert result==size and b.raw[size:128]==b'\xa5'*(128-size)
   assert not size or b.raw[:size]==raw.raw[:size];rows.append(dict(bytes=size,result=result,sentinel_preserved=True))
  dc=g.CreateCompatibleDC(None);assert dc;old=g.SelectObject(dc,h);assert old
  try:
   faces=[]
   for size in (0,1,2,64):
    b=c.create_unicode_buffer(64);result=g.GetTextFaceW(dc,size,b);assert (size!=0 or result==0) and (size!=1 or result==1 and not b.value);faces.append(dict(capacity=size,result=result,actual_face=b.value))
  finally:g.SelectObject(dc,old);assert g.DeleteDC(dc)
 finally:assert g.DeleteObject(h)
 report=dict(passed=True,scope=__doc__,host=platform.version(),logical_font_bytes=92,partial_object_buffers=rows,actual_face_buffers=faces,visible_windows_created=0,vendor_code_executed=False)
 out=ROOT/'build/m14-native/stage8/font-reference';out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2))
if __name__=='__main__':main()
