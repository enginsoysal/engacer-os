"""Check the app boundary used for secondary module mapping."""
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

source = (Path(__file__).resolve().parents[2] / "user/windows8/loader141.inc").read_text()
rule = source[source.index("static unsigned dependency_path_owned141("):
              source.index("static unsigned system_candidate141(")]
fixture = r"""
#include <assert.h>
#include <string.h>
#define APP_A "/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}"
#define APP_B "/Applications/Windows/{83170F69-40C1-2702-2606-000001000001}"
static struct { const char* product_root; } context = { APP_A }, *job8 = &context;
static struct { const char* path; } modules141[] = {{ APP_A "/app.exe" }};
static unsigned len8(const char *s){return (unsigned)strlen(s);}
static unsigned equal8(const char *a,const char *b){return !strcmp(a,b);}
""" + rule + r"""
int main(void){
 assert(dependency_path_owned141(APP_A "/System/System32/shared.dll"));
 assert(!dependency_path_owned141(APP_B "/System/System32/shared.dll"));
 assert(!dependency_path_owned141(APP_A "suffix/shared.dll"));
 assert(!dependency_path_owned141("/Users/Owner/Downloads/shared.dll"));
 assert(!dependency_path_owned141("/System/Windows/Installer/msi.dll"));
 modules141[0].path="/System/Windows/Installer/msiexec.exe";
 assert(dependency_path_owned141("/System/Windows/Installer/msi.dll"));
 assert(!dependency_path_owned141("/System/Windows/Installer/private.dll"));
 return 0;
}
"""
with TemporaryDirectory() as directory:
    source = Path(directory) / "owner.c"
    executable = source.with_suffix(".exe")
    source.write_text(fixture, encoding="utf-8")
    subprocess.run(["clang", "-Wall", "-Wextra", "-Werror", str(source), "-o", str(executable)], check=True)
    subprocess.run([str(executable)], check=True)
print("Secondary DLL mapping remains inside the owner bundle")
