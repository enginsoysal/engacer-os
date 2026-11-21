"""The original utility action also copies the exact French XML from the pinned NPP MSI."""
import hashlib,json,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 source=ROOT/'tests/m14/wix_tools147_run.py';raw=source.read_bytes();text=raw.decode();old='payload=bytes((i*37+19)&255 for i in range(1024*1024+17));';new="payload=(Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/notepadpp-msi/filtWRK_yvXKeZnh2irUzylG9VQuQk').read_bytes();assert len(payload)==122556 and hashlib.sha256(payload).hexdigest()=='7bd00f2d43f7700524d2a11ba643909229d87255b8aa43b27a0a7bc6ca7e52ef';"
 changes=[('stage7/wix-tools-pilot','stage7/wix-tools-french'),('m147-wix-tools-pilot','m147-wix-tools-french'),(old,new)]
 for a,b in changes:assert text.count(a)==(2 if a=='stage7/wix-tools-pilot'else 1),(a,text.count(a));text=text.replace(a,b)
 out=ROOT/'build/m14-native/stage7/wix-tools-french';out.mkdir(parents=True,exist_ok=True);(out/'data-observer.json').write_bytes((json.dumps(dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),changes=changes,original_payload_sha256='7bd00f2d43f7700524d2a11ba643909229d87255b8aa43b27a0a7bc6ca7e52ef'),indent=2)+'\n').encode());namespace={'__file__':str(source),'__name__':'wix_tools147_french'};exec(compile(text,str(source),'exec'),namespace);namespace['main']()
if __name__=='__main__':main()
