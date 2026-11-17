"""M12.13 real appearance transactions, independent input and owner journeys."""
import hashlib,json,os,struct,traceback
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE13'
import settings_observe as h
c=h.c;f=h.f;s=h.s;t=h.t;ui=h.ui;ROOT=h.ROOT

def main():
    out=ROOT/'build/m12/stage13/settings-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m12-stage13-settings');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);report=dict(passed=False,stage='M12.13',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],owned_fixture=work.name,checks=[])
    try:
        with ui.guest(work/'install',disk) as g:
            p=h.q.install(g);baseline=f.stats(g);initial=h.colors(g);original=h.appearance(g);before=f.sha_file(disk);c.open_settings(g,p);first=next(w for w in t.records(g) if w['app']==3);c.shot(g,'appearance')
            p.desktop(43,True);p.desktop(45001,True);assert h.colors(g)[1]==1 and h.preview(g)[0]==first['token'];c.shot(g,'live-preview');p.desktop(59005,True);assert h.colors(g)==initial and h.appearance(g)[5:7]==original[5:7] and not h.preview(g)[0] and f.sha_file(disk)==before
            p.desktop(40,True);h.close(g,p);assert s.windows(g)==0 and h.colors(g)==initial and f.sha_file(disk)==before
            report['checks'].append('Actual install/retained-ISO startup exposes four native categories; Cancel and closing restore previous visual state with an independently identical complete disk and no preference writes')
            c.open_settings(g,p);p.desktop(43,True);first=next(w for w in t.records(g) if w['app']==3);other=t.launch(g,p,'settings',3);assert h.preview(g)[0]==first['token'] and not f.has(g,44) and not f.has(g,47)
            _,(x,y,w,hh)=f.model(g);p.logical(x+24+74,y+56+96+108+18,True);assert h.colors(g)[1]==1 and h.preview(g)[0]==first['token'];c.shot(g,'competing-preview-refused');h.close(g,p);assert h.preview(g)[0]==first['token'];t.focus(g,p,first);c.key(g,'esc');assert h.colors(g)==initial and not h.preview(g)[0];h.close(g,p)
            report['checks'].append('A second real Settings generation cannot overwrite the first visual preview; its disabled controls explain ownership, closing it preserves the first, and Escape cancels only the actual owner')
            editor=t.launch(g,p,'text editor',2);c.type_text(g,'Keep unsaved settings guard');p.desktop(54001,True);assert c.flag(g,'file_dialog_state11')==10;settings=t.launch(g,p,'settings',3);disk_before=f.sha_file(disk);p.desktop(43,True);p.desktop(47,True);assert h.preview(g)[0]==settings['token'] and 'file operation' in f.app(g)['notice'];p.desktop(59001,True);p.desktop(112,True);assert 'file dialog' in f.app(g)['notice'] and c.flag(g,'scale73')==2 and c.flag(g,'file_dialog_state11')==10 and f.sha_file(disk)==disk_before;c.shot(g,'active-dialog-save-scale-refused');h.close(g,p);t.focus(g,p,editor);assert c.flag(g,'file_dialog_state11')==10 and bytes(t.app_view(g).text)==b'Keep unsaved settings guard';p.desktop(54010,True);s.close(g,p);p.desktop(60,True);assert s.windows(g)==0
            report['checks'].append('A real dirty Editor Save As retains its owner and exact text while Settings refuses persistence and scale changes; the complete disk remains unchanged and closing a color preview leaves the file dialog intact')
            c.open_settings(g,p);settings=next(w for w in t.records(g) if w['app']==3);p.desktop(43,True);software=t.launch(g,p,'software',11);h.software_change(g,p,4);h.close(g,p);t.focus(g,p,settings);p.desktop(59005,True);assert h.colors(g)==initial;s.search(g,p,'calc');assert (1,4) not in s.results(g);c.key(g,'esc');c.key(g,'esc');t.focus(g,p,settings);p.desktop(59006,True);h.save(g,p);assert h.colors(g)==(0x087c71,0);assert h.appearance(g)[5:7]==(0x142c35,0);h.close(g,p);s.search(g,p,'calc');assert (1,4) not in s.results(g);c.key(g,'esc');c.key(g,'esc');t.launch(g,p,'software',11);h.software_change(g,p,4);h.close(g,p);t.launch(g,p,'calc',4);h.close(g,p)
            report['checks'].append('Cancelling and applying distribution defaults do not restore a separately removed Calculator: actual package removal remains independent, while reinstall launches without breaking Settings or the desktop')
            c.open_settings(g,p);p.desktop(43,True);p.desktop(40,True);p.desktop(45001,True);h.save(g,p);saved=h.record(disk);assert saved==ui.memory(g,ui.symbol('appearance11',352,True)[0],352) and struct.unpack_from('<8I',saved)[2:7]==(0x62e5bd,1,0,0x182039,0)
            p.desktop(59002,True)
            for action,speed in [(59020,200),(59021,500),(59022,900)]:p.desktop(action,True);assert h.click_interval(g)==speed and ui.s.s.document(disk,'/System/Settings/input11.bin')==struct.pack('<2I',0x31314955,speed)
            p.desktop(20006,True);assert ui.s.s.document(disk,'/System/Settings/keyboard10.bin')==struct.pack('<2I',0x30314c4b,1);p.desktop(20005,True);assert ui.s.s.document(disk,'/System/Settings/keyboard10.bin')==struct.pack('<2I',0x30314c4b,0);assert h.record(disk)==saved;c.shot(g,'explicit-input-preferences');p.desktop(59003,True);p.desktop(20000,True);assert h.q.hardware_view(g)==1;c.shot(g,'real-system-devices');p.desktop(20001,True);assert h.page(g)==3 and not h.q.hardware_view(g);h.close(g,p)
            report['checks'].append('Apply saves exact validated appearance bytes; explicit 200/500/900-ms intervals and QWERTY/Dvorak write their actual independent records, and real Devices Back returns to the remembered System category')
            # The shared repair harness independently checks these persisted pins.
            for name,kind in [('clock',8),('calendar',9),('media',16),('calc',4),('image',14)]:t.pin(g,p,name,kind)
            preferences=bytes(s.prefs(g));assert ui.s.s.document(disk,'/System/Settings/start11-Owner.bin')==preferences;f.same_pages(baseline,f.stats(g));c.idle(g);report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0);report['preferences_sha256']=hashlib.sha256(preferences).hexdigest();report['appearance_sha256']=hashlib.sha256(saved).hexdigest();report['record_hex']=saved.hex();(out/'native.log').write_bytes(g.log().encode())
        for label,ps2 in [('usb',False),('ps2',True)]:
            boot=ui.guest(work/('ordinary-'+label),disk,media='installed',ready='M7_DESKTOP_READY',ps2_only=ps2);ui.s.normal_boot(boot,work/'install/vars.fd')
            with boot as g:
                p=ui.Pointer(g);p.drain();assert ui.memory(g,ui.symbol('appearance11',352,True)[0],352)==saved and h.colors(g)==(0x62e5bd,1) and h.click_interval(g)==900 and not h.preview(g)[0];assert bytes(s.prefs(g))==preferences;c.open_settings(g,p);assert h.page(g)==0 and not c.flag(g,'settings_invalid13');c.shot(g,'ordinary-'+label);h.close(g,p);c.idle(g);(out/('ordinary-'+label+'.log')).write_bytes(g.log().encode())
        report['checks'].append('Two ordinary no-ISO USB/PS2 startups reload exact appearance, click interval and Start records; Settings opens in Appearance without a stale preview or validation warning and idles without polling')
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
