"""Installed caption/window journeys through ordinary guest input only."""
import json,os,struct,time,traceback
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE4'
import components as c
ui=c.ui;ROOT=ui.ROOT;OUT=ROOT/'build/m12/stage4/chrome-native'
OUT.mkdir(parents=True,exist_ok=True);c.OUT=OUT

def controls(g):
    n=ui.integer(g,'control_count',True);raw=ui.memory(g,ui.symbol('controls',65536,True)[0],n*32)
    return [struct.unpack_from('<iiiiQI',raw,i*32) for i in range(n)]
def focused(g):
    base=ui.symbol('model',installed=True)[0];slot=int.from_bytes(ui.memory(g,base+236,4),'little')
    assert slot<8;return slot,struct.unpack('<4i',ui.memory(g,base+slot*28,16))
def geometry(g):return focused(g)[1]
def count(g):return int.from_bytes(ui.memory(g,ui.symbol('model',installed=True)[0]+232,4),'little')
def launch(g,p,name):
    if not c.flag(g,'launcher'):p.desktop(0,True)
    p.desktop(42004,True);c.key(g,'ctrl','a');c.type_text(g,name);c.key(g,'ret');p.drain()
def move(g,p,x,y):
    scale=c.flag(g,'scale73');p.move(x*scale//2,y*scale//2);p.drain()
def drag(g,p,x,y,xx,yy,release=True):
    move(g,p,x,y);p.down(True);p.drain();move(g,p,xx,yy)
    if release:p.down(False);p.drain()
def menu(g,p,command):
    n=c.flag(g,'file_menu_count11');raw=ui.memory(g,ui.symbol('file_menu_items11',installed=True)[0],n*16)
    matches=[i for i in range(n) if struct.unpack_from('<II',raw,i*16+8)==(command,1)]
    assert len(matches)==1,(command,n);p.desktop(32000+matches[0],True)
def stats(g):return struct.unpack('<4Q',ui.memory(g,ui.symbol('stats',32,True)[0],32))
def caption_states(g,p,label):
    x,y,w,h=geometry(g);move(g,p,x+180,y+80)
    normal=c.pixel(g,x+w-35,y+6)
    move(g,p,x+w-26,y+20);assert c.pixel(g,x+w-35,y+6)==0xb42318
    c.shot(g,label+'-close-hover');p.down(True);p.drain()
    assert c.pixel(g,x+w-35,y+6)==0x88180f;c.shot(g,label+'-close-pressed')
    move(g,p,x+180,y+80);p.down(False);p.drain();assert geometry(g)==(x,y,w,h)
    assert c.pixel(g,x+w-35,y+6)==normal
    # Caption controls participate in the real Tab ring, without activation.
    for _ in range(150):
        c.key(g,'tab')
        if c.flag(g,'control_active') and c.flag(g,'focused_action')==49001:break
    else:raise AssertionError('Maximize is unreachable through Tab')
    assert c.pixel(g,x+w-91,y+20)==(0xffffff if c.dark(g) else 0),hex(c.pixel(g,x+w-91,y+20))
    c.shot(g,label+'-keyboard-focus');c.key(g,'ret');base=ui.symbol('model',installed=True)[0];width,height=struct.unpack('<II',ui.memory(g,base+240,8));assert geometry(g)==(0,0,width,height-60)
    p.desktop(49001,True);assert geometry(g)==(x,y,w,h)

def main():
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m12-stage4-chrome');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
    report=dict(passed=False,stage='M12.4',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],owned_fixture=work.name,checks=[],profiles=[])
    try:
        live=ui.guest(work/'install',disk,resolution=(1280,800))
        with live as g:
            p=ui.Pointer(g)
            for command in (2,2,100,2,2,2):c.wizard(g,p,command)
            at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240)
            at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain()
            assert 'M7_DESKTOP_READY build='+meta['build_id'] in g.log()
            baseline=stats(g);normal=geometry(g);caption_states(g,p,'light')
            report['checks'].append('Caption hover/press/focus are distinct actual pixels; release outside cancels; Tab/Enter maximize and pointer restore preserve exact normal bounds')
            x,y,w,h=normal;owner=next(r[4] for r in controls(g) if r[5]==49000)
            active_border=c.pixel(g,x,y+80);launch(g,p,'text editor')
            assert c.pixel(g,x,y+80)!=active_border;c.shot(g,'active-inactive-frames');p.desktop(49002,True)
            p.desktop(49000,True)
            task=next(r for r in controls(g) if r[4]==owner and r[5]==70);p.logical(task[0]+task[2]//2,task[1]+task[3]//2,True);p.drain();assert geometry(g)==normal
            report['checks'].append('Inactive frame differs visibly from the active owner; Minimize and its exact taskbar target restore the normal window')
            p.desktop(49003,True);assert c.flag(g,'context11');c.shot(g,'window-menu');menu(g,p,44004)
            c.key(g,'left');c.key(g,'up');c.key(g,'esc');assert geometry(g)==normal
            c.key(g,'alt','spc');menu(g,p,44005);c.key(g,'right');c.key(g,'down');c.key(g,'ret')
            assert geometry(g)[2:]==(normal[2]+16,normal[3]+16)
            report['checks'].append('App icon and Alt+Space expose the same real menu; keyboard Move cancels and Size commits')
            for horizontal,vertical in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)):
                x,y,w,h=old=geometry(g);px=x+2 if horizontal<0 else x+w-2 if horizontal>0 else x+w//2;py=y+2 if vertical<0 else y+h-2 if vertical>0 else y+h//2
                drag(g,p,px,py,px+horizontal*16,py+vertical*12,False);assert geometry(g)!=old,(horizontal,vertical,old,geometry(g));c.key(g,'esc');p.down(False);p.drain();assert geometry(g)==old
            x,y,w,h=geometry(g);drag(g,p,x+w//2,y+h-2,x+w//2,738)
            edge=geometry(g);x,y,w,h=edge;drag(g,p,x+2,y+h-2,x-14,y+h-14,False)
            assert geometry(g)!=edge,('Bottom-left at full usable height is unreachable',edge,geometry(g))
            c.key(g,'esc');p.down(False);p.drain();assert geometry(g)==edge
            old=geometry(g);x,y,w,h=old;drag(g,p,x+180,y+18,x+240,y+52,False);c.key(g,'esc');p.down(False);p.drain();assert geometry(g)==old
            report['checks'].append('All eight resize edges/corners operate alongside the caption hit rectangles; Escape restores a captured move')
            x,y,w,h=geometry(g);drag(g,p,x+180,y+18,50,y+18)
            assert geometry(g)[0]<0,geometry(g)
            c.key(g,'alt','spc');assert c.flag(g,'context11');c.shot(g,'offscreen-window-menu')
            mx=c.flag(g,'context_x11');assert 0<=mx<1280
            c.key(g,'esc');c.key(g,'meta_l','up');assert geometry(g)==(0,0,1280,740);c.key(g,'meta_l','down')
            # A desktop click transfers keyboard ownership; Alt+F4 must not close background work.
            before=count(g);p.logical(1260,660,True);assert c.flag(g,'desktop_focus11');c.key(g,'alt','f4');assert count(g)==before
            c.key(g,'alt','spc');assert not c.flag(g,'context11')
            report['checks'].append('Partially off-screen windows keep a reachable menu; desktop Alt+F4/Alt+Space cannot act on a background window')
            launch(g,p,'text editor');c.type_text(g,'Unsaved caption test');slot=focused(g)[0]
            p.desktop(49002,True);c.shot(g,'unsaved-close-review')
            raw=ui.memory(g,ui.symbol('apps',installed=True)[0],ui.symbol('apps',installed=True)[1]);assert b'Unsaved caption test' in raw
            p.desktop(61,True)
            if focused(g)[0]!=slot:
                c.shot(g,'keep-editing-focus-failure');report['focus_failure']=dict(expected_slot=slot,actual=list(focused(g)),window_count=count(g),controls=[list(r) for r in controls(g) if r[5] in (60,61,49002)])
            assert focused(g)[0]==slot
            before=count(g);p.desktop(49002,True);p.desktop(60,True);p.drain();assert count(g)==before-1
            c.key(g,'meta_l','e');p.drain();owner=c.control(g,49002)[4];assert owner&0xffffffff==focused(g)[0]+1
            c.key(g,'ctrl','shift','n');assert c.flag(g,'file_dialog_state11')
            assert not any(r[5] in range(49000,49004) and r[4]==owner for r in controls(g))
            before=count(g);blocked_bounds=geometry(g)
            for chord in [('alt','f4'),('alt','spc'),('meta_l','up'),('meta_l','left'),('meta_l','right'),('meta_l','down')]:
                c.key(g,*chord);assert count(g)==before and geometry(g)==blocked_bounds and not c.flag(g,'context11'),chord
            assert any(r[5] in range(49000,49004) and r[4]!=owner for r in controls(g))
            c.shot(g,'owner-dialog');c.key(g,'esc');assert not c.flag(g,'file_dialog_state11')
            p.desktop(49002,True)
            report['checks'].append('Caption Close preserves unsaved text behind review; Keep editing returns to the same owner; file dialog blocks its owner caption/menu/Win-key geometry routes while unrelated captions remain available; explicit Discard closes it')
            c.open_settings(g,p);p.desktop(43,True);p.desktop(47,True);caption_states(g,p,'dark');p.close_app(3,True);p.drain()
            after=stats(g);assert baseline[0]==after[0] and baseline[3]==after[3]
            c.idle(g);report['resources']=dict(before=list(baseline),after=list(after),retained_pages=after[0]-baseline[0])
            report['checks'].append('Light/dark caption journeys retain zero managed pages and no new allocation failures; idle CPUs halt without repaint polling')
            (OUT/'install.log').write_text(g.log(),encoding='utf-8')
        assert ui.s.s.document(disk,'/Users/Owner/Documents/Welcome.txt')==(ROOT/'distros/packages/m12-desktop-guide/content.txt').read_bytes()
        for number in (1,2):
            boot=ui.guest(work/f'disk-{number}',disk,media='installed',ready='M7_DESKTOP_READY');ui.s.normal_boot(boot,live.folder/'vars.fd')
            with boot as g:
                p=ui.Pointer(g);p.drain();assert 'M7_DESKTOP_READY build='+meta['build_id'] in g.log();p.desktop(49003,True);assert c.flag(g,'context11');c.key(g,'esc');c.idle(g)
                c.shot(g,f'disk-only-{number}');(OUT/f'disk-{number}.log').write_text(g.log(),encoding='utf-8')
        report['checks'].append('Matching installed guide and two independent ordinary disk starts retain usable window controls')
        for label,resolution,scale_action in [('150',(1920,1200),112),('4k',(3840,2160),113)]:
            with ui.guest(work/label,disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution) as g:
                p=ui.Pointer(g);p.drain();c.open_settings(g,p);p.desktop(scale_action,True);p.close_app(3,True);p.drain();assert c.flag(g,'scale73')==(3 if label=='150' else 4)
                caption_states(g,p,'native-'+label);c.shot(g,'native-'+label);c.idle(g);report['profiles'].append(dict(physical=list(resolution),scale=c.flag(g,'scale73')))
        report['checks'].append('Actual 1920x1200/150% and 3840x2160/200% framebuffers exercise the same caption controls and idle halt without image resizing')
        report['passed']=True
    except Exception:
        report['error']=ui.q.clean(traceback.format_exc());raise
    finally:
        report['idle_observations']=c.IDLE_OBSERVATIONS
        (OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
