"""Own hidden Windows control reference; no original app and no visible host UI."""
import ctypes as c
from ctypes import wintypes as w
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
P=c.c_void_p;I=c.c_ssize_t;PROC=c.WINFUNCTYPE(I,P,w.UINT,P,I)
class CLS(c.Structure):
 _fields_=[('style',w.UINT),('proc',PROC),('ce',c.c_int),('we',c.c_int),('instance',P),('icon',P),('cursor',P),('background',P),('menu',c.c_wchar_p),('name',c.c_wchar_p)]
class ITEM(c.Structure):
 _fields_=[('mask',w.UINT),('item',c.c_int),('sub',c.c_int),('state',w.UINT),('state_mask',w.UINT),('pad',w.UINT),('text',P),('capacity',c.c_int),('image',c.c_int),('parameter',I),('indent',c.c_int),('group',c.c_int),('columns',w.UINT),('pad2',w.UINT),('column_ids',P),('formats',P),('group_index',c.c_int),('pad3',w.UINT)]
class COLUMN(c.Structure):
 _fields_=[('mask',w.UINT),('format',c.c_int),('width',c.c_int),('pad',w.UINT),('text',c.c_wchar_p),('capacity',c.c_int),('sub',c.c_int),('image',c.c_int),('order',c.c_int),('min',c.c_int),('default',c.c_int),('ideal',c.c_int),('pad2',w.UINT)]

def main():
 u=c.WinDLL('user32');k=c.WinDLL('kernel32');cc=c.WinDLL('comctl32');assert c.sizeof(ITEM)==88 and c.sizeof(COLUMN)==56
 u.DefWindowProcW.argtypes=[P,w.UINT,P,I];u.DefWindowProcW.restype=I;u.RegisterClassW.argtypes=[c.POINTER(CLS)];u.RegisterClassW.restype=w.ATOM
 u.CreateWindowExW.argtypes=[w.DWORD,c.c_wchar_p,c.c_wchar_p,w.DWORD,c.c_int,c.c_int,c.c_int,c.c_int,P,P,P,P];u.CreateWindowExW.restype=P
 u.SendMessageW.argtypes=[P,w.UINT,P,I];u.SendMessageW.restype=I;u.DestroyWindow.argtypes=[P];u.UnregisterClassW.argtypes=[c.c_wchar_p,P];u.IsWindowVisible.argtypes=[P]
 k.GetModuleHandleW.argtypes=[c.c_wchar_p];k.GetModuleHandleW.restype=P
 seen=[]
 @PROC
 def proc(h,m,wp,lp):
  if m==0x4e and c.c_uint.from_address(lp+16).value==(-177&0xffffffff):
   item=ITEM.from_address(lp+24);seen.append(item.sub);text='Callback name'if not item.sub else'Callback size';data=text.encode('utf-16-le')+b'\0\0';c.memmove(item.text,data,min(len(data),item.capacity*2));return 0
  return u.DefWindowProcW(h,m,wp,lp)
 init=(w.DWORD*2)(8,1);assert cc.InitCommonControlsEx(c.byref(init));instance=k.GetModuleHandleW(None);cls=CLS();cls.proc=proc;cls.instance=instance;cls.name='EngacerHiddenReference145';assert u.RegisterClassW(c.byref(cls));parent=None;observations=[]
 try:
  parent=u.CreateWindowExW(0,cls.name,'',0,0,0,400,300,None,None,instance,None);assert parent and not u.IsWindowVisible(parent)
  view=u.CreateWindowExW(0,'SysListView32','',0x40000001,0,0,300,200,parent,None,instance,None);assert view and not u.IsWindowVisible(view)
  for index,name in enumerate(['Name','Size']):
   col=COLUMN();col.mask=6;col.width=100;col.text=name;assert u.SendMessageW(view,0x1061,index,c.addressof(col))==index
  for callback in(True,False,None):
   assert u.SendMessageW(view,0x1009,0,0)
   stored=c.create_unicode_buffer('Stored name');item=ITEM();item.mask=4 if callback is None else 5;item.parameter=17;item.text=0xffffffffffffffff if callback else c.addressof(stored);assert u.SendMessageW(view,0x104d,0,c.addressof(item))==0
   for sub in(0,1):
    seen.clear();buffer=c.create_unicode_buffer(160);get=ITEM();get.sub=sub;get.text=c.addressof(buffer);get.capacity=160;length=u.SendMessageW(view,0x1073,0,c.addressof(get));observations.append(dict(callback_main=callback,subitem=sub,text=buffer.value,length=length,callbacks=list(seen)))
   empty=c.create_unicode_buffer('');item=ITEM();item.sub=1;item.text=c.addressof(empty);assert u.SendMessageW(view,0x1074,0,c.addressof(item))
   seen.clear();buffer=c.create_unicode_buffer(160);item=ITEM();item.sub=1;item.text=c.addressof(buffer);item.capacity=160;assert u.SendMessageW(view,0x1073,0,c.addressof(item))==0 and not buffer.value and not seen
 finally:
  if parent:u.DestroyWindow(parent)
  u.UnregisterClassW(cls.name,instance)
 result=dict(passed=True,scope='Hidden host control reference only; not native Engacer OS qualification',visible_host_windows=False,original_apps_executed=False,observations=observations,explicit_empty_suppresses_callback=True,observer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
 out=ROOT/'build/m14-native/stage5/list-reference';out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_bytes((json.dumps(result,indent=2)+'\n').encode());print(json.dumps(result))

if __name__=='__main__':main()
