"""Native streaming/hash probe on an isolated clone of accepted M14.6 media."""
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]

def main():
    import replay6
    loader=replay6.ReplayLoader();sys.meta_path.insert(0,loader)
    try:
        source=ROOT/'tests/m14/global146_run.py';raw=source.read_bytes();text=raw.decode()
        before="try:mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())"
        after="try:\n  mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())\n  inputs=json.loads((ROOT/'build/m14-native/stage7/cab-inputs/inputs.json').read_text(encoding='utf-8-sig'))\n  for index,row in enumerate(inputs['inputs']):mounted.put('/Users/Owner/Documents/m147-cab-'+str(index)+'.bin',(ROOT/'build/m14-native/stage7/cab-inputs'/row['cabinet']).read_bytes())"
        replacements=[('from global146_build import build','from cab147_build import build'),('stage6/global-native','stage7/cab-native'),('m146-global-native','m147-cab-native'),('M146_GLOBAL_MEMORY_OWNERSHIP_QUOTA_THREADS_PASS','M147_ORIGINAL_CAB_STREAM_ALL_323_SHA256_PASS'),('concurrent_alloc_free_rounds=200','original_files_hashed=323'),('Owned global-memory ABI, handle/LocalAlloc separation, allocation quota and native thread concurrency; not original application qualification','Owned production streaming LZX and SHA-256 of all 323 original files on accepted M14.6 media; not reusable MSI installation, custom-action or new OS qualification'),(before,after)]
        for before,after in replacements:assert text.count(before)==1,(before,text.count(before));text=text.replace(before,after)
        out=ROOT/'build/m14-native/stage7/cab-native';out.mkdir(parents=True,exist_ok=True);(out/'observer.json').write_bytes((json.dumps(dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),replacements=replacements),indent=2)+'\n').encode());namespace={'__file__':str(source),'__name__':'cab147_derived'};exec(compile(text,str(source),'exec'),namespace);namespace['main']()
    finally:
        sys.meta_path.remove(loader);out=ROOT/'build/m14-native/stage7/cab-native';out.mkdir(parents=True,exist_ok=True);(out/'dependencies.json').write_bytes((json.dumps(replay6.observed,indent=2)+'\n').encode())

if __name__=='__main__':main()
