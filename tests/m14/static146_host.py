"""Compare exact shipped ELF load pages and fixed writable linker sections."""
import hashlib,json,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
    records={};manifests={};builds={}
    for stage in (5,6):
        manifest_path=ROOT/f'dist/m14stage{stage}-build-manifest.json'
        meta=json.loads(manifest_path.read_text());builds[stage]=meta['build_id']
        manifests[f'M14.{stage}']=hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        if stage==5:
            public=json.loads((ROOT/'evidence/M14'/str(stage)/'downloads.json').read_text())
            assert public['passed']and public['build_id']==meta['build_id']
            assert next(row['sha256']for row in public['artifacts']if row['name']==manifest_path.name)==manifests[f'M14.{stage}']
        else:
            for path,digest in meta['source_sha256'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
        result={}
        for kind,part in [('installed','-installed'),('live','')]:
            name=f'EngacerOS-M14STAGE{stage}'+part+'-kernel.elf'
            image=ROOT/'dist'/name;raw=image.read_bytes();digest=hashlib.sha256(raw).hexdigest()
            assert digest==meta['artifacts'][name]['sha256']and raw[:5]==b'\x7fELF\x02'
            offset=struct.unpack_from('<Q',raw,32)[0];width,count=struct.unpack_from('<HH',raw,54)
            assert width==56 and count<=64 and offset+width*count<=len(raw)
            pages=set();segments=[]
            for index in range(count):
                typ,flags,start,virtual,physical,filesz,memsz,align=struct.unpack_from('<IIQQQQQQ',raw,offset+index*width)
                if typ!=1:continue
                assert filesz<=memsz and start+filesz<=len(raw)and memsz<32*1024**2
                pages.update(range(physical//4096,(physical+memsz+4095)//4096))
                segments.append(dict(physical_start=physical,file_bytes=filesz,memory_bytes=memsz))
            sections={}
            for line in image.with_suffix('.map').read_text().splitlines():
                values=line.split()
                if len(values)==5 and values[-1]in('.text','.rodata','.data','.bss'):sections[values[-1]]=int(values[2],16)
            assert set(sections)=={'.text','.rodata','.data','.bss'}
            result[kind]=dict(elf_sha256=digest,elf_file_bytes=len(raw),load_memory_bytes=sum(row['memory_bytes']for row in segments),rounded_physical_load_pages=len(pages),writable_static_sections_bytes=sections['.data']+sections['.bss'],sections=sections,segments=segments)
        records[f'M14.{stage}']=result
    result=dict(passed=True,build_id=builds[6],baseline_build_id=builds[5],manifest_sha256=manifests,records=records,scope='Exact ELF load headers and writable linker sections; overlapping scopes, not total OS RAM, dynamic tasks, framebuffer cost or CPU/storage performance',sources={'tests/m14/static146_host.py':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    current=records[f'M14.{6}'];baseline=records[f'M14.{5}']
    result['delta']={kind:{key:current[kind][key]-baseline[kind][key]for key in('elf_file_bytes','load_memory_bytes','rounded_physical_load_pages','writable_static_sections_bytes')}for kind in('installed','live')}
    work=ROOT/'build/m14-native/stage6';out=work/'static-host';out.mkdir(parents=True,exist_ok=True)
    for path in(out/'results.json',work/'static-resource-comparison.json'):path.write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps(result['delta'],indent=2))

if __name__=='__main__':main()
