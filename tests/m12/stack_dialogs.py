"""Compile-only frame evidence for the two observed nested-dialog overflows."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools

def main():
    out=ROOT/'build/m12/stage8/diagnostics';out.mkdir(parents=True,exist_ok=True)
    definitions=['-DENGINE_'+n for n in ('M2','M3','M4','M45','M5','M51','M6','M7','M71','M72','M73','M74','M75','M8','M9','M92','M10','M11','M12')]
    flags=['--target=x86_64-unknown-none-elf','-std=c17','-O2','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-red-zone','-mgeneral-regs-only','-Wall','-Wextra','-Werror','-fno-pic','-fno-pie','-fno-asynchronous-unwind-tables','-fstack-usage','-Iinclude','-Ibuild/m12','-Ithird_party/bearssl/inc','-Ithird_party/bearssl-port']
    frames={};wanted=('keyboard','keyboard11','picker_accept12','picker_editor_open12','app7_document12','request7','zip_load74','zip_extract_at74')
    for source,name in [('kernel/desktop/session.c','stack-final-session'),('kernel/desktop/app.c','stack-final-app')]:
        subprocess.run([pinned_tools()['clang'],*flags,*definitions,'-c',source,'-o',str(out/(name+'.o'))],cwd=ROOT,check=True)
        for line in (out/(name+'.su')).read_text().splitlines():
            fields=line.split('\t');function=fields[0].rsplit(':',1)[-1]
            if function in wanted:frames[function]=int(fields[1])
    assert frames['keyboard']<1024 and frames['picker_editor_open12']<256 and frames['app7_document12']<512
    sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ('kernel/desktop/session.c','kernel/desktop/picker12.inc','kernel/desktop/app.c','kernel/desktop/document12.inc','include/engine/process.h','tests/m12/stack_dialogs.py')}
    result=dict(passed=True,guarded_kernel_stack_bytes=16384,frames=frames,source_sha256=sources,scope='Individual optimized compile-only frames, not a complete worst-case call-stack proof. Actual native keyboard ZIP/Open/extraction and focus tasks remain mandatory.')
    (out/'stack-final-results.json').write_bytes((json.dumps(result,indent=2)+'\n').encode());print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
