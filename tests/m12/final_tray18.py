"""M12.18 native provider ownership, replacement and persistent settings journeys."""
import hashlib,json,os,struct,sys,traceback
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE18'
import tray_observe as q
c=q.c;f=q.f;s=q.s;t=q.t;ui=q.ui;ROOT=q.ROOT

def usb_control(g,eject=False):
    return next(r for r in f.controls(g) if (58220 if eject else 58200)<=r[5]<(58236 if eject else 58216))

def usb_panel(g,p):
    if c.flag(g,'tray_open12')!=2:
        if not c.flag(g,'tray_open12'):q.open_quick(g)
        p.desktop(58002,True)

def disk_audio(disk):return ui.s.s.document(disk,'/System/Settings/audio74.bin')

def main():
    out=ROOT/'build/m12/stage18/tray-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m12-stage18-tray');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
    sys.path.insert(0,str(ROOT/'tools/build'));from media import fat32
    payloads=[b'Original removable source A.\n',b'Replacement removable source B, independently verified.\n']
    sources=[]
    for label,payload in zip(('a','b'),payloads):
        path=work/('usb-'+label+'.img');path.write_bytes(fat32([(2,b'TRAY    TXT',payload)]));sources.append(path)
    source_hashes=[f.sha_file(path) for path in sources]
    report=dict(passed=False,stage='M12.18',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],owned_fixture=work.name,checks=[])
    try:
        with ui.guest(work/'install',disk,extra=['-drive',f'if=none,id=tray-source,format=raw,file={sources[0]}']) as g:
            p=q.install(g);before,saved=q.basic(g,p,out,report['checks']);assert struct.unpack('<2I',disk_audio(disk))==(0x41443734,saved)
            report['boot_resources']=dict(before=list(before),after=list(f.stats(g)),retained_pages=0)
            editor=t.launch(g,p,'text editor',2);c.type_text(g,'Keep this exact unsaved text');p.desktop(54001,True);assert c.flag(g,'file_dialog_state11')==10
            before_audio=disk_audio(disk);disk_hash=f.sha_file(disk);q.open_quick(g);p.desktop(58010,True)
            assert q.audio(g)[4]==max(0,saved-10) and 'session' in q.notice(g).lower();assert c.flag(g,'file_dialog_state11')==10 and t.app_view(g).dirty
            assert bytes(t.app_view(g).text)==b'Keep this exact unsaved text' and disk_audio(disk)==before_audio and f.sha_file(disk)==disk_hash
            c.shot(g,'picker-volume-session-only');c.key(g,'esc');assert c.flag(g,'file_dialog_state11')==10;p.desktop(54010,True);s.close(g,p);p.desktop(60,True)
            q.open_quick(g);p.desktop(58011,True);assert q.audio(g)[4]==saved and 'saved' in q.notice(g);c.key(g,'esc')
            report['checks'].append('Changing PCM level while Save As owns a dirty Editor applies only to the live provider: the exact whole disk and saved level remain unchanged, and Escape preserves the picker and unsaved text')
            f.attach(g,p,'tray-source','tray-a');usb_panel(g,p);control=usb_control(g);index=control[5]-58200;record=dict(q.disks(g))[index]
            assert record[0]==4 and record[4] and control[4]==(1<<63)|(record[7]<<16)|(index+1)
            c.shot(g,'usb-provider-actions');p.desktop(control[5],True);assert f.app(g)['mode']==2 and f.app(g)['context']==record[7] and f.has(g,90) and 'TRAY.TXT' in f.usb_rows(g)
            usb_panel(g,p);at=len(g.log());p.desktop(usb_control(g,True)[5],True);g.wait('M10_USB_SAFE_TO_REMOVE',at,90);assert 'removed' in q.notice(g).lower() or 'unplug' in q.notice(g).lower();c.shot(g,'safe-remove-complete');c.key(g,'esc');p.desktop(90,True);s.close(g,p)
            g.qmp('device_del',{'id':'tray-a'});p.drain();g.qmp('blockdev-add',{'node-name':'tray-source-again','driver':'raw','file':{'driver':'file','filename':str(sources[0])}});f.attach(g,p,'tray-source-again','tray-a2');usb_panel(g,p);old=usb_control(g,True)
            x,y,w,h,owner,action=old;f.move(g,p,x+w//2,y+h//2);p.down(True);p.drain()
            g.qmp('device_del',{'id':'tray-a2'});p.drain();g.qmp('blockdev-add',{'node-name':'tray-replacement','driver':'raw','file':{'driver':'file','filename':str(sources[1])}});f.attach(g,p,'tray-replacement','tray-b');new=usb_control(g,True)
            assert new[5]==action and new[4]!=owner,(old,new);at=len(g.log());p.down(False);p.drain();assert 'M10_USB_SAFE_TO_REMOVE' not in g.log()[at:];assert dict(q.disks(g))[index][4]
            c.shot(g,'replacement-stale-press-cancelled');p.desktop(usb_control(g)[5],True);assert f.app(g)['context']==dict(q.disks(g))[index][7]
            p.desktop(f.row(g,'TRAY.TXT'),True);p.desktop(21004,True);assert ui.s.s.document(disk,'/Users/Owner/Downloads/TRAY.TXT')==payloads[1]
            usb_panel(g,p);at=len(g.log());p.desktop(usb_control(g,True)[5],True);g.wait('M10_USB_SAFE_TO_REMOVE',at,90);c.key(g,'esc');s.close(g,p);g.qmp('device_del',{'id':'tray-b'});p.drain()
            assert [f.sha_file(path) for path in sources]==source_hashes
            report['checks'].append('USB tray actions bind to the real storage generation; safe removal completes its provider flush, a held click cannot eject a same-slot replacement, and explicit replacement import matches independent source bytes without changing either USB image')
            for name,kind in [('clock',8),('calendar',9),('media',16)]:t.pin(g,p,name,kind)
            t.pin(g,p,'calc',4);t.pin(g,p,'image',14);saved_prefs=bytes(s.prefs(g));assert ui.s.s.document(disk,'/System/Settings/start11-Owner.bin')==saved_prefs
            warm=f.stats(g)
            for _ in range(3):
                q.open_quick(g);p.desktop(58002,True);p.desktop(58003,True);c.idle(g);c.key(g,'esc')
            f.same_pages(warm,f.stats(g));c.idle(g);report['resources']=dict(before=list(warm),after=list(f.stats(g)),retained_pages=0);report['hardware_resources']=dict(before=list(before),after=list(warm));report['preferences_sha256']=hashlib.sha256(saved_prefs).hexdigest();report['saved_volume']=saved;(out/'native.log').write_bytes(g.log().encode())
        for label,ps2 in [('usb',False),('ps2',True)]:
            boot=ui.guest(work/('ordinary-'+label),disk,media='installed',ready='M7_DESKTOP_READY',ps2_only=ps2);ui.s.normal_boot(boot,work/'install/vars.fd')
            with boot as g:
                p=ui.Pointer(g);p.drain();assert bytes(s.prefs(g))==saved_prefs and q.audio(g)[4]==saved and not c.flag(g,'tray_open12');baseline=f.stats(g)
                c.key(g,'meta_l','a');assert c.flag(g,'tray_open12')==1;c.key(g,'meta_r','a');assert not c.flag(g,'tray_open12');f.same_pages(baseline,f.stats(g));c.idle(g);c.shot(g,'ordinary-'+label);(out/('ordinary-'+label+'.log')).write_bytes(g.log().encode())
        report['checks'].append('Two ordinary no-ISO startups preserve exact Start preferences and provider volume; both Windows-key+A routes work with USB HID and legacy PS/2, with no flyout retained after closing and no idle polling')
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
