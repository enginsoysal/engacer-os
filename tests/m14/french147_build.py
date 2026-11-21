"""Build a private French preference fixture over an unchanged full-kernel ABI."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
from m8 import privacy_input
from m5_layout import compact_elf
from m14_integrity import verify_working_inputs
from runtime147_build import build as build_runtime

def build():
 base=json.loads((ROOT/'dist/m14stage7-build-manifest.json').read_text(encoding='utf-8'));tools=pinned_tools();commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();fixture_sha=hashlib.sha256((ROOT/'tests/m14/french147_native.c').read_bytes()).hexdigest();name='french-'+commit[:8]+'-'+fixture_sha[:8];out=ROOT/'build/m14-native/stage7'/('runtime-'+name)
 if not(out/'compile-inputs.json').exists():build_runtime(name)
 private=json.loads((out/'compile-inputs.json').read_text(encoding='utf-8'));verify_working_inputs(ROOT,private['source_sha256']);assert private['kernel_build_id']==base['build_id'];production=out/'WINDOWS8.ELF'
 flags=['-std=c17','-O2','-g','-fdebug-compilation-dir=.','-ffile-prefix-map='+str(ROOT)+'=.','-fdebug-prefix-map='+str(ROOT)+'=.','-ffile-prefix-map='+str(out)+'=/owned-install-fixture','-fdebug-prefix-map='+str(out)+'=/owned-install-fixture','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-red-zone','-mgeneral-regs-only','-Wall','-Wextra','-Werror','-I',ROOT/'include','-I',out]
 for milestone in ['M2','M6','M71','M72','M73','M74','M75','M8','M9','M92','M10','M11','M12','M14','M13','SETUP_MEDIA75','M7','M3','M4','M45','M51']:flags.append('-DENGINE_'+milestone)
 fixture=ROOT/'tests/m14/french147_native.c';obj=out/'fixture-msi147.o';command([tools['clang'],'--target=x86_64-unknown-none-elf',*flags,'-mcmodel=large','-fno-pic','-fno-pie','-fno-asynchronous-unwind-tables','-c',fixture,'-o',obj]);objects=sorted(p for p in out.glob('windows8-*.o')if p.name!='windows8-msi.o');binary=out/'fixture-runtime8.elf';command([tools['ld.lld'],'-T',ROOT/'user/windows8/linker.ld','--build-id=none','-o',binary,*objects,obj]);binary.write_bytes(compact_elf(binary.read_bytes()));data=binary.read_bytes();assert len(data)<=1024*1024 and str(ROOT).encode()not in privacy_input(data);verify_working_inputs(ROOT,private['source_sha256'])

 report=dict(scope=__doc__,kernel_build_id=base['build_id'],source_commit=commit,private_runtime_receipt_sha256=hashlib.sha256((out/'compile-inputs.json').read_bytes()).hexdigest(),test_sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ['tests/m14/french147_native.c','tests/m14/french147_build.py','tests/m14/fixture1.py']},artifacts={p.name:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())for p in [production,binary,out/'msi147/msi.dll',out/'msi147/msiexec.exe']});(out/'routing-inputs.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());return binary
if __name__=='__main__':build()
