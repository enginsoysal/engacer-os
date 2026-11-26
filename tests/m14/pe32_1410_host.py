"""Build an actual i386 PE and exercise native loader code without executing it."""
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[2]
with TemporaryDirectory() as work:
    work = Path(work)
    source = work / "helper.c"
    source.write_text(
        "static unsigned value=42; static unsigned *volatile pointer=&value;\n"
        "unsigned entry(void){return *pointer;}\n", encoding="utf-8")
    obj = work / "helper.obj"
    image = work / "helper.exe"
    subprocess.run(["clang", "--target=i386-pc-windows-msvc", "-O2", "-ffreestanding",
                    "-c", str(source), "-o", str(obj)], check=True)
    subprocess.run(["lld-link", "/machine:x86", "/entry:entry", "/nodefaultlib",
                    "/subsystem:console", "/dynamicbase", "/fixed:no", "/safeseh:no",
                    "/timestamp:0", "/out:" + str(image), str(obj)], check=True)
    native = work / "loader-test.exe"
    subprocess.run(["clang", "-Wall", "-Wextra", "-Werror", "-I", str(ROOT / "include"),
                    str(ROOT / "tests/m14/pe32_1410_host.c"), "-o", str(native)], check=True)
    subprocess.run([str(native), str(image)], check=True)
print("PE32 section loading, HIGHLOW relocations and section protections passed")
