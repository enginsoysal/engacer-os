"""Compile the owned pending-dialog teardown fixture."""
import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/build'))
from m1 import command, pinned_tools


def build():
    out = ROOT / 'build/m14-native/stage6/picker-lifetime-fixture'
    out.mkdir(parents=True, exist_ok=True)
    tools = pinned_tools()
    source = ROOT / 'tests/m14/picker_lifetime146_native.c'
    exports = set(re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;', source.read_text()))
    user = {'RegisterClassW', 'CreateWindowExW', 'DefWindowProcW', 'DestroyWindow', 'SetTimer', 'KillTimer'}
    dialog = {'GetOpenFileNameW', 'GetSaveFileNameW', 'CommDlgExtendedError'}
    libraries = []
    for provider, names in [('kernel32', exports - user - dialog), ('user32', user), ('comdlg32', dialog)]:
        definition = out / (provider + '.def')
        definition.write_bytes(('LIBRARY ' + provider + '.dll\nEXPORTS\n' + '\n'.join(sorted(names)) + '\n').encode())
        lib = out / (provider + '.lib')
        command([tools['lld-link'], '/lib', '/machine:x64', '/def:' + str(definition), '/out:' + str(lib)])
        libraries.append(lib)
    command([tools['clang'], '--target=x86_64-pc-windows-msvc', '-O2', '-Wall', '-Wextra', '-Werror',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-mno-stack-arg-probe', '-I', ROOT / 'include',
             '-c', source, '-o', out / 'lifetime.obj'])
    command([tools['lld-link'], '/nodefaultlib', '/timestamp:0', '/subsystem:windows', '/entry:entry',
             '/dynamicbase', '/fixed:no', '/out:' + str(out / 'lifetime.exe'), out / 'lifetime.obj', *libraries])
    return out / 'lifetime.exe'


if __name__ == '__main__':
    build()
