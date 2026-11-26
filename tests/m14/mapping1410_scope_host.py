"""Hosted regression for the production named-mapping lookup policy."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/build"))
from m1 import pinned_tools


def main():
    canonical = ROOT / "tests/m14/mapping146_host.c"
    source = canonical.read_text(encoding="utf-8")
    include = '#include "../../kernel/windows8/mapping146.inc"'
    assert source.count(include) == 1
    source = source.replace(include, '''static char scope_a[256] = "app-a";
static char scope_b[256] = "app-b";
#define W8_NAMED_OWNER (active_space142 == 2 ? scope_b : scope_a)
#include "kernel/windows8/mapping146.inc"''')
    source = source.replace("strcpy(sync_objects[0].owner,input8.user_root)",
                            "strcpy(sync_objects[0].owner,W8_NAMED_OWNER)")
    needle = " mapping_generation146=0x7fffff;"
    assert source.count(needle) == 1
    source = source.replace(needle, '''
 request(&r,4096);
 CHECK(!create(&r,&out,0)&&!out.existed);
 uint64_t a=out.handle;
 ((unsigned char*)(uintptr_t)mapping_objects146[0]->pages[0])[0]=42;
 active_space142=2;
 memset(&r,0,sizeof(r));r.name[0]='T';r.access=4;
 CHECK(create(&r,&out,1)==-2);
 request(&r,4096);
 CHECK(!create(&r,&out,0)&&!out.existed);
 uint64_t b=out.handle;
 CHECK(mapping_objects146[0]->pages[0]!=mapping_objects146[1]->pages[0]);
 CHECK(((unsigned char*)(uintptr_t)mapping_objects146[1]->pages[0])[0]==0);
 active_space142=0;CHECK(!mapping_close146(a));
 active_space142=2;CHECK(mapping_slot146(b)>=0&&!mapping_close146(b));
 CHECK(!live&&!mapping_resident146);
 active_space142=0;
''' + needle)
    with tempfile.TemporaryDirectory(prefix="engacer-m1410-") as temp:
        fixture = Path(temp) / "mapping.c"
        binary = Path(temp) / "mapping.exe"
        fixture.write_bytes(source.encode())
        subprocess.run([pinned_tools()["clang"], "-std=c17", "-O2", "-Wall",
                        "-Wextra", "-Werror", "-Wno-unused-function", "-Iinclude",
                        "-I.", str(fixture), "-o", str(binary)], cwd=ROOT, check=True)
        result = json.loads(subprocess.check_output([str(binary)], cwd=ROOT))
    assert result["passed"]
    result["app_scope_lookup"] = "same-name new backing, foreign open refusal, independent cleanup"
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
