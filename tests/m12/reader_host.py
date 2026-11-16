"""Production FAT32 code: real owned image, I/O counts, fragmentation and faults."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE7'
import transfers_native as native
ROOT=native.ROOT;sys.path.insert(0,str(ROOT/'tools/build'));from m1 import pinned_tools

def main():
    out=ROOT/'build/m12/stage7/reader-host';out.mkdir(parents=True,exist_ok=True);work=native.ui.q.new_work('m12-stage7-reader-host');image,payload=native.fixture(work)
    from pyfatfs.PyFatFS import PyFatFS
    with PyFatFS(str(image),preserve_case=True) as fs:
        with fs.openbin('/Fragment.bin','w') as file:
            for i in range(128):file.write(payload[:2048]);file.flush();fs.writebytes('/Gap'+str(i)+'.bin',b'G'*2048)
        fs.writebytes('/Odd.bin',payload[:12345]);fs.writebytes('/Empty.bin',b'')
    before=native.f.sha_file(image);exe=out/'reader.exe'
    subprocess.run([pinned_tools()['clang'],'-std=c17','-O2','-Wall','-Wextra','-Werror','-Iinclude','tests/m12/reader_host.c','-o',str(exe)],cwd=ROOT,check=True)
    run=subprocess.run([str(exe),str(image)],cwd=ROOT,capture_output=True,check=True);result=json.loads(run.stdout);assert result['passed'] and native.f.sha_file(image)==before
    reference=subprocess.check_output(['git','rev-parse','f550385^{commit}'],cwd=ROOT).decode().strip();legacy=out/'reference';legacy.mkdir(exist_ok=True);baseline_hashes={}
    for name in ('fat32.c','fat32-write10.inc'):
        raw=subprocess.check_output(['git','show',reference+':kernel/storage/'+name],cwd=ROOT);(legacy/name).write_bytes(raw);baseline_hashes['kernel/storage/'+name]=hashlib.sha256(raw).hexdigest()
    oldexe=out/'reader-reference.exe'
    subprocess.run([pinned_tools()['clang'],'-std=c17','-O2','-Wall','-Wextra','-Werror','-Iinclude','-DREADER_BASELINE12','-DFAT32_SOURCE12="'+(legacy/'fat32.c').as_posix()+'"','tests/m12/reader_host.c','-o',str(oldexe)],cwd=ROOT,check=True)
    baseline=json.loads(subprocess.check_output([str(oldexe),str(image)],cwd=ROOT));assert baseline['passed'] and native.f.sha_file(image)==before
    result['baseline']=dict(**baseline,source_commit=reference,source_sha256=baseline_hashes)
    result['io_command_ratio']=baseline['full_single_sector_reads']/(result['full_single_sector_reads']+result['full_data_commands'])
    assert result['io_command_ratio']>10
    result['scope']='Production old/new readers validate the same owned FAT32 bytes. I/O request counts are a host control-flow measurement, not physical/VM throughput or a human study.'
    result['owned_fixture']=work.name;result['image_sha256']=before;result['image_unchanged']=True
    paths=['kernel/storage/fat32.c','kernel/storage/fat32-write10.inc','include/engine/hardware10.h','tests/m12/reader_host.c']
    result['source_sha256']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
    (out/'results.json').write_bytes((json.dumps(result,indent=2)+'\n').encode());print(json.dumps(result,indent=2))
if __name__=='__main__':main()
