"""Native accessibility preserves modal, generation and full-window ownership."""
import json,os,traceback,struct
from PIL import Image
from pathlib import Path
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE18'
import access_observe16 as a
from access_fixtures16 import clone
c=a.c;f=a.f;h=a.h;t=a.t;ui=a.ui;ROOT=a.ROOT

def text(g,name):
 address,size=ui.symbol(name,installed=True);return ui.memory(g,address,size).split(b'\0')[0].decode()

def main():
 out=ROOT/'build/m12/stage18/access-ownership';out.mkdir(parents=True,exist_ok=True);c.OUT=out;meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));native=json.loads((ROOT/'build/m12/stage18/access-native/results.json').read_text(encoding='utf-8'));assert native['passed'] and native['build_id']==meta['build_id'];source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage18-access'/native['owned_fixture']/'owned.img';original=f.sha_file(source);work,disk,cloned=clone(ui,source,'m12-stage18-access-ownership');report=dict(passed=False,build_id=meta['build_id'],clone=cloned,checks=[])
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
   logical=struct.unpack('<II',ui.memory(g,ui.symbol('model',installed=True)[0]+240,8));pw=860 if logical[0]>900 else logical[0]-40;ph=620 if logical[1]>712 else logical[1]-92;left=(logical[0]-pw)//2;top=(logical[1]-60-ph)//2
   with Image.open(out/'save-as-focus-help.png') as picture:
    pixels=picture.convert('RGB');assert pixels.getpixel((left,top+40))==(255,255,255) and pixels.getpixel((left+3,top+40))==(0,0,0),'High-contrast picker boundary is not visibly separated'
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
   windows=t.records(g)
   assert len(windows)==8,('Actual window count',windows)
   a.key(g,'ctrl','esc');c.type_text(g,'calc');a.key(g,'ret')
   assert len(t.records(g))==8 and text(g,'shell_notice'),('Limit preserves windows and reports reason',t.records(g),text(g,'shell_notice'))
   for _ in range(4):
    if not c.flag(g,'launcher'):break
    a.key(g,'esc')
   assert not c.flag(g,'launcher'),'Escape returns through Search and Start before focusing the notification'
   for _ in range(4):
    a.key(g,'f6')
    if c.flag(g,'access_region16')==3:break
   assert c.flag(g,'access_region16')==3 and a.focus(g)==(1,0,60002)
   a.key(g,'f1')
   assert c.flag(g,'access_help16') and a.semantic(g,'access_help_item16')['label']=='Dismiss' and t.records(g)==windows
   c.shot(g,'eight-windows-notification-help')
   with Image.open(out/'eight-windows-notification-help.png') as picture:
    pixels=picture.convert('RGB');left=logical[0]-480-16;assert pixels.getpixel((left,56))==(255,255,255) and pixels.getpixel((left+3,56))==(0,0,0),'High-contrast notification boundary is not visibly separated'
   report['checks'].append('Actual high-contrast reduced-effects picker and notification borders have white outer boundary pixels and black inner surfaces, independently read from their real physical framebuffer captures')
   a.key(g,'esc')
   assert a.focus(g)==(1,0,60002)
   a.key(g,'ret')
   assert not text(g,'shell_notice') and t.records(g)==windows
   while t.records(g):a.close(g)
   f.same_pages(baseline,f.stats(g));c.idle(g);report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0);(out/'native.log').write_bytes(g.log().encode());report['checks'].append('Closing/reopening a reused slot cannot expose the earlier generation semantic name; at the actual eight-window limit, F6/F1/Escape/Enter describes and dismisses the real notification without allocating a ninth app or changing any existing window')
  assert f.sha_file(source)==original;report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
