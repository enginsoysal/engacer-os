"""Actual M12.2 icon binding, retained installation, scaling and idle checks."""
import hashlib
import json
import os
import struct
import traceback
from PIL import Image, ImageChops

os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE2'
import components as c
import icons_host as host

ui=c.ui;ROOT=ui.ROOT;OUT=ROOT/'build/m12/stage2/icons-native';OUT.mkdir(parents=True,exist_ok=True);c.OUT=OUT

def stats(g):return struct.unpack('<4Q',ui.memory(g,ui.symbol('stats',32,True)[0],32))
def windows(g):return int.from_bytes(ui.memory(g,ui.symbol('model',installed=True)[0]+232,4),'little')

def theme(g,p,value,save=False):
    c.open_settings(g,p);p.desktop(43 if value else 44,True)
    assert c.dark(g)==value
    if save:p.desktop(47,True)
    p.close_app(3,True);p.drain()

def controls(g):
    count=ui.integer(g,'control_count',True)
    raw=ui.memory(g,ui.symbol('controls',65536,True)[0],count*32)
    return [struct.unpack_from('<iiiiQI',raw,i*32) for i in range(count)]

def compare_icon(image,exe,number,x,y,size,scale,dark):
    left=x*scale//2;top=y*scale//2;extent=(x+size)*scale//2-left
    background=image.getpixel(((x-4)*scale//2,(y+14)*scale//2))
    expected=Image.new('RGBA',(extent,extent),background+(255,))
    expected.alpha_composite(host.icon(exe,number,extent,dark))
    actual=image.crop((left,top,left+extent,top+extent))
    diff=ImageChops.difference(actual,expected.convert('RGB'))
    maximum=max(high for low,high in diff.getextrema())
    if maximum>1:
        actual.save(OUT/f'mismatch-{number}-actual.png');expected.save(OUT/f'mismatch-{number}-expected.png')
    assert maximum<=1,(number,x,y,size,scale,dark,maximum)
    return dict(app=number,physical_size=extent,max_channel_difference=maximum)

def all_apps(g,p,label):
    if not c.flag(g,'launcher'):p.desktop(0,True)
    p.desktop(42001,True);p.move(1200,80);p.drain()
    scale=c.flag(g,'scale73');dark=c.dark(g);before=stats(g);count_before=windows(g)
    count=c.flag(g,'start_result_count11');assert count==19,count
    raw=ui.memory(g,ui.symbol('start_results11',installed=True)[0],count*8)
    results=[struct.unpack_from('<2I',raw,i*8) for i in range(count)]
    assert all(kind==1 for kind,_ in results) and {app for _,app in results}==set(range(1,20))
    seen={};page=0
    while True:
        name=f'{label}-all-apps-{page}';c.shot(g,name)
        with Image.open(OUT/(name+'.png')) as source:
            image=source.convert('RGB')
            for x,y,w,h,token,action in controls(g):
                if 42200<=action<42200+count:
                    number=results[action-42200][1]
                    seen[number]=compare_icon(image,ROOT/'build/m12/stage2/icons-host.exe',number,x+10,y+10,26,scale,dark)
        if len(seen)==count:break
        assert page<10 and any(row[5]==42006 for row in controls(g))
        p.desktop(42006,True);p.move(1200,80);p.drain();page+=1
    c.key(g,'esc');p.drain();after=stats(g)
    assert windows(g)==count_before and after[0]==before[0] and after[3]==before[3]
    c.idle(g)
    return dict(profile=label,scale=scale,dark=dark,apps=[seen[k] for k in sorted(seen)],managed_before_bytes=before[0]*4096,managed_after_bytes=after[0]*4096,managed_peak_bytes=after[1]*4096,no_application_launch=True,retained_pages=after[0]-before[0])

def main():
    meta=json.loads(ui.manifest_path12().read_text());work=ui.q.new_work('m12-stage2-icons')
    disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
    report=dict(passed=False,stage='M12.2',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],owned_fixture=work.name,checks=[],profiles=[])
    try:
        live=ui.guest(work/'install',disk,resolution=(1280,800))
        with live as g:
            p=ui.Pointer(g)
            for action in (2,2,100,2,2,2):c.wizard(g,p,action)
            at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240)
            at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180)
            assert 'M7_DESKTOP_READY build='+meta['build_id'] in g.log()
            p=ui.Pointer(g);p.drain();c.shot(g,'installed-desktop')
            report['checks'].append('Real UEFI installation and retained-ISO restart reach the matching installed desktop')
            report['profiles'].append(all_apps(g,p,'ordinary-light'))
            theme(g,p,1,True);report['profiles'].append(all_apps(g,p,'ordinary-dark'))
            c.open_settings(g,p);c.scroll_test(g,p);c.shot(g,'application-folders')
            import focus_ownership
            focus_ownership.journey(g,p)
            report['checks'].append('The real Files scrollbar and keyboard ownership survive app-folder icons and USB/address transitions')
            assert c.flag(g,'icon12_draws',8)>0 and c.flag(g,'icon12_max_physical',4)<=128
            (OUT/'install.log').write_bytes(g.log().encode())
        for number in (1,2):
            candidate=ui.guest(work/f'disk-{number}',disk,media='installed',ready='M7_DESKTOP_READY')
            ui.s.normal_boot(candidate,live.folder/'vars.fd')
            with candidate as g:
                assert 'M7_DESKTOP_READY build='+meta['build_id'] in g.log()
                ui.Pointer(g).drain();assert c.dark(g)==1;c.idle(g);c.shot(g,f'disk-only-{number}')
                (OUT/f'disk-only-{number}.log').write_bytes(g.log().encode())
            report['checks'].append(f'Independent disk startup {number} retains the same firmware variables, saved dark theme and matching build without forced boot order')
        for label,resolution,action in [('150',(1920,1200),112),('4k',(3840,2160),113)]:
            with ui.guest(work/label,disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution) as g:
                p=ui.Pointer(g);p.drain();c.open_settings(g,p);p.desktop(action,True);p.close_app(3,True);p.drain()
                assert c.flag(g,'scale73')==(3 if label=='150' else 4)
                for value in (0,1):
                    theme(g,p,value);report['profiles'].append(all_apps(g,p,label+('-dark' if value else '-light')))
                c.shot(g,'native-'+label)
                assert 'M7_DESKTOP_READY build='+meta['build_id'] in g.log()
                (OUT/(label+'.log')).write_bytes(g.log().encode())
        assert len(report['profiles'])==6 and sum(len(p['apps']) for p in report['profiles'])==114
        report['checks'].append('All nineteen Start app identities match production host pixels in light/dark at ordinary, actual 150% and actual 3840x2160/200%, without launching apps or retaining pages')
        report['passed']=True
    except Exception:
        report['error']=ui.q.clean(traceback.format_exc());raise
    finally:
        report['idle_observations']=c.IDLE_OBSERVATIONS
        (OUT/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
