"""Own Windows thread-queue age/deadline/timer reference; no visible UI."""
import ctypes as c,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 u=c.WinDLL('user32');k=c.WinDLL('kernel32');u.MsgWaitForMultipleObjects.argtypes=[c.c_uint,c.c_void_p,c.c_int,c.c_uint,c.c_uint];u.MsgWaitForMultipleObjects.restype=c.c_uint;u.PostThreadMessageW.argtypes=[c.c_uint,c.c_uint,c.c_size_t,c.c_ssize_t];u.SetTimer.argtypes=[c.c_void_p,c.c_size_t,c.c_uint,c.c_void_p];u.SetTimer.restype=c.c_size_t;u.KillTimer.argtypes=[c.c_void_p,c.c_size_t];msg=c.create_string_buffer(64);rows=[]
 while u.PeekMessageW(c.byref(msg),None,0,0,1):pass
 def observe(label,expected):
  values=[u.MsgWaitForMultipleObjects(0,None,1,0,mask)for mask in [8,256,0x1cff]];assert values==expected,(label,values);rows.append(dict(case=label,post_allpost_allinput=values))
 observe('empty',[258,258,258]);assert u.PostThreadMessageW(k.GetCurrentThreadId(),0x8148,0,0);observe('new posted message',[0,0,0]);observe('repeated wait without peek',[0,0,0]);assert u.PeekMessageW(c.byref(msg),None,0x8148,0x8148,0);observe('filtered peek no remove',[258,0,258]);assert u.PeekMessageW(c.byref(msg),None,0,0,1);observe('unfiltered remove',[258,258,258])
 for message in [0x100,0x200,0xf,0x113]:
  assert u.PostThreadMessageW(k.GetCurrentThreadId(),message,0,0);values=[u.MsgWaitForMultipleObjects(0,None,0,0,mask)for mask in [1,2,8,16,32,256]];assert values==[258,258,0,258,258,0];rows.append(dict(case='posted message '+hex(message),key_move_post_timer_paint_allpost=values));assert u.PeekMessageW(c.byref(msg),None,0,0,1)
 start=time.monotonic();assert u.MsgWaitForMultipleObjects(0,None,1,25,0)==258;elapsed=time.monotonic()-start;assert elapsed>=.020
 timer=u.SetTimer(None,0,25,None);assert timer
 try:
  assert u.MsgWaitForMultipleObjects(0,None,0,2000,16)==0;assert u.PeekMessageW(c.byref(msg),None,0x113,0x113,1)
 finally:assert u.KillTimer(None,timer)
 report=dict(passed=True,scope=__doc__,cases=rows,empty_mask_timeout_seconds=elapsed,real_timer_wake=True,native_profile='Zero handles only; mixed object/message arrays explicitly refuse until implemented.')
 out=ROOT/'build/m14-native/stage8/message-wait-reference';out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2))
if __name__=='__main__':main()
