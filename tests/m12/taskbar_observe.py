"""Stage-neutral bounded taskbar/window observation; never selects historical media."""
import argparse,ctypes,hashlib,json,os,struct,traceback
import start_observe as s
c=s.c;f=s.f;ui=s.ui;ROOT=s.ROOT
def records(g):
    raw=ui.memory(g,ui.symbol('model',installed=True)[0],224);out=[]
    for slot in range(8):
        x,y,w,h,generation,app,live,minimum=struct.unpack_from('<4iII2B',raw,slot*28)
        if live:out.append(dict(slot=slot,token=generation<<32|slot+1,app=app,minimized=bool(minimum)))
    return out
def group_controls(g):
    return [r for r in f.controls(g) if r[4]==0 and 43100<r[5]<43120]
def group_order(g):
    rows=group_controls(g);assert len({r[5] for r in rows})==len(rows)
    return [r[5]-43100 for r in sorted(rows,key=lambda r:r[0])]
def menu_rows(g):
    n=c.flag(g,'file_menu_count11');assert n<=12;raw=ui.memory(g,ui.symbol('file_menu_items11',installed=True)[0],n*16);out=[]
    for i in range(n):
        pointer,command,enabled=struct.unpack_from('<QII',raw,i*16)
        label=ui.memory(g,pointer,96).split(b'\0')[0].decode()
        out.append(dict(label=label,command=command,enabled=enabled))
    return out
def right_group(g,p,app):
    x,y,w,h,*_=c.control(g,43100+app);f.right(g,p,x+w//2,y+h//2)
def focus(g,p,window):
    slot=window['slot'];current=next(w for w in records(g) if w['slot']==slot)
    assert current['token']==window['token']
    if f.model(g)[0]==slot and not current['minimized'] and not c.flag(g,'launcher') and not c.flag(g,'desktop_focus11'):return
    app=window['app'];action=43100+app
    if not any(r[5]==action for r in group_controls(g)):
        p.desktop(43001,True)
        for _ in range(3):
            if any(r['command']==43220+app for r in menu_rows(g)):break
            f.menu(g,p,43200)
        f.menu(g,p,43220+app)
    else:p.desktop(action,True)
    if sum(w['app']==app for w in records(g))>1:f.menu(g,p,43020+slot)
    assert f.model(g)[0]==slot and not next(w for w in records(g) if w['slot']==slot)['minimized']
def launch(g,p,name,kind):
    before=s.windows(g,kind);s.search(g,p,name);rows=s.results(g);matches=[i for i,row in enumerate(rows) if row==(1,kind)];assert len(matches)==1,rows
    if len(rows)==1:c.key(g,'ret')
    else:p.desktop(42200+matches[0],True)
    assert s.windows(g,kind)==before+1
    return next(w for w in records(g) if w['slot']==f.model(g)[0])
def app_view(g):
    address,size=ui.symbol('apps',installed=True);slot=f.model(g)[0]
    from focus_ownership import View
    return View.from_buffer_copy(ui.memory(g,address+slot*(size//8),ctypes.sizeof(View)))
def closing(g):
    address,size=ui.symbol('apps',installed=True);slot=f.model(g)[0]
    from focus_ownership import View
    return int.from_bytes(ui.memory(g,address+slot*(size//8)+ctypes.sizeof(View)+352,4),'little')
def pin(g,p,name,app):
    if app in s.prefs(g).task[:s.prefs(g).tasks]:return
    s.search(g,p,name);c.key(g,'shift','f10');f.menu(g,p,42700+app);c.key(g,'esc');c.key(g,'esc')
    assert app in s.prefs(g).task[:s.prefs(g).tasks]
def close_all(g,p):
    while records(g):
        target=records(g)[-1];focus(g,p,target);s.close(g,p)
        if any(w['token']==target['token'] for w in records(g)):
            assert closing(g);p.desktop(60,True)
    p.drain()
