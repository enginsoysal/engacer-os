"""Ordinary native EXE source selection and read-only review; no EXE installation acceptance."""
import hashlib,json,os,struct,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 import replay8
 loader=replay8.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  from window144_native import ui,c,f,t,clone,library,StoppedDisk,task
  out=ROOT/'build/m14-native/stage8/exe-review-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out;meta=json.loads(ui.manifest_path12().read_text());base=json.loads((ROOT/'build/m14-native/stage8/compact/results.json').read_text());assert base['passed']and base['build_id']==meta['build_id']
  source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage8-compact'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m148-exe-review-native');mounted=StoppedDisk(disk,library());original=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/SumatraPDF-3.6.1-64-install.exe';data=original.read_bytes();assert hashlib.sha256(data).hexdigest()=='1eee71cccd2ea6e94d5bcea54ee2f759844da3e1a0ee2f6045035b1d17b94381'
  try:
   mounted.put('/Users/Owner/Downloads/'+original.name,data);mounted.put('/Users/Owner/Downloads/Unknown-review148.exe',b'MZUnknown review-only content');mounted.put('/Users/Owner/Downloads/Not-an-installer148.txt',b'not an installer');mounted.put('/Users/Owner/Documents/Review-sentinel148.txt',b'Personal data retained')
  finally:mounted.close()
  report=dict(passed=False,scope=__doc__,build_id=meta['build_id'],clone=cloned,ordinary_exe_installation_qualified=False,cases=[])
  try:
   boot=ui.guest(work/'review',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
   with boot as g:
    p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19);address,size=ui.symbol('apps',installed=True);address+=front['slot']*(size//8)
    def state():return struct.unpack('<9I',ui.memory(g,address,36))
    initial=state();p.desktop(12013,True);assert c.flag(g,'picker12')==9;p.desktop(54010,True);assert state()==initial
    for index,name in enumerate([original.name,'Unknown-review148.exe']):
     path='/Users/Owner/Downloads/'+name;p.desktop(12013,True);assert c.flag(g,'picker12')==9;p.desktop(54019,True);c.key(g,'ctrl','a');c.type_text(g,'/Users/Owner/Downloads');c.key(g,'ret');p.drain();entries=f.entries(g);row=entries[path]['index'];bad=entries['/Users/Owner/Downloads/Not-an-installer148.txt']['index'];assert not any(r[5]==55000+bad for r in f.controls(g))
     for _ in range(128):
      if any(r[5]==55000+row for r in f.controls(g)):break
      p.desktop(54023,True)
     else:raise AssertionError('EXE source is not reachable in the installer list')
     p.desktop(55000+row,True);p.desktop(54011,True);assert not c.flag(g,'file_dialog_state11');before=f.entries(g);output=task(g,p,12000);after=f.entries(g);assert before==after,'Read-only EXE review changed the volume entries'
     assert 'Mapped original image'not in output and not c.flag(g,'w8_active');review=state();assert review[4]==(4 if index==0 else 0) and review[1]==(1 if index==0 else 0),review
     raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496)
     if index==0:
      digest=ui.memory(g,address+68,32);assert digest==hashlib.sha256(data).digest();assert review[5:9]==(4,227,2,1),review;assert raw[40:136].split(b'\0')[0]==b'SumatraPDF'
     assert not any(k.startswith('/Applications/Windows/')for k in after);at=len(g.log())
     if index==0:
      p.desktop(12001,True);assert any(r[5]==12003 for r in f.controls(g));assert not c.flag(g,'w8_active');p.desktop(12004,True)
     p.drain();assert not c.flag(g,'w8_active')and 'M8_CPL3_CREATED'not in g.log()[at:]and not any(r[5]==12003 for r in f.controls(g))
     c.shot(g,'ordinary-exe-review-'+str(index));report['cases'].append(dict(file=name,review=review,source_digest=hashlib.sha256(data if index==0 else b'MZUnknown review-only content').hexdigest(),unchanged_volume=True,no_original_executed=True,installation_disabled=index!=0,confirmation_cancelled=index==0))
    assert ui.s.s.document(disk,'/Users/Owner/Documents/Review-sentinel148.txt',4096)==b'Personal data retained';report['passed']=True;(out/'serial.log').write_bytes(g.log().encode())
  except Exception:
   if 'g'in locals():(out/'serial.log').write_bytes(g.log().encode())
   report['error']=ui.q.clean(traceback.format_exc());raise
  finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
 finally:sys.meta_path.remove(loader)
if __name__=='__main__':main()
