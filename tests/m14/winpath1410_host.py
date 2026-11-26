"""Check the Windows names returned for app-private system module paths."""
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

source = (Path(__file__).resolve().parents[2] / "user/windows8/api.c").read_text()
winpath = source[source.index("static void winpath8("):source.index("static int nativepath_mode143(")]
case = r"""
#include <assert.h>
#include <stdio.h>
#include <string.h>
#define ENGINE_M14
#define ROOT "/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}"
static struct { const char *product_root,*windows_root,*user_root; } job = {
 ROOT,"C:\\Program Files\\7-Zip","/Users/Owner"
}, *job8=&job;
static unsigned len8(const char *s){return (unsigned)strlen(s);}
static unsigned equal8(const char *a,const char *b){return !strcmp(a,b);}
static void copy8(char *out,const char *in,unsigned cap){snprintf(out,cap,"%s",in);}
static void append8(char *out,const char *in,unsigned cap){
 unsigned n=len8(out);copy8(out+n,in,cap-n);
}
""" + winpath + r"""
int main(void){
 char out[256];
 winpath8(ROOT "/System/System32/same.dll",out,sizeof(out));
 assert(!strcmp(out,"C:\\Windows\\System32\\same.dll"));
 winpath8(ROOT "/System/SysWOW64/same.dll",out,sizeof(out));
 assert(!strcmp(out,"C:\\Windows\\SysWOW64\\same.dll"));
 winpath8(ROOT "/System/System32-Backup/same.dll",out,sizeof(out));
 assert(!strcmp(out,"C:\\Program Files\\7-Zip\\System\\System32-Backup\\same.dll"));
 winpath8("/Users/Owner/Documents/file.txt",out,sizeof(out));
 assert(!strcmp(out,"C:\\Users\\Owner\\Documents\\file.txt"));
 return 0;
}
"""
with TemporaryDirectory() as tmp:
    src = Path(tmp) / "path.c"
    exe = src.with_suffix(".exe")
    src.write_text(case, encoding="utf-8")
    subprocess.run(["clang", "-Wall", "-Wextra", "-Werror", str(src), "-o", str(exe)], check=True)
    subprocess.run([str(exe)], check=True)
