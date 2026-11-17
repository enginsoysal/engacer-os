"""Compare exact M12.16/current production raster bodies, not a second raster model."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools
out=ROOT/'build/m12/stage17/raster-host';out.mkdir(parents=True,exist_ok=True)
reference='87fedd75c46fe4bcc3263a29f39be1491b6e7069';assert subprocess.check_output(['git','rev-parse','m1216-v0.12.16^{commit}'],cwd=ROOT).decode().strip()==reference
previous=subprocess.check_output(['git','show',reference+':kernel/core/graphics73.inc'],cwd=ROOT).decode('utf-8');current=(ROOT/'kernel/core/graphics73.inc').read_text(encoding='utf-8');functions={}
for name,source in [('baseline',previous),('current',current)]:
 start=source.index('static void round_alpha73(');end=source.index('\nvoid ui73_round',start);body=source[start:end];functions[name]=hashlib.sha256(body.encode()).hexdigest();assert body.count('for(unsigned xx=l;xx<right;++xx){')==1;body=body.replace('static void round_alpha73(',f'static void {name}17(').replace('for(unsigned xx=l;xx<right;++xx){','for(unsigned xx=l;xx<right;++xx){++visits[which];');(out/f'raster-{name}.h').write_text(body+'\n',encoding='utf-8')
exe=out/'raster.exe';subprocess.run([pinned_tools()['clang'],'-std=c17','-O2','-Wall','-Wextra','-Werror','-I',str(out),'tests/m12/raster_host17.c','-o',str(exe)],cwd=ROOT,check=True,capture_output=True);run=subprocess.run([str(exe)],cwd=ROOT,check=True,capture_output=True);report=json.loads(run.stdout);report.update(scope='Host execution of the exact production round bodies, with only identifier/loop-visit instrumentation; bounded framebuffer probes compare pixels, blending, dirty bounds and audio pump cadence. Host CPU measurements are not native FPS.',baseline_source_commit=reference,function_sha256=functions,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['kernel/core/graphics73.inc','tests/m12/raster_host17.c','tests/m12/raster_host17.py']});(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report),flush=True)
