"""Native accessibility preserves modal, generation and full-window ownership."""
import json,os,traceback
from pathlib import Path
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE16'
import access_observe16 as a
from access_fixtures16 import clone
c=a.c;f=a.f;h=a.h;t=a.t;ui=a.ui;ROOT=a.ROOT

def text(g,name):
 address,size=ui.symbol(name,installed=True);return ui.memory(g,address,size).split(b'\0')[0].decode()

def main():
 out=ROOT/'build/m12/stage16/access-ownership';out.mkdir(parents=True,exist_ok=True);c.OUT=out;meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));native=json.loads((ROOT/'build/m12/stage16/access-native/results.json').read_text(encoding='utf-8'));assert native['passed'] and native['build_id']==meta['build_id'];source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage16-access'/native['owned_fixture']/'owned.img';original=f.sha_file(source);work,disk,cloned=clone(ui,source,'m12-stage16-access-ownership');report=dict(passed=False,build_id=meta['build_id'],clone=cloned,checks=[])
 try:
  with ui.guest(work/'tasks',disk,media='installed',ready='M7_DESKTOP_READY') as g:
   p=ui.Pointer(g);p.drain()
   while t.records(g):a.close(g)
   baseline=f.stats(g)
   editor=a.launch(g,'text editor',2)
   c.type_text(g,'Accessibility preserves this unsaved document')
   a.activate(g,54001)
   assert c.flag(g,'file_dialog_state11')==10
   a.key(g,'tab')
   before=ui.memory(g,ui.symbol('file_dialog_state11',installed=True)[0],ui.symbol('file_dialog_state11',installed=True)[1])
   saved_focus=a.focus(g)
   a.key(g,'f1')
   assert c.flag(g,'access_help16')
   item=a.semantic(g,'access_help_item16')
   assert item['owner']==editor['token'] and item['label']
   c.shot(g,'save-as-focus-help')
   a.key(g,'esc')
   assert not c.flag(g,'control_active') and ui.memory(g,ui.symbol('file_dialog_state11',installed=True)[0],len(before))==before and bytes(t.app_view(g).text)==b'Accessibility preserves this unsaved document'
   a.key(g,'f6')
   assert c.flag(g,'file_dialog_state11')==10 and not c.flag(g,'access_region16')
   a.key(g,'esc')
   assert not c.flag(g,'file_dialog_state11')
   a.close(g)
   p.desktop(60,True)
   assert not t.records(g)
   report['checks'].append('F1/Escape preserves the exact real Save As state, full-generation owner, focused control and unsaved Editor bytes; F6 cannot escape the modal review and explicit cancellation/discard remain available')
   settings=a.launch(g,'settings',3);a.tab_to(g,59004);old=a.semantic(g);a.close(g);fresh=a.launch(g,'calc',4);assert fresh['token']!=settings['token'];a.key(g,'tab');a.key(g,'f1');assert a.semantic(g,'access_help_item16')['owner']!=old['owner'];a.key(g,'esc');a.close(g)
   for _ in range(8):a.launch(g,'calc',4)
   windows=t.records(g);assert len(windows)==8;a.key(g,'ctrl','esc');c.type_text(g,'calc');a.key(g,'ret');assert len(t.records(g))==8 and text(g,'shell_notice');a.key(g,'esc');assert not c.flag(g,'launcher')
   for _ in range(4):
    a.key(g,'f6')
    if c.flag(g,'access_region16')==3:break
   assert c.flag(g,'access_region16')==3 and a.focus(g)==(1,0,60002);a.key(g,'f1');assert c.flag(g,'access_help16') and a.semantic(g,'access_help_item16')['label']=='Dismiss notification' and t.records(g)==windows;c.shot(g,'eight-windows-notification-help');a.key(g,'esc');assert a.focus(g)==(1,0,60002);a.key(g,'ret');assert not text(g,'shell_notice') and t.records(g)==windows
   while t.records(g):a.close(g)
   f.same_pages(baseline,f.stats(g));c.idle(g);report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0);(out/'native.log').write_bytes(g.log().encode());report['checks'].append('Closing/reopening a reused slot cannot expose the earlier generation semantic name; at the actual eight-window limit, F6/F1/Escape/Enter describes and dismisses the real notification without allocating a ninth app or changing any existing window')
  assert f.sha_file(source)==original;report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
