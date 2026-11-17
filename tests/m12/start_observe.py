"""Stage-neutral Start/window observations through normal guest input."""
import ctypes,struct
import files_observe as f
c=f.c;ui=f.ui;ROOT=f.ROOT
class Pin(ctypes.Structure):
    _fields_=[('kind',ctypes.c_uint),('app',ctypes.c_uint),('path',ctypes.c_char*256),('label',ctypes.c_char*32)]
class Preferences(ctypes.Structure):
    _fields_=[('magic',ctypes.c_uint64)]+[(n,ctypes.c_uint) for n in ('version','categories','pins','tasks','view','tab','centered','reserved')]+[('names',(ctypes.c_char*32)*12),('order',ctypes.c_uint*12),('hidden',ctypes.c_uint*12),('assignment',ctypes.c_uint*20),('pinned',Pin*32),('task',ctypes.c_uint*8)]
def prefs(g):
    return Preferences.from_buffer_copy(ui.memory(g,ui.symbol('start_preferences11',ctypes.sizeof(Preferences),True)[0],ctypes.sizeof(Preferences)))
def results(g):
    count=c.flag(g,'start_result_count11');assert count<=52
    raw=ui.memory(g,ui.symbol('start_results11',installed=True)[0],count*8)
    return list(struct.iter_unpack('<II',raw))
def bounds(g):return tuple(int.from_bytes(c.field(g,'start_bounds11',i,4),'little',signed=True) for i in range(4))
def windows(g,kind=None):
    raw=ui.memory(g,ui.symbol('model',installed=True)[0],224)
    return sum(bool(raw[i*28+24]) and (kind is None or struct.unpack_from('<I',raw,i*28+20)[0]==kind) for i in range(8))
def close(g,p):
    slot=f.model(g)[0];rows=[r for r in f.controls(g) if r[5]==49002 and (r[4]&0xffffffff)==slot+1];assert len(rows)==1
    x,y,w,h,*_=rows[0];p.logical(x+w//2,y+h//2,True);p.drain()
def search(g,p,value):
    if not c.flag(g,'launcher'):p.desktop(0,True)
    if c.flag(g,'start_manage11'):p.desktop(42008,True)
    p.desktop(42004,True);c.key(g,'ctrl','a');c.type_text(g,value);p.drain()
def context(g,p):
    c.key(g,'shift','f10');assert c.flag(g,'context11')
def label(g,p,value):c.key(g,'ctrl','a');c.type_text(g,value);c.key(g,'ret');p.drain()
def launch(g,p,value,kind):
    search(g,p,value);assert results(g)==[(1,kind)],results(g);c.key(g,'ret');assert windows(g,kind)==1
