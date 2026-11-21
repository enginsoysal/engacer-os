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
text=text.replace(needle,"REPLACEMENTS.extend([('stage7','stage8'),('STAGE7','STAGE8'),('M14.7','M14.8'),('0.14.7','0.14.8'),('m147-','m148-'),('evidence/M14/7','evidence/M14/8')])\n"+needle)
text=text.replace("'assert stage==7'","'assert stage==8'")
sys.modules['replay7']=sys.modules[__name__]
exec(compile(text,str(canonical),'exec'),globals())
