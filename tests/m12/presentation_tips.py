"""Actual HiDPI native/USB complete-name tips after pointer ownership checks."""
import json,time,traceback
import presentation_native as n
f=n.f;c=n.c;ui=n.ui;ROOT=n.ROOT
def main():
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));native=json.loads((n.OUT/'results.json').read_text(encoding='utf-8'));assert native['passed'] and native['build_id']==meta['build_id']
    source=ui.q.BASE/'m12-stage6-presentation'/native['owned_fixture'];disk=source/'owned.img';usb=source/'owned-usb.img';before_sha=f.sha_file(usb)
    out=ROOT/'build/m12/stage6/name-tips';out.mkdir(exist_ok=True);c.OUT=out;work=ui.q.new_work('m12-stage6-tips')
    result=dict(passed=False,build_id=meta['build_id'],iso_sha256=native['iso_sha256'],profiles=[])
    try:
        for label,resolution,scale in [('150',(1920,1200),112),('4k',(3840,2160),113)]:
            with ui.guest(work/label,disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution,extra=['-drive',f'if=none,id=tips-source,format=raw,file={usb}']) as g:
                p=ui.Pointer(g);p.drain();assert 'M7_DESKTOP_READY build='+meta['build_id'] in g.log();c.open_settings(g,p);p.desktop(scale,True);p.close_app(3,True);p.drain();before=f.stats(g)
                n.scene(g,p);n.hover(g,p,f.item(g,p,'W'*55+'.txt'));native_tip=n.tip(g);assert native_tip[2]>0;c.shot(g,label+'-native-name');p.desktop(21000,True);assert n.tip(g)[2]==0
                f.attach(g,p,'tips-source','tips-usb');c.key(g,'home');c.key(g,'ret');n.hover(g,p,f.row(g,'W'*120+'.txt'));usb_tip=n.tip(g);assert usb_tip[2]>0;c.shot(g,label+'-usb-name')
                g.qmp('device_del',{'id':'tips-usb'});p.desktop(92,True);assert n.tip(g)[2]==0
                deadline=time.monotonic()+30
                while f.stats(g)[0]!=before[0]:
                    if time.monotonic()>deadline:raise TimeoutError('Tip profile retained device pages')
                    time.sleep(.1);p.drain()
                after=f.stats(g);f.same_pages(before,after);c.idle(g);(out/(label+'.log')).write_text(g.log(),encoding='utf-8');result['profiles'].append(dict(physical=list(resolution),scale=c.flag(g,'scale73'),native_tip=list(native_tip),usb_tip=list(usb_tip),retained_pages=0,managed_current_bytes=after[0]*4096))
        assert f.sha_file(usb)==before_sha;result.update(passed=True,usb_unchanged=True,idle_observations=c.IDLE_OBSERVATIONS)
    except Exception:
        result['error']=ui.q.clean(traceback.format_exc());raise
    finally:
        (out/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
