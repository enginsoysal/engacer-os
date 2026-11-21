"""Observe original Windows locks on one owned running reference image; no third-party execution or user-file mutation."""
import ctypes as C,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
def main():
 out=(ROOT/'build/m14-native/stage8/image-source-reference').resolve();out.mkdir(parents=True,exist_ok=True);source=ROOT/'tests/m14/image_source148_reference.c';t=pinned_tools();definition=out/'kernel32.def';definition.write_text('LIBRARY kernel32.dll\nEXPORTS\nGetStdHandle\nWriteFile\nSleep\nExitProcess\n')
 command([t['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/'kernel32.lib')]);command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',source,'-o',out/'reference.obj'])
 exe=out/'owned-image148.exe';renamed=out/'owned-image148-renamed.exe';assert exe.parent==out and renamed.parent==out
 command([t['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(exe),out/'reference.obj',out/'kernel32.lib']);original=exe.read_bytes()
 k=C.WinDLL('kernel32',use_last_error=True);k.CreateFileW.argtypes=[C.c_wchar_p,C.c_uint32,C.c_uint32,C.c_void_p,C.c_uint32,C.c_uint32,C.c_void_p];k.CreateFileW.restype=C.c_void_p;k.CloseHandle.argtypes=[C.c_void_p];k.DeleteFileW.argtypes=[C.c_wchar_p];k.MoveFileW.argtypes=[C.c_wchar_p,C.c_wchar_p]
 process=subprocess.Popen([str(exe)],stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=0x08000000);observed={}
 try:
  assert process.stdout.readline()==b'READY\n'and process.poll()is None
  C.set_last_error(0);handle=k.CreateFileW(str(exe),0x40000000,7,None,3,0x80,None);observed['open_write']=dict(succeeded=handle!=C.c_void_p(-1).value,error=C.get_last_error())
  if handle!=C.c_void_p(-1).value:assert k.CloseHandle(handle)
  C.set_last_error(0);deleted=k.DeleteFileW(str(exe));observed['delete_running']=dict(succeeded=bool(deleted),error=C.get_last_error())
  if exe.exists():
   assert not renamed.exists();C.set_last_error(0);moved=k.MoveFileW(str(exe),str(renamed));observed['rename_running']=dict(succeeded=bool(moved),error=C.get_last_error())
  assert process.wait(timeout=10)==0
 finally:
  if process.poll()is None:process.kill();process.wait(timeout=10)
  if renamed.exists():renamed.replace(exe)
  if not exe.exists():exe.write_bytes(original)
 assert exe.read_bytes()==original
 report=dict(passed=True,scope=__doc__,observations=observed,reference_image_sha256=hashlib.sha256(original).hexdigest(),source_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in[source,Path(__file__)]})
 (out/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,observations=observed),indent=2))
if __name__=='__main__':main()
