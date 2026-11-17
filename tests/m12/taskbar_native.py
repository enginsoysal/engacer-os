"""M12.10 real grouped taskbar, window ownership and persistent pin journeys."""
import argparse,ctypes,hashlib,json,os,struct,traceback
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE10'
import start_observe as s
c=s.c;f=s.f;ui=s.ui;ROOT=s.ROOT
def records(g):
    raw=ui.memory(g,ui.symbol('model',installed=True)[0],224);out=[]
    for slot in range(8):
        x,y,w,h,generation,app,live,minimum=struct.unpack_from('<4iII2B',raw,slot*28)
        if live:out.append(dict(slot=slot,token=generation<<32|slot+1,app=app,minimized=bool(minimum)))
    return out
def group_controls(g):
    return [r for r in f.controls(g) if r[4]==0 and 43100<r[5]<43120]
def group_order(g):
    rows=group_controls(g);assert len({r[5] for r in rows})==len(rows)
    return [r[5]-43100 for r in sorted(rows,key=lambda r:r[0])]
def menu_rows(g):
    n=c.flag(g,'file_menu_count11');assert n<=12;raw=ui.memory(g,ui.symbol('file_menu_items11',installed=True)[0],n*16);out=[]
    for i in range(n):
        pointer,command,enabled=struct.unpack_from('<QII',raw,i*16)
        label=ui.memory(g,pointer,96).split(b'\0')[0].decode()
        out.append(dict(label=label,command=command,enabled=enabled))
    return out
