"""Check cached movement against real full repaint for the M12 component candidate."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import statistics
import struct
import time
import traceback
from PIL import Image
parser=argparse.ArgumentParser();parser.add_argument('--stage',type=int,required=True);parser.add_argument('--native-group',default='icons-native');parser.add_argument('--fixture-family');args=parser.parse_args();stage=args.stage
assert 2<=stage<=18 and args.native_group.replace('-','').isalnum()
os.environ['ENGACER12_IMAGE']=f'EngacerOS-M12STAGE{stage}'
import components as c

ui=c.ui;ROOT=ui.ROOT

def geometry(g):
    model=ui.symbol('model',installed=True)[0]
    slot=int.from_bytes(ui.memory(g,model+236,4),'little')
    return struct.unpack('<4i',ui.memory(g,model+slot*28,16))

def main():
    meta=json.loads(ui.manifest_path12().read_text())
    native=json.loads((ROOT/f'build/m12/stage{stage}/{args.native_group}/results.json').read_text())
    assert native['passed'] and native['build_id']==meta['build_id']
    base=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6'/(args.fixture_family or f'm12-stage{stage}-icons')
    assert base.resolve().is_relative_to((Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6').resolve())
    disk=base/native['owned_fixture']/'owned.img'
    assert disk.resolve().is_relative_to(base.resolve()) and disk.is_file()
    out=ROOT/f'build/m12/stage{stage}/motion';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    report=dict(passed=False,build_id=meta['build_id'],iso_sha256=hashlib.sha256(ui.iso_path12().read_bytes()).hexdigest(),profiles=[])
    work=ui.q.new_work(f'm12-stage{stage}-motion')
    try:
        for resolution,scale in [((1280,800),2),((1920,1200),3),((3840,2160),4)]:
            label=f'{resolution[0]}x{resolution[1]}'
            with ui.guest(work/label,disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution,ps2_only=scale==2) as g:
                assert 'M7_DESKTOP_READY build='+meta['build_id'] in g.log()
                p=ui.Pointer(g);p.drain()
                if scale==3:
                    c.open_settings(g,p)
                    if stage>=13:p.desktop(59001,True)
                    p.desktop(112,True)
                    # A M12.13 preview is explicitly cancelled on close. Minimize
                    # its owner during this session-only rendering observation.
                    if stage>=13:p.desktop(49000,True)
                    else:p.close_app(3,True)
                    p.drain()
                assert c.flag(g,'scale73')==scale
                model=ui.symbol('model',installed=True)[0]
                width,height=struct.unpack('<2I',ui.memory(g,model+240,8))
                before=struct.unpack('<4Q',ui.memory(g,ui.symbol('stats',32,True)[0],32))
                timings=[];comparisons=[]
                for number,(nx,ny) in enumerate([(20,160),(width-20,160),(width//2,height-90),(width//2,200)]):
                    x,y,w,h=geometry(g)
                    p.move((x+180)*scale//2,(y+18)*scale//2);p.drain();p.down(True);p.drain()
                    started=time.perf_counter();p.move(nx*scale//2,ny*scale//2);p.drain();timings.append((time.perf_counter()-started)*1000)
                    assert c.flag(g,'dragging') and not c.flag(g,'window_snap_preview11')
                    bounds=geometry(g)
                    if number==0:assert bounds[0]<0
                    if number==1:assert bounds[0]+bounds[2]>width
                    if number==2:assert bounds[1]+bounds[3]>height-60
                    cached=f'{label}-cached-{number}';full=f'{label}-full-{number}'
                    c.shot(g,cached);p.down(False);p.drain()
                    c.key(g,'f10');assert c.flag(g,'launcher');c.key(g,'esc');assert not c.flag(g,'launcher');c.shot(g,full)
                    with Image.open(out/(cached+'.png')) as a,Image.open(out/(full+'.png')) as b:
                        crop=(0,0,resolution[0],(height-60)*scale//2)
                        assert a.crop(crop).tobytes()==b.crop(crop).tobytes(),(label,number,bounds)
                    comparisons.append(dict(bounds=list(bounds),cached_equals_full_viewport=True))
                after=struct.unpack('<4Q',ui.memory(g,ui.symbol('stats',32,True)[0],32))
                assert before[0]==after[0] and before[3]==after[3];c.idle(g)
                graphics=struct.unpack('<8Q4I',ui.memory(g,ui.symbol('graphics9',80,True)[0],80));assert graphics[4]>0
                report['profiles'].append(dict(physical=list(resolution),scale_percent=scale*50,comparisons=comparisons,managed_bytes_before=before[0]*4096,managed_bytes_after=after[0]*4096,managed_peak_bytes=after[1]*4096,cached_copy_frames=graphics[4],event_to_drain_ms=timings,median_ms=statistics.median(timings),measurement='Host event through completed native composition including observation; not FPS or display refresh',all_cpus_halted_when_idle=True,idle_paints_unchanged=True))
                (out/(label+'.log')).write_bytes(g.log().encode())
        report['passed']=True
    except Exception:
        report['error']=ui.q.clean(traceback.format_exc());raise
    finally:
        (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
