"""A genuinely empty desktop must remain recoverable when all references are hidden."""
import json,struct,traceback
import desktop_native as d
c=d.c;ui=d.ui;ROOT=d.ROOT;OUT=ROOT/'build/m12/stage3/desktop-empty';OUT.mkdir(parents=True,exist_ok=True);c.OUT=OUT

def hide_all(g,p):
    for item in range(4):d.right(g,p,*d.point(g,30000+item));d.menu(g,p,48000)
    assert c.flag(g,'desktop_hidden12')==15
    assert not any(30000<=v[5]<30004 or 33000<=v[5]<34024 for v in d.controls(g))
    assert d.count(g)==0

def blank_keys(g):
    for key in ('home','end','left','right','up','down','ret'):c.key(g,key);assert d.count(g)==0

def main():
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m12-stage3-empty');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
    report=dict(passed=False,stage='M12.3',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],checks=[])
    try:
        live=ui.guest(work/'install',disk)
        with live as g:
            p=ui.Pointer(g)
            for action in (2,2,100,2,2,2):c.wizard(g,p,action)
            at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240)
            at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain();d.close_files(g,p)
            assert not any(k.startswith('/Users/Owner/Desktop/') for k in d.rows(g))
            hide_all(g,p);blank_keys(g);c.shot(g,'all-icons-hidden-empty-desktop')
            c.open_settings(g,p);assert d.count(g)==1;p.close_app(3,True);p.drain()
            d.right(g,p,1260,660);d.menu(g,p,48001);assert c.flag(g,'desktop_hidden12')==0
            hide_all(g,p);c.idle(g);(OUT/'install.log').write_text(g.log(),encoding='utf-8')
        assert struct.unpack('<QII',ui.s.s.document(disk,'/System/Settings/desktop12-Owner.bin'))==(0x31504f544b534544,1,15)
        report['checks'].append('Fresh installation with no user desktop objects can hide all four icons, safely consume navigation/Enter, open Settings through Start and restore defaults without a terminal')
        boot=ui.guest(work/'independent',disk,media='installed',ready='M7_DESKTOP_READY');ui.s.normal_boot(boot,live.folder/'vars.fd')
        with boot as g:
            p=ui.Pointer(g);p.drain();d.close_files(g,p);assert c.flag(g,'desktop_hidden12')==15
            blank_keys(g);c.shot(g,'persisted-empty-desktop');d.right(g,p,1260,660);d.menu(g,p,48001)
            assert c.flag(g,'desktop_hidden12')==0 and all(any(v[5]==30000+i for v in d.controls(g)) for i in range(4))
            c.shot(g,'restored-desktop-icons');c.idle(g);(OUT/'independent.log').write_text(g.log(),encoding='utf-8')
        assert struct.unpack('<QII',ui.s.s.document(disk,'/System/Settings/desktop12-Owner.bin'))==(0x31504f544b534544,1,0)
        report['checks'].append('Ordinary same-firmware disk-only restart retains the empty layout; Restore desktop icons restores all references and writes the independently verified visible preference')
        report['passed']=True
    except Exception:
        report['error']=ui.q.clean(traceback.format_exc());raise
    finally:
        (OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
