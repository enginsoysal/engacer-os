"""Exercise the production registry capability lookup with two app owners."""
from pathlib import Path
import tempfile
import subprocess

root = Path(__file__).resolve().parents[2]
source = (root / "kernel/windows8/registry143.inc").read_text(encoding="utf-8")
lookup = source[source.index("static unsigned registry_object_owned143("):
                source.index("static unsigned registry_close143(")]
# Exercise the exact production invalidation predicate as well as lookup.
start = source.index("for(unsigned i=0;i<REGISTRY_KEYS143;++i){registry_object143*object=registry_objects143[i];if(registry_object_owned143(object)")
end = source.index("\n", start)
invalidate = source[start:end]
fixture = """
#include <stdint.h>
#include <string.h>
#define ENGINE_M14
#define W8_REGISTRY_TAG143 UINT64_C(0x80000000)
#define W8_HANDLE_TAG_MASK UINT64_C(0xe0000000)
#define REGISTRY_KEYS143 64
typedef struct { char user[256],canonical[768]; } record;
typedef struct { record record; char app_owner[65]; unsigned deleted; } registry_object143;
typedef struct { unsigned live,generation,object,access; } registry_cap143;
typedef struct { char owner[65]; registry_cap143 registry_handles[32]; } space;
static space a={.owner="A"}, b={.owner="B"};
static space *spaces142[]={&a,&b};
static unsigned active_space142;
#define W8_NAMED_OWNER (spaces142[active_space142]->owner)
static int equal8(const char*a,const char*b){return !strcmp(a,b);}
static registry_object143 first={.record={"user","key"},.app_owner="A"},second={.record={"user","key"},.app_owner="B"};
static registry_object143 *registry_objects143[64]={&first,&second};
static const char *registry_owner147(void){return "user";}
""" + lookup + """
static void invalidate_key(const char *canonical){
""" + invalidate + """
}
""" + """
int main(void){
 uint64_t h=W8_REGISTRY_TAG143|(7u<<5);
 a.registry_handles[0]=(registry_cap143){1,7,0,1};
 if(registry_slot143(h)!=0)return 1;
 active_space142=1;
 b.registry_handles[0]=a.registry_handles[0];
 if(registry_slot143(h)!=-1)return 2;
 b.registry_handles[0].object=1;
 if(registry_slot143(h)!=0)return 3;
 invalidate_key("key");
 if(first.deleted||!second.deleted)return 4;
 ++b.registry_handles[0].generation;
 return registry_slot143(h)!=-1;
}
"""
with tempfile.TemporaryDirectory() as temp:
    path = Path(temp) / "registry.c"
    exe = path.with_suffix(".exe")
    path.write_text(fixture, encoding="utf-8")
    subprocess.run(["clang", "-Wall", "-Wextra", "-Werror", str(path), "-o", str(exe)], check=True)
    subprocess.run([str(exe)], check=True)
print("Registry capability lookup passed for own, foreign and stale handles")
