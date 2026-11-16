"""Actual installed desktop tasks using normal guest input and read-only observations."""
import hashlib,json,os,struct,time,traceback,subprocess,sys
from PIL import Image,ImageChops
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE3'
import components as c
ui=c.ui;ROOT=ui.ROOT;OUT=ROOT/'build/m12/stage3/desktop-native';OUT.mkdir(parents=True,exist_ok=True);c.OUT=OUT
import icons_host as art

def rows(g):
    raw=ui.memory(g,ui.symbol('volume',0xd3040,True)[0]+64,1024*280)
    result={}
    for i in range(1024):
        value=raw[i*280:(i+1)*280];first,size,crc,kind=struct.unpack_from('<QQII',value,256)
        if kind:result[value[:256].split(b'\0')[0].decode()]=(i,kind,size,crc)
    return result

def controls(g):
    n=ui.integer(g,'control_count',True);raw=ui.memory(g,ui.symbol('controls',65536,True)[0],n*32)
    return [struct.unpack_from('<iiiiQI',raw,i*32) for i in range(n)]

def double(g,p,action):
    x,y=point(g,action);scale=c.flag(g,'scale73');p.move(x*scale//2,y*scale//2);p.drain();began=time.monotonic()
    for down in (True,False,True,False):
        g.qmp('input-send-event',{'events':[{'type':'btn','data':{'down':down,'button':'left'}}]});time.sleep(.06)
    assert time.monotonic()-began<.5,'Host did not deliver a double-click within the configured interval'
    p.drain()

def count(g):return int.from_bytes(ui.memory(g,ui.symbol('model',installed=True)[0]+232,4),'little')

def point(g,action):
    matches=[r for r in controls(g) if r[5]==action];assert matches,action
    x,y,w,h,_,_=matches[-1];return x+w//2,y+h//2

def right(g,p,x,y):
    scale=c.flag(g,'scale73');p.move(x*scale//2,y*scale//2);p.drain()
    for down in (True,False):g.qmp('input-send-event',{'events':[{'type':'btn','data':{'down':down,'button':'right'}}]});p.drain()
    assert c.flag(g,'context11')

def menu(g,p,command):
    n=c.flag(g,'file_menu_count11');raw=ui.memory(g,ui.symbol('file_menu_items11',installed=True)[0],n*16)
    matches=[i for i in range(n) if struct.unpack_from('<II',raw,i*16+8)==(command,1)];assert len(matches)==1,(command,n)
    p.desktop(32000+matches[0],True)

def job(g,p):
    end=time.monotonic()+90
    while True:
        active,waiting=struct.unpack('<II',ui.memory(g,ui.symbol('file_job_state11',installed=True)[0],8))
        assert not waiting,'Unexpected conflict'
        if not active:break
        if time.monotonic()>end:raise TimeoutError('File transaction')
        time.sleep(.05)
    p.drain();assert c.flag(g,'file_job_error11')==0

def text_dialog(g,name):
    assert c.flag(g,'file_dialog_state11') in (1,7,8)
    c.key(g,'ctrl','a');c.type_text(g,name);c.key(g,'ret');assert not c.flag(g,'file_dialog_state11')

def create(g,p,name):
    c.key(g,'ctrl','shift','n');text_dialog(g,name)
    assert '/Users/Owner/Desktop/'+name in rows(g)

def desktop_item(g,p,path):
    index=rows(g)[path][0]
    raw=ui.memory(g,ui.symbol('file_lists11',installed=True)[0]+8*2328,2328)
    n=struct.unpack_from('<I',raw,264)[0];order=struct.unpack_from('<1024H',raw,276)
    row=order[:n].index(index);action=33000+row
    for _ in range(30):
        if any(v[5]==action for v in controls(g)):return action
        current=c.flag(g,'desktop_page11');visible=[v[5]-33000 for v in controls(g) if 33000<=v[5]<34024]
        assert visible
        p.desktop(40027 if row<min(visible) else 40028,True)
        assert c.flag(g,'desktop_page11')!=current
    raise AssertionError('Desktop item unreachable')

def selected(g,path):
    index=rows(g)[path][0];raw=ui.memory(g,ui.symbol('desktop_files_selected11',installed=True)[0],128)
    return bool(raw[index//8]&(1<<(index%8)))

def close_files(g,p):
    p.close_app(1,True);p.drain();assert count(g)==0

def icon_pixels(g,p,name,theme,objects=None):
    p.move(1200,80);p.drain();c.shot(g,name);scale=c.flag(g,'scale73');compared=[]
    with Image.open(OUT/(name+'.png')) as source:
        image=source.convert('RGB')
        for action,identity,*overlay in (objects or [(30000,42),(30001,20),(30002,3),(30003,38)]):
            x,y,w,h,_,_=next(r for r in controls(g) if r[5]==action)
            left=(x+36)*scale//2;top=(y+6)*scale//2;extent=48*scale//2
            background=Image.new('RGBA',(extent,extent))
            for row in range(extent):
                color=image.getpixel((left-4*scale//2,top+row))+(255,)
                for column in range(extent):background.putpixel((column,row),color)
            background.alpha_composite(art.icon(OUT/'icon-oracle.exe',identity,extent,theme))
            if overlay:background.alpha_composite(art.icon(OUT/'icon-oracle.exe',28,extent//2,theme),(0,extent//2))
            difference=ImageChops.difference(image.crop((left,top,left+extent,top+extent)),background.convert('RGB'))
            maximum=max(high for low,high in difference.getextrema());assert maximum<=1,(action,theme,maximum)
            compared.append(dict(action=action,theme=theme,physical_size=extent,max_channel_difference=maximum))
    return compared

def main():
    sys.path.insert(0,str(ROOT/'tools/build'));from m2 import pinned_tools
    subprocess.run([pinned_tools()['clang'],'-std=c17','-O2','-Wall','-Wextra','-Werror','-I','include','tests/m12/icons_host.c','-o',str(OUT/'icon-oracle.exe')],cwd=ROOT,check=True)
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m12-stage3-desktop');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
    report=dict(passed=False,stage='M12.3',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],owned_fixture=work.name,checks=[],profiles=[])
    try:
        live=ui.guest(work/'install',disk)
        with live as g:
            p=ui.Pointer(g)
            for action in (2,2,100,2,2,2):c.wizard(g,p,action)
            at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240)
            at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain()
            assert 'M7_DESKTOP_READY build='+meta['build_id'] in g.log();close_files(g,p)
            baseline=struct.unpack('<4Q',ui.memory(g,ui.symbol('stats',32,True)[0],32))
            report['icon_comparisons']=icon_pixels(g,p,'desktop-dark-wallpaper',1)
            c.open_settings(g,p);p.desktop(45002,True);p.close_app(3,True);p.drain();report['icon_comparisons']+=icon_pixels(g,p,'desktop-paper-wallpaper',0)
            c.open_settings(g,p);p.desktop(45000,True);p.close_app(3,True);p.drain()
            for _ in range(20):
                c.key(g,'tab')
                if c.flag(g,'control_active') and c.flag(g,'focused_action')==30000:break
            else:raise AssertionError('My files cannot receive Tab focus')
            c.key(g,'ret');assert count(g)==1;close_files(g,p)
            p.desktop(30000,True);assert count(g)==0 and c.flag(g,'desktop_selection11')==1
            c.key(g,'ret');assert count(g)==1;close_files(g,p)
            double(g,p,30001);assert count(g)==1;close_files(g,p)
            p.desktop(30003,True);assert count(g)==0 and c.flag(g,'desktop_selection11')==8
            c.shot(g,'selected-recycle-bin');c.key(g,'ret');assert count(g)==1
            assert '/System/Recycle/Owner' in rows(g);close_files(g,p)
            p.desktop(30000,True);before=rows(g);c.key(g,'delete');assert rows(g)==before and count(g)==0
            assert ui.memory(g,ui.symbol('shell_notice',96,True)[0],96).split(b'\0')[0].startswith(b'Right-click built-in icons')
            report['checks'].append('Real UEFI install/retained-ISO restart; one click selects, double-click opens Documents, Enter opens My files and Recycle Bin, protected launcher deletion leaves core objects unchanged')
            # Genuine marquee edges, with all four built-ins inside the rectangle.
            scale=c.flag(g,'scale73');p.move(20*scale//2,100*scale//2);p.drain();p.down(True);p.drain();p.move(154*scale//2,530*scale//2);p.drain()
            assert c.flag(g,'marquee11') and c.flag(g,'desktop_selection11')==15
            c.shot(g,'desktop-marquee');p.down(False);p.drain();c.key(g,'esc');assert count(g)==0
            right(g,p,600,300);c.shot(g,'background-menu');menu(g,p,26);text_dialog(g,'draft')
            path='/Users/Owner/Desktop/draft';action=desktop_item(g,p,path);p.desktop(action,True);assert selected(g,path) and count(g)==0
            c.key(g,'f2');text_dialog(g,'project');path='/Users/Owner/Desktop/project';assert path in rows(g) and '/Users/Owner/Desktop/draft' not in rows(g)
            action=desktop_item(g,p,path);p.desktop(action,True);c.key(g,'shift','f10');menu(g,p,43000)
            action=desktop_item(g,p,path);p.desktop(action,True);c.key(g,'shift','f10');menu(g,p,40010);job(g,p)
            link='/Users/Owner/Desktop/project.link';assert link in rows(g)
            action=desktop_item(g,p,link);p.desktop(action,True);assert count(g)==0
            report['icon_comparisons']+=icon_pixels(g,p,'desktop-shortcut',1,[(action,21,True)])
            c.key(g,'ret');assert count(g)==1;close_files(g,p)
            # Removing a reference cannot remove its target.
            action=desktop_item(g,p,link);p.desktop(action,True);c.key(g,'delete');job(g,p);assert path in rows(g) and link not in rows(g)
            action=desktop_item(g,p,path);p.desktop(action,True);c.key(g,'delete');job(g,p);assert path not in rows(g)
            p.desktop(30003,True);c.key(g,'ret');assert count(g)==1
            # Restore only the project folder, using its real metadata label.
            table=rows(g);folder=next(k for k,v in table.items() if k.startswith('/System/Recycle/Owner/') and v[1]==2)
            # Home/Down traverse the two real recycled entries; inspect selection identity.
            c.key(g,'home')
            for _ in range(4):
                raw=ui.memory(g,ui.symbol('selected11',installed=True)[0],8*128);idx=table[folder][0]
                if any(raw[slot*128+idx//8]&(1<<(idx%8)) for slot in range(8)):break
                c.key(g,'down')
            else:raise AssertionError('Recycled project selection')
            p.desktop(40005,True);job(g,p);assert path in rows(g);close_files(g,p)
            action=desktop_item(g,p,path);p.desktop(action,True);c.key(g,'shift','f10');menu(g,p,43000)
            report['checks'].append('Background and keyboard menus create/rename/pin a real folder; validated shortcut opens its target, recycling the shortcut preserves the target, and Recycle Bin restores the original folder')
            overflow_before=g.log().count('M73_TEXT_OVERFLOW')
            create(g,p,'a long desktop folder name for readability');c.shot(g,'long-name-selection')
            assert g.log().count('M73_TEXT_OVERFLOW')==overflow_before,'Expected caption shortening emitted a paragraph overflow'
            # Hover a different object, then compare the dirty update with a genuine full repaint.
            target=desktop_item(g,p,'/Users/Owner/Desktop/project');x,y=point(g,target);scale=c.flag(g,'scale73');p.move(x*scale//2,y*scale//2);p.drain();c.shot(g,'hovered-name-dirty')
            c.key(g,'esc');c.shot(g,'hovered-name-full')
            with Image.open(OUT/'hovered-name-dirty.png') as a,Image.open(OUT/'hovered-name-full.png') as b:
                assert a.crop((30*scale//2,82*scale//2,(1280-30)*scale//2,110*scale//2)).tobytes()==b.crop((30*scale//2,82*scale//2,(1280-30)*scale//2,110*scale//2)).tobytes()
            p.move(1200,80);p.drain()
            # Create enough real desktop folders through the wizard to overflow the ordinary grid.
            p.logical(600,300,True)
            for number in range(33):
                create(g,p,'d'+str(number).zfill(2));print('Created desktop overflow fixture',number,flush=True)
            assert c.flag(g,'desktop_page11')>0
            c.shot(g,'desktop-overflow');assert any(v[5]==40027 for v in controls(g))
            p.desktop(40027,True);assert c.flag(g,'desktop_page11')==0
            assert not any(v[5]==40027 for v in controls(g));assert any(v[5]==40028 for v in controls(g))
            p.desktop(40028,True);assert c.flag(g,'desktop_page11')==1
            assert not any(v[5]==40028 for v in controls(g))
            c.key(g,'home');assert c.flag(g,'desktop_item_focus11')==0
            c.key(g,'right');assert c.flag(g,'desktop_item_focus11')==4
            c.key(g,'left');assert c.flag(g,'desktop_item_focus11')==0
            c.key(g,'end');assert c.flag(g,'desktop_page11')==1
            c.shot(g,'keyboard-overflow-focus');c.idle(g)
            after=struct.unpack('<4Q',ui.memory(g,ui.symbol('stats',32,True)[0],32));assert after[0]==baseline[0] and after[3]==baseline[3]
            report['resources']=dict(before=baseline,after=after,retained_pages=after[0]-baseline[0])
            report['checks'].append('Thirty-three actual GUI-created folders overflow to reachable pages; unavailable Previous has no hit target; spatial keys skip the reserved gap, End reveals the selected item; no retained pages/new allocation failures and idle CPUs halt')
            # Hide every built-in reference independently, without removing its service.
            before_refs=rows(g)
            for reference in range(4):
                right(g,p,*point(g,30000+reference));menu(g,p,48000)
                assert not any(v[5]==30000+reference for v in controls(g))
            assert c.flag(g,'desktop_hidden12')==15 and c.flag(g,'desktop_selection11')==0
            c.key(g,'home');assert c.flag(g,'desktop_item_focus11')==4
            c.key(g,'left');assert c.flag(g,'desktop_item_focus11')==4
            c.open_settings(g,p);assert count(g)==1;p.close_app(3,True);p.drain()
            assert all(rows(g).get(path)==value for path,value in before_refs.items())
            right(g,p,1260,660);c.shot(g,'restore-desktop-references');menu(g,p,48001)
            assert c.flag(g,'desktop_hidden12')==0 and all(any(v[5]==30000+i for v in controls(g)) for i in range(4))
            right(g,p,*point(g,30002));menu(g,p,48000);assert c.flag(g,'desktop_hidden12')==4
            refs_stats=struct.unpack('<4Q',ui.memory(g,ui.symbol('stats',32,True)[0],32));assert refs_stats[0]==baseline[0] and refs_stats[3]==baseline[3]
            report['checks'].append('Each built-in reference can be hidden without deleting user/core entries; keyboard skips hidden cells, Settings remains reachable through Start, Restore defaults works and display-only changes retain no pages')
            (OUT/'install.log').write_text(g.log(),encoding='utf-8')
        assert '/Users/Owner/Desktop/project' in ui.s.directories(disk)
        pins=ui.s.s.document(disk,'/System/Settings/start11-Owner.bin');assert b'/Users/Owner/Desktop/project\0' in pins
        assert ui.s.s.document(disk,'/Users/Owner/Documents/Welcome.txt')==(ROOT/'distros/packages/m12-desktop-guide/content.txt').read_bytes()
        assert struct.unpack('<QII',ui.s.s.document(disk,'/System/Settings/desktop12-Owner.bin'))==(0x31504f544b534544,1,4)
        report['checks'].append('Independent stored directories, pinned-folder bytes and the matching bundled guide confirm persistence, not just compositor state')
        for number in (1,2):
            boot=ui.guest(work/f'disk-{number}',disk,media='installed',ready='M7_DESKTOP_READY');ui.s.normal_boot(boot,live.folder/'vars.fd')
            with boot as g:
                p=ui.Pointer(g);p.drain();assert '/Users/Owner/Desktop/project' in rows(g)
                assert c.flag(g,'desktop_hidden12')==4 and not any(v[5]==30002 for v in controls(g))
                close_files(g,p);right(g,p,1260,660);menu(g,p,48001)
                assert c.flag(g,'desktop_hidden12')==0 and any(v[5]==30002 for v in controls(g))
                if number==1:right(g,p,*point(g,30002));menu(g,p,48000)
                c.shot(g,f'disk-only-{number}');c.idle(g);(OUT/f'disk-{number}.log').write_text(g.log(),encoding='utf-8')
            report['checks'].append(f'Independent disk boot {number} uses ordinary firmware discovery and retains real desktop objects and hidden-reference settings, with working restore')
        for label,resolution,scale_action in [('150',(1920,1200),112),('4k',(3840,2160),113)]:
            with ui.guest(work/label,disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution) as g:
                p=ui.Pointer(g);p.drain();c.open_settings(g,p);p.desktop(scale_action,True);p.desktop(43,True);p.close_app(3,True);p.drain();p.close_app(1,True);p.drain()
                assert c.flag(g,'scale73')==(3 if label=='150' else 4)
                p.desktop(30003,True);assert count(g)==0;report['icon_comparisons']+=icon_pixels(g,p,'native-'+label,1);c.idle(g)
                report['profiles'].append(dict(physical=list(resolution),scale=c.flag(g,'scale73'),dark=c.dark(g)))
        report['checks'].append('Actual 150% and 3840x2160/200% dark desktop captures preserve whole-object selection and native vector icons')
        report['passed']=True
    except Exception:
        report['error']=ui.q.clean(traceback.format_exc());raise
    finally:
        report['idle_observations']=c.IDLE_OBSERVATIONS
        (OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
