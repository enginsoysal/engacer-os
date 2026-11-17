"""Stage-neutral read-only Settings observations and ordinary-input helpers."""
import struct,time
import tray_observe as q
c=q.c;f=q.f;s=q.s;t=q.t;ui=q.ui;ROOT=q.ROOT
APPEARANCE='/System/Settings/appearance11-Owner.bin'

def preview(g):return tuple(int.from_bytes(c.field(g,'settings_preview13',i,8 if i==0 else 4),'little') for i in range(6))
def appearance(g):return struct.unpack('<8I',ui.memory(g,ui.symbol('appearance11',352,True)[0],32))
def colors(g):return struct.unpack_from('<II',ui.memory(g,ui.symbol('preferences',24,True)[0],24),8)
def click_interval(g):return struct.unpack_from('<I',ui.memory(g,ui.symbol('interaction11',installed=True)[0]+72,4))[0]
def page(g):return ui.memory(g,ui.symbol('settings_page13',8,True)[0],8)[f.model(g)[0]]
def record(disk):return ui.s.s.document(disk,APPEARANCE)

def close(g,p):
    target=next(w for w in t.records(g) if w['slot']==f.model(g)[0]);deadline=time.monotonic()+15
    while True:
        rows=[r for r in f.controls(g) if r[5]==49002 and r[4]==target['token']]
        if len(rows)==1:break
        if time.monotonic()>deadline:raise AssertionError(('Caption not painted for owner',target))
        time.sleep(.05)
    x,y,w,h,*_=rows[0];p.logical(x+w//2,y+h//2,True);p.drain()

def software_change(g,p,kind):
    for _ in range(8):
        if f.has(g,10300+kind):break
        assert f.has(g,10002);p.desktop(10002,True)
    else:raise AssertionError(('Optional app not reachable',kind))
    p.desktop(10300+kind,True)
    if f.has(g,10004):p.desktop(10004,True)

def save(g,p):
    p.desktop(47,True);assert not preview(g)[0] and 'saved' in f.app(g)['notice'].lower()

def appearance_tab(g,p):
    if page(g)!=0:p.desktop(59000,True)
