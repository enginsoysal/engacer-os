"""Owned hidden Windows progress ranges, positions and steps; no visible UI."""
import ctypes as c,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 u=c.WinDLL('user32');cc=c.WinDLL('comctl32');H=c.c_void_p;u.CreateWindowExW.argtypes=[c.c_uint,c.c_wchar_p,c.c_wchar_p,c.c_uint,c.c_int,c.c_int,c.c_int,c.c_int,H,H,H,H];u.CreateWindowExW.restype=H;u.DestroyWindow.argtypes=[H];u.SendMessageW.argtypes=[H,c.c_uint,c.c_size_t,c.c_ssize_t];u.SendMessageW.restype=c.c_ssize_t;assert cc.InitCommonControlsEx((c.c_uint*2)(8,32));parent=u.CreateWindowExW(0,'STATIC','Owned invisible progress reference',0x80000000,0,0,300,200,None,None,None,None);bar=u.CreateWindowExW(0,'msctls_progress32','',0x40000000,0,0,200,30,parent,None,None,None);assert parent and bar;rows=[]
 def send(msg,w=0,l=0):return u.SendMessageW(bar,msg,w&0xffffffffffffffff,l)
 try:
  cases=[(0x406,-5,10,0x640000,-5,10,0),(0x402,20,0,0,-5,10,10),(0x403,-30,0,10,-5,10,-5),(0x404,7,0,10,-5,10,-5),(0x405,0,0,-5,-5,10,2),(0x405,0,0,2,-5,10,9),(0x405,0,0,9,-5,10,1),(0x401,0,5|(50<<16),0x000afffb,5,50,5),(0x402,70,0,5,5,50,50),(0x406,10,-5,50<<16|5,10,-5,10)]
  for msg,w,l,result,low,high,position in cases:
   actual=(send(msg,w,l),send(0x407,1),send(0x407,0),send(0x408));assert actual==(result,low,high,position),(msg,actual);rows.append(dict(message=hex(msg),wparam=w,lparam=l,result=result,minimum=low,maximum=high,position=position))
  guarded=(c.c_int*4)(0x148,0,0,0x148);assert send(0x407,1,c.addressof(guarded)+4)==10 and list(guarded)==[0x148,10,-5,0x148]
 finally:assert u.DestroyWindow(bar)and u.DestroyWindow(parent)
 report=dict(passed=True,scope=__doc__,cases=rows,range_buffer_guards=True,visible_windows_created=0,native_profile='Finite classic progress; marquee and unsupported common-control extensions refuse.')
 out=ROOT/'build/m14-native/stage8/progress-reference';out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2))
if __name__=='__main__':main()
