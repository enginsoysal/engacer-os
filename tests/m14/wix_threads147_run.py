"""Original DLL runs on native action threads, including real checked/Continue results."""
import hashlib,json,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 source=ROOT/'tests/m14/wix_tools147_run.py';raw=source.read_bytes();text=raw.decode();changes=[('from wix_tools147_build import build','from wix_threads147_build import build'),('stage7/wix-tools-pilot','stage7/wix-threads-pilot'),('m147-wix-tools-pilot','m147-wix-threads-pilot'),('M147_ORIGINAL_WIX_COPY_DELETE_FAILURE_PROPAGATION_PASS','M147_THREADED_ORIGINAL_WIX_COPY_DELETE_CONTINUE_PASS'),('original_deferred_action_calls=8','original_deferred_action_calls=9'),('Original unchanged WiX drives own native copy/delete utilities, byte-exact Unicode-path copy, quoted ampersands, missing-file and self-copy/directory/operator refusals; test-only session owner, not the authored Notepad++ sequence or full installation','Production deferred dispatcher creates and joins real action threads for original unchanged WiX; byte-exact utilities, checked failures and authored Continue handling. Test-only session owner; authored Notepad++ sequence and full installation remain unqualified.')]
 for a,b in changes:assert text.count(a)==(2 if a=='stage7/wix-tools-pilot'else 1),(a,text.count(a));text=text.replace(a,b)
 cycles=int(os.environ.get('ENGACER147_ACTION_CYCLES','1'));assert cycles in (1,21)
 if cycles==21:
  marker="('range(21)','range(1)'),";start=text.index('extra=');section=text[start:];assert section.count(marker)==1;text=text[:start]+section.replace(marker,"('range(21)','range(21)'),",1)
  text=text.replace('stage7/wix-threads-pilot','stage7/wix-threads-native').replace('m147-wix-threads-pilot','m147-wix-threads-native')
 out=ROOT/'build/m14-native/stage7'/('wix-threads-native'if cycles==21 else'wix-threads-pilot');out.mkdir(parents=True,exist_ok=True);(out/'thread-observer.json').write_bytes((json.dumps(dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),changes=changes,cycles=cycles),indent=2)+'\n').encode());namespace={'__file__':str(source),'__name__':'wix_threads147_pilot'};exec(compile(text,str(source),'exec'),namespace);namespace['main']()
if __name__=='__main__':main()
