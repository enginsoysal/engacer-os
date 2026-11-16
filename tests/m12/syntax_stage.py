"""Compile-only M11/M12 guards without mutating media or maps under test."""
import argparse,json,subprocess,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'tools/build')]
from m1 import pinned_tools

def main():
    p=argparse.ArgumentParser();p.add_argument('--stage',type=int,required=True);stage=p.parse_args().stage;assert 1<=stage<=18
    compiler=pinned_tools()['clang'];flags=['--target=x86_64-unknown-none-elf','-std=c17','-O2','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-red-zone','-mgeneral-regs-only','-Wall','-Wextra','-Werror','-fsyntax-only','-Iinclude','-Ibuild/m12','-Ithird_party/bearssl/inc','-Ithird_party/bearssl-port']
    names=('M2','M3','M4','M45','M5','M51','M6','M7','M71','M72','M73','M74','M75','M8','M9','M92','M10','M11')
    definitions=['-DENGINE_'+name for name in names];reports=[]
    for mode in ('M11','M12'):
        for source in ('kernel/desktop/session.c','kernel/storage/fat32.c','kernel/install/installer6.c','kernel/desktop/app.c'):
            r=subprocess.run([compiler,*flags,*definitions,*(['-DENGINE_M12'] if mode=='M12' else []),source],cwd=ROOT,capture_output=True)
            assert r.returncode==0,(mode,source,r.stderr.decode(errors='replace'))
            reports.append(dict(mode=mode,source=source,passed=True))
    out=ROOT/f'build/m12/stage{stage}';out.mkdir(parents=True,exist_ok=True)
    sources={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for folder in ('kernel','include') for p in (ROOT/folder).rglob('*') if p.is_file()}
    (out/'syntax-results.json').write_bytes((json.dumps(dict(passed=True,checks=reports,source_sha256=sources,compiler_sha256=hashlib.sha256(Path(compiler).read_bytes()).hexdigest(),scope='Compile-only compatibility of conditional source paths; does not requalify historical media.'),indent=2)+'\n').encode())
    print('PASS: native M12 and preserved M11 conditional desktop/FAT32/installer sources compile with warnings as errors.')
if __name__=='__main__':main()
