"""Build the same Windows probe and two differently backed DLLs."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/build"))
from m1 import command, pinned_tools


def build():
    out = ROOT / "build/m14-native/stage10/private-storage-fixtures"
    out.mkdir(parents=True, exist_ok=True)
    clang, link = (pinned_tools()[name] for name in ("clang", "lld-link"))
    flags = ["--target=x86_64-pc-windows-msvc", "-O2", "-Wall", "-Wextra", "-Werror",
             "-ffreestanding", "-fno-builtin", "-fno-stack-protector", "-mno-stack-arg-probe"]
    for library, symbols in {
        "kernel32": "LoadLibraryW GetProcAddress FreeLibrary GetModuleFileNameW GetLastError GetTempPathW CreateFileW ReadFile WriteFile GetStdHandle CloseHandle ExitProcess",
        "advapi32": "RegCreateKeyExW RegQueryValueExW RegSetValueExW RegCloseKey",
    }.items():
        definition = out / (library + ".def")
        definition.write_bytes(("LIBRARY " + library + ".dll\nEXPORTS\n" + "\n".join(symbols.split()) + "\n").encode())
        command([link, "/lib", "/machine:x64", "/def:" + str(definition), "/out:" + str(out / (library + ".lib"))])

    sources = Path(__file__).resolve().parent
    app = out / "isolation.obj"
    command([clang, *flags, "-c", sources / "private1410_native.c", "-o", app])
    command([link, "/nodefaultlib", "/timestamp:0", "/subsystem:console", "/entry:entry",
             "/dynamicbase", "/fixed:no", "/out:" + str(out / "isolation.exe"),
             app, out / "kernel32.lib", out / "advapi32.lib"])
    for marker in ("A", "B"):
        folder = out / marker
        folder.mkdir(exist_ok=True)
        obj = folder / "bundle-test.obj"
        command([clang, *flags, "-DBUNDLE_IDENTITY=" + str(ord(marker)), "-c",
                 sources / "private1410_dll.c", "-o", obj])
        command([link, "/dll", "/noentry", "/nodefaultlib", "/timestamp:0", "/dynamicbase",
                 "/fixed:no", "/out:" + str(folder / "bundle-test.dll"), obj])
    return out


if __name__ == "__main__":
    build()
