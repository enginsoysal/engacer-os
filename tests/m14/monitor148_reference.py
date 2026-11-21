"""Own read-only Windows monitor rectangle/point behavior; no desktop control."""
import ctypes as c,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 u=c.WinDLL('user32');u.MonitorFromPoint.argtypes=[c.c_uint64,c.c_uint];u.MonitorFromPoint.restype=c.c_void_p;u.MonitorFromRect.argtypes=[c.c_void_p,c.c_uint];u.MonitorFromRect.restype=c.c_void_p;u.GetMonitorInfoW.argtypes=[c.c_void_p,c.c_void_p]
 primary=u.MonitorFromPoint(0,1);info=(c.c_int*10)();info[0]=40;assert primary and u.GetMonitorInfoW(primary,info);left,top,right,bottom=info[1:5];x=(left+right)//2;y=(top+bottom)//2;rows=[]
 for name,rect,expected in [('inside',(x,y,x+10,y+10),True),('point',(x,y,x,y),True),('zero-width',(x,y,x,y+10),True),('inverted-inside',(x+10,y+10,x,y),True),('outside',(2147483637,2147483637,2147483647,2147483647),False),('inverted-crossing',(2147483647,y,x,y+10),False)]:
  r=(c.c_int*4)(*rect);actual=u.MonitorFromRect(r,0);assert bool(actual)==expected;assert u.MonitorFromRect(r,1)==(actual or primary);assert u.MonitorFromRect(r,2);rows.append(dict(case=name,none_returns_monitor=bool(actual),primary_fallback=True,nearest_exists=True))
 report=dict(passed=True,scope=__doc__,cases=rows,empty_rectangle='A nonpositive width or height uses the supplied top-left point, rather than normalizing the rectangle.',native_profile='One actual native monitor; no fabricated secondary displays.')
 out=ROOT/'build/m14-native/stage8/monitor-reference';out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2))
if __name__=='__main__':main()
