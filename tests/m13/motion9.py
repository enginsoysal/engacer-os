"""Measure ordinary input to independently observed native display patches.

Only a new authenticated loopback QEMU display is used. No host desktop input,
guest-memory writes or image scaling. Times include VNC scanout/transport and
observation overhead; they are not hardware refresh rates or native GPU FPS.
"""
import argparse,hashlib,importlib.util,json,os,secrets,socket,statistics,struct,sys,time,traceback
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
os.environ['ENGACER12_IMAGE']='EngacerOS-M13STAGE9'
sys.path.insert(0,str(ROOT/'tests/m12'))
import components as c
from access_fixtures16 import clone
import observer8,capture14
ui=c.ui
observer8.bind(ui);capture14.bind(ui)
spec=importlib.util.spec_from_file_location('motion_rfb9',ROOT/'tests/m7/rfb.py')
rfb=importlib.util.module_from_spec(spec);spec.loader.exec_module(rfb)


def region(display,rect):
    x,y,w,h=rect
    assert 0<=x<display.width and 0<=y<display.height and 0<w<=display.width-x and 0<h<=display.height-y
    display.socket.sendall(struct.pack('!BBHHHH',3,0,x,y,w,h))
    image=Image.new('RGB',(w,h));coverage=Image.new('1',(w,h),0)
    deadline=time.monotonic()+5
    while True:
        kind=display.read(1)[0]
        if kind==0:
            _,count=struct.unpack('!BH',display.read(3));assert count<=4096
            if not count:
                if time.monotonic()>deadline:raise TimeoutError('Owned display returned no requested pixels')
                display.socket.sendall(struct.pack('!BBHHHH',3,0,x,y,w,h));continue
            for _ in range(count):
                rx,ry,rw,rh,encoding=struct.unpack('!HHHHi',display.read(12))
                assert encoding==0 and rw<=display.width-rx and rh<=display.height-ry
                raw=display.read(rw*rh*4)
                piece=Image.frombytes('RGB',(rw,rh),raw,'raw','BGRX')
                image.paste(piece,(rx-x,ry-y));coverage.paste(1,(rx-x,ry-y,rx-x+rw,ry-y+rh))
            assert coverage.getextrema()==(1,1),'No complete requested native patch received'
            return image
        if kind==2:continue
        if kind==3:
            length=struct.unpack_from('!I',display.read(7),3)[0];assert length<=1024**2;display.read(length);continue
        raise AssertionError('Unexpected owned RFB message '+str(kind))


def pointer(display,x,y,buttons=0):
    display.socket.sendall(struct.pack('!BBHH',5,buttons,x,y))


