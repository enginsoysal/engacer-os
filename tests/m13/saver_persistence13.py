"""Two ordinary starts for remaining offered saver styles/timeouts/enabled values."""
import hashlib,json,os,struct,traceback
from pathlib import Path
import saver_native13 as n
from access_fixtures16 import clone
c=n.c;f=n.f;h=n.h;t=n.t;ui=n.ui;ROOT=n.ROOT


def main():
    out=ROOT/'build/m13/stage13/screensaver-persistence';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m13/stage13/screensaver-native/results.json').read_text(encoding='utf-8'));assert base['passed'] and base['build_id']==meta['build_id']
    source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m1313-saver'/base['owned_fixture']/'owned.img';original=f.sha_file(source)
    report=dict(passed=False,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],checks=[],cases=[],resources=dict(retained_pages=0))
    try:
        for label,seconds,style,timeout,command in [('logo-one-minute',60,0,60203,60206),('clock-five-minutes',300,1,60204,60207)]:
            work,disk,cloned=clone(ui,source,'m1313-saver-persistence');welcome=ui.s.s.document(disk,'/Users/Owner/Documents/Welcome.txt');expected=struct.pack('<5I',0x31325345,1,1,seconds,style)
            with ui.guest(work/'save',disk,media='installed',ready='M7_DESKTOP_READY') as g:
                p=ui.Pointer(g);p.drain();t.close_all(g,p);baseline=f.stats(g);n.open_saver(g,p);p.desktop(60202,True);p.desktop(timeout,True);p.desktop(command,True);p.desktop(60210,True);assert ui.s.s.document(disk,n.PATH)==expected;c.shot(g,label+'-saved');h.close(g,p);f.same_pages(baseline,f.stats(g));c.idle(g)
            boots=[]
            for number,ps2 in [(1,False),(2,True)]:
                with ui.guest(work/('start-'+str(number)),disk,media='installed',ready='M7_DESKTOP_READY',ps2_only=ps2) as g:
                    p=ui.Pointer(g);p.drain();t.close_all(g,p);baseline=f.stats(g);assert n.saved(g)==struct.unpack('<5I',expected) and not c.flag(g,'saver_invalid21');n.open_saver(g,p);n.preview(g,p);c.shot(g,label+'-start-'+str(number));n.wake(g);h.close(g,p);f.same_pages(baseline,f.stats(g));c.idle(g);boots.append(dict(number=number,ps2_only=ps2,record_hex=expected.hex(),before=list(baseline),after=list(f.stats(g))))
            assert ui.s.s.document(disk,'/Users/Owner/Documents/Welcome.txt')==welcome
            report['cases'].append(dict(name=label,clone=cloned,boots=boots));print('PASS two ordinary starts: '+label,flush=True)
        assert f.sha_file(source)==original
        report['checks']=['Additional On/one-minute/logo and On/five-minute/Clock records each survive two ordinary USB/PS2 starts and visible native preview/wake; together with the full task Off/ten-minute/Blank covers every offered field value, without claiming every Cartesian combination'];report['passed']=True
    except Exception:report['resources']['retained_pages']=None;report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':main()
