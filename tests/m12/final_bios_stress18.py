"""Twelve fresh BIOS/AHCI lifecycles in three deliberately concurrent batches."""
import concurrent.futures,subprocess,sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'build/m12/stage18/bios-stress';OUT.mkdir(parents=True,exist_ok=True)
def run(case):
 out=OUT/f'case-{case}';out.mkdir(parents=True,exist_ok=True)
 with (out/'harness.log').open('wb') as log:code=subprocess.run([sys.executable,str(ROOT/'tests/m12/final_bios_case18.py'),'--stage','18','--case',str(case)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT).returncode
 print('BIOS stress case',case,'exit',code,flush=True);return code
meta=json.loads((ROOT/'dist/m12stage18-build-manifest.json').read_text(encoding='utf-8'));sha=meta['artifacts']['EngacerOS-M12STAGE18.iso']['sha256'];codes=[]
for batch in range(3):
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:codes.extend(pool.map(run,range(batch*4,batch*4+4)))
rows=[json.loads((OUT/f'case-{n}/results.json').read_text(encoding='utf-8')) for n in range(12)]
assert len({r['owned_fixture'] for r in rows})==12
passed=not any(codes) and all(r['passed'] and r['build_id']==meta['build_id'] and r['iso_sha256']==sha for r in rows)
assert hashlib.sha256((ROOT/'dist/EngacerOS-M12STAGE18.iso').read_bytes()).hexdigest()==sha
r=dict(passed=passed,build_id=meta['build_id'],iso_sha256=sha,concurrent_guests=4,batches=3,cases=rows,checks=['Twelve separate fresh BIOS/AHCI installations, retained-ISO resets and 24 independent no-ISO starts in three deliberately concurrent batches'] if passed else [],scope='Named owned virtual stress only. An unreproduced earlier failure trigger is not identified or claimed universally fixed.')
(OUT/'results.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');assert passed
