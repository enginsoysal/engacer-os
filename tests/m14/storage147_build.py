"""Build an explicitly test-only worker over the frozen production kernel ABI."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
from m8 import runtime,privacy_input
from m5_layout import compact_elf
from m14_integrity import verify_working_inputs,verify_committed_inputs

def build():
 base=json.loads((ROOT/'dist/m14stage7-build-manifest.json').read_text(encoding='utf-8'));verify_committed_inputs(ROOT,base['source_sha256'],base['source_commit']);out=ROOT/'build/m14-native/stage7/storage-fixture';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
 flags=['-std=c17','-O2','-g','-fdebug-compilation-dir=.','-ffile-prefix-map='+str(ROOT)+'=.','-fdebug-prefix-map='+str(ROOT)+'=.','-ffile-prefix-map='+str(out)+'=/owned-storage-fixture','-fdebug-prefix-map='+str(out)+'=/owned-storage-fixture','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-red-zone','-mgeneral-regs-only','-Wall','-Wextra','-Werror','-I',ROOT/'include','-I',out]
 for milestone in ['M2','M6','M71','M72','M73','M74','M75','M8','M9','M92','M10','M11','M12','M14','M13','SETUP_MEDIA75','M7','M3','M4','M45','M51']:flags.append('-DENGINE_'+milestone)
 runtime(out,tools,flags);production=out/'production-runtime8.elf';production.write_bytes((out/'WINDOWS8.ELF').read_bytes());fixture=ROOT/'tests/m14/storage147_native.c';obj=out/'fixture-msi147.o';command([tools['clang'],'--target=x86_64-unknown-none-elf',*flags,'-mcmodel=large','-fno-pic','-fno-pie','-fno-asynchronous-unwind-tables','-c',fixture,'-o',obj]);objects=sorted(p for p in out.glob('windows8-*.o')if p.name!='windows8-msi.o');binary=out/'fixture-runtime8.elf';command([tools['ld.lld'],'-T',ROOT/'user/windows8/linker.ld','--build-id=none','-o',binary,*objects,obj]);binary.write_bytes(compact_elf(binary.read_bytes()));data=binary.read_bytes();assert len(data)<=1024*1024 and str(ROOT).encode()not in privacy_input(data);verify_working_inputs(ROOT,base['source_sha256'])
 report=dict(scope='Own primitive test worker replaces only msi8_execute; confirmed real INSTALL job and unchanged production kernel. Not an original MSI installer task or public media.',kernel_build_id=base['build_id'],source_commit=base['source_commit'],test_sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ['tests/m14/storage147_native.c','tests/m14/storage147_build.py']},artifacts={p.name:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())for p in [production,binary]});(out/'compile-inputs.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());return binary
if __name__=='__main__':build()
