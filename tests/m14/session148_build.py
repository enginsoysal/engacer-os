"""Build owned native message/SRW callers with unchanged vendor bodies separate."""
import hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
def build():
 out=ROOT/'build/m14-native/stage8/session-fixture';out.mkdir(parents=True,exist_ok=True)
 t=pinned_tools();source=ROOT/'tests/m14/session148_native.c'
 imports=set(re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;',source.read_text()))
 user={'RegisterWindowMessageW','RegisterWindowMessageA','PeekMessageW','PostMessageW','RegisterClassExW','GetClassInfoExW','UnregisterClassW','CreateWindowExW','DestroyWindow','GetDesktopWindow','GetParent','IsWindow','GetWindowRect','GetClientRect','GetSystemMetrics','GetDC','ReleaseDC','GetWindowLongW','GetWindowLongPtrW','SetWindowLongPtrW','AdjustWindowRectEx','AdjustWindowRect','SetWindowPos','DefWindowProcW','SendMessageW','GetWindowDC','DrawTextExW','MonitorFromRect','MonitorFromPoint','GetMonitorInfoW','GetMonitorInfoA','SetForegroundWindow','GetForegroundWindow','MsgWaitForMultipleObjects','SetTimer','KillTimer','MapWindowPoints'};gdi={'GetDeviceCaps','CreateFontIndirectW','GetStockObject','SelectObject','GetCurrentObject','GetObjectW','GetTextMetricsW','GetTextFaceW','GetTextExtentPoint32W','DeleteObject','TextOutW'}
 advapi={'RegCreateKeyExW','RegOpenKeyExW','RegSetValueExW','RegQueryValueExW','RegDeleteKeyW','RegCloseKey'};shell={'SHDeleteValueW'}
 for provider,names in [('user32',user),('gdi32',gdi),('advapi32',advapi),('shlwapi',shell),('kernel32',imports-user-gdi-advapi-shell)]:
  definition=out/(provider+'.def');definition.write_bytes(('LIBRARY '+provider+'.dll\nEXPORTS\n'+'\n'.join(sorted(names))+'\n').encode())
  command([t['lld-link'],'/lib','/machine:x64','/def:'+str(definition),'/out:'+str(out/(provider+'.lib'))])
 command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-I',ROOT/'include','-c',source,'-o',out/'probe.obj'])
 exe=out/'probe.exe';command([t['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:console','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(exe),out/'probe.obj',out/'kernel32.lib',out/'user32.lib',out/'gdi32.lib',out/'advapi32.lib',out/'shlwapi.lib'])
 (out/'compile-inputs.json').write_bytes((json.dumps(dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),fixture_sha256=hashlib.sha256(exe.read_bytes()).hexdigest()),indent=2)+'\n').encode());return exe
if __name__=='__main__':build()
