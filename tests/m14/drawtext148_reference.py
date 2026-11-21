"""Independent own off-screen GDI text rectangle and DC release contracts."""
import ctypes as c,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];H=c.c_void_p

def main():
 u=c.WinDLL('user32');g=c.WinDLL('gdi32');g.CreateCompatibleDC.argtypes=[H];g.CreateCompatibleDC.restype=H;g.DeleteDC.argtypes=[H];g.GetTextExtentPoint32W.argtypes=[H,c.c_wchar_p,c.c_int,c.c_void_p];g.GetTextMetricsW.argtypes=[H,c.c_void_p];u.DrawTextExW.argtypes=[H,c.c_void_p,c.c_int,c.c_void_p,c.c_uint,H]
 dc=g.CreateCompatibleDC(None);assert dc;metrics=c.create_string_buffer(60);assert g.GetTextMetricsW(dc,metrics);height=c.c_int.from_buffer(metrics).value;rows=[]
 try:
  cases=[('',0x2500,[]),('',0x2520,['']),('A',0x2500,['A']),('A\nB',0x2500,['A','B']),('A\n',0x2500,['A']),('\n',0x2500,['']),('A\rB',0x2500,['A','B']),('\r\n',0x2500,['']),('A\n\n',0x2500,['A','']),('&A',0x2500,['A']),('&&A',0x2500,['&A']),('&',0x2500,['']),('&&&',0x2500,['&']),('&A',0x2d00,['&A']),('A\nB',0x2520,['AB'])]
  for text,flags,lines in cases:
   widths=[]
   for line in lines:
    size=(c.c_int*2)();assert g.GetTextExtentPoint32W(dc,line,len(line),size);widths.append(size[0])
   rect=(c.c_int*4)(5,7,5,7);buffer=c.create_unicode_buffer(text);result=u.DrawTextExW(dc,buffer,len(text),rect,flags,None);expected=[5,7,5+max(widths,default=0),7+height*len(lines)];assert list(rect)==expected and result==(height*len(lines) or 1),(text,result,list(rect),expected)
   rows.append(dict(text=text,flags=hex(flags),result=result,rectangle=list(rect)))
 finally:assert g.DeleteDC(dc)
 u.CreateWindowExW.argtypes=[c.c_uint,c.c_wchar_p,c.c_wchar_p,c.c_uint,c.c_int,c.c_int,c.c_int,c.c_int,H,H,H,H];u.CreateWindowExW.restype=H;u.GetWindowDC.argtypes=[H];u.GetWindowDC.restype=H;u.GetDC.argtypes=[H];u.GetDC.restype=H;u.ReleaseDC.argtypes=[H,H];u.DestroyWindow.argtypes=[H]
 a=u.CreateWindowExW(0,'Static','Owned hidden DC',0,0,0,100,100,None,None,None,None);b=u.CreateWindowExW(0,'Static','Owned hidden other DC',0,0,0,100,100,None,None,None,None);assert a and b;release=[]
 try:
  for acquire in [u.GetDC,u.GetWindowDC]:
   for window in [None,a,b]:
    dc=acquire(a);assert dc;result=u.ReleaseDC(window,dc);assert result;release.append(dict(acquire=acquire.__name__,advisory_window='null' if window is None else 'same' if window==a else 'other',result=result))
 finally:assert u.DestroyWindow(a) and u.DestroyWindow(b)
 report=dict(passed=True,scope=__doc__,visible_windows_created=0,text_cases=rows,release_cases=release,embedded_nul_profile='Explicit positive counts can measure embedded NUL on Windows; this native profile must refuse instead of truncating.')
 out=ROOT/'build/m14-native/stage8/drawtext-reference';out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2))
if __name__=='__main__':main()
