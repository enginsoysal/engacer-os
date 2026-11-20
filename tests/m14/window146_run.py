"""Retain every original window task with a stable same-window idle observation."""
import hashlib
import json
from pathlib import Path
from replay6 import REPLACEMENTS

ROOT=Path(__file__).resolve().parents[2]

def derive(source):
    for before,after in REPLACEMENTS:
        source=source.replace(before,after)
    before="    halted=g.qmp('human-monitor-command',{'command-line':'info registers -a'}).count('HLT=1');assert halted==2,halted;sample['halted_cpus_while_message_waiting']=halted"
    assert source.count(before)==1
    after="""    idle=[];deadline=time.monotonic()+2
    slot=f.model(g)[0];token=next(row['token']for row in t.records(g)if row['slot']==slot)
    while time.monotonic()<deadline:
     assert ui.integer(g,'w8_active',True)and f.model(g)[0]==slot
     assert any(row['token']==token and row['slot']==slot for row in t.records(g))
     halted=g.qmp('human-monitor-command',{'command-line':'info registers -a'}).count('HLT=1');idle.append(halted)
     if len(idle)>=3 and idle[-3:]==[2,2,2]:break
     time.sleep(.05)
    else:raise AssertionError(('No stable same-window idle interval',idle))
    sample['halted_cpus_while_message_waiting']=halted;sample['idle_observations']=idle"""
    return source.replace(before,after)

def main():
    canonical=ROOT/'tests/m14/window144_native.py'
    raw=canonical.read_bytes();source=derive(raw.decode())
    namespace={'__file__':str(canonical),'__name__':'window146_derived'}
    exec(compile(source,str(canonical),'exec'),namespace)
    namespace['main']()
    out=ROOT/'build/m14-native/stage6/window-native'
    report=dict(canonical_path='tests/m14/window144_native.py',canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(source.encode()).hexdigest(),adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),scope='Every retained original window/input/move/resize/close/retention assertion; idle requires three consecutive two-CPU halt samples within the same live window token and two-second bound')
    (out/'observer.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())

if __name__=='__main__':main()
