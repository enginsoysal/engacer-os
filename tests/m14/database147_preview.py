"""New production MSI DLL on a frozen kernel: real active database capabilities."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 source=ROOT/'tests/m14/preview147_run.py';raw=source.read_bytes();text=raw.decode();old="    try:mounted.put('/Users/Owner/Downloads/7z2606-x64.msi',data)";new="    try:\n     mounted.put('/Users/Owner/Downloads/7z2606-x64.msi',data)\n     mounted.put('/System/Windows/Installer/msi.dll',dll)\n     mounted.put('/System/Windows/Installer/msiexec.exe',exe)"
 replacement="  binaries=ROOT/'build/m14-native/stage7/api-native-fixture/msi147';receipt=json.loads((binaries/'build-inputs.json').read_text());dll=(binaries/'msi.dll').read_bytes();exe=(binaries/'msiexec.exe').read_bytes();assert hashlib.sha256(dll).hexdigest()==receipt['artifacts']['msi.dll']['sha256'];assert hashlib.sha256(exe).hexdigest()==receipt['artifacts']['msiexec.exe']['sha256']\n  meta=json.loads(ui.manifest_path12()"
 substitutions=[('stage7/preview-native','stage7/database-preview-native'),('m147-preview-','m147-database-preview-'),('  meta=json.loads(ui.manifest_path12()',replacement),(old,new),("      raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496)","      assert ('Authored registry entries: 16 shortcuts: 2'if index==0 else'Authored registry entries: 10 shortcuts: 1')in output\n      raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496)"),("report=dict(passed=False,build_id=meta['build_id'],scope=__doc__,packages=[])","report=dict(passed=False,build_id=meta['build_id'],scope=__doc__,packages=[],production_service_override=receipt,override_sha256=hashlib.sha256(dll).hexdigest())")]
 for before,after in substitutions:assert text.count(before)==(2 if before=='stage7/preview-native'else 1),(before,text.count(before));text=text.replace(before,after)
 out=ROOT/'build/m14-native/stage7/database-preview-native';out.mkdir(parents=True,exist_ok=True);(out/'observer.json').write_bytes((json.dumps(dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),substitutions=substitutions),indent=2)+'\n').encode());namespace={'__file__':str(source),'__name__':'database147_preview'};exec(compile(text,str(source),'exec'),namespace);namespace['main']()
if __name__=='__main__':main()
