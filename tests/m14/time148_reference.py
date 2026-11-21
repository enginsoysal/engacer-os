"""Read-only Windows UTC and calendar reference; no system-clock changes."""
import ctypes as C,datetime as D,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 k=C.WinDLL('kernel32',use_last_error=True);k.GetSystemTime.argtypes=[C.c_void_p];k.GetSystemTimeAsFileTime.argtypes=[C.c_void_p];k.FileTimeToSystemTime.argtypes=[C.c_void_p,C.c_void_p]
 epoch=D.datetime(1601,1,1)
 def ticks(dt):
  delta=dt-epoch;return (delta.days*86400+delta.seconds)*10000000+delta.microseconds*10
 def fields(dt):return [dt.year,dt.month,(dt.weekday()+1)%7,dt.day,dt.hour,dt.minute,dt.second,dt.microsecond//1000]
 rows=[]
 for dt in [epoch,D.datetime(1900,3,1),D.datetime(2000,2,29,23,59,58,123000),D.datetime(2024,2,29,12,34,56,789000),D.datetime(9999,12,31,23,59,59,999000)]:
  value=C.c_uint64(ticks(dt));out=(C.c_uint16*8)();assert k.FileTimeToSystemTime(C.byref(value),out);assert list(out)==fields(dt);rows.append(dict(filetime=value.value,systemtime=list(out)))
 before=C.c_uint64();after=C.c_uint64();out=(C.c_uint16*8)();k.GetSystemTimeAsFileTime(C.byref(before));k.GetSystemTime(out);k.GetSystemTimeAsFileTime(C.byref(after));v=list(out);converted=ticks(D.datetime(v[0],v[1],v[3],v[4],v[5],v[6],v[7]*1000));assert converted+9999>=before.value and converted<=after.value
 report=dict(passed=True,scope=__doc__,current_systemtime=v,bracket_before=before.value,bracket_after=after.value,vectors=rows,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
 target=ROOT/'build/m14-native/stage8/time-reference';target.mkdir(parents=True,exist_ok=True);(target/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
