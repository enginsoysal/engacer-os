"""Real M12 shared controls, installed startup, scale and idle/resource checks."""
import hashlib
import json
import os
import re
import struct
import time
import traceback
from PIL import Image
import ui

ROOT=ui.ROOT
OUT=ROOT/'build/m12/stage1/components'
OUT.mkdir(parents=True,exist_ok=True)
os.environ['ENGACER11_DISMISS_GUIDE']='1'
IDLE_OBSERVATIONS=[]

def flag(g,name,size=None):
    address,length=ui.symbol(name,size,True)
    return int.from_bytes(ui.memory(g,address,min(length,4)),'little')

def field(g,name,index,size):
    # LLVM may split private structs into scalar symbols; read, never modify them.
    address,_=ui.symbol(re.escape(name)+r'\.'+str(index),size,True)
    return ui.memory(g,address,size)

def key(g,*names):
    g.qmp('send-key',{'keys':[{'type':'qcode','data':n} for n in names],'hold-time':40})
    time.sleep(.16)
    ui.Pointer(g).drain()

def type_text(g,value):
    for c in value:
        if c.isupper():key(g,'shift',c.lower())
        else:key(g,{' ':'spc','/':'slash','.':'dot','-':'minus'}.get(c,c))

def control(g,action):
    count=ui.integer(g,'control_count',True)
    raw=ui.memory(g,ui.symbol('controls',65536,True)[0],count*32)
    found=[struct.unpack_from('<iiiiQI',raw,i*32) for i in range(count) if struct.unpack_from('<I',raw,i*32+24)[0]==action]
    assert found,(action,count)
    return found[-1]

def shot(g,name):
    ui.Pointer(g).drain()
    g.qmp('stop')
    try:ui.raw_shot(g,OUT,name,True)
    finally:g.qmp('cont')

