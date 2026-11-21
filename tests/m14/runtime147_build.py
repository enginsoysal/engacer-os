"""Compile an isolated development worker for an unchanged qualified kernel ABI.

Only private stopped test clones may consume this worker. Full media builds,
source verification and native release qualification remain mandatory.
"""
import argparse,hashlib,json,re,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools
from m8 import runtime,privacy_input
from m14_integrity import verify_committed_inputs,verify_working_inputs

def build(name):
 assert re.fullmatch('[a-z][a-z0-9-]{0,31}',name)
 base=json.loads((ROOT/'dist/m14stage7-build-manifest.json').read_text(encoding='utf-8'))
 for path,digest in base['source_sha256'].items():
  if path.startswith(('include/','kernel/')):assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,('Kernel or ABI changed; build full media instead',path)
 out=ROOT/'build/m14-native/stage7'/('runtime-'+name);assert not(out/'compile-inputs.json').exists(),'A frozen development worker is immutable';out.mkdir(parents=True,exist_ok=True)
 files=set((ROOT/'user/windows8').glob('*.c'))|set((ROOT/'user/windows8').glob('*.inc'))|set((ROOT/'user/windows8').glob('*.h'))|set((ROOT/'include').rglob('*.h'))|set((ROOT/'third_party/libmspack').glob('*.h'))|set((ROOT/'third_party/libmspack-port').glob('*.h'))
 files.update(ROOT/p for p in ['runtime/sha256.c','third_party/libmspack/lzxd.c','tools/build/m8.py','tools/build/msi147.py','tools/build/m1.py','tools/build/m5_layout.py','tools/build/m14_integrity.py','tests/m14/runtime147_build.py'])
 hashes={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(files)};commit=verify_committed_inputs(ROOT,hashes);tools=pinned_tools()
 flags=['-std=c17','-O2','-g','-fdebug-compilation-dir=.','-ffile-prefix-map='+str(ROOT)+'=.','-fdebug-prefix-map='+str(ROOT)+'=.','-ffile-prefix-map='+str(out)+'=/development-worker','-fdebug-prefix-map='+str(out)+'=/development-worker','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-red-zone','-mgeneral-regs-only','-Wall','-Wextra','-Werror','-I',ROOT/'include','-I',out]
 for milestone in ['M2','M6','M71','M72','M73','M74','M75','M8','M9','M92','M10','M11','M12','M14','M13','SETUP_MEDIA75','M7','M3','M4','M45','M51']:flags.append('-DENGINE_'+milestone)
 runtime(out,tools,flags);verify_working_inputs(ROOT,hashes);binary=out/'WINDOWS8.ELF';data=binary.read_bytes();assert len(data)<=1024*1024 and data[:7]==b'\x7fELF\x02\x01\x01'
 for private in [str(ROOT).encode(),str(ROOT).replace('\\','/').encode()]:assert private not in privacy_input(data),'Private build path in worker'
 report=dict(scope=__doc__,source_commit=commit,kernel_build_id=base['build_id'],source_sha256=hashes,compiler_flags=[str(x).replace(str(ROOT),'<project-root>')for x in flags],artifacts={p.name:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())for p in [binary,out/'msi147/msi.dll',out/'msi147/msiexec.exe']});(out/'compile-inputs.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(dict(worker=binary.name,kernel_build_id=base['build_id'],sha256=report['artifacts'][binary.name]['sha256'])));return binary
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--name',required=True);args=parser.parse_args();build(args.name)
