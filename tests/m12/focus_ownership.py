"""A scrollbar must not steal keyboard input from a different Files provider."""
import argparse
import ctypes
import json
import os
from pathlib import Path
import struct
import components as c

ui=c.ui;ROOT=ui.ROOT
class View(ctypes.Structure):
    _fields_=[('text',ctypes.c_char*8192),('length',ctypes.c_uint32),('cursor',ctypes.c_uint32),('dirty',ctypes.c_uint32),('error',ctypes.c_uint32),('number',ctypes.c_int64),('operand',ctypes.c_int64),('operation',ctypes.c_uint32),('entered',ctypes.c_uint32)]

def app_offset(g):
    model=ui.symbol('model',installed=True)[0]
    slot=int.from_bytes(ui.memory(g,model+236,4),'little')
    address,size=ui.symbol('apps',installed=True)
    assert size%8==0 and slot<8
    address+=slot*(size//8)+ctypes.sizeof(View)+256+96+4
    return int.from_bytes(ui.memory(g,address,4),'little')

def journey(g,p):
    p.desktop(40015,True);c.key(g,'ctrl','a');c.type_text(g,'/Applications');c.key(g,'ret')
    x,y,w,h,_,_=c.control(g,47000)
    p.logical(x+w//2,y+10,True);p.drain();c.key(g,'home');assert app_offset(g)==0
    p.desktop(21000,True);assert app_offset(g)==0
    c.key(g,'end');observed=app_offset(g)
    assert observed==0,('Hidden native scrollbar stole End in the USB provider',observed)
    c.key(g,'home');assert app_offset(g)==0
    p.desktop(21001,True)
    # An address field gets Home/End even if the scrollbar previously had focus.
    x,y,w,h,_,_=c.control(g,47000);p.logical(x+w//2,y+10,True);p.drain();c.key(g,'home')
    p.desktop(40015,True);c.key(g,'end');assert app_offset(g)==0
    c.key(g,'esc')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--fixture',required=True);args=parser.parse_args()
    base=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage1-components'
    disk=base/args.fixture/'owned.img';assert disk.resolve().is_relative_to(base.resolve()) and disk.is_file()
    meta=json.loads(ui.manifest_path12().read_text());work=ui.q.new_work('m12-stage1-focus')
    with ui.guest(work/'focus',disk,media='installed',ready='M7_DESKTOP_READY') as g:
        assert 'M7_DESKTOP_READY build='+meta['build_id'] in g.log()
        p=ui.Pointer(g);p.drain();journey(g,p)
    print('PASS: Files provider transitions preserve keyboard ownership.')

if __name__=='__main__':main()
