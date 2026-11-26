"""Build a native AMD64 parent and i386 Windows helpers for the M14.10 guest."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]


def build():
    out = ROOT / "build/m14-native/stage10/x86-fixtures"
    out.mkdir(parents=True, exist_ok=True)
    sources = Path(__file__).resolve().parent
    common = ["-O2", "-Wall", "-Wextra", "-Werror", "-ffreestanding", "-fno-builtin",
              "-fno-stack-protector", "-mno-stack-arg-probe"]

    def library(machine, exports):
        definition = out / ("kernel-" + machine + ".def")
        definition.write_bytes(("LIBRARY kernel32.dll\nEXPORTS\n" + "\n".join(exports) + "\n").encode())
        result = out / ("kernel-" + machine + ".lib")
        subprocess.run(["lld-link", "/lib", "/machine:" + machine, "/def:" + str(definition),
                        "/out:" + str(result)], check=True)
        return result

    x64 = library("x64", "CreateProcessW WaitForSingleObject GetExitCodeProcess ExitProcess GetStdHandle WriteFile CloseHandle".split())
    symbols = {"ExitProcess": 4, "GetCurrentProcessId": 0, "GetLastError": 0,
               "SetLastError": 4, "GetStdHandle": 4, "WriteFile": 20}
    x86 = library("x86", [f"_{name}@{size} == {name}" for name, size in symbols.items()])

    for name, machine, target, source, lib, flags in [
        ("x86-parent", "x64", "x86_64", "x86_parent1410.c", x64, []),
        ("helper32", "x86", "i386", "x86_child1410.c", x86, []),
        ("fault32", "x86", "i386", "x86_child1410.c", x86, ["-DTEST_FAULT"]),
    ]:
        obj = out / (name + ".obj")
        subprocess.run(["clang", "--target=" + target + "-pc-windows-msvc",
                        *common, *flags, "-c", str(sources / source), "-o", str(obj)], check=True)
        options = ["/safeseh:no"] if machine == "x86" else []
        subprocess.run(["lld-link", "/machine:" + machine, "/nodefaultlib", "/timestamp:0",
                        "/subsystem:console", "/entry:entry", "/dynamicbase", "/fixed:no",
                        *options, "/out:" + str(out / (name + ".exe")), str(obj), str(lib)], check=True)
    return out


if __name__ == "__main__":
    build()
