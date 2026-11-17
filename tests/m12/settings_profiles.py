"""Real compact/light/dark/150%/4K Settings, scale cancellation and modal safety."""
import json,os,struct,traceback
from pathlib import Path
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE13'
import settings_observe as h
c=h.c;f=h.f;s=h.s;t=h.t;ui=h.ui;ROOT=h.ROOT

def main():
    out=ROOT/'build/m12/stage13/settings-profiles';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    native=json.loads((ROOT/'build/m12/stage13/settings-native/results.json').read_text(encoding='utf-8'));meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));assert native['passed'] and native['build_id']==meta['build_id'];work=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage13-settings'/native['owned_fixture'];disk=work/'owned.img';before_disk=f.sha_file(disk);report=dict(passed=False,build_id=meta['build_id'],profiles=[],checks=[])
    try:
        for label,resolution,scale,dark in [('compact',(800,600),2,False),('compact-dark',(800,600),2,True),('150',(1920,1200),3,False),('4k',(3840,2160),4,False)]:
            with ui.guest(work/('profile-'+label),disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution) as g:
                p=ui.Pointer(g);p.drain();c.open_settings(g,p);before=f.stats(g);initial_scale=c.flag(g,'scale73');initial_colors=h.colors(g);settings=next(w for w in t.records(g) if w['app']==3);p.desktop(43 if dark else 44,True)
                if label=='150':p.desktop(59001,True);p.desktop(112,True)
                assert c.flag(g,'scale73')==scale
                for action,name in [(59000,'appearance'),(59001,'display'),(59002,'input'),(59003,'system')]:
                    p.desktop(action,True);assert h.page(g)==action-59000;logical=struct.unpack('<II',ui.memory(g,ui.symbol('model',installed=True)[0]+240,8))
                    for x,y,w,hh,owner,command in f.current_controls(g):assert x>=0 and y>=0 and x+w<=logical[0] and y+hh<=logical[1],(label,name,command,(x,y,w,hh),logical)
                    c.key(g,'tab');assert c.flag(g,'control_active');c.shot(g,name+'-'+label)
                if label=='150':
                    editor=t.launch(g,p,'text editor',2);c.type_text(g,'Scale guard preserves me');p.desktop(54001,True);assert c.flag(g,'file_dialog_state11')==10;t.focus(g,p,settings);h.close(g,p);assert any(w['token']==settings['token'] for w in t.records(g)) and h.preview(g)[0]==settings['token'] and c.flag(g,'scale73')==3 and 'file dialog' in f.app(g)['notice'];c.shot(g,'scale-close-modal-refused');t.focus(g,p,editor);assert bytes(t.app_view(g).text)==b'Scale guard preserves me';p.desktop(54010,True);s.close(g,p);p.desktop(60,True);t.focus(g,p,settings)
                    report['checks'].append('An actual 150% scale preview refuses owner closure while another window owns Save As; exact unsaved work survives, and after cancelling the dialog closing restores the previous display choice')
                h.close(g,p);assert not h.preview(g)[0] and c.flag(g,'scale73')==initial_scale and h.colors(g)==initial_colors;f.same_pages(before,f.stats(g));c.idle(g);stats=f.stats(g);report['profiles'].append(dict(name=label,physical=list(resolution),logical=list(logical),scale=scale,theme='dark' if dark else 'light',managed_current_bytes=stats[0]*4096,managed_peak_bytes=stats[1]*4096,retained_pages=0));(out/(label+'.log')).write_bytes(g.log().encode())
        assert f.sha_file(disk)==before_disk;report['checks'].append('Four actual display profiles keep all four Settings categories and registered controls reachable; cancelled previews leave the complete disk unchanged, retain zero managed pages and halt at idle');report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
