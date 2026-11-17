"""Stage-neutral tray observations and ordinary-input helpers."""
import ctypes,struct
import taskbar_observe as t
c=t.c;f=t.f;s=t.s;ui=t.ui;ROOT=t.ROOT

def audio(g):return struct.unpack_from('<5I',ui.memory(g,ui.symbol('info74',64,True)[0],64))
def network(g):return struct.unpack_from('<6I',ui.memory(g,ui.symbol('configuration',32,True)[0],32))
def notice(g):return ui.memory(g,ui.symbol('tray_notice12',160,True)[0],160).split(b'\0')[0].decode()
def has(g,action):return any(r[5]==action for r in f.controls(g))
def open_quick(g):c.key(g,'meta_l','a');assert c.flag(g,'tray_open12')==1
def date(g):return tuple(c.flag(g,'tray_'+field+'12') for field in ('year','month','day'))
def hardware_view(g):
    from focus_ownership import View
    address,size=ui.symbol('apps',installed=True);return int.from_bytes(ui.memory(g,address+f.model(g)[0]*(size//8)+ctypes.sizeof(View)+628,4),'little')
def disks(g):
    address,size=ui.symbol('disks',16*40,True);assert size==16*40
    raw=ui.memory(g,address,size)
    return [(i,struct.unpack_from('<6I Q 2I',raw,i*40)) for i in range(16) if struct.unpack_from('<I',raw,i*40)[0]]

def install(g):
    p=ui.Pointer(g)
    for action in (2,2,100,2,2,2):c.wizard(g,p,action)
    at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180)
    p=ui.Pointer(g);p.drain();s.close(g,p);return p

def basic(g,p,out,checks):
    before=f.stats(g);assert s.windows(g)==0 and network(g)[0]==0
    open_quick(g);assert not has(g,58013) and has(g,58014) and has(g,58010);assert audio(g)[0]==0
    c.shot(g,'quick-settings');c.idle(g);initial=audio(g)[4];p.desktop(58012,True);assert audio(g)[4]==0;p.desktop(58012,True);assert audio(g)[4]==initial;p.desktop(58010,True);saved=initial-10 if initial>=10 else 0;assert audio(g)[4]==saved
    c.shot(g,'playback-level-saved');assert 'saved' in notice(g)
    p.desktop(0,True);assert not c.flag(g,'tray_open12') and c.flag(g,'launcher');c.key(g,'esc');assert s.windows(g)==0
    checks.append('Real install/retained-ISO startup; Windows+A opens a slot-free provider-backed panel, unsupported network retry is disabled, PCM level/mute updates the actual provider, and one visible Start click switches menus')
    p.desktop(58006,True);assert c.flag(g,'tray_open12')==3;original=date(g);assert 2000<=original[0]<=2099 and 1<=original[1]<=12 and 1<=original[2]<=31
    p.desktop(58020,True);assert date(g)[:2]==((original[0],original[1]-1) if original[1]>1 else (original[0]-1,12));p.desktop(58021,True);assert date(g)[:2]==original[:2];p.desktop(58022,True);assert date(g)==original
    c.shot(g,'calendar');p.desktop(58023,True);assert not c.flag(g,'tray_open12') and s.windows(g,9)==1;assert f.app(g)['path'].endswith('/%04d-%02d-%02d.txt'%original);c.shot(g,'calendar-app-date');s.close(g,p)
    checks.append('Actual UTC calendar values and bounded month navigation drive an explicit Calendar launch for the selected real date; the panel itself does not create an application window')
    open_quick(g);p.desktop(58014,True);assert s.windows(g,3)==1 and hardware_view(g)==1 and not c.flag(g,'tray_open12');c.shot(g,'actual-devices');s.close(g,p)
    open_quick(g);p.desktop(58002,True);assert c.flag(g,'tray_open12')==2 and not any(58200<=r[5]<58236 for r in f.controls(g));c.shot(g,'no-usb');c.key(g,'tab');assert c.flag(g,'control_active') and 58000<=c.flag(g,'focused_action')<58300;c.key(g,'esc');assert not c.flag(g,'tray_open12') and s.windows(g)==0
    f.same_pages(before,f.stats(g));c.idle(g)
    checks.append('Devices opens the required real inventory; USB excludes the system SATA disk in no-device state, keyboard focus and Escape work, and completed panel/app journeys retain zero managed pages and halt at idle')
    return before,saved
