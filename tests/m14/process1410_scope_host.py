"""Test the production process-query owner check with two live app spaces."""
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/build"))
from m1 import pinned_tools


def main():
    production = (ROOT / "kernel/windows8/process142.inc").read_text(encoding="utf-8")
    start = production.index("static int64_t open_process148(")
    end = production.index("static int64_t process_image148(", start)
    fixture = """
#include <stdint.h>
#include <string.h>
typedef struct { unsigned pid, live; } object;
typedef struct { unsigned access; } handle;
typedef struct { unsigned object; handle handles[1]; char named_owner1410[256]; } private_space142;
#define SPACES142 3
static object process_objects142[SPACES142] = {{10,1},{11,1},{12,1}};
static private_space142 states[SPACES142] = {
    {.object=0,.named_owner1410="app-a"},
    {.object=1,.named_owner1410="app-a"},
    {.object=2,.named_owner1410="app-b"}
};
static private_space142 *spaces142[SPACES142] = {states,states+1,states+2};
static unsigned active_space142;
typedef object process_object142;
static int equal8(const char *a,const char *b) { return strcmp(a,b)==0; }
static uint64_t new_process_handle142(unsigned index,unsigned kind) {
    return kind==1 ? index+1 : 0;
}
static int process_handle_slot142(uint64_t value) { return value ? 0 : -1; }
""" + production[start:end] + """
int main(void) {
    if (open_process148(11,0x1000,0)!=2 || states[0].handles[0].access!=0x1000) return 1;
    if (open_process148(12,0x1000,0)!=-5) return 2;
    active_space142=2;
    if (open_process148(10,0x1000,0)!=-5 || open_process148(12,0x1000,0)!=3) return 3;
    process_objects142[2].live=0;
    return open_process148(12,0x1000,0)!=-87 ? 4 : 0;
}
"""
    with tempfile.TemporaryDirectory(prefix="engacer-m1410-process-") as directory:
        source = Path(directory) / "process.c"
        binary = Path(directory) / "process.exe"
        source.write_text(fixture, encoding="utf-8")
        subprocess.run([pinned_tools()["clang"], "-std=c17", "-Wall", "-Wextra",
                        "-Werror", str(source), "-o", str(binary)], check=True)
        subprocess.run([str(binary)], check=True)
    print("Same-owner process query, foreign-owner denial and exited process check passed")


if __name__ == "__main__":
    main()
