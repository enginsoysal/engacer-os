"""Own hidden Windows callback-chain reference; no vendor app or visible UI."""
import ctypes as c,json,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
H=c.c_void_p;U=c.c_uint;P=c.c_size_t;L=c.c_ssize_t
WND=c.WINFUNCTYPE(L,H,U,P,L);SUB=c.WINFUNCTYPE(L,H,U,P,L,P,P)
class CLASS(c.Structure):_fields_=[('style',U),('proc',WND),('extra',c.c_int),('window_extra',c.c_int),('instance',H),('icon',H),('cursor',H),('background',H),('menu',c.c_wchar_p),('name',c.c_wchar_p)]

def main():
 u=c.WinDLL('user32',use_last_error=True);m=c.WinDLL('comctl32',use_last_error=True);k=c.WinDLL('kernel32')
 k.GetModuleHandleW.argtypes=[c.c_wchar_p];k.GetModuleHandleW.restype=H
 u.RegisterClassW.argtypes=[c.POINTER(CLASS)];u.RegisterClassW.restype=c.c_ushort
 u.CreateWindowExW.argtypes=[U,c.c_wchar_p,c.c_wchar_p,U,c.c_int,c.c_int,c.c_int,c.c_int,H,H,H,H];u.CreateWindowExW.restype=H
 u.SendMessageW.argtypes=[H,U,P,L];u.SendMessageW.restype=L;u.DefWindowProcW.argtypes=[H,U,P,L];u.DefWindowProcW.restype=L
 u.DestroyWindow.argtypes=[H];u.UnregisterClassW.argtypes=[c.c_wchar_p,H]
 m.SetWindowSubclass.argtypes=[H,SUB,P,P];m.RemoveWindowSubclass.argtypes=[H,SUB,P];m.GetWindowSubclass.argtypes=[H,SUB,P,c.POINTER(P)];m.DefSubclassProc.argtypes=[H,U,P,L];m.DefSubclassProc.restype=L
 rows=[];order=[];fail=[]
 @WND
 def base(h,msg,wp,lp):return 10 if 0x8100<=msg<=0x8104 else u.DefWindowProcW(h,msg,wp,lp)
 @SUB
 def sub(h,msg,wp,lp,id,data):
  if 0x8100<=msg<=0x8104:
   order.append(int(id))
   if id==2 and msg==0x8101 and not m.RemoveWindowSubclass(h,sub,1):fail.append('remove pending')
   if id==2 and msg==0x8102 and not m.SetWindowSubclass(h,sub,1,77):fail.append('insert during dispatch')
   if id==2 and msg==0x8103 and not m.RemoveWindowSubclass(h,sub,2):fail.append('remove self')
   if msg==0x8104 and u.SendMessageW(h,0x8100,0,0)!=110:fail.append('nested result')
   return m.DefSubclassProc(h,msg,wp,lp)+id*100
  return m.DefSubclassProc(h,msg,wp,lp)
 instance=k.GetModuleHandleW(None);name='EngacerOwnedSubclass148'+uuid.uuid4().hex;cls=CLASS(0,base,0,0,instance,None,None,None,None,name);assert u.RegisterClassW(c.byref(cls));window=None
 try:
  window=u.CreateWindowExW(0,name,'Hidden owned callback contract',0,0,0,100,100,None,None,instance,None);assert window
  assert m.SetWindowSubclass(window,sub,1,11) and m.SetWindowSubclass(window,sub,2,22)
  for i in range(500):assert m.SetWindowSubclass(window,sub,1,i)
  data=P();assert m.GetWindowSubclass(window,sub,1,c.byref(data)) and data.value==499
  for msg,result,expected in [(0x8100,310,[2,1]),(0x8101,210,[2]),(0x8102,210,[2]),(0x8103,310,[1,2]),(0x8104,110,[1,1])]:
   order.clear();actual=u.SendMessageW(window,msg,0,0);rows.append(dict(message=hex(msg),result=actual,order=list(order)));assert actual==result and order==expected,(rows,fail)
  assert not fail;assert u.DestroyWindow(window);window=None
 finally:
  if window:u.DestroyWindow(window)
  assert u.UnregisterClassW(name,instance)
 report=dict(passed=True,scope=__doc__,visible_windows_created=0,duplicate_updates=500,cases=rows)
 out=ROOT/'build/m14-native/stage8/subclass-reference';out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2))
if __name__=='__main__':main()
