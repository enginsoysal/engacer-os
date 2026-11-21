"""Actual current ELF/static state against immutable accepted M14.6 measurements."""
import hashlib,json,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tests/m12'))
from verify_components import desktop_state
def main():
 baseline_path=ROOT/'evidence/M14/6/static-resource-comparison.json';baseline=json.loads(baseline_path.read_text(encoding='utf-8'));assert baseline['passed'];accepted=json.loads((ROOT/'evidence/M14/6/acceptance-results.json').read_text(encoding='utf-8'));assert accepted['passed']and accepted['build_id']==baseline['build_id'];meta=json.loads((ROOT/'dist/m14stage7-build-manifest.json').read_text(encoding='utf-8'))
 for path,sha in meta['source_sha256'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,path
 current={}
 for kind,part in [('installed','-installed'),('live','')]:
  name='EngacerOS-M14STAGE7'+part+'-kernel.elf';image=ROOT/'dist'/name;raw=image.read_bytes();sha=hashlib.sha256(raw).hexdigest();assert sha==meta['artifacts'][name]['sha256']and raw[:5]==b'\x7fELF\x02';offset=struct.unpack_from('<Q',raw,32)[0];width,count=struct.unpack_from('<HH',raw,54);assert width==56 and count<=64 and offset+width*count<=len(raw);pages=set();segments=[]
  for index in range(count):
   typ,flags,start,virtual,physical,filesz,memsz,align=struct.unpack_from('<IIQQQQQQ',raw,offset+index*width)
   if typ!=1:continue
   assert filesz<=memsz and start+filesz<=len(raw)and memsz<32*1024**2;pages.update(range(physical//4096,(physical+memsz+4095)//4096));segments.append(dict(physical_start=physical,file_bytes=filesz,memory_bytes=memsz))
  sections={}
  for line in image.with_suffix('.map').read_text(encoding='utf-8').splitlines():
   values=line.split()
   if len(values)==5 and values[-1]in('.text','.rodata','.data','.bss'):sections[values[-1]]=int(values[2],16)
  assert set(sections)=={'.text','.rodata','.data','.bss'};current[kind]=dict(elf_sha256=sha,elf_file_bytes=len(raw),load_memory_bytes=sum(row['memory_bytes']for row in segments),rounded_physical_load_pages=len(pages),writable_static_sections_bytes=sections['.data']+sections['.bss'],sections=sections,segments=segments)
 previous=baseline['records']['M14.6'];report=dict(passed=True,build_id=meta['build_id'],baseline_build_id=baseline['build_id'],baseline_receipt_sha256=hashlib.sha256(baseline_path.read_bytes()).hexdigest(),records={'M14.6':previous,'M14.7':current},delta={kind:{key:current[kind][key]-previous[kind][key]for key in('elf_file_bytes','load_memory_bytes','rounded_physical_load_pages','writable_static_sections_bytes')}for kind in current},desktop_fixed=desktop_state(ROOT/'dist/EngacerOS-M14STAGE7-installed-kernel.map'),scope='Exact current ELF headers and writable state. Historical baseline is the immutable accepted receipt, not re-executed old source. Overlapping scopes, not total OS RAM or M14.15 CPU/storage optimization.',sources={'tests/m14/static147_host.py':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()});work=ROOT/'build/m14-native/stage7';out=work/'static-host';out.mkdir(exist_ok=True)
 for path in [out/'results.json',work/'static-resource-comparison.json']:path.write_bytes((json.dumps(report,indent=2)+'\n').encode())
 print(json.dumps(dict(delta=report['delta'],desktop_fixed_bytes=report['desktop_fixed']['bytes']),indent=2))
if __name__=='__main__':main()
