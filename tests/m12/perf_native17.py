"""M12.17 keyboard-only installation, focus, contrast and persisted independence."""
import argparse,hashlib,json,os,struct,traceback
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE17'
import access_observe16 as a
c=a.c;f=a.f;s=a.s;t=a.t;h=a.h;ui=a.ui;ROOT=a.ROOT

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--development',action='store_true');args=parser.parse_args()
 out=ROOT/'build/m12/stage17/access-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out
 meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m12-stage17-access');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);report=dict(passed=False,development_only=args.development,stage='M12.17',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],owned_fixture=work.name,checks=[])
 try:
  with ui.guest(work/'install',disk) as g:
   mouse=[];original=g.qmp
   def observed(command,args=None):
    if command=='input-send-event' and any(e.get('type') in ('abs','rel','btn') for e in (args or {}).get('events',[])):mouse.append(command)
    if command=='human-monitor-command' and any(x in (args or {}).get('command-line','') for x in ('mouse_move','mouse_button')):mouse.append(command)
    return original(command,args) if args is not None else original(command)
   g.qmp=observed;p=a.keyboard_install(g,out);assert c.flag(g,'guide_open11');c.shot(g,'visible-first-guide');a.key(g,'f1');assert c.flag(g,'access_help16');item=a.semantic(g,'access_help_item16');assert item['action']==46000 and 'desktop' in item['label'];c.shot(g,'guide-help');a.key(g,'esc');assert c.flag(g,'guide_open11') and a.focus(g)==(1,0,46000);a.key(g,'esc');assert not c.flag(g,'guide_open11');a.close(g);assert not t.records(g);baseline=f.stats(g)
   settings=a.launch(g,'settings',3);a.tab_to(g,59004);assert a.semantic(g)['label']=='Accessibility';a.key(g,'f1');assert a.semantic(g,'access_help_item16')['label']=='Accessibility';a.key(g,'esc');assert a.focus(g)==(1,settings['token'],59004);a.key(g,'ret');assert h.page(g)==4;c.shot(g,'keyboard-accessibility')
   original_appearance=h.record(disk);a.activate(g,60010,space=True);assert c.flag(g,'access_flags16')==1 and h.record(disk)==original_appearance;a.tab_to(g,60010);a.key(g,'f1');item=a.semantic(g,'access_help_item16');assert item['role']==4 and '[x] High contrast' in item['label'];c.shot(g,'high-contrast-checkbox-help');a.key(g,'esc');assert a.focus(g)==(1,settings['token'],60010)
   a.activate(g,60011,space=True);assert c.flag(g,'access_flags16')==3 and h.record(disk)==original_appearance;record=struct.pack('<4I',0x36314155,1,3,0);assert ui.s.s.document(disk,'/System/Settings/accessibility16-Owner.bin')==record;c.shot(g,'saved-high-contrast-and-reduced-motion');a.activate(g,60010,space=True);assert c.flag(g,'access_flags16')==2 and h.colors(g)==(0x087c71,0);a.activate(g,60010,space=True);a.close(g);assert not t.records(g)
   a.key(g,'f6');assert c.flag(g,'access_region16')==1 and a.focus(g)==(1,0,0);a.key(g,'f1');assert a.semantic(g,'access_help_item16')['label']=='Start';c.shot(g,'named-taskbar-help');a.key(g,'esc');assert a.focus(g)==(1,0,0);a.key(g,'ret');assert c.flag(g,'launcher');c.type_text(g,'files');a.key(g,'ret');assert len(t.records(g))==1 and t.records(g)[0]['app']==1
   a.tab_to(g,94);a.key(g,'ret');assert f.app(g)['path']=='/Users/Owner/Documents';a.tab_to(g,90);a.key(g,'f1');assert a.semantic(g,'access_help_item16')['label']=='Back';a.key(g,'esc');a.key(g,'ret');assert f.app(g)['path']=='/Users/Owner';a.close(g);assert not t.records(g)
   a.key(g,'f6');a.key(g,'f6');assert c.flag(g,'access_region16')==2;a.key(g,'f1');assert a.semantic(g,'access_help_item16')['label']=='My files' and a.semantic(g,'access_help_item16')['role']==3;c.shot(g,'named-desktop-help');a.key(g,'esc');a.key(g,'ret');assert len(t.records(g))==1;a.close(g);assert not mouse,mouse
   report['checks'].append('The real eight-step installation, first-start help/dismissal, Start search, Settings checkbox Space activation, taskbar and desktop F6/Enter, Files Documents/Back and exact semantic names run with no mouse events sent by the harness')
   report['checks'].append('High contrast and reduced effects save an exact independent 16-byte record, preserve the entire appearance record, restore the original Light theme when contrast is disabled and expose checked state through native Focus Help')
   # Shared later repair independently verifies these exact durable Start bytes.
   for title,kind in [('clock',8),('calendar',9),('media',16),('calc',4),('image',14)]:t.pin(g,p,title,kind)
   preferences=bytes(s.prefs(g));assert ui.s.s.document(disk,'/System/Settings/start11-Owner.bin')==preferences;f.same_pages(baseline,f.stats(g));c.idle(g);report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0);report['preferences_sha256']=hashlib.sha256(preferences).hexdigest();report['accessibility_record_hex']=record.hex();(out/'native.log').write_bytes(g.log().encode())
  for label,ps2 in [('usb',False),('ps2',True)]:
   boot=ui.guest(work/('ordinary-'+label),disk,media='installed',ready='M7_DESKTOP_READY',ps2_only=ps2);ui.s.normal_boot(boot,work/'install/vars.fd')
   with boot as g:
    p=ui.Pointer(g);p.drain();assert c.flag(g,'access_flags16')==3 and not c.flag(g,'access_invalid16');assert h.record(disk)==original_appearance and bytes(s.prefs(g))==preferences;assert ui.s.s.document(disk,'/System/Settings/accessibility16-Owner.bin')==record;a.key(g,'f6');a.key(g,'f1');assert c.flag(g,'access_help16') and a.semantic(g,'access_help_item16')['label']=='Start';c.shot(g,'ordinary-'+label);a.key(g,'esc');c.idle(g);(out/('ordinary-'+label+'.log')).write_bytes(g.log().encode())
  report['checks'].append('Two independent no-ISO USB and PS2 startups reload exact accessibility, appearance and Start records; F1/F6 work through both real input providers and the native desktop halts at idle');report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
