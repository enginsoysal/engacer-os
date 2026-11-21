"""Blocked pipe readers/writers halt and cancel through ordinary native UI."""
import hashlib,json,os,struct,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 import replay7
 loader=replay7.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  from window144_native import ui,c,f,t,clone,library,StoppedDisk,output
  from apps_native4 import task
  from pipe147_build import build
  files=build();out=ROOT/'build/m14-native/stage7/pipe-cancel';out.mkdir(parents=True,exist_ok=True);c.OUT=out;meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage7/apps/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id'];source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m147-window-apps'/base['owned_fixture']/'owned.img';report=dict(passed=False,build_id=meta['build_id'],scope=__doc__,cases=[])
  try:
   for name in ['block-read','block-write']:
    work,disk,cloned=clone(ui,source,'m147-pipe-'+name);mounted=StoppedDisk(disk,library())
    try:mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',files[name].read_bytes())
    finally:mounted.close()
    boot=ui.guest(work/'blocked',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
    with boot as g:
     p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19);task(g,p,12005);before=f.stats(g)[0];p.desktop(12100,True,settle=False);deadline=time.monotonic()+30
     while 'M147_PIPE_BLOCK_READY'not in output(g):
      if time.monotonic()>deadline:raise TimeoutError(output(g))
      time.sleep(.05)
     observations=[]
     for _ in range(20):
      p.drain();halted=g.qmp('human-monitor-command',{'command-line':'info registers -a'}).count('HLT=1');waits=int.from_bytes(ui.memory(g,ui.symbol('pipe_waits147',8,True)[0],8),'little');observations.append(dict(halted=halted,waits=waits,resident_pages=ui.integer(g,'pipe_resident147',True)))
      if len(observations)>=3 and all(x['halted']==2 and x['waits']>0 and x['resident_pages']>0 for x in observations[-3:]):break
      time.sleep(.1)
     assert len(observations)>=3 and all(x['halted']==2 and x['waits']>0 and x['resident_pages']>0 for x in observations[-3:]),observations
     p.desktop(12008,True);p.drain();assert not ui.integer(g,'w8_active',True);assert ui.integer(g,'pipe_resident147',True)==0 and f.stats(g)[0]==before
     raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496);assert struct.unpack_from('<I',raw)[0]==3 and b'cancel' in raw[304:496].lower();assert len(t.records(g))==1 and t.records(g)[0]['token']==front['token'];c.shot(g,name);(out/(name+'.log')).write_bytes(g.log().encode());report['cases'].append(dict(name=name,clone=cloned,fixture_sha256=hashlib.sha256(files[name].read_bytes()).hexdigest(),idle_observations=observations,retained_pages=0))
   report['passed']=True
  except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
  finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
 finally:
  sys.meta_path.remove(loader);out=ROOT/'build/m14-native/stage7/pipe-cancel';out.mkdir(parents=True,exist_ok=True);(out/'dependencies.json').write_bytes((json.dumps(replay7.observed,indent=2)+'\n').encode())
if __name__=='__main__':main()
