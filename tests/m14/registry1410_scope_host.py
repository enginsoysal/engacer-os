"""Exercise the production registry capability lookup with two app owners."""
from pathlib import Path
import tempfile
import subprocess

root = Path(__file__).resolve().parents[2]
source = (root / "kernel/windows8/registry143.inc").read_text(encoding="utf-8")
lookup = source[source.index("static unsigned registry_object_owned143("):
                source.index("static unsigned registry_close143(")]
delete = source.index("/* Invalidate all views")
start = source.index("for(unsigned", delete)
end = source.index(" return v6_remove(volume,directory)", start)
invalidate = source[start:end]
process = (root / "kernel/windows8/process.c").read_text(encoding="utf-8")
owner = process[process.index("static void init_app_owner1410("):
                process.index("\n#endif", process.index("static void init_app_owner1410("))]
authority = process[process.index("static uint64_t group_generation1410;"):
                    process.index("static int equal8", process.index("static uint64_t group_generation1410;"))]
backing = source[source.index("static void registry_root143("):
                 source.index("static unsigned registry_load_key143(")]
protected = (root / "kernel/windows8/protected143.inc").read_text(encoding="utf-8")
hash_path = protected[protected.index("static void protected_hash143("):
                      protected.index("static void protected_root143(")]
fixture = """
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "engine/sha256.h"
#include "engine/winproduct147.h"
#define ENGINE_M14
#define W8_REMOVE 4
#define W8_REGISTRY_TAG143 UINT64_C(0x80000000)
#define W8_HANDLE_TAG_MASK UINT64_C(0xe0000000)
#define REGISTRY_KEYS143 64
typedef struct { char user[256],canonical[768]; } record;
typedef struct { record record; char app_owner[65],directory[256]; unsigned deleted; } registry_object143;
typedef struct { unsigned live,generation,object,access; } registry_cap143;
typedef struct { char named_owner1410[256],app_id1410[39]; uint64_t app_generation1410; unsigned install_authority147; registry_cap143 registry_handles[32]; } private_space142;
static private_space142 a={.app_generation1410=1}, b={.app_generation1410=2};
static private_space142 *spaces142[]={&a,&b};
static unsigned length8(const char *s){return (unsigned)strlen(s);}
static unsigned active_space142;
#define W8_NAMED_OWNER (spaces142[active_space142]->named_owner1410)
static int equal8(const char*a,const char*b){return !strcmp(a,b);}
static registry_object143 first={.record={"user","key"},.app_owner="A",.directory="/shared"},second={.record={"user","key"},.app_owner="B",.directory="/shared"};
static registry_object143 *registry_objects143[64]={&first,&second};
static struct { const char *product_root; } input8;
static const char *registry_owner147(void){return "/Machine/64";}
static void copy8(char *out,const char *in,unsigned cap){snprintf(out,cap,"%s",in);}
static void path_append143(char *out,const char *in,unsigned cap){
 unsigned n=length8(out);copy8(out+n,in,cap-n);
}
#define registry_hash143 protected_hash143
""" + hash_path + backing + owner + authority + lookup + """
static void invalidate_key(const char *directory){
""" + invalidate + """
}
int main(void){
 const char root[]=WIN_PRODUCT_BASE147 "{A23B657D-838B-4C9B-8F9D-386E50C1A76B}";
 char path_a[256],path_b[256];
 input8.product_root=root;
 registry_directory143("software\\example",path_a);
 input8.product_root=WIN_PRODUCT_BASE147 "{B23B657D-838B-4C9B-8F9D-386E50C1A76B}";
 registry_directory143("software\\example",path_b);
 if(strncmp(path_a,root,strlen(root))||
    strncmp(path_b,input8.product_root,strlen(input8.product_root))||
    !strstr(path_a,"/.Engacer/Registry/")||!strstr(path_b,"/.Engacer/Registry/")||
    !strcmp(path_a,path_b))return 10;
 init_app_owner1410(&a,root,"/Users/Owner");
 init_app_owner1410(&b,root,"/Users/Owner");
 if(!strcmp(a.named_owner1410,b.named_owner1410))return 6;
 memcpy(first.app_owner,a.named_owner1410,sizeof(first.app_owner));
 memcpy(second.app_owner,b.named_owner1410,sizeof(second.app_owner));
 a.install_authority147=b.install_authority147=1;
 group_generation1410=a.app_generation1410;
 memcpy(group_owner1410,a.named_owner1410,sizeof(group_owner1410));
 if(!installer_authority147())return 7;
 group_generation1410=b.app_generation1410;
 memcpy(group_owner1410,b.named_owner1410,sizeof(group_owner1410));
 if(installer_authority147())return 8;
 active_space142=1;
 if(!installer_authority147()||installer_remove_authority1410())return 9;
 group_command1410=W8_REMOVE;
 if(!installer_remove_authority1410())return 11;
 active_space142=0;
 if(installer_remove_authority1410())return 12;
 uint64_t h=W8_REGISTRY_TAG143|(7u<<5);
 a.registry_handles[0]=(registry_cap143){1,7,0,1};
 if(registry_slot143(h)!=0)return 1;
 active_space142=1;
 b.registry_handles[0]=a.registry_handles[0];
 if(registry_slot143(h)!=-1)return 2;
 b.registry_handles[0].object=1;
 if(registry_slot143(h)!=0)return 3;
 ++b.registry_handles[0].generation;
 if(registry_slot143(h)!=-1)return 4;
 invalidate_key("/shared");
 if(!first.deleted||!second.deleted)return 5;
 first.deleted=second.deleted=0;
 memcpy(second.directory,"/private-b",sizeof("/private-b"));
 invalidate_key("/shared");
 return !first.deleted||second.deleted;

}
"""
with tempfile.TemporaryDirectory() as temp:
    path = Path(temp) / "registry.c"
    exe = path.with_suffix(".exe")
    path.write_text(fixture, encoding="utf-8")
    subprocess.run(["clang", "-Wall", "-Wextra", "-Werror", str(path), str(root / "runtime/sha256.c"), "-I", str(root / "include"), "-o", str(exe)], check=True)
    subprocess.run([str(exe)], check=True)
print("Registry capability lookup passed for own, foreign and stale handles")
