"""Compile the owned Unicode GDI pixel probe; never execute it on the host."""
import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/build'))
from m1 import command, pinned_tools


def build(profile='compact'):
    assert profile in ('compact', 'ordinary', '4k')
    out = ROOT / 'build/m14-native/stage6/font-fixture' / profile
    out.mkdir(parents=True, exist_ok=True)
    tools = pinned_tools()
    source = ROOT / 'tests/m14/font146_native.c'
    exports = set(re.findall(r'__declspec\(dllimport\).*?\b(\w+)\([^;]*;', source.read_text()))
    kernel = {'GetStdHandle', 'WriteFile', 'ExitProcess'}
    gdi = {'TextOutW', 'SetTextColor', 'SetBkMode', 'GetTextExtentPoint32W'}
    libraries = []
    for provider, names in [('kernel32', kernel), ('gdi32', gdi), ('user32', exports - kernel - gdi)]:
        definition = out / (provider + '.def')
        definition.write_bytes(('LIBRARY ' + provider + '.dll\nEXPORTS\n' + '\n'.join(sorted(names)) + '\n').encode())
        lib = out / (provider + '.lib')
        command([tools['lld-link'], '/lib', '/machine:x64', '/def:' + str(definition), '/out:' + str(lib)])
        libraries.append(lib)
    command([tools['clang'], '--target=x86_64-pc-windows-msvc', '-O2', '-Wall', '-Wextra', '-Werror',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-mno-stack-arg-probe',
             '-c', source, '-o', out / 'font.obj'])
    command([tools['lld-link'], '/nodefaultlib', '/timestamp:0', '/subsystem:windows', '/entry:entry',
             '/dynamicbase', '/fixed:no', '/out:' + str(out / 'font.exe'), out / 'font.obj', *libraries])
    return out / 'font.exe'


if __name__ == '__main__':
    build()
