"""Native common dialogs, actual file bytes and independent stopped-disk verification."""
import argparse,hashlib,json,os,struct,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
from window144_native import ui,c,f,t,clone,library,StoppedDisk,task,output
from picker146_build import build
from original_window_trace4 import wait_for

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--cycles',type=int,default=1);args=parser.parse_args();assert 1<=args.cycles<=21
 out=ROOT/'build/m14-native/stage6/picker-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out;fixture=build();meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage6/apps/results.json').read_text(encoding='utf-8'));assert base['passed']and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m146-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m146-picker-native');mounted=StoppedDisk(disk,library());source_path='/Users/Owner/Documents/m146-open-'+chr(233)+'.txt';target_path='/Users/Owner/Documents/m146-save-'+chr(233)+'.txt';payload='original dialog source '+chr(233)+'\n';final='final dialog save '+chr(233)+'\n'
 try:
  mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes());mounted.put(source_path,payload.encode());mounted.put('/Users/Owner/Documents/m146-hidden.bin',b'filter exclusion')
 finally:mounted.close()
 report=dict(passed=False,build_id=meta['build_id'],scope='Owned native common-dialog ABI, Unicode selected files, native cancel/replacement consent, caller writes and independent bytes; not original-app dialog qualification',clone=cloned,fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest(),cycles=[])
 try:
  boot=ui.guest(work/'picker',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19);task(g,p,12005);before=f.stats(g)[0]
   def picker():return struct.unpack('<3I',ui.memory(g,ui.symbol('picker12',installed=True)[0],12))
   def ready(marker,purpose):
    def observed():
     text=output(g)
     if 'M146_PICKER_FAIL'in text:raise AssertionError(text)
     return marker in text and c.flag(g,'file_dialog_state11')==10 and picker()[0]==purpose
    wait_for(g,observed,30);p.drain()
   def choose():
    index=f.entries(g)[source_path]['index'];hidden=f.entries(g)['/Users/Owner/Documents/m146-hidden.bin']['index'];assert not any(row[5]==55000+hidden for row in f.controls(g))
    for _ in range(128):
     if any(row[5]==55000+index for row in f.controls(g)):break
     p.desktop(54023,True)
    else:raise AssertionError('Qualified dialog source not selectable')
    p.desktop(55000+index,True);c.key(g,'ret')
   for cycle in range(args.cycles):
    at=len(g.log());p.desktop(12100,True,settle=False);g.wait('M8_CPL3_CREATED',at)
    ready('M146_PICKER_CANCEL_READY',7)
    if not cycle:c.shot(g,'native-open-dialog')
    p.desktop(54010,True);ready('M146_PICKER_OPEN_READY',7);choose();ready('M146_PICKER_SHORT_READY',7);choose();ready('M146_PICKER_SAVE_READY',8)
    if not cycle:c.shot(g,'native-save-unicode-name')
    c.key(g,'ctrl','a');c.key(g,'ctrl','c');c.key(g,'end');c.key(g,'backspace');assert b'm146-save-'+bytes([0])in ui.memory(g,*ui.symbol('picker12',installed=True));c.key(g,'ctrl','a');c.key(g,'ctrl','v');p.desktop(54011,True);ready('M146_PICKER_REPLACE_CANCEL_READY',8);p.desktop(54011,True);assert picker()[1]==1
    if not cycle:c.shot(g,'native-replace-consent')
    p.desktop(54026,True);assert picker()[1]==0;p.desktop(54010,True);ready('M146_PICKER_REPLACE_READY',8);p.desktop(54011,True);assert picker()[1]==1;p.desktop(54025,True);g.wait('M8_JOB_DONE',at);p.drain();assert 'M146_COMMON_DIALOG_BYTES_CANCEL_REPLACE_PASS'in output(g),output(g)
    assert len(t.records(g))==1 and t.records(g)[0]['token']==front['token'];assert not c.flag(g,'file_dialog_state11') and ui.integer(g,'ui_resident144',True)==0;assert ui.memory(g,ui.symbol('picker_request',installed=True)[0],8)==bytes(8)
    retained=f.stats(g)[0]-before;assert retained==0,retained;report['cycles'].append(dict(cycle=cycle+1,retained_pages=retained,cancel_preserves_buffer=True,nt4_and_current_structures=True,short_buffer_required_units=True,filters_exclude_binary=True,unicode_open_read_save_replace=True,dialog_does_not_create_destination=True))
   value=task(g,p,12005);assert 'Mapped original image: 7z.exe'in value and '7-Zip'in value;report['subsequent_original_console_success']=True
  assert ui.s.s.document(disk,source_path,8192)==payload.encode();assert ui.s.s.document(disk,target_path,8192)==final.encode();report.update(passed=True,source_unchanged=True,saved_bytes_independently_verified=True)
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
