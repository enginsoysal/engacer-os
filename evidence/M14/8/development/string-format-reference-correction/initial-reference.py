"""Own off-screen GDI+ text-format behavior, independent of vendor executables."""
import ctypes as c,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];H=c.c_void_p
class INPUT(c.Structure):_fields_=[('version',c.c_uint),('callback',H),('thread',c.c_int),('codecs',c.c_int)]

def main():
 p=c.WinDLL('gdiplus');p.GdiplusStartup.argtypes=[c.POINTER(c.c_size_t),c.POINTER(INPUT),H];p.GdiplusShutdown.argtypes=[c.c_size_t];p.GdipCreateStringFormat.argtypes=[c.c_int,c.c_ushort,c.POINTER(H)];p.GdipDeleteStringFormat.argtypes=[H];p.GdipCloneStringFormat.argtypes=[H,c.POINTER(H)]
 for name in ['Flags','Align','LineAlign','Trimming','MeasurableCharacterRangeCount']:getattr(p,'GdipGetStringFormat'+name).argtypes=[H,c.POINTER(c.c_int)]
 for name in ['Flags','Align','LineAlign','Trimming']:getattr(p,'GdipSetStringFormat'+name).argtypes=[H,c.c_int]
 p.GdipSetStringFormatMeasurableCharacterRanges.argtypes=[H,c.c_int,H]
 token=c.c_size_t();assert not p.GdiplusStartup(c.byref(token),INPUT(1,None,0,0),None);rows=[]
 def value(h,name):
  out=c.c_int(-99);assert not getattr(p,'GdipGetStringFormat'+name)(h,c.byref(out));return out.value
 try:
  for creator,expected in [('GdipCreateStringFormat',[0,0,0,1,0]),('GdipStringFormatGetGenericDefault',[0,0,0,1,0]),('GdipStringFormatGetGenericTypographic',[0x6004,0,0,0,0])]:
   h=H();fn=getattr(p,creator)
   if creator=='GdipCreateStringFormat':status=fn(0,0,c.byref(h))
   else:fn.argtypes=[c.POINTER(H)];status=fn(c.byref(h))
   assert not status;names=['Flags','Align','LineAlign','Trimming','MeasurableCharacterRangeCount'];actual=[value(h,name)for name in names];assert actual==expected;rows.append(dict(creator=creator,defaults=actual))
   try:
    for name in ['Flags','Align','LineAlign','Trimming']:
     for next_value in [-1,0,1,2,3,5,6,0x7fffffff]:
      before=value(h,name);status=getattr(p,'GdipSetStringFormat'+name)(h,next_value);valid=name=='Flags' or 0<=next_value<=(5 if name=='Trimming' else 2);assert status==(0 if valid else 2) and value(h,name)==(next_value if valid else before);rows.append(dict(property=name,input=next_value,status=status))
    ranges=(c.c_int*66)()
    for count in [-1,0,1,32,33]:
     before=value(h,'MeasurableCharacterRangeCount');status=p.GdipSetStringFormatMeasurableCharacterRanges(h,count,ranges);assert status==(11 if count>32 else 0) and value(h,'MeasurableCharacterRangeCount')==(before if count>32 else count);rows.append(dict(range_count=count,status=status))
    assert p.GdipSetStringFormatMeasurableCharacterRanges(h,0,None)==2;clone=H();assert not p.GdipCloneStringFormat(h,c.byref(clone)) and clone.value!=h.value
    try:
     before=value(h,'Flags');assert not p.GdipSetStringFormatFlags(clone,0x12345678) and value(h,'Flags')==before
    finally:assert not p.GdipDeleteStringFormat(clone)
   finally:assert not p.GdipDeleteStringFormat(h)
 finally:p.GdiplusShutdown(token)
 report=dict(passed=True,scope=__doc__,cases=rows,clone_mutation_independent=True,visible_windows_created=0)
 out=ROOT/'build/m14-native/stage8/format-reference';out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(dict(passed=True,cases=len(rows))))
if __name__=='__main__':main()
