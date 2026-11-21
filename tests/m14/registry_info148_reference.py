"""Owned temporary Windows registry metadata reference; no original app executes."""
import ctypes as c,hashlib,json,uuid,winreg
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 name='Software\\EngacerOSReference148_'+uuid.uuid4().hex;key=winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER,name,0,winreg.KEY_ALL_ACCESS);children=['k000','ABC'+chr(0xe9)+chr(0x1f600)];report=dict(passed=False,scope=__doc__,cases=[])
 try:
  for child in children:winreg.CreateKeyEx(key,child,0,winreg.KEY_ALL_ACCESS).Close()
  winreg.SetValueEx(key,'number',0,winreg.REG_DWORD,0x148);winreg.SetValueEx(key,'value'+chr(0x1f600),0,winreg.REG_BINARY,b'1234567')
  api=c.WinDLL('advapi32').RegQueryInfoKeyW;api.argtypes=[c.c_void_p]*12;api.restype=c.c_long;outputs=[c.c_uint(99)for _ in range(6)];status=api(int(key),None,None,None,*[c.byref(x)for x in outputs],None,None);actual=[x.value for x in outputs];assert status==0 and actual==[2,6,0,2,7,7],actual;report['cases'].append(dict(scope='Counts and UTF-16 maxima',result=status,values=actual))
  for capacity in [0,1]:
   text=c.create_unicode_buffer(2);text[0]='X';units=c.c_uint(capacity);status=api(int(key),text,c.byref(units),None,None,None,None,None,None,None,None,None);assert status==0 and not units.value,(capacity,status,units.value);report['cases'].append(dict(scope='Empty class buffer',capacity=capacity,result=status,units=units.value,first_unit=ord(text[0])))
  report['passed']=True
 finally:
  for child in children:winreg.DeleteKey(key,child)
  key.Close();winreg.DeleteKey(winreg.HKEY_CURRENT_USER,name)
 report['owned_fixture_removed']=True;report['observer_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();out=ROOT/'build/m14-native/stage8/registry-info-reference';out.mkdir(exist_ok=True);(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2))
if __name__=='__main__':main()
