"""Original helper diagnostic with an identified runtime and frozen kernel.

This mixed development image never qualifies an ISO or original-app task.
The canonical original observer retains all app hashes and ordinary input.
"""
import hashlib
import json
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    picker = '--picker' in sys.argv
    if picker:
        sys.argv.remove('--picker')
    sys.path.insert(0, str(ROOT / 'tools/build'))
    from m1 import pinned_tools
    from m8 import runtime

    meta = json.loads((ROOT / 'dist/m14stage6-build-manifest.json').read_text())
    for path, digest in meta['source_sha256'].items():
        if path.startswith(('kernel/', 'include/', 'boot/')):
            assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    out = ROOT / 'build/m14-native/stage6/helper-runtime-traces' / uuid.uuid4().hex
    work = out / 'runtime'
    work.mkdir(parents=True)
    inputs = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted((ROOT / 'user/windows8').glob('*')) if p.is_file()}
    common = ['-std=c17', '-O2', '-ffreestanding', '-fno-builtin',
              '-fno-stack-protector', '-mno-red-zone', '-mgeneral-regs-only',
              '-Wall', '-Wextra', '-Werror', '-DENGINE_M10', '-DENGINE_M14',
              '-I', ROOT / 'include']
    runtime(work, pinned_tools(), common)
    rt = work / 'WINDOWS8.ELF'
    digest = hashlib.sha256(rt.read_bytes()).hexdigest()
    original = ROOT / 'tests/m14/original_add146_run.py'
    source = original.read_bytes().decode('utf-8')
    before = "out=ROOT/'build/m14-native/stage6'/('original-add-probe'+(''if profile=='compact'else'-'+profile))"
    assert source.count(before) == 1
    source = source.replace(before, 'out=trace_out')
    before = 'mounted=StoppedDisk(disk,library());folder='
    assert source.count(before) == 1
    source = source.replace(before, "mounted=StoppedDisk(disk,library());mounted.put('/System/Windows/runtime8.elf',trace_runtime.read_bytes());folder=")
    source = source.replace('report=dict(passed=False,', 'report=dict(mixed_runtime=True,runtime_sha256=trace_digest,passed=False,')
    source = source.replace('m146-original-add-probe', 'm146-original-add-mixed-trace')
    callback = None
    if picker:
        from original_picker146_probe import dialog_task
        callback = dialog_task
        before = "c.shot(g,'original-add-selected')"
        assert source.count(before) == 1
        source = source.replace(before, "c.key(g,'ctrl','c');" + before)
        before = "c.shot(g,'original-add-result');report['scope']="
        assert source.count(before) == 1
        source = source.replace(before, 'trace_picker146(g,p,report);' + before)
    source = source.replace('Read-only native diagnostic of the actual original 7-Zip Add action; no archive/common-dialog compatibility qualification',
                            'Mixed frozen-kernel/new-runtime original helper diagnostic only; no ISO or original-app qualification')
    receipt = dict(kernel_build_id=meta['build_id'], mixed_candidate=True, original_picker=picker,
                   scope='Diagnostic only; never stage or release qualification',
                   runtime_sha256=digest, runtime_source_sha256=inputs,
                   canonical_observer_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),
                   adapted_observer_sha256=hashlib.sha256(source.encode()).hexdigest(),
                   adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    if picker:
        receipt['picker_observer_sha256'] = hashlib.sha256((ROOT / 'tests/m14/original_picker146_probe.py').read_bytes()).hexdigest()
    (out / 'identity.json').write_bytes((json.dumps(receipt, indent=2) + '\n').encode())
    namespace = dict(__file__=str(original), __name__='original_add_mixed146',
                     trace_out=out, trace_runtime=rt, trace_digest=digest, trace_picker146=callback)
    exec(compile(source, str(original), 'exec'), namespace)
    namespace['main']()
    for path, wanted in inputs.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == wanted, path
    print('Mixed runtime diagnostic: ' + out.relative_to(ROOT).as_posix(), flush=True)


if __name__ == '__main__':
    main()