def right_group(g,p,app):
    x,y,w,h,*_=c.control(g,43100+app);f.right(g,p,x+w//2,y+h//2)
def focus(g,p,window):
    slot=window['slot'];current=next(w for w in records(g) if w['slot']==slot)
    assert current['token']==window['token']
    if f.model(g)[0]==slot and not current['minimized'] and not c.flag(g,'launcher') and not c.flag(g,'desktop_focus11'):return
    app=window['app'];action=43100+app
    if not any(r[5]==action for r in group_controls(g)):
        p.desktop(43001,True)
        for _ in range(3):
            if any(r['command']==43220+app for r in menu_rows(g)):break
            f.menu(g,p,43200)
        f.menu(g,p,43220+app)
    else:p.desktop(action,True)
    if sum(w['app']==app for w in records(g))>1:f.menu(g,p,43020+slot)
    assert f.model(g)[0]==slot and not next(w for w in records(g) if w['slot']==slot)['minimized']
def launch(g,p,name,kind):
    before=s.windows(g,kind);s.search(g,p,name);assert s.results(g)==[(1,kind)],s.results(g);c.key(g,'ret');assert s.windows(g,kind)==before+1
    return next(w for w in records(g) if w['slot']==f.model(g)[0])
def app_view(g):
    address,size=ui.symbol('apps',installed=True);slot=f.model(g)[0]
    from focus_ownership import View
    return View.from_buffer_copy(ui.memory(g,address+slot*(size//8),ctypes.sizeof(View)))
def closing(g):
    address,size=ui.symbol('apps',installed=True);slot=f.model(g)[0]
    from focus_ownership import View
    return int.from_bytes(ui.memory(g,address+slot*(size//8)+ctypes.sizeof(View)+352,4),'little')
def pin(g,p,name,app):
    if app in s.prefs(g).task[:s.prefs(g).tasks]:return
    s.search(g,p,name);c.key(g,'shift','f10');f.menu(g,p,42700+app);c.key(g,'esc');c.key(g,'esc')
    assert app in s.prefs(g).task[:s.prefs(g).tasks]
def close_all(g,p):
    while records(g):
        target=records(g)[-1];focus(g,p,target);s.close(g,p)
        if any(w['token']==target['token'] for w in records(g)):
            assert closing(g);p.desktop(60,True)
    p.drain()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--smoke',action='store_true');args=parser.parse_args()
    out=ROOT/('build/m12/stage10/taskbar-smoke' if args.smoke else 'build/m12/stage10/taskbar-native');out.mkdir(parents=True,exist_ok=True);c.OUT=out
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m12-stage10-taskbar-smoke' if args.smoke else 'm12-stage10-taskbar');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
    report=dict(passed=False,stage='M12.10',development_only=args.smoke,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],owned_fixture=work.name,checks=[])
    try:
        with ui.guest(work/'install',disk) as g:
            p=ui.Pointer(g)
            for action in (2,2,100,2,2,2):c.wizard(g,p,action)
            at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain();s.close(g,p);baseline=f.stats(g)
            assert group_order(g)==[1,2,7] and s.windows(g)==0 and not any(r[5]==70 for r in f.controls(g));c.shot(g,'pins-no-duplicate-window-buttons')
            for _ in range(64):
                c.key(g,'tab')
                if c.flag(g,'control_active') and c.flag(g,'focused_action')==43101:break
            else:raise AssertionError('Grouped Files button cannot receive keyboard focus')
            c.shot(g,'keyboard-group-focus');c.key(g,'ret');first=records(g)[0];assert first['app']==1 and not first['minimized'];p.desktop(43101,True);assert records(g)[0]['minimized'];c.shot(g,'single-minimized');p.desktop(43101,True);assert not records(g)[0]['minimized']
            report['checks'].append('Actual install/retained-ISO startup; unopened pins share one group with their app, and single-window group clicks minimize and restore the real window')
            second=launch(g,p,'files',1);f.visit(g,p,'Documents');assert s.windows(g,1)==2 and group_order(g).count(1)==1
            p.desktop(43101,True);rows=menu_rows(g);assert sum(43020<=r['command']<43028 for r in rows)==2 and any('Documents' in r['label'] for r in rows);assert all(r['label'][0].isdigit() for r in rows[:-1]);c.shot(g,'two-files-chooser');f.menu(g,p,43020+first['slot']);assert f.model(g)[0]==first['slot']
            p.desktop(43101,True);expected=menu_rows(g)[c.flag(g,'context_choice11')]['command']-43020;c.key(g,'ret');assert f.model(g)[0]==expected
            focus(g,p,second);s.close(g,p);assert s.windows(g,1)==1;right_group(g,p,1);f.menu(g,p,31002);assert records(g)[0]['minimized'];right_group(g,p,1);assert any(r['label']=='Restore window' for r in menu_rows(g));f.menu(g,p,43020+first['slot']);assert not records(g)[0]['minimized'];right_group(g,p,1);f.menu(g,p,31001);assert s.windows(g)==0
            report['checks'].append('Multiple Files windows share one numbered chooser; mouse and Enter select actual generation tokens, and right-click minimize/restore/close controls the one intended remaining window')
            p.desktop(43102,True);editor=records(g)[0];c.type_text(g,'Keep my work');assert app_view(g).dirty;right_group(g,p,2);f.menu(g,p,31001);assert closing(g)==1 and s.windows(g,2)==1;c.shot(g,'dirty-group-close');p.desktop(61,True);assert not closing(g) and bytes(app_view(g).text)==b'Keep my work'
            p.desktop(54001,True);assert c.flag(g,'file_dialog_state11')==10;p.desktop(43102,True);assert c.flag(g,'file_dialog_state11')==10 and not records(g)[0]['minimized'];right_group(g,p,2);assert all(not r['enabled'] for r in menu_rows(g) if r['command'] in (31001,31002));c.key(g,'esc');p.desktop(54010,True);s.close(g,p);p.desktop(60,True);assert s.windows(g)==0
            report['checks'].append('Group close retains dirty Editor work until explicit review; Keep editing preserves exact text, and an active file picker blocks owner minimize/close without consuming another window')
            if not args.smoke:
                p.desktop(0,True);p.desktop(42007,True);p.desktop(42030,True);p.desktop(43302,True);p.desktop(42034,True);p.desktop(42008,True);c.key(g,'esc');assert list(s.prefs(g).task[:3])==[1,7,2] and group_order(g)==[1,7,2]
                right_group(g,p,2);f.menu(g,p,42702);assert group_order(g)==[1,7];editor=launch(g,p,'text editor',2);assert group_order(g)==[1,7,2];right_group(g,p,2);f.menu(g,p,42702);s.close(g,p)
                report['checks'].append('Existing per-user pin reordering and unpinning are reflected immediately; an unpinned running app remains reachable and can be pinned again without duplicating a button')
                pin(g,p,'calc',4);p.desktop(43104,True);assert s.windows(g,4)==1;launch(g,p,'software',11);p.desktop(10304,True);p.desktop(10004,True);assert s.windows(g,4)==0 and 4 not in s.prefs(g).task[:s.prefs(g).tasks] and 4 not in group_order(g);c.shot(g,'optional-app-removal');p.desktop(10304,True);s.close(g,p)
                report['checks'].append('Actual optional Calculator removal closes its real worker and removes its pin/group while the shell and Software Manager stay usable; reinstall remains available')
                for name,app in [('calc',4),('clock',8),('calendar',9),('image',14),('media',16)]:pin(g,p,name,app)
                assert list(s.prefs(g).task[:8])==[1,7,2,4,8,9,14,16]
                for name,app in [('settings',3),('downloads',5),('monitor',6),('disk utility',10),('software',11),('recovery',12),('archive',13),('help',18)]:launch(g,p,name,app)
                assert s.windows(g)==8;p.desktop(43001,True);rows=menu_rows(g);assert len(rows)<=12 and any(r['command']==43238 for r in rows);c.shot(g,'overflow-with-eight-windows');f.menu(g,p,43238);assert next(w for w in records(g) if w['slot']==f.model(g)[0])['app']==18
                s.search(g,p,'settings');c.key(g,'ret');assert s.windows(g)==8 and c.flag(g,'launcher');notice=ui.memory(g,ui.symbol('start_notice11',installed=True)[0],160).split(b'\0')[0];assert b'Close a window' in notice;c.shot(g,'window-quota-refusal');c.key(g,'esc');c.key(g,'esc');close_all(g,p)
                report['checks'].append('Eight pins and eight distinct running apps remain reachable through bounded overflow; selecting a hidden app focuses its real window and the eight-window quota refuses another without losing existing windows')
            f.same_pages(baseline,f.stats(g));c.idle(g);after=f.stats(g);report['resources']=dict(before=list(baseline),after=list(after),retained_pages=0);saved=bytes(s.prefs(g));
            if not args.smoke:assert ui.s.s.document(disk,'/System/Settings/start11-Owner.bin')==saved
            report['preferences_sha256']=hashlib.sha256(saved).hexdigest();(out/'native.log').write_bytes(g.log().encode())
        if not args.smoke:
            for n in (1,2):
                boot=ui.guest(work/f'ordinary-{n}',disk,media='installed',ready='M7_DESKTOP_READY');ui.s.normal_boot(boot,work/'install/vars.fd')
                with boot as g:
                    p=ui.Pointer(g);p.drain();assert bytes(s.prefs(g))==saved and group_order(g)==[1,7,2,4,8,9];assert len(group_controls(g))==6;c.shot(g,f'ordinary-{n}');p.desktop(43101,True);assert records(g)[0]['minimized'];p.desktop(43101,True);c.idle(g);(out/f'ordinary-{n}.log').write_bytes(g.log().encode())
            report['checks'].append('Two ordinary no-ISO starts preserve exact independently read pin/order preferences and restore the live Files group without a duplicate window button')
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode('utf-8'));print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
