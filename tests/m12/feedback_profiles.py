"""M12.14 actual menu/search feedback at compact, dark, 150% and 4K."""
import json,os,struct,traceback
from pathlib import Path
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE14'
import settings_observe as h
c=h.c;f=h.f;s=h.s;t=h.t;ui=h.ui;ROOT=h.ROOT

def restore_window(g,p,window):
    # No focused slot is legitimate when the sole remaining window is minimized.
    action=43100+window['app'];target=43220+window['app']
    if any(r[5]==action for r in t.group_controls(g)):p.desktop(action,True)
    else:
        p.desktop(43001,True)
        for _ in range(3):
            if any(r['command']==target for r in t.menu_rows(g)):break
            f.menu(g,p,43200)
        f.menu(g,p,target)
    if sum(w['app']==window['app'] for w in t.records(g))>1:f.menu(g,p,43020+window['slot'])
    assert f.model(g)[0]==window['slot'] and next(w for w in t.records(g) if w['slot']==window['slot'])['token']==window['token']

def main():
    out=ROOT/'build/m12/stage14/feedback-profiles';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    native=json.loads((ROOT/'build/m12/stage14/feedback-native/results.json').read_text(encoding='utf-8'));meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));assert native['passed'] and native['build_id']==meta['build_id'];work=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage14-feedback'/native['owned_fixture'];disk=work/'owned.img';before_disk=f.sha_file(disk);report=dict(passed=False,build_id=meta['build_id'],profiles=[],checks=[])
    try:
        for label,resolution,scale,dark in [('compact',(800,600),2,False),('compact-dark',(800,600),2,True),('150',(1920,1200),3,False),('4k',(3840,2160),4,False)]:
            with ui.guest(work/('profile-'+label),disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution) as g:
                p=ui.Pointer(g);p.drain();t.close_all(g,p);before=f.stats(g);c.open_settings(g,p);settings=next(w for w in t.records(g) if w['app']==3);p.desktop(43 if dark else 44,True)
                if label=='150':p.desktop(59001,True);p.desktop(112,True)
                assert c.flag(g,'scale73')==scale;p.desktop(49000,True)
                t.launch(g,p,'files',1);f.visit(g,p,'/System');p.desktop(f.item(g,p,'Settings'),True);c.key(g,'shift','f10');assert c.flag(g,'context11');logical=struct.unpack('<II',ui.memory(g,ui.symbol('model',installed=True)[0]+240,8));x=c.flag(g,'context_x11');y=c.flag(g,'context_y11');count=c.flag(g,'file_menu_count11');assert x+400<=logical[0] and y+count*38+64<=logical[1]-60;c.shot(g,'menu-'+label);c.key(g,'esc');h.close(g,p)
                s.search(g,p,'clock');assert any(r[5]==42036 for r in f.controls(g));c.shot(g,'search-'+label);p.desktop(42036,True);c.key(g,'esc')
                for _ in range(7):
                    before_count=s.windows(g,1);p.desktop(0,True);rows=s.results(g);preferences=s.prefs(g);index=next(i for i,(kind,item) in enumerate(rows) if (kind==1 and item==1) or (kind==3 and preferences.pinned[item].app==1));p.desktop(42200+index,True);assert s.windows(g,1)==before_count+1;p.desktop(49000,True)
                assert len(t.records(g))==8 and all(w['minimized'] for w in t.records(g))
                s.search(g,p,'clock');c.key(g,'ret');c.key(g,'esc');c.key(g,'esc');dismiss=[r for r in f.controls(g) if r[5]==60002];assert len(dismiss)==1;xx,yy,ww,hh,*_=dismiss[0];assert xx>=0 and yy>=0 and xx+ww<=logical[0] and yy+hh<=logical[1]-60;c.shot(g,'notice-'+label);p.desktop(60002,True)
                for window in [w for w in t.records(g) if w['app']==1]:restore_window(g,p,window);c.key(g,'alt','f4')
                restore_window(g,p,settings);h.close(g,p)
                assert not h.preview(g)[0];f.same_pages(before,f.stats(g));c.idle(g);stats=f.stats(g);report['profiles'].append(dict(name=label,physical=list(resolution),logical=list(logical),scale=scale,theme='dark' if dark else 'light',managed_current_bytes=stats[0]*4096,managed_peak_bytes=stats[1]*4096,retained_pages=0,notification_scope='Eight real live minimized windows; one restored/closed at a time. The independent native journey covers eight visible windows.'));(out/(label+'.log')).write_bytes(g.log().encode())
        assert f.sha_file(disk)==before_disk;report['checks'].append('Actual compact light/dark, 150% and 4K profiles display complete protected-item context explanations and explicit global-search controls within the logical display');report['checks'].append('Session-only appearance previews restore on close, leave the complete fixture disk unchanged and retain zero managed pages at idle');report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
