"""Stage-neutral ordinary-input Files helpers and read-only observations."""
import ctypes,json,struct,time,hashlib
import components as c
from focus_ownership import View
ui=c.ui;ROOT=ui.ROOT

def model(g):
    base=ui.symbol('model',installed=True)[0];slot=int.from_bytes(ui.memory(g,base+236,4),'little');assert slot<8
    return slot,struct.unpack('<4i',ui.memory(g,base+slot*28,16))
def app(g,slot=None):
    if slot is None:slot=model(g)[0]
    address,size=ui.symbol('apps',installed=True);raw=ui.memory(g,address+slot*(size//8)+ctypes.sizeof(View),1164)
    values=struct.unpack_from('<6I',raw,628)
    return dict(slot=slot,path=raw[:256].split(b'\0')[0].decode(),notice=raw[256:352].split(b'\0')[0].decode(),offset=struct.unpack_from('<I',raw,356)[0],mode=values[1],disk=values[2],part=values[3],context=values[4],selected=values[5],usb_path=raw[652:908].split(b'\0')[0].decode())
def controls(g):
    count=ui.integer(g,'control_count',True);raw=ui.memory(g,ui.symbol('controls',65536,True)[0],count*32)
    return [struct.unpack_from('<iiiiQI',raw,i*32) for i in range(count)]
def current_controls(g):
    slot=model(g)[0];return [r for r in controls(g) if r[4]&0xffffffff==slot+1]
def has(g,action):return any(r[5]==action for r in current_controls(g))
def history(g):
    raw=ui.memory(g,ui.symbol('navigation',8*2216,True)[0]+model(g)[0]*2216,2216);count,position=struct.unpack_from('<II',raw,2208)
    assert count<=8 and position<count
    return dict(count=count,position=position,locations=[dict(zip(('path','provider','disk','context','part','offset'),(path.split(b'\0')[0].decode(),*values))) for path,*values in struct.iter_unpack('<256s5I',raw[:count*276])])
def address(g):
    address,size=ui.symbol('file_windows11',installed=True);stride=size//8;assert stride==296
    raw=ui.memory(g,address+model(g)[0]*stride,stride)
    return raw[16:288].split(b'\0')[0].decode(),struct.unpack_from('<I',raw,12)[0]
def type_text(g,text):
    for ch in text:
        if ch==':':c.key(g,'shift','semicolon')
        else:c.type_text(g,ch)
def visit(g,p,text):
    p.desktop(40015,True);c.key(g,'ctrl','a');type_text(g,text);c.key(g,'ret');p.drain()
def usb_rows(g):
    raw=ui.memory(g,ui.symbol('usb_rows10',6*264,True)[0],6*264)
    return [name.split(b'\0')[0].decode() for name,kind,size in struct.iter_unpack('<256sII',raw)]
def row(g,name):
    values=usb_rows(g);index=values.index(name);assert index<6 and has(g,21200+index),(name,values);return 21200+index
def drive(g):return next(r[5] for r in current_controls(g) if 21100<=r[5]<21116)
def double(g,p,action):
    x,y,w,h,_,_=c.control(g,action);scale=c.flag(g,'scale73');p.move((x+w//2)*scale//2,(y+h//2)*scale//2);p.drain();start=time.monotonic()
    for down in (True,False,True,False):g.qmp('input-send-event',{'events':[{'type':'btn','data':{'down':down,'button':'left'}}]});time.sleep(.06)
    assert time.monotonic()-start<.5,'Host did not deliver the double-click in time';p.drain()
def stats(g):return struct.unpack('<4Q',ui.memory(g,ui.symbol('stats',32,True)[0],32))
def same_pages(a,b):assert a[0]==b[0] and a[3]==b[3],(a,b)
def attach(g,p,node,identity):
    at=len(g.log());g.qmp('device_add',{'driver':'usb-storage','id':identity,'bus':'xhci.0','drive':node});g.wait('M10_USB_WRITABLE',at,90);p.drain()
def wait_selected_clear(g,p):
    deadline=time.monotonic()+30
    while app(g)['selected']:
        if time.monotonic()>deadline:raise TimeoutError('Removed drive selection was retained')
        time.sleep(.05);p.drain()
def sha_file(path):
    digest=hashlib.sha256()
    with path.open('rb') as stream:
        for data in iter(lambda:stream.read(1024**2),b''):digest.update(data)
    return digest.hexdigest()

def entries(g):
    raw=ui.memory(g,ui.symbol('volume',0xd3040,True)[0]+64,1024*280);result={}
    for index in range(1024):
        value=raw[index*280:(index+1)*280];first,size,crc,kind=struct.unpack_from('<QQII',value,256)
        if kind:result[value[:256].split(b'\0')[0].decode()]=dict(index=index,kind=kind,size=size,crc=crc)
    return result

def listing(g):
    address,size=ui.symbol('file_lists11',installed=True);stride=size//9;assert stride==2328
    raw=ui.memory(g,address+model(g)[0]*stride,stride);count=struct.unpack_from('<I',raw,264)[0]
    order=struct.unpack_from('<1024H',raw,276)[:count];table={e['index']:(path,e) for path,e in entries(g).items()}
    return [dict(path=table[i][0],**table[i][1]) for i in order]

def names(g):return [e['path'].rsplit('/',1)[-1] for e in listing(g)]

def view(g):
    address,size=ui.symbol('file_windows11',installed=True);return struct.unpack('<3I',ui.memory(g,address+model(g)[0]*(size//8),12))

def item(g,p,name):
    values=names(g);row=values.index(name);action=1000+row
    for _ in range(128):
        if has(g,action):return action
        command=98 if row<app(g)['offset'] else 99
        assert has(g,command),(name,values,app(g));p.desktop(command,True)
    raise AssertionError('Item did not become visible')

def selected(g,slot=None):
    if slot is None:slot=model(g)[0]
    raw=ui.memory(g,ui.symbol('selected11',installed=True)[0]+slot*128,128)
    return sorted(path for path,e in entries(g).items() if raw[e['index']//8]&(1<<(e['index']%8)))

def create(g,p,name,folder=False):
    p.desktop(26 if folder else 40018,True);assert c.flag(g,'file_dialog_state11') in (7,8)
    c.key(g,'ctrl','a');c.type_text(g,name);c.key(g,'ret');assert not c.flag(g,'file_dialog_state11')
    assert app(g)['path']+'/'+name in entries(g)

def move(g,p,x,y):
    scale=c.flag(g,'scale73');p.move(x*scale//2,y*scale//2);p.drain()

def right(g,p,x,y):
    move(g,p,x,y)
    for down in (True,False):g.qmp('input-send-event',{'events':[{'type':'btn','data':{'down':down,'button':'right'}}]});p.drain()
    assert c.flag(g,'context11')

def menu(g,p,command):
    n=c.flag(g,'file_menu_count11');raw=ui.memory(g,ui.symbol('file_menu_items11',installed=True)[0],n*16)
    found=[i for i in range(n) if struct.unpack_from('<II',raw,i*16+8)==(command,1)];assert len(found)==1,(command,n)
    p.desktop(32000+found[0],True)

def resize(g,p,width,height):
    _,(x,y,w,h)=model(g);move(g,p,x+w-2,y+h-2);p.down(True);p.drain();move(g,p,x+width-2,y+height-2);p.down(False);p.drain()
    assert model(g)[1][2:]==(width,height),model(g)