def pixel(g,x,y):
    boot=ui.physical_boot(g,True)
    base=struct.unpack_from('<Q',boot,80)[0]
    stride,fmt=struct.unpack_from('<II',boot,136)
    scale=flag(g,'scale73')
    raw=int.from_bytes(ui.memory(g,base+y*scale//2*stride+x*scale//2*4,4),'little')
    return raw&0xffffff if fmt==2 else (raw&255)<<16|(raw&0xff00)|(raw>>16&255)

def wizard(g,p,action):
    count=ui.integer(g,'controls')
    raw=ui.memory(g,ui.symbol('buttons',480)[0],count*20)
    found=[struct.unpack_from('<5I',raw,i*20) for i in range(count) if struct.unpack_from('<I',raw,i*20+16)[0]==action]
    assert len(found)==1,(action,found)
    x,y,w,h,_=found[0]
    start=len(g.log())
    p.logical(x+w//2,y+h//2)
    if action not in (3,30,84):g.wait('M73_VIEW step=',start)
    return start

def open_settings(g,p):
    if not flag(g,'launcher'):p.desktop(0,True)
    p.desktop(42004,True)
    key(g,'ctrl','a')
    type_text(g,'settings')
    shot(g,'search-field')
    x,y,_,_,_,_=control(g,42200);scale=flag(g,'scale73')
    with Image.open(OUT/'search-field.png') as image:
        tile=image.convert('RGB').crop(((x+11)*scale//2,(y+11)*scale//2,(x+35)*scale//2,(y+35)*scale//2))
        assert any(min(pixel)>240 for pixel in tile.getdata()),'Accent badge foreground is not readable on the dark custom accent'
    key(g,'ret')
    p.drain()

def dark(g):
    return struct.unpack_from('<I',ui.memory(g,ui.symbol('preferences',24,True)[0],24),12)[0]

def idle(g):
    observations=[]
    # Startup/status/minute-clock events may finish here. Retain them and require
    # an actual stable idle window; sustained repaint still fails all three tries.
    for attempt in range(3):
        ui.Pointer(g).drain()
        before=int.from_bytes(ui.memory(g,ui.symbol('paints',8,True)[0],8),'little')
        time.sleep(.6)
        after=int.from_bytes(ui.memory(g,ui.symbol('paints',8,True)[0],8),'little')
        observations.append(dict(attempt=attempt+1,paints_before=before,paints_after=after))
        if before!=after:continue
        ui.Pointer(g).drain()
        if g.qmp('human-monitor-command',{'command-line':'info registers -a'}).count('HLT=1')==len(g.qmp('query-cpus-fast')):
            IDLE_OBSERVATIONS.append(observations);return
    raise AssertionError(('No stable idle window',observations))

def file_first(g):
    count=ui.integer(g,'control_count',True)
    raw=ui.memory(g,ui.symbol('controls',65536,True)[0],count*32)
    values=[struct.unpack_from('<I',raw,i*32+24)[0] for i in range(count)]
    return min(v-1000 for v in values if 1000<=v<2024)

def scroll_test(g,p):
    p.close_app(3,True);p.drain()
    p.desktop(40015,True);key(g,'ctrl','a');type_text(g,'/Applications');key(g,'ret')
    x,y,w,h,_,_=control(g,47000)
    assert file_first(g)==0
    # Grab near the top of the actual thumb, then move to the track end.
    scale=flag(g,'scale73')
    p.move((x+w//2)*scale//2,(y+10)*scale//2);p.drain();p.down(True);p.drain()
    assert field(g,'scroll_capture12',0,8)!=bytes(8)
    p.move((x+w//2)*scale//2,(y+h-2)*scale//2);p.drain()
    assert file_first(g)>0;shot(g,'scroll-drag')
    key(g,'esc');p.down(False);p.drain();assert file_first(g)==0
    p.move((x+w//2)*scale//2,(y+10)*scale//2);p.drain();p.down(True);p.drain()
    p.move((x+w//2)*scale//2,(y+h-2)*scale//2);p.drain()
    key(g,'ctrl','esc');p.down(False);p.drain()
    assert file_first(g)==0 and not flag(g,'launcher')
    # Track paging and keyboard Home/End change the real visible row identities.
    p.logical(x+w//2,y+h-2,True);p.drain();assert file_first(g)>0
    key(g,'home');assert file_first(g)==0
    key(g,'end');assert file_first(g)>0
    key(g,'home');assert file_first(g)==0
    shot(g,'scroll-keyboard-home')

def main():
    meta=json.loads(ui.manifest_path12().read_text())
    report={'passed':False,'stage':'M12.1','build_id':meta['build_id'],'iso_sha256':hashlib.sha256(ui.iso_path12().read_bytes()).hexdigest(),'checks':[]}
    work=ui.q.new_work('m12-stage1-components')
    report['owned_fixture']=work.name
    disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
    try:
        live=ui.guest(work/'install',disk,resolution=(1280,800))
        with live as g:
            p=ui.Pointer(g)
            counter,size=ui.symbol('full_frames75')
            setup_full_before=int.from_bytes(ui.memory(g,counter,size),'little')
            for action in (2,2,100,2,2,2):wizard(g,p,action)
            setup_full_after=int.from_bytes(ui.memory(g,counter,size),'little')
            assert setup_full_after==setup_full_before
            report['setup_full_paints_before_install']=[setup_full_before,setup_full_after]
            report['checks'].append('Ordinary Next/disk-selection steps repaint content without adding full-frame clears')
            start=wizard(g,p,2);g.wait('M6_INSTALL_PASS',start,240)
            start=wizard(g,p,84);g.wait('M7_DESKTOP_READY',start,180)
            p=ui.Pointer(g);p.drain();shot(g,'installed-desktop')
            report['checks'].append('Real graphical installation and retained-ISO reset reach the installed desktop')
            assert pixel(g,58,326)==0xffffff
            p.move(15,400);p.drain();p.down(True);p.drain();p.move(90,440);p.drain()
            assert pixel(g,20,400)==0xffffff
            shot(g,'desktop-marquee-contrast');key(g,'esc');p.down(False);p.drain()
            report['checks'].append('Desktop accent glyph and selection marquee have readable foregrounds on the actual dark wallpaper')
            p.desktop(0,True)
            sx,sy,sw,sh=struct.unpack('<4i',b''.join(field(g,'start_bounds11',i,4) for i in range(4)))
            count=ui.integer(g,'control_count',True)
            rows=ui.memory(g,ui.symbol('controls',65536,True)[0],count*32)
            assert all(struct.unpack_from('<I',rows,i*32+24)[0]!=42005 for i in range(count))
            assert pixel(g,sx+28,sy+sh-30)==0xf8fafc
            p.logical(sx+40,sy+sh-30,True);p.drain()
            assert flag(g,'start_page11')==0 and flag(g,'launcher')
            shot(g,'disabled-page-control')
            report['checks'].append('Disabled Start pagination is visibly distinct, excluded from activation targets and cannot change the page')
            open_settings(g,p)
            p.move(1200,80);p.drain()
            assert dark(g)==0
            x,y,w,h,token,_=control(g,43)
            assert pixel(g,x+8,y+18)==0xffffff
            scale=flag(g,'scale73');p.move((x+w//2)*scale//2,(y+h//2)*scale//2);p.drain()
            assert pixel(g,x+8,y+18)==0xe0eeed,hex(pixel(g,x+8,y+18))
            shot(g,'light-hover')
            p.down(True);p.drain()
            assert pixel(g,x+8,y+18)==0xc1dedb,hex(pixel(g,x+8,y+18))
            shot(g,'light-pressed')
            p.move(1200,80);p.drain();p.down(False);p.drain()
            assert dark(g)==0
            report['checks'].append('Actual framebuffer distinguishes normal, hover and press; release outside preserves the previous theme')
            key(g,'tab')
            assert flag(g,'control_active')
            command=flag(g,'focused_action');fx,fy,fw,fh,_,_=control(g,command)
            assert pixel(g,fx+1,fy+fh//2)==0x17212f
            shot(g,'keyboard-focus')
            report['checks'].append('Keyboard focus has its own contrast border without activating the control')
            p.desktop(43,True);assert dark(g)==1
            p.move(1200,80);p.drain();x,y,w,h,_,_=control(g,44)
            assert pixel(g,x+8,y+18)==0x202732
            p.move(x+w//2,y+h//2);p.drain()
            assert pixel(g,x+8,y+18)==0x1d3139
            shot(g,'dark-hover')
            p.desktop(47,True)
            baseline=struct.unpack('<4Q',ui.memory(g,ui.symbol('stats',32,True)[0],32))
            for _ in range(4):p.desktop(44,True);p.desktop(43,True)
            after=struct.unpack('<4Q',ui.memory(g,ui.symbol('stats',32,True)[0],32))
            assert after[0]==baseline[0] and after[3]==baseline[3]
            idle(g)
            report['managed_current_bytes']=after[0]*4096;report['managed_peak_bytes']=after[1]*4096
            report['retained_page_delta']=after[0]-baseline[0]
            report['checks'].append('Light/dark switches retain no managed pages or new allocation failures; idle paints stop and CPUs halt')
            p.desktop(47,True)
            scroll_test(g,p)
            report['checks'].append('Native Files scrollbar drags actual row identities; Escape and Ctrl+Escape restore its start without opening Start; track paging and keyboard Home/End work')
            import focus_ownership
            focus_ownership.journey(g,p)
            report['checks'].append('A previous scrollbar focus cannot steal Home/End from the USB provider or the native address field')
            (OUT/'install.log').write_text(g.log(),encoding='utf-8')
        welcome=ui.s.s.document(disk,'/Users/Owner/Documents/Welcome.txt')
        assert welcome==(ROOT/'distros/packages/m12-desktop-guide/content.txt').read_bytes()
        report['checks'].append('Independent metadata/CRC and file-byte inspection confirms the matching M12 welcome guide was installed')
        for number in (1,2):
            boot=ui.guest(work/f'independent-{number}',disk,media='installed',ready='M7_DESKTOP_READY')
            ui.s.normal_boot(boot,live.folder/'vars.fd')
            with boot as g:
                assert 'M7_DESKTOP_READY build='+meta['build_id'] in g.log()
                p=ui.Pointer(g);p.drain();assert dark(g)==1;idle(g)
                shot(g,f'disk-only-{number}')
                (OUT/f'disk-only-{number}.log').write_text(g.log(),encoding='utf-8')
            report['checks'].append(f'Independent disk boot {number} retains saved appearance and the same firmware variables without forced boot order')
        for name,resolution in [('150',(1920,1200)),('4k',(3840,2160))]:
            with ui.guest(work/name,disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution) as g:
                assert 'M7_DESKTOP_READY build='+meta['build_id'] in g.log()
                p=ui.Pointer(g);p.drain();open_settings(g,p)
                p.desktop(112 if name=='150' else 113,True)
                assert flag(g,'scale73')==(3 if name=='150' else 4)
                shot(g,'native-'+name);idle(g)
                stats=struct.unpack('<4Q',ui.memory(g,ui.symbol('stats',32,True)[0],32))
                report.setdefault('display_profiles',[]).append(dict(physical=list(resolution),scale=flag(g,'scale73'),managed_current_bytes=stats[0]*4096,managed_peak_bytes=stats[1]*4096,allocation_failures=stats[3],idle_cpus_halted=True,idle_paints_unchanged=True))
                report['checks'].append(f'Actual {resolution[0]}x{resolution[1]} framebuffer with {name} scale uses native shared typography and idle halt')
        report['passed']=True
    except Exception as error:
        report['error']=str(error)
        (OUT/'failure.txt').write_text(traceback.format_exc().replace(str(ROOT),'<project-root>'),encoding='utf-8')
        raise
    finally:
        report['idle_observations']=IDLE_OBSERVATIONS
        (OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
