"""Stage-neutral accessibility observations and ordinary keyboard actions."""
import struct,time
import setup_observe as z
c=z.c;f=z.f;s=z.s;t=z.t;h=z.h;ui=z.ui;ROOT=z.ROOT

def scalar(g,name,size=4):
 address,actual=ui.symbol(name,installed=True);return int.from_bytes(ui.memory(g,address,min(size,actual)),'little')
def focus(g):return scalar(g,'control_active'),scalar(g,'focused_control_window',8),scalar(g,'focused_action')
def semantic(g,name='access_focus16'):
 raw=ui.memory(g,ui.symbol(name,96,True)[0],96);owner,action,role=struct.unpack_from('<QII',raw)
 return dict(owner=owner,action=action,role=role,label=raw[16:96].split(b'\0')[0].decode())
def key(g,*names):z.key(g,*names)
def tab_to(g,action,owner=None):
 if owner is None:owner=next(w['token'] for w in t.records(g) if w['slot']==f.model(g)[0])
 for _ in range(128):
  if focus(g)==(1,owner,action):return
  key(g,'tab')
 raise AssertionError(('Keyboard focus not reachable',owner,action,focus(g)))
def activate(g,action,owner=None,space=False):tab_to(g,action,owner);key(g,'spc' if space else 'ret')
def launch(g,title,kind):
 before={w['token'] for w in t.records(g)};key(g,'ctrl','esc');c.type_text(g,title);key(g,'ret')
 rows=[w for w in t.records(g) if w['app']==kind and w['token'] not in before];assert len(rows)==1,(title,rows)
 return rows[0]
def close(g):key(g,'alt','f4')
def keyboard_install(g,out):
 p=ui.Pointer(g);p.drain();before=f.sha_file(g.disk) if hasattr(g,'disk') else None
 key(g,'ret');assert z.flag(g,'keyboard_page11')==1
 key(g,'ret');assert z.flag(g,'step')==1
 key(g,'ret');assert z.flag(g,'chosen')==0
 for _ in range(3):key(g,'tab')
 key(g,'ret');assert z.flag(g,'step')==2
 key(g,'ret');assert z.flag(g,'step')==3
 key(g,'ret');assert z.flag(g,'step')==4
 z.shot(g,out,'keyboard-install-review');at=len(g.log());key(g,'ret');g.wait('M6_INSTALL_PASS',at,240);at=len(g.log());key(g,'ret');g.wait('M7_DESKTOP_READY',at,180);ui.Pointer(g).drain()
 return p
