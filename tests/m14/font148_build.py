"""Build owned font raster fixture without executing Windows code on the host."""
import re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command

def build():
 out=ROOT/'build/m14-native/stage8/font-fixture';out.mkdir(parents=True,exist_ok=True);t=pinned_tools();source=ROOT/'tests/m14/font148_native.c'
 names=set(re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;',source.read_text()))
 gp={'GdiplusStartup','GdiplusShutdown','GdipCreateFromHDC','GdipGraphicsClear','GdipDeleteGraphics','GdipCreateSolidFill','GdipDeleteBrush','GdipFillRectangleI','GdipCreateBitmapFromScan0','GdipDrawImageI','GdipDisposeImage','GdipGetImageGraphicsContext','GdipCreateFontFamilyFromName','GdipCreateFont','GdipDeleteFont','GdipDeleteFontFamily','GdipDrawString','GdipRotateWorldTransform','GdipTranslateWorldTransform'};shell={'SHChangeNotify'};kernel={'GetStdHandle','WriteFile','ExitProcess'};gdi={'CreateFontIndirectW','SelectObject','DeleteObject','SetTextColor','SetBkMode','TextOutW'}
 for provider,exports in [('kernel32',kernel),('gdi32',gdi),('gdiplus',gp),('shell32',shell),('user32',names-kernel-gdi-gp-shell)]:
  d=out/(provider+'.def');d.write_bytes(('LIBRARY '+provider+'.dll\nEXPORTS\n'+'\n'.join(sorted(exports))+'\n').encode());command([t['lld-link'],'/lib','/machine:x64','/def:'+str(d),'/out:'+str(out/(provider+'.lib'))])
 command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',source,'-o',out/'font.obj'])
 exe=out/'font.exe';command([t['lld-link'],'/nodefaultlib','/timestamp:0','/subsystem:windows','/entry:entry','/dynamicbase','/fixed:no','/out:'+str(exe),out/'font.obj',out/'kernel32.lib',out/'gdi32.lib',out/'gdiplus.lib',out/'user32.lib',out/'shell32.lib']);return exe
if __name__=='__main__':build()
