"""Hosted regression for the production child image admission check."""
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
source = (ROOT / "kernel/windows8/process142.inc").read_text(encoding="utf-8")
start = source.index("static unsigned child_image142(")
end = source.index("static unsigned environment_validate143(", start)
fixture = r"""
#include <stdint.h>
#include <string.h>
#define ENGINE_M14
typedef struct { unsigned kind; uint64_t size; } v6_entry;
static v6_entry entry = {1,512};
static uint8_t image[512];
static const v6_entry *find8(const char *name) { return *name ? &entry : 0; }
static int exact8(const char *name,uint64_t off,void *out,unsigned length) {
    (void)name;
    if (off>entry.size || length>entry.size-off) return 1;
    memcpy(out,image+off,length);
    return 0;
}
static void put16(unsigned off,uint16_t value) { memcpy(image+off,&value,2); }
""" + source[start:end] + r"""
int main(void) {
    uint32_t pe=64;
    memcpy(image,"MZ",2);
    memcpy(image+60,&pe,4);
    memcpy(image+64,"PE\0\0",4);
    put16(68,0x8664);
    put16(84,240);
    put16(88,0x020b);
    put16(156,3);
    if (child_image142("helper")!=0) return 1;
    put16(68,0x014c);
    put16(88,0x010b);
    if (child_image142("helper")!=216) return 2;
    put16(84,500);
    if (child_image142("helper")!=193) return 3;
    put16(84,224);
    put16(88,0x020b);
    if (child_image142("helper")!=193) return 4;
    put16(88,0x010b);
    put16(86,0x2000);
    if (child_image142("helper")!=193) return 5;
    return child_image142("")!=2;
}
"""
with tempfile.TemporaryDirectory(prefix="engacer-m1410-pe-") as directory:
    path = Path(directory) / "pe.c"
    executable = path.with_suffix(".exe")
    path.write_text(fixture, encoding="utf-8")
    subprocess.run(["clang", "-std=c17", "-Wall", "-Wextra", "-Werror",
                    str(path), "-o", str(executable)], check=True)
    subprocess.run([str(executable)], check=True)
print("Child image admission passed for x64, x86 mismatch, truncated headers and DLL refusal")
