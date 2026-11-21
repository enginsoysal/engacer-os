"""Own hidden version-6 button shield state and previous-icon contract."""
import ctypes as c,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];H=c.c_void_p
class ACTCTX(c.Structure):_fields_=[('size',c.c_uint),('flags',c.c_uint),('source',c.c_wchar_p),('arch',c.c_ushort),('lang',c.c_ushort),('directory',c.c_wchar_p),('resource',c.c_wchar_p),('application',c.c_wchar_p),('module',H)]

def main():
 out=ROOT/'build/m14-native/stage8/shield-reference';out.mkdir(parents=True,exist_ok=True);manifest=out/'owned.manifest';manifest.write_bytes(b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0"><assemblyIdentity version="1.0.0.0" processorArchitecture="amd64" name="Engacer.Owned.Button.Reference" type="win32"/><dependency><dependentAssembly><assemblyIdentity type="win32" name="Microsoft.Windows.Common-Controls" version="6.0.0.0" processorArchitecture="amd64" publicKeyToken="6595b64144ccf1df" language="*"/></dependentAssembly></dependency></assembly>')
 k=c.WinDLL('kernel32');u=c.WinDLL('user32');k.CreateActCtxW.argtypes=[c.POINTER(ACTCTX)];k.CreateActCtxW.restype=H;k.ActivateActCtx.argtypes=[H,c.POINTER(c.c_size_t)];k.DeactivateActCtx.argtypes=[c.c_uint,c.c_size_t];k.ReleaseActCtx.argtypes=[H]
 context=ACTCTX();context.size=c.sizeof(context);context.source=str(manifest.resolve());handle=k.CreateActCtxW(c.byref(context));assert handle and handle!=c.c_void_p(-1).value;cookie=c.c_size_t();assert k.ActivateActCtx(handle,c.byref(cookie));window=None;icons=set();rows=[]
 u.CreateWindowExW.argtypes=[c.c_uint,c.c_wchar_p,c.c_wchar_p,c.c_uint,c.c_int,c.c_int,c.c_int,c.c_int,H,H,H,H];u.CreateWindowExW.restype=H;u.SendMessageW.argtypes=[H,c.c_uint,c.c_size_t,c.c_ssize_t];u.SendMessageW.restype=c.c_ssize_t;u.DestroyWindow.argtypes=[H];u.DestroyIcon.argtypes=[H]
 try:
  controls=c.WinDLL('comctl32');classes=(c.c_uint*2)(8,0x4000);assert controls.InitCommonControlsEx(classes);window=u.CreateWindowExW(0,'Button','Own hidden shield',0,0,0,180,40,None,None,None,None);assert window;previous=0
  for show in [0,1,1,0,0,1,0]:
   returned=u.SendMessageW(window,0x160c,0,show);current=u.SendMessageW(window,0xf6,1,0);assert returned==previous and bool(current)==bool(show);assert not current or current!=previous;rows.append(dict(show=bool(show),returns_previous_icon=returned==previous,current_present=bool(current),new_handle_when_enabled=bool(current and current!=previous)));previous=current
   if returned:icons.add(returned)
 finally:
  if window:assert u.DestroyWindow(window)
  for icon in icons:u.DestroyIcon(icon)
  assert k.DeactivateActCtx(0,cookie);k.ReleaseActCtx(handle)
 report=dict(passed=True,scope=__doc__,common_controls_version=6,visible_windows_created=0,cases=rows,documentation_discrepancy='The actual successful return is the previous HICON, including zero; do not treat zero as a failed state change or invent BOOL 1.')
 (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2))
if __name__=='__main__':main()
