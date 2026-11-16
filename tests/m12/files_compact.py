"""Verify the common navigation in an actual narrow installed Files window."""
import json,os,traceback
from pathlib import Path
import files_native as f

def main():
    meta=json.loads(f.ui.manifest_path12().read_text(encoding='utf-8'))
    native=json.loads((f.OUT/'results.json').read_text(encoding='utf-8'))
    assert native['passed'] and native['build_id']==meta['build_id']
    out=f.ROOT/'build/m12/stage5/files-compact';out.mkdir(exist_ok=True);f.c.OUT=out
    work=f.ui.q.new_work('m12-stage5-compact')
    disk=f.ui.q.BASE/'m12-stage5-files'/native['owned_fixture']/'owned.img'
    result=dict(passed=False,build_id=meta['build_id'],iso_sha256=native['iso_sha256'])
    try:
        with f.ui.guest(work/'boot',disk,media='installed',ready='M7_DESKTOP_READY') as g:
            p=f.ui.Pointer(g);p.drain();before=f.stats(g)
            _,(x,y,w,h)=f.model(g)
            p.move(x+w-2,y+h-2);p.drain();p.down(True);p.drain()
            p.move(x+498,y+418);p.drain();p.down(False);p.drain()
            _,bounds=f.model(g);assert bounds[2:]==(500,420),bounds
            p.desktop(40016,True);p.desktop(32002,True)
            assert f.app(g)['path'].endswith('/Documents')
            p.desktop(40016,True);p.desktop(32006,True)
            assert f.app(g)['mode']==1 and all(f.has(g,a) for a in (90,50000,40016,40015))
            assert not any(40200<=r[5]<40208 for r in f.current_controls(g))
            f.c.shot(g,'compact-no-device');p.desktop(90,True)
            assert f.app(g)['mode']==0 and f.app(g)['path'].endswith('/Documents')
            f.c.shot(g,'compact-documents');p.desktop(91,True);assert f.app(g)['mode']==1
            f.c.open_settings(g,p);p.desktop(43,True);p.close_app(3,True);p.drain()
            assert f.c.dark(g)==1 and f.app(g)['mode']==1
            f.c.shot(g,'compact-dark-no-device');p.desktop(90,True)
            assert f.app(g)['path'].endswith('/Documents');f.c.shot(g,'compact-dark-documents')
            f.same_pages(before,f.stats(g));f.c.idle(g)
            (out/'boot.log').write_text(g.log(),encoding='utf-8')
            result.update(passed=True,bounds=list(bounds),navigation=['Back','Forward','Refresh','Places','address'],themes=['light','dark'],retained_pages=0,idle_observations=f.c.IDLE_OBSERVATIONS)
    except Exception:
        result['error']=f.ui.q.clean(traceback.format_exc());raise
    finally:
        (out/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
if __name__=='__main__':main()
