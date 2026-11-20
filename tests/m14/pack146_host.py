"""Run the unchanged production decoder corpus in isolated current-stage paths."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 original=ROOT/'tests/m12/pack_host.py';source=original.read_text(encoding='utf-8');adapted=source
 changes={'build/m12/stage7/pack-host':'build/m14-native/stage6/pack-host','build/m12/installed/KERNEL.ELF':'build/m14-native/installed/KERNEL.ELF','build/m12/BOOTX64.EFI':'build/m14-native/BOOTX64.EFI'}
 for old,new in changes.items():
  assert old in adapted;adapted=adapted.replace(old,new)
 namespace={'__file__':str(original),'__name__':'encoder146_replay'};exec(compile(adapted,str(original),'exec'),namespace);namespace['main']()
 path=ROOT/'build/m14-native/stage6/pack-host/results.json';report=json.loads(path.read_text(encoding='utf-8'));assert report['passed'];report['observer_replay']={'original_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'executed_sha256':hashlib.sha256(adapted.encode()).hexdigest(),'adapter_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'path_replacements':changes};path.write_bytes((json.dumps(report,indent=2)+'\n').encode())
if __name__=='__main__':main()
