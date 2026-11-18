"""M13.10 feedback through actual installed guest input and persistent bytes."""
import hashlib,json,os,struct,traceback
os.environ['ENGACER12_IMAGE']='EngacerOS-M13STAGE10'
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'m12'))
import settings_observe as h
import capture14,observe20,observer8
capture14.bind(h.ui);observe20.bind(h.ui);observer8.bind(h.ui)
c=h.c;f=h.f;s=h.s;t=h.t;ui=h.ui;ROOT=h.ROOT

def text_symbol(g,name,size):return ui.memory(g,ui.symbol(name,installed=True)[0],min(size,ui.symbol(name,installed=True)[1])).split(b'\0')[0].decode()
def dialog_owner(g):return int.from_bytes(ui.memory(g,ui.symbol('file_dialog_state11',installed=True)[0]+32,8),'little')
def main():
    out=ROOT/'build/m13/stage10/feedback-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m1310-feedback');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);report=dict(passed=False,stage='M13.10',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],owned_fixture=work.name,checks=[])
    try:
        with ui.guest(work/'install',disk) as g:
            p=h.q.install(g);baseline=f.stats(g)
            editor=t.launch(g,p,'text editor',2);path=f.app(g)['path'];assert path not in f.entries(g) and not t.app_view(g).dirty;c.shot(g,'new-document-not-saved');c.type_text(g,'Feedback keeps my document');p.desktop(20,True);assert ui.s.s.document(disk,path)==b'Feedback keeps my document' and not t.app_view(g).dirty;c.shot(g,'document-saved');h.close(g,p)
            report['checks'].append('A new empty Editor document has no published disk entry; explicit Save publishes the exact text and changes its actual saved state')
            t.pin(g,p,'clock',8);s.search(g,p,'clock');assert not text_symbol(g,'start_notice11',128);assert any(r[5]==42036 for r in f.controls(g));c.shot(g,'global-search-clear');p.desktop(42036,True);assert not text_symbol(g,'start_query11',256);c.key(g,'esc')
            report['checks'].append('Global app/folder search exposes Clear search and removes stale pin notices; Clear returns to browsing without launching an app')
            files=t.launch(g,p,'files',1);f.visit(g,p,'/System');p.desktop(f.item(g,p,'Settings'),True);c.key(g,'shift','f10');assert c.flag(g,'context11');reason=text_symbol(g,'file_menu_reason11',128);assert 'protected' in reason;assert not c.flag(g,'file_menu_scroll11');c.shot(g,'protected-folder-explanation');c.key(g,'esc');h.close(g,p)
            report['checks'].append('A real protected System item exposes the complete source-specific context-menu explanation without a destructive action')
            editor=t.launch(g,p,'text editor',2);c.type_text(g,'Keep dialog ownership');p.desktop(54001,True);owner=dialog_owner(g);assert owner==editor['token'];c.open_settings(g,p);settings=next(w for w in t.records(g) if w['slot']==f.model(g)[0]);p.desktop(43,True);p.desktop(47,True);assert dialog_owner(g)==owner and c.flag(g,'file_dialog_state11')==10 and 'file operation' in f.app(g)['notice'];assert f.has(g,60003);c.shot(g,'blocked-save-show-dialog');p.desktop(60003,True);assert f.model(g)[0]==editor['slot'] and bytes(t.app_view(g).text)==b'Keep dialog ownership';p.desktop(54010,True);h.close(g,p);p.desktop(60,True);t.focus(g,p,settings);p.desktop(59005,True);h.close(g,p)
            report['checks'].append('Settings refuses persistence during another window Save As; Show current dialog returns to the exact generation owner and preserves its unsaved text')
            files=t.launch(g,p,'files',1);f.visit(g,p,'/Users/Owner/Documents');p.desktop(f.item(g,p,path.rsplit('/',1)[-1]),True);p.desktop(40000,True);p.desktop(40002,True);assert c.flag(g,'file_dialog_state11')==2 and dialog_owner(g)==files['token'];editor=t.launch(g,p,'text editor',2);c.type_text(g,'Keep conflict ownership');p.desktop(54001,True);assert c.flag(g,'file_dialog_state11')==2 and dialog_owner(g)==files['token'] and 'current file dialog' in f.app(g)['notice'];t.focus(g,p,files);p.desktop(40022,True);assert not c.flag(g,'file_dialog_state11');copies=[name for name in f.entries(g) if name.startswith('/Users/Owner/Documents/') and name!=path and name.endswith('.txt') and ui.s.s.document(disk,name)==b'Feedback keeps my document'];assert copies;assert ui.s.s.document(disk,path)==b'Feedback keeps my document';t.focus(g,p,editor);assert bytes(t.app_view(g).text)==b'Keep conflict ownership';h.close(g,p);p.desktop(60,True);t.focus(g,p,files);h.close(g,p)
            report['checks'].append('An actual same-folder copy collision retains its Files review owner while another Editor is refused a picker; Keep both produces independently verified identical file bytes and preserves the other unsaved document')
            files=t.launch(g,p,'files',1);f.visit(g,p,'/Users/Owner/Documents');clone=copies[0];f.double(g,p,f.item(g,p,clone.rsplit('/',1)[-1]));first=next(w for w in t.records(g) if w['slot']==f.model(g)[0]);t.focus(g,p,files);f.double(g,p,f.item(g,p,clone.rsplit('/',1)[-1]));second=next(w for w in t.records(g) if w['slot']==f.model(g)[0]);assert first['token']!=second['token'];c.type_text(g,'Second edit ');unsaved=bytes(t.app_view(g).text);t.focus(g,p,first);c.type_text(g,'First edit ');p.desktop(20,True);committed=ui.s.s.document(disk,clone);t.focus(g,p,second);p.desktop(20,True);assert 'changed on disk' in f.app(g)['notice'] and bytes(t.app_view(g).text)==unsaved and t.app_view(g).dirty and ui.s.s.document(disk,clone)==committed;c.shot(g,'changed-file-save-refused');h.close(g,p);p.desktop(60,True);t.focus(g,p,first);h.close(g,p);t.focus(g,p,files);f.visit(g,p,'USB drives');assert f.app(g)['mode']==1 and not any(21100<=r[5]<21116 for r in f.current_controls(g));c.shot(g,'missing-usb-empty-state');h.close(g,p)
            report['checks'].append('Two real Editors open the same existing file: after one commits, the other Save refuses the changed source, preserves exact unsaved text and leaves committed bytes untouched; missing USB also has a real empty view')
            for i in range(8):t.launch(g,p,'files',1)
            s.search(g,p,'clock');c.key(g,'ret');assert s.windows(g)==8;c.key(g,'esc');c.key(g,'esc');assert text_symbol(g,'shell_notice',96);assert any(r[5]==60002 for r in f.controls(g));c.shot(g,'bounded-window-limit-notice');unchanged=t.records(g);width=int.from_bytes(ui.memory(g,ui.symbol('model',installed=True)[0]+240,4),'little');dismiss=next(r for r in f.controls(g) if r[5]==60002);p.logical(dismiss[0]-300,dismiss[1]+64,True);p.drain();assert t.records(g)==unchanged;p.desktop(60002,True);assert not text_symbol(g,'shell_notice',96);t.close_all(g,p)
            report['checks'].append('The eight-window limit leaves all existing windows intact and exposes a bounded, explicitly dismissible notice instead of covering the Files footer')
            for name,kind in [('clock',8),('calendar',9),('media',16),('calc',4),('image',14)]:t.pin(g,p,name,kind)
            preferences=bytes(s.prefs(g));assert ui.s.s.document(disk,'/System/Settings/start11-Owner.bin')==preferences;f.same_pages(baseline,f.stats(g));c.idle(g);report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0);report['preferences_sha256']=hashlib.sha256(preferences).hexdigest();(out/'native.log').write_bytes(g.log().encode())
        for label,ps2 in [('usb',False),('ps2',True)]:
            boot=ui.guest(work/('ordinary-'+label),disk,media='installed',ready='M7_DESKTOP_READY',ps2_only=ps2);ui.s.normal_boot(boot,work/'install/vars.fd')
            with boot as g:
                p=ui.Pointer(g);p.drain();assert bytes(s.prefs(g))==preferences and ui.s.s.document(disk,path)==b'Feedback keeps my document';assert not c.flag(g,'file_dialog_state11') and not text_symbol(g,'shell_notice',96);c.shot(g,'ordinary-'+label);c.idle(g);(out/('ordinary-'+label+'.log')).write_bytes(g.log().encode())
        report['checks'].append('Independent no-ISO USB and PS/2 startups retain exact saved document and Start preferences, clear transient dialogs/messages and halt at idle')
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
