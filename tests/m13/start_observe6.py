"""Normal-input Start observation: dismiss notices and await actual rendered rows."""
import json,sys,time
from pathlib import Path
import start_native6 as native
import observe6
observe6.bind(native.ui)
original=native.f.create
observations=[]
profile=sys.argv[sys.argv.index('--profile')+1] if '--profile' in sys.argv else 'ordinary'
out=native.ROOT/('build/m13/stage6/start-'+profile)
def create(g,p,name,folder=False):
 original(g,p,name,folder)
 # The original helper already asserts the independently observed directory entry.
 # Do not write guest state, trigger Refresh or infer that an API return is a frame.
 start=time.monotonic();rows=[]
 for attempt in range(101):
  rows=native.f.names(g)
  if name in rows:break
  p.drain();time.sleep(.05)
 matched=name in rows;observations.append(dict(name=name,attempts=attempt+1,matched=matched,host_observation_seconds=time.monotonic()-start,scope='Read-only wait for rendered list cache after independently observed filesystem mutation, not native latency/FPS'))
 if not matched:native.c.shot(g,'listing-failure')
 assert matched,dict(name=name,listing=rows,app=native.f.app(g))
native.f.create=create
original_close=native.close
def close(g,p):
 slot=native.f.model(g)[0]
 raw=native.ui.memory(g,native.ui.symbol('model',installed=True)[0]+slot*28,28)
 token=int.from_bytes(raw[16:20],'little')<<32|slot+1
 for attempt in range(101):
  if any(r[5]==49002 and r[4]==token for r in native.f.controls(g)):break
  p.drain();time.sleep(.05)
 ready=any(r[5]==49002 and r[4]==token for r in native.f.controls(g));observations.append(dict(type='caption-ready',attempts=attempt+1,matched=ready));assert ready,(slot,token)
 if any(r[5]==60002 for r in native.f.controls(g)):p.desktop(60002,True)
 original_close(g,p)

native.close=close
try:native.main()
finally:(out/'listing-observations.json').write_text(json.dumps(dict(passed=all(r['matched'] for r in observations),observations=observations),indent=2)+'\n',encoding='utf-8')
