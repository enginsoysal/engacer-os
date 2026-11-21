"""Owned temporary HKCU tree-deletion reference; never modify unrelated keys."""
import ctypes as C,hashlib,json,uuid,winreg as R
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 name='Software\\EngacerOS-Ref-'+uuid.uuid4().hex;assert name.startswith('Software\\EngacerOS-Ref-') and len(name.rsplit('-',1)[1])==32
 shell=C.WinDLL('shlwapi',use_last_error=True);shell.SHDeleteKeyW.argtypes=[C.c_void_p,C.c_wchar_p];shell.SHDeleteKeyW.restype=C.c_long
 rows={}
 try:
  with R.CreateKeyEx(R.HKEY_CURRENT_USER,name,0,R.KEY_ALL_ACCESS) as root:
   with R.CreateKeyEx(root,'gone\\child\\grand',0,R.KEY_ALL_ACCESS) as key:R.SetValueEx(key,'value',0,R.REG_DWORD,3)
   with R.CreateKeyEx(root,'peer',0,R.KEY_ALL_ACCESS) as key:R.SetValueEx(key,'value',0,R.REG_DWORD,5)
   rows['recursive_status']=shell.SHDeleteKeyW(int(root),'gone');assert rows['recursive_status']==0
   try:R.OpenKey(root,'gone');raise AssertionError('Deleted tree remains')
   except FileNotFoundError:pass
   with R.OpenKey(root,'peer') as key:assert R.QueryValueEx(key,'value')[0]==5
   rows['peer_preserved']=True;R.SetValueEx(root,'rootvalue',0,R.REG_DWORD,7)
   rows['null_status']=shell.SHDeleteKeyW(int(root),None);assert rows['null_status']==0 and R.QueryInfoKey(root)[:2]==(0,0)
   with R.OpenKey(R.HKEY_CURRENT_USER,name):rows['null_keeps_key']=True
   R.SetValueEx(root,'guard',0,R.REG_DWORD,3)
   with R.OpenKey(R.HKEY_CURRENT_USER,name,0,R.KEY_READ) as readonly:rows['readonly_null_status']=shell.SHDeleteKeyW(int(readonly),None)
   rows['readonly_guard_remains']=R.QueryValueEx(root,'guard')[0]==3
   rows['empty_status']=shell.SHDeleteKeyW(int(root),'');assert rows['empty_status']==0
   try:R.OpenKey(R.HKEY_CURRENT_USER,name);raise AssertionError('Empty-string target remains')
   except FileNotFoundError:rows['empty_deletes_key']=True
  rows['missing_status']=shell.SHDeleteKeyW(C.c_void_p(-2147483647),name);rows['invalid_handle']=shell.SHDeleteKeyW(0x12345678,'x');assert rows['missing_status']==2 and rows['invalid_handle']==6
 finally:shell.SHDeleteKeyW(C.c_void_p(-2147483647),name)
 report=dict(passed=True,scope=__doc__,observations=rows,current_native_capability_difference='Native readonly-relative reopening is denied with 5. This Windows readonly-NULL call returns 0 while leaving its value untouched.',source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
 out=ROOT/'build/m14-native/stage8/shdeletetree-reference';out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
