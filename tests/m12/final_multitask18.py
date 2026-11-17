"""M12.18 native switch/arrange/snap journeys on a real installed guest."""
import argparse,hashlib,json,os,struct,time,traceback
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE18'
from PIL import Image
import taskbar_observe as t
c=t.c;f=t.f;ui=t.ui;s=t.s;ROOT=t.ROOT

def geometry(g,slot=None):
    if slot is None:slot=f.model(g)[0]
    return struct.unpack('<4i',ui.memory(g,ui.symbol('model',installed=True)[0]+slot*28,16))

def alt(g,down):
    g.qmp('input-send-event',{'events':[{'type':'key','data':{'down':down,'key':{'type':'qcode','data':'alt'}}}]});time.sleep(.12);ui.Pointer(g).drain()

def tokens(g):
    n=c.flag(g,'switch_count11');assert n<=8
    return list(struct.unpack('<'+str(n)+'Q',ui.memory(g,ui.symbol('switch_tokens11',installed=True)[0],n*8)))

def arrange(g,p):
    c.key(g,'alt','spc');assert c.flag(g,'context11');f.menu(g,p,44006);assert c.flag(g,'switch_open11')==2

def drag(g,p,x,y,xx,yy,release=True):
    scale=c.flag(g,'scale73');p.move(x*scale//2,y*scale//2);p.drain();p.down(True);p.drain();p.move(xx*scale//2,yy*scale//2);p.drain()
    if release:p.down(False);p.drain()

def selected_contrast(g,path):
    # Default shipped dark teal requires actual light glyphs inside the selected row.
    x,y,w,h,*_=c.control(g,44100+c.flag(g,'switch_choice11'));scale=c.flag(g,'scale73')
    with Image.open(path) as image:
        crop=image.convert('RGB').crop(tuple(v*scale//2 for v in (x+50,y+8,x+w-30,y+28)))
        assert sum(pixel==(255,255,255) for pixel in crop.getdata())>=3,'Selected row is missing its shared contrast foreground'

def close_all18(g,p):
    from settings_observe import close
    while t.records(g):
        target=t.records(g)[-1];t.focus(g,p,target);c.key(g,'alt','f4');deadline=time.monotonic()+15
        while any(w['token']==target['token'] for w in t.records(g)):
            if t.closing(g):p.desktop(60,True)
            if time.monotonic()>deadline:raise AssertionError(('Window failed to close',target,t.records(g),c.flag(g,'file_dialog_state11'),c.flag(g,'launcher')))
            time.sleep(.05);p.drain()
    p.drain()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--smoke',action='store_true');args=parser.parse_args()
    out=ROOT/('build/m12/stage18/multitask-smoke' if args.smoke else 'build/m12/stage18/multitask-native');out.mkdir(parents=True,exist_ok=True);c.OUT=out
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m12-stage18-multitask-smoke' if args.smoke else 'm12-stage18-multitask');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
    report=dict(passed=False,stage='M12.18',development_only=args.smoke,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],owned_fixture=work.name,checks=[])
    try:
        with ui.guest(work/'install',disk) as g:
            p=ui.Pointer(g)
            for action in (2,2,100,2,2,2):c.wizard(g,p,action)
            at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain();s.close(g,p);baseline=f.stats(g)
            first=t.launch(g,p,'files',1);normal_first=geometry(g);second=t.launch(g,p,'files',1);f.visit(g,p,'Documents');normal_second=geometry(g)
            arrange(g,p);assert geometry(g)==normal_second;c.shot(g,'arrange-preview');selected_contrast(g,out/'arrange-preview.png');c.key(g,'esc');assert not c.flag(g,'switch_open11') and geometry(g)==normal_second
            arrange(g,p);p.desktop(44100,True);assert geometry(g,second['slot'])==(0,0,640,740);assert c.flag(g,'switch_open11')==3 and tokens(g)==[first['token']];c.shot(g,'snap-assist');p.desktop(44100,True);assert geometry(g,first['slot'])==(640,0,640,740) and not c.flag(g,'switch_open11')
            c.shot(g,'two-real-windows-side-by-side');c.key(g,'meta_l','down');assert geometry(g)==normal_first;t.focus(g,p,second);c.key(g,'meta_l','down');assert geometry(g)==normal_second
            report['checks'].append('Real install and retained-ISO startup; discoverable Arrange windows previews without mutating bounds, Escape preserves them, and choosing the complementary real Files window places both halves with exact independent normal-bounds restoration')
            editor=t.launch(g,p,'text editor',2);c.type_text(g,'Keep this unsaved work');other=t.launch(g,p,'text editor',2);c.shot(g,'documents-before-switch')
            alt(g,True);c.key(g,'tab');assert c.flag(g,'switch_open11')==1 and len(tokens(g))==4;before=f.model(g)[0];c.shot(g,'switcher-icons-documents');selected_contrast(g,out/'switcher-icons-documents.png');c.key(g,'down');chosen=tokens(g)[c.flag(g,'switch_choice11')];assert f.model(g)[0]==before;alt(g,False);assert next(w for w in t.records(g) if w['slot']==f.model(g)[0])['token']==chosen
            before=f.model(g)[0];alt(g,True);c.key(g,'tab');c.key(g,'esc');alt(g,False);assert f.model(g)[0]==before and not c.flag(g,'switch_open11')
            alt(g,True);c.key(g,'shift','tab');chosen=tokens(g)[c.flag(g,'switch_choice11')];alt(g,False);assert next(w for w in t.records(g) if w['slot']==f.model(g)[0])['token']==chosen
            alt(g,True);c.key(g,'tab');chosen=tokens(g)[0];p.desktop(44100,True);alt(g,False);assert next(w for w in t.records(g) if w['slot']==f.model(g)[0])['token']==chosen
            t.focus(g,p,editor);assert bytes(t.app_view(g).text)==b'Keep this unsaved work';c.key(g,'meta_l','down');assert next(w for w in t.records(g) if w['token']==editor['token'])['minimized'];alt(g,True);c.key(g,'tab');choice=tokens(g).index(editor['token']);p.desktop(44100+choice,True);alt(g,False);assert not next(w for w in t.records(g) if w['token']==editor['token'])['minimized'] and bytes(t.app_view(g).text)==b'Keep this unsaved work'
            report['checks'].append('Actual Alt+Tab keeps a bounded MRU snapshot with original icons and document/folder identities; arrows preview choice, Alt release and mouse commit, Escape preserves focus, and selecting a minimized dirty Editor restores exact unsaved text')
            if not args.smoke:
                p.desktop(54001,True);assert c.flag(g,'file_dialog_state11')==10;old=geometry(g);c.key(g,'meta_l','left');assert geometry(g)==old and not c.flag(g,'switch_open11');c.key(g,'alt','spc');assert not c.flag(g,'context11')
                t.focus(g,p,second);c.key(g,'meta_l','left');assert c.flag(g,'switch_open11')==3 and editor['token'] not in tokens(g);c.shot(g,'assist-excludes-modal-owner');c.key(g,'esc');t.focus(g,p,editor);p.desktop(54010,True);assert bytes(t.app_view(g).text)==b'Keep this unsaved work'
                report['checks'].append('Active file-dialog ownership blocks Arrange/keyboard geometry changes and excludes that owner from complementary snap choices; cancellation preserves the dirty document')
                close_all18(g,p);first=t.launch(g,p,'files',1);second=t.launch(g,p,'files',1);normal=geometry(g);x,y,w,h=normal
                drag(g,p,x+180,y+18,2,160,False);assert c.flag(g,'window_snap_preview11')==2;c.shot(g,'edge-preview');c.key(g,'esc');p.down(False);p.drain();assert geometry(g)==normal and not c.flag(g,'switch_open11')
                x,y,w,h=geometry(g);drag(g,p,x+180,y+18,2,160);assert c.flag(g,'switch_open11')==3;c.key(g,'esc');assert geometry(g)==(0,0,640,740);c.key(g,'meta_l','down');assert geometry(g)==normal
                c.key(g,'meta_l','right');assert geometry(g,second['slot'])==(640,0,640,740);c.key(g,'esc');c.key(g,'meta_l','down');assert geometry(g)==normal
                report['checks'].append('Actual caption edge drag previews and Escape cancel restore exact bounds; release and Win+Left/Right commit supported halves, Skip/Escape retain the other side, and Win+Down restores the original normal rectangle')
                settings=t.launch(g,p,'settings',3);old=geometry(g);arrange(g,p);assert c.flag(g,'switch_choice11')==2;assert not any(r[5] in (44100,44101) for r in f.controls(g));c.key(g,'up');c.shot(g,'minimum-size-refusal');c.key(g,'ret');assert geometry(g)==old and c.flag(g,'switch_open11')==2;c.key(g,'esc');t.focus(g,p,settings);s.close(g,p)
                while s.windows(g)<8:t.launch(g,p,'files',1)
                before=s.windows(g);s.search(g,p,'files');c.key(g,'ret');assert s.windows(g)==before and c.flag(g,'launcher');c.key(g,'esc');c.key(g,'esc');alt(g,True);c.key(g,'tab');assert len(tokens(g))==8;c.shot(g,'eight-window-switcher');c.key(g,'esc');alt(g,False)
                report['checks'].append('Apps whose actual minimum exceeds half the display expose disabled half choices with a reason and keep their bounds; the eight-window quota refuses another window while the full switcher remains reachable')
            close_all18(g,p)
            if not args.smoke:
                t.pin(g,p,'calc',4);t.right_group(g,p,4);f.menu(g,p,42704);saved=bytes(s.prefs(g));assert ui.s.s.document(disk,'/System/Settings/start11-Owner.bin')==saved;report['preferences_sha256']=hashlib.sha256(saved).hexdigest()
            f.same_pages(baseline,f.stats(g));c.idle(g);report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0);(out/'native.log').write_bytes(g.log().encode())
        if not args.smoke:
            for n in (1,2):
                boot=ui.guest(work/f'ordinary-{n}',disk,media='installed',ready='M7_DESKTOP_READY');ui.s.normal_boot(boot,work/'install/vars.fd')
                with boot as g:
                    p=ui.Pointer(g);p.drain();assert bytes(s.prefs(g))==saved and not c.flag(g,'switch_open11');arrange(g,p);c.key(g,'esc');c.idle(g);c.shot(g,f'ordinary-{n}');(out/f'ordinary-{n}.log').write_bytes(g.log().encode())
            report['checks'].append('Two ordinary no-ISO starts reach the installed desktop and retain usable Arrange/Cancel without persisting transient overlays or changing firmware boot order')
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