def quantiles(values):
    ordered=sorted(values)
    return dict(median_ms=statistics.median(values),p95_ms=ordered[min(len(ordered)-1,int(.95*len(ordered)))],maximum_ms=max(values),samples_ms=values)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--profile',choices=['ordinary','4k'],required=True);parser.add_argument('--samples',type=int,default=32);parser.add_argument('--accel',choices=['tcg','whpx'],required=True);parser.add_argument('--whpx-legacy-irq',action='store_true');args=parser.parse_args()
    assert not args.whpx_legacy_irq or args.accel=='whpx'
    assert 16<=args.samples<=120 and not (ROOT/'evidence/M13/9/publication-results.json').exists()
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'))
    native=json.loads((ROOT/'build/m13/stage9/ordinary/results.json').read_text(encoding='utf-8'))
    assert native['passed'] and native['build_id']==meta['build_id']
    source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m13-stage9-ordinary'/native['owned_fixture']/'owned.img'
    work,disk,cloned=clone(ui,source,'m139-motion-'+args.profile)
    label=args.accel+('-legacy' if args.whpx_legacy_irq else '')+'-'+args.profile
    out=ROOT/'build/m13/stage9/motion'/label;out.mkdir(parents=True,exist_ok=True);c.OUT=out
    physical,ram,scale,limit={'ordinary':((1920,1080),512,2,33.3),'4k':((3840,2160),1024,4,50)}[args.profile]
    # Owned test listeners stay outside this host's outgoing ephemeral range.
    from vmware_stage8 import observer_port8
    port,policy=observer_port8();password=secrets.token_hex(4)
    report=dict(passed=False,stage='M13.9',profile=args.profile,build_id=meta['build_id'],iso_sha256=meta['artifacts']['EngacerOS-M13STAGE9.iso']['sha256'],physical=list(physical),configured_guest_mib=ram,cpus=2,owned_fixture=work.name,clone=cloned,observation_port_policy=policy,method='Host ordinary pointer event to exact translated native title patch over authenticated loopback RFB; includes scanout, transport and observer overhead, not GPU FPS',checks=[])
    report['acceleration']=args.accel
    report['legacy_irq_profile']=args.whpx_legacy_irq
    try:
        guest=ui.guest(work/'motion',disk,resolution=physical,ram=ram,media='installed',ready='M7_DESKTOP_READY',extra=['-vnc',f'127.0.0.1:{port-5900},password=on'])
        assert guest.args[guest.args.index('-accel')+1]=='tcg'
        guest.args[guest.args.index('-accel')+1]=args.accel+(',hyperv=off,kernel-irqchip=off' if args.whpx_legacy_irq else '')
        with guest as g:
            g.qmp('set_password',{'protocol':'vnc','password':password})
            report['initial_cpu_monitor']=dict(halted=g.qmp('human-monitor-command',{'command-line':'info registers -a'}).count('HLT=1'),cpus=len(g.qmp('query-cpus-fast')),input={name:ui.integer(g,name,True) for name in ('mouse_dirty','mouse_head11','mouse_tail11','head','tail')})
            p=ui.Pointer(g);p.drain()
            g.qmp('send-key',{'keys':[{'type':'qcode','data':'esc'}],'hold-time':30});time.sleep(.15);p.drain()
            if scale==4:
                # The cloned ordinary fixture explicitly saves 100%. Apply
                # 200% through actual Settings on this owned clone only.
                c.open_settings(g,p);p.desktop(59001,True);p.desktop(113,True);p.desktop(47,True);p.close_app(3,True);p.drain()
            assert c.flag(g,'scale73')==scale
            base=ui.symbol('model',installed=True)[0]
            raw=ui.memory(g,base,8*28)
            windows=[struct.unpack_from('<4iII2B',raw,i*28) for i in range(8)]
            files=next(row for row in windows if row[5]==1 and row[6]);x,y,w,h=files[:4]
            before=struct.unpack('<4Q',ui.memory(g,ui.symbol('stats',32,True)[0],32))
            display=rfb.RFB(port,password);display.socket.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
            try:
                assert (display.width,display.height)==physical
                display.shot(out/'before-drag.png')
                factor=scale/2
                patch=(int((x+12)*factor),int((y+8)*factor),int(110*factor),int(24*factor))
                title=region(display,patch);assert len(title.getcolors(100000))>4;title.save(out/'reference-title.png')
                reference=title.tobytes()
                grab_x,grab_y=int((x+230)*factor),int((y+18)*factor)
                # QEMU's relative RFB path uses its first packet as the client
                # origin. Align through ordinary native input before timing
                # subsequent RFB deltas; never rewrite guest pointer state.
                def position():return {name:c.flag(g,name) for name in ('mouse_x','mouse_y','mouse_buttons','pointer_x','pointer_y','previous_buttons')}
                report['pointer_calibration']=[dict(step='before',**position())]
                p.move(grab_x,grab_y);p.drain();report['pointer_calibration'].append(dict(step='qmp-origin',**position()))
                pointer(display,grab_x,grab_y);p.drain();report['pointer_calibration'].append(dict(step='rfb-origin',**position()))
                pointer(display,grab_x,grab_y,1);p.drain();report['pointer_calibration'].append(dict(step='rfb-down',**position()))
                # Native caption capture becomes a drag only after movement
                # crosses the existing threshold. The translated visible
                # patch below, rather than mouse-down alone, proves motion.
                latencies=[];visible=[];completed=[]
                for number in range(args.samples):
                    dx,dy=(24,20) if number%2==0 else (0,0)
                    target=(int(patch[0]+dx*factor),int(patch[1]+dy*factor),patch[2],patch[3])
                    began=time.perf_counter();pointer(display,int(grab_x+dx*factor),int(grab_y+dy*factor),1)
                    deadline=time.monotonic()+5
                    image=region(display,target)
                    while image.tobytes()!=reference:
                        if time.monotonic()>deadline:
                            report['failure_sample']=number;report['expected_patch']=list(target)
                            report['failure_geometry']=list(struct.unpack('<4i',ui.memory(g,base+windows.index(files)*28,16)))
                            report['native_dragging']=c.flag(g,'dragging')
                            image.save(out/'unmatched-title.png');display.shot(out/'unmatched-native-frame.png')
                            (out/'native.log').write_text(g.log(),encoding='utf-8')
                            raise AssertionError('Native title did not reach the requested position')
                        image=region(display,target)
                    done=time.perf_counter();latencies.append((done-began)*1000);visible.append(done);completed.append([dx,dy])
                pointer(display,grab_x,grab_y,0);p.drain();display.shot(out/'after-drag.png')
                report['drag_feedback']=quantiles(latencies)
                report['observed_position_intervals']=quantiles([(b-a)*1000 for a,b in zip(visible,visible[1:])])
                report['requested_positions']=args.samples;report['visible_positions']=len(completed);report['missed_requested_positions']=args.samples-len(completed)
                report['drag_interval_target_ms']=limit
                report['drag_interval_target_passed']=report['observed_position_intervals']['p95_ms']<=limit
                report['ordinary_feedback_target_ms']=100
                report['ordinary_feedback_target_passed']=report['drag_feedback']['p95_ms']<=100
                report['checks'].append('Every requested held-pointer drag position has an independently observed exact native title patch at its translated physical location')
            finally:display.close()
            after=struct.unpack('<4Q',ui.memory(g,ui.symbol('stats',32,True)[0],32));assert after[0]==before[0] and after[3]==before[3]
            c.idle(g)
            report['resources']=dict(managed_before=list(before),managed_after=list(after),retained_task_delta_pages=0,all_cpus_halted_when_idle=True)
            report['checks'].append('Completed motion retains zero managed pages, adds no allocation failures and returns all CPUs to idle halt')
            (out/'native.log').write_text(g.log(),encoding='utf-8')
            report['passed']=report['drag_interval_target_passed'] and report['ordinary_feedback_target_passed']
    except Exception:
        report['error']=ui.q.clean(traceback.format_exc());raise
    finally:
        (out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(report,indent=2),flush=True)
    assert report['passed'],'Published reference performance targets are not met'


if __name__=='__main__':main()
