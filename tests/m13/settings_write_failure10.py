"""Controlled first-write refusal: readable recovery and retained preview/work.

This injects a declared functional error into an owned clone. It is not a
natural-freeze experiment, duration test or stability qualification.
"""
import hashlib,json,os,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
os.environ['ENGACER12_IMAGE']='EngacerOS-M13STAGE10'
sys.path.insert(0,str(ROOT/'tests/m12'))
import settings_observe as h
import capture14,observe20,observer8
from access_fixtures16 import clone
c=h.c;f=h.f;t=h.t;ui=h.ui
capture14.bind(ui);observe20.bind(ui);observer8.bind(ui)


def main():
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'))
    native=json.loads((ROOT/'build/m13/stage10/ordinary/results.json').read_text(encoding='utf-8'))
    assert native['passed'] and native['build_id']==meta['build_id']
    source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m13-stage10-ordinary'/native['owned_fixture']/'owned.img'
    work,disk,cloned=clone(ui,source,'m1310-settings-write-failure')
    out=ROOT/'build/m13/stage10/settings-write-failure';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    report=dict(passed=False,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],
                clone=cloned,checks=[],injected_fault=dict(event='write_aio',errno=5,once=True,immediately=True))
    original=ui.s.s.document(disk,'/Users/Owner/Documents/Welcome.txt')
    try:
        with ui.guest(work/'installed',disk,media='installed',ready='M7_DESKTOP_READY',fault=report['injected_fault']) as g:
            p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);baseline=f.stats(g)
            editor=t.launch(g,p,'text editor',2);c.type_text(g,'Keep unsaved work');text=bytes(t.app_view(g).text)
            settings=t.launch(g,p,'settings',3);initial=h.colors(g);p.desktop(43,True);assert h.preview(g)[0]==settings['token']
            p.desktop(47,True);message=f.app(g)['notice'];report['message']=message
            assert 'could not be saved' in message and 'Cancel preview' in message
            assert h.preview(g)[0]==settings['token'] and h.colors(g)[1]==1
            c.shot(g,'readable-write-refusal');p.desktop(59005,True);assert h.colors(g)==initial and not h.preview(g)[0]
            h.close(g,p);t.focus(g,p,editor);assert bytes(t.app_view(g).text)==text and t.app_view(g).dirty
            c.shot(g,'cancel-restores-look-keeps-work');t.close_all(g,p);f.same_pages(baseline,f.stats(g));c.idle(g)
            report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0)
            report['message']=message;(out/'native.log').write_bytes(g.log().encode('utf-8'))
        assert ui.s.s.document(disk,'/Users/Owner/Documents/Welcome.txt')==original
        assert f.sha_file(source)==cloned['source_sha256']
        report['checks'].append('Declared real write refusal explains the retained preview and Cancel route; Cancel restores the previous look, another Editor retains exact unsaved text, original personal bytes and source image remain unchanged, and the task retains zero managed pages')
        report['passed']=True
    except Exception:
        report['error']=ui.q.clean(traceback.format_exc())
        if 'g' in locals():(out/'failure.log').write_bytes(g.log().encode('utf-8'))
        raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode('utf-8'));print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':main()
