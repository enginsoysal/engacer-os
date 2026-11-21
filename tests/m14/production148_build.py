"""Build an unchanged production worker against exact current development kernel inputs."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def build():
 canonical=ROOT/'tests/m14/runtime147_build.py';raw=canonical.read_bytes();source=raw.decode();old="out=ROOT/'build/m14-native/stage7'/('runtime-'+name)";assert source.count(old)==1;source=source.replace(old,"out=ROOT/'build/m14-native/stage8'/('runtime-'+name)").replace('dist/m14stage7-build-manifest.json','dist/m14stage8-build-manifest.json');namespace=dict(__file__=str(canonical),__name__='production148_worker_builder');exec(compile(source,str(canonical),'exec'),namespace)
 commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();name='production148-'+commit[:8];out=ROOT/'build/m14-native/stage8'/('runtime-'+name)
 if not(out/'compile-inputs.json').exists():namespace['build'](name)
 binary=out/'WINDOWS8.ELF';receipt=json.loads((out/'compile-inputs.json').read_text());assert hashlib.sha256(binary.read_bytes()).hexdigest()==receipt['artifacts'][binary.name]['sha256'];return binary
if __name__=='__main__':print(build())
