"""Own off-screen Windows affine reference against actual production scalar math."""
import ctypes as c,hashlib,json,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
H=c.c_void_p;V=c.c_float*6
class INPUT(c.Structure):_fields_=[('version',c.c_uint),('callback',H),('thread',c.c_int),('codecs',c.c_int)]
def main():
 out=ROOT/'build/m14-native/stage8/transform-reference';out.mkdir(parents=True,exist_ok=True);t=pinned_tools();source=ROOT/'tests/m14/transform148_reference.c';obj=out/'math.obj';dll=out/'math.dll';command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-mgeneral-regs-only','-c',source,'-o',obj]);command([t['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(dll),obj]);own=c.CDLL(str(dll));own.rotate.argtypes=[c.c_float,c.POINTER(c.c_float)];own.combine.argtypes=[c.POINTER(c.c_float),c.POINTER(c.c_float),c.c_int]
 gp=c.WinDLL('gdiplus');gp.GdiplusStartup.argtypes=[c.POINTER(c.c_size_t),c.POINTER(INPUT),H];gp.GdiplusShutdown.argtypes=[c.c_size_t];gp.GdipCreateMatrix2.argtypes=[c.c_float]*6+[c.POINTER(H)];gp.GdipRotateMatrix.argtypes=[H,c.c_float,c.c_int];gp.GdipMultiplyMatrix.argtypes=[H,H,c.c_int];gp.GdipGetMatrixElements.argtypes=[H,c.POINTER(c.c_float)];gp.GdipDeleteMatrix.argtypes=[H];token=c.c_size_t();assert not gp.GdiplusStartup(c.byref(token),INPUT(1,None,0,0),None);rng=random.Random(148);rotations=0;products=0;max_rotation=max_product=0.0
 try:
  angles=[-720,-360,-180,-90,-45,0,45,90,180,360,720]+[rng.uniform(-720,720)for _ in range(500)]
  for angle in angles:
   angle=c.c_float(angle).value;matrix=H();expected=V();actual=V();assert not gp.GdipCreateMatrix2(1,0,0,1,0,0,c.byref(matrix))
   try:assert not gp.GdipRotateMatrix(matrix,angle,0)and not gp.GdipGetMatrixElements(matrix,expected)and not own.rotate(angle,actual)
   finally:assert not gp.GdipDeleteMatrix(matrix)
   delta=max(abs(a-b)for a,b in zip(actual,expected));assert delta<0.000002,(angle,list(actual),list(expected),delta);max_rotation=max(max_rotation,delta);rotations+=1
  for order in [0,1]:
   for _ in range(256):
    a=V(*[rng.uniform(-8,8)for _ in range(6)]);b=V(*[rng.uniform(-8,8)for _ in range(6)]);matrix=H();operation=H();expected=V();actual=V(*a);assert not gp.GdipCreateMatrix2(*a,c.byref(matrix))and not gp.GdipCreateMatrix2(*b,c.byref(operation))
    try:assert not gp.GdipMultiplyMatrix(matrix,operation,order)and not gp.GdipGetMatrixElements(matrix,expected)and not own.combine(actual,b,order)
    finally:assert not gp.GdipDeleteMatrix(matrix)and not gp.GdipDeleteMatrix(operation)
    delta=max(abs(x-y)for x,y in zip(actual,expected));assert delta<0.00004,(order,list(actual),list(expected),delta);max_product=max(max_product,delta);products+=1
  guard=V(1,0,0,1,10,20);saved=list(guard);assert own.combine(guard,V(1,0,0,1,0,0),2)==2 and list(guard)==saved;assert own.rotate(float('nan'),V())==2
 finally:gp.GdiplusShutdown(token)
 paths=['user/windows8/transform-math148.h','tests/m14/transform148_reference.c','tests/m14/transform148_reference.py'];report=dict(passed=True,scope=__doc__,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in paths},own_dll_sha256=hashlib.sha256(dll.read_bytes()).hexdigest(),rotation_cases=rotations,prepend_append_products=products,max_absolute_rotation_error=max_rotation,max_absolute_product_error=max_product,invalid_order_preserves_state=True,visible_windows_created=0)
 (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2))
if __name__=='__main__':main()
