"""Preserve canonical stage-seven adaptations on distinct stage-eight media."""
import hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
canonical=ROOT/'tests/m14/replay7.py'
raw=canonical.read_bytes()
text=raw.decode().replace('stage7','stage8').replace('STAGE7','STAGE8').replace('M14.7','M14.8').replace('0.14.7','0.14.8').replace('m147-','m148-').replace('evidence/M14/7','evidence/M14/8')
# Current canonical fixtures may themselves carry literal stage-seven identities.
needle='observed = {}'
assert text.count(needle)==1
mappings148=[('stage7', 'stage8'), ('STAGE7', 'STAGE8'), ('M14.7', 'M14.8'), ('0.14.7', '0.14.8'), ('m147-', 'm148-'), ('evidence/M14/7', 'evidence/M14/8'), ("'--stage','7'", "'--stage','8'"), ("'--stage', '7'", "'--stage', '8'")]
text=text.replace(needle,'REPLACEMENTS.extend('+repr(mappings148)+')\n'+needle)
text=text.replace("'assert stage==7'","'assert stage==8'")
# Native stage-seven entry wrappers execute another adapter from raw source.
# Map that nested adapter explicitly and retain both actual source hashes.
needle148="        observed[source.relative_to(ROOT).as_posix()] = {"
assert text.count(needle148)==1
hook148=r"""        if module.__name__ == 'native147_entry':
            old148="    exec(compile(raw.decode('utf-8'),str(source),'exec'),scope)"
            assert text.count(old148)==1
            new148="    adapter148=raw.decode('utf-8')\n    for before148,after148 in replay7.REPLACEMENTS:adapter148=adapter148.replace(before148,after148)\n    replay7.observed[source.relative_to(source.parents[2]).as_posix()]['executed_sha256']=hashlib.sha256(adapter148.encode()).hexdigest()\n    exec(compile(adapter148,str(source),'exec'),scope)"
            text=text.replace(old148,new148)
"""
text=text.replace(needle148,hook148+needle148)
sys.modules['replay7']=sys.modules[__name__]
exec(compile(text,str(canonical),'exec'),globals())
