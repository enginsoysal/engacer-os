"""Owned temporary HKCU SHDeleteValueW reference; no original app or system-key writes."""
import ctypes as C,hashlib,json,uuid,winreg as R
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 name='Software\\EngacerOS-Ref-'+uuid.uuid4().hex;assert name.startswith('Software\\EngacerOS-Ref-') and len(name.rsplit('-',1)[1])==32
 shell=C.WinDLL('shlwapi',use_last_error=True);shell.SHDeleteValueW.argtypes=[C.c_void_p,C.c_wchar_p,C.c_wchar_p];shell.SHDeleteValueW.restype=C.c_long
 try:
  with R.CreateKeyEx(R.HKEY_CURRENT_USER,name,0,R.KEY_READ|R.KEY_WRITE) as key:
   for value in ['alpha','beta','','guard']:R.SetValueEx(key,value,0,R.REG_DWORD,3)
   rows=dict(root_subkey=shell.SHDeleteValueW(C.c_void_p(-2147483647),name,'alpha'),null_subkey=shell.SHDeleteValueW(int(key),None,'beta'),empty_subkey_default=shell.SHDeleteValueW(int(key),'',''))
   with R.OpenKey(R.HKEY_CURRENT_USER,name,0,R.KEY_READ) as readonly:rows['readonly_null_subkey']=shell.SHDeleteValueW(int(readonly),None,'guard')
   rows.update(missing_value=shell.SHDeleteValueW(int(key),None,'absent'),missing_key=shell.SHDeleteValueW(C.c_void_p(-2147483647),name+'-missing','x'),invalid_handle=shell.SHDeleteValueW(0x12345678,None,'x'))
   assert rows==dict(root_subkey=0,null_subkey=0,empty_subkey_default=0,readonly_null_subkey=0,missing_value=2,missing_key=2,invalid_handle=6),rows
 finally:R.DeleteKey(R.HKEY_CURRENT_USER,name)
 report=dict(passed=True,scope=__doc__,observations=rows,current_native_capability_difference='Readonly-relative reopening cannot widen access in the native explicit-capability profile; native returns 5 instead of the observed Windows 0.',source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
 out=ROOT/'build/m14-native/stage8/shdelete-reference';out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
