"""Fresh production objects plus a labelled private original-EXE routing probe."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools
from m5_layout import compact_elf
from m14_integrity import verify_working_inputs

def build():
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    name='exe148-'+commit[:8]
    canonical=ROOT/'tests/m14/runtime147_build.py'
    raw=canonical.read_bytes();source=raw.decode()
    before="out=ROOT/'build/m14-native/stage7'/('runtime-'+name)"
    assert source.count(before)==1
    source=source.replace(before,"out=ROOT/'build/m14-native/stage8'/('runtime-'+name)")
    source=source.replace('dist/m14stage7-build-manifest.json','dist/m14stage8-build-manifest.json')
    scope=dict(__file__=str(canonical),__name__='exe148_private_production_build')
    exec(compile(source,str(canonical),'exec'),scope)
    out=ROOT/'build/m14-native/stage8'/('runtime-'+name)
    if not(out/'compile-inputs.json').exists():scope['build'](name)
    receipt=json.loads((out/'compile-inputs.json').read_text(encoding='utf-8'))
    verify_working_inputs(ROOT,receipt['source_sha256'])
    tools=pinned_tools();flags=[str(x).replace('<project-root>',str(ROOT))for x in receipt['compiler_flags']]
    obj=out/'exe148-dispatch.o'
    command([tools['clang'],'--target=x86_64-unknown-none-elf',*flags,'-mcmodel=large','-fno-pic','-fno-pie','-fno-asynchronous-unwind-tables','-c',ROOT/'tests/m14/exe148_probe_dispatch.c','-o',obj])
    objects=sorted(p for p in out.glob('windows8-*.o')if p.name!='windows8-msi.o')
    binary=out/'exe148-private-runtime.elf'
    command([tools['ld.lld'],'-T',ROOT/'user/windows8/linker.ld','--build-id=none','-o',binary,*objects,obj])
    binary.write_bytes(compact_elf(binary.read_bytes()))
    report=dict(scope=__doc__,kernel_build_id=receipt['kernel_build_id'],source_commit=commit,
        private_dispatch_only=True,ordinary_installer_route_qualified=False,
        canonical_recipe_sha256=hashlib.sha256(raw).hexdigest(),executed_recipe_sha256=hashlib.sha256(source.encode()).hexdigest(),
        production_receipt_sha256=hashlib.sha256((out/'compile-inputs.json').read_bytes()).hexdigest(),
        test_sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ['tests/m14/exe148_probe_dispatch.c','tests/m14/exe148_probe_build.py']},
        runtime_sha256=hashlib.sha256(binary.read_bytes()).hexdigest())
    (out/'exe148-routing-inputs.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    return binary,report

if __name__=='__main__':build()
