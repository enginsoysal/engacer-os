"""Repeat the exact real original deferred action/child-output pilot 21 times."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 source=ROOT/'tests/m14/wix_action147_run.py';raw=source.read_bytes();text=raw.decode();changes=[('stage7/wix-action-pilot','stage7/wix-action-native'),('m147-wix-action-pilot','m147-wix-action-native'),("('range(21)','range(1)')","('range(21)','range(21)')")]
 for a,b in changes:assert text.count(a)==(2 if a=='stage7/wix-action-pilot'else 1),(a,text.count(a));text=text.replace(a,b)
 out=ROOT/'build/m14-native/stage7/wix-action-native';out.mkdir(parents=True,exist_ok=True);(out/'lifetime-observer.json').write_bytes((json.dumps(dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),changes=changes),indent=2)+'\n').encode());namespace={'__file__':str(source),'__name__':'wix_action147_lifetimes'};exec(compile(text,str(source),'exec'),namespace);namespace['main']()
if __name__=='__main__':main()
