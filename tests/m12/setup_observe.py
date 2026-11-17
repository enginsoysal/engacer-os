"""Stage-neutral setup observations; all choices use ordinary guest controls."""
import struct,time
import settings_observe as h
import os
os.environ["ENGACER11_DISMISS_GUIDE"]="0"
c=h.c;f=h.f;s=h.s;t=h.t;ui=h.ui;ROOT=h.ROOT

def flag(g,name,installed=False):
    address,size=ui.symbol(name,4 if name=='controls' else None,installed=installed)
    return int.from_bytes(ui.memory(g,address,min(size,4)),'little')
def options(g):return struct.unpack('<6I',ui.memory(g,ui.symbol('setup11',24)[0],24))
def account(g):return ui.memory(g,ui.symbol('preferences',40)[0],32).split(b'\0')[0].decode()
def controls(g):
    count=flag(g,'controls');assert count<=24
    return list(struct.iter_unpack('<5I',ui.memory(g,ui.symbol('buttons',480)[0],count*20)))
def has(g,command):return any(row[4]==command for row in controls(g))
def wizard(g,p,command):return c.wizard(g,p,command)
def go(g,p,*commands):
    for command in commands:wizard(g,p,command)
def key(g,*names):
    g.qmp('send-key',{'keys':[{'type':'qcode','data':name} for name in names],'hold-time':40});time.sleep(.16);ui.Pointer(g).drain()
def text(g,value):
    for ch in value:
        names=['shift',ch.lower()] if ch.isupper() else [{' ':'spc','-':'minus'}.get(ch,ch)]
        key(g,*names)
def shot(g,out,name,installed=False):
    if not installed:
        left,top,width,height=(flag(g,name) for name in ('left','top','width','height'))
        rows=controls(g)
        for x,y,w,h,command in rows:assert w>=36 and h>=36 and left<=x and top<=y and x+w<=left+width and y+h<=top+height,(name,command,(x,y,w,h),(left,top,width,height))
        for i,a in enumerate(rows):
            for b in rows[i+1:]:assert not (a[0]<b[0]+b[2] and b[0]<a[0]+a[2] and a[1]<b[1]+b[3] and b[1]<a[1]+a[3]),('Overlapping setup hit targets',name,a,b)
    g.qmp('stop')
    try:ui.raw_shot(g,out,name,installed)
    finally:g.qmp('cont')
