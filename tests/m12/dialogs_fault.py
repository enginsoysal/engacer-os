"""Inject an actual write failure into an isolated owned installed disk clone."""
import hashlib,json,os,subprocess,traceback
from pathlib import Path
import dialogs_native as d
c=d.c;f=d.f;ui=d.ui;ROOT=d.ROOT

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(8*1024**2),b''):h.update(block)
    return h.hexdigest()

def main():
    out=ROOT/'build/m12/stage8/dialogs-fault';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    native=json.loads((ROOT/'build/m12/stage8/dialogs-native/results.json').read_text());meta=json.loads(ui.manifest_path12().read_text());assert native['build_id']==meta['build_id']
    base=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage8-dialogs'/native['owned_fixture']/'owned.img'
    work=ui.q.new_work('m12-stage8-dialogs-fault');clone=work/'owned-clone.img';before=digest(base)
    qimg=Path(ui.q.qemu_tools()['qemu-system-x86_64']).with_name('qemu-img.exe')
    subprocess.run([str(qimg),'convert','-f','raw','-O','raw','-S','4k',str(base),str(clone)],check=True,capture_output=True)
    assert digest(clone)==before
    report=dict(passed=False,build_id=meta['build_id'],owned_fixture=work.name,base_sha256=before,qemu_img_sha256=digest(qimg),checks=[])
    try:
        with ui.guest(work/'write-failure',clone,media='installed',ready='M7_DESKTOP_READY',fault={'event':'write_aio','errno':5,'once':True,'immediately':True}) as g:
            p=ui.Pointer(g);p.drain();p.desktop(94,True);p.desktop(f.item(g,p,'Existing.txt'),True);c.key(g,'ret');original=f.app(g)['path'];before_pages=f.stats(g);c.key(g,'end');c.type_text(g,' unsaved after fault');text=bytes(d.appview(g).text)
            p.desktop(54001,True);d.field(g,p,54020,'WriteFailed.txt');p.desktop(54011,True)
            assert c.flag(g,'file_dialog_state11')==10 and d.picker(g).error and d.appview(g).dirty and bytes(d.appview(g).text)==text and f.app(g)['path']==original
            assert '/Users/Owner/Documents/WriteFailed.txt' not in f.entries(g)
            c.shot(g,'write-failure-preserves-work');p.desktop(54010,True);assert d.appview(g).dirty and bytes(d.appview(g).text)==text;f.same_pages(before_pages,f.stats(g));report['retained_pages_after_failed_save']=0;c.idle(g)
            (out/'failure.log').write_bytes(g.log().encode())
        assert digest(base)==before
        report['checks'].append('Actual injected first-write failure keeps dirty text, original document path and actionable picker error; Cancel keeps work and the source disk remains byte-identical')
        report['passed']=True
    except Exception:
        report['error']=ui.q.clean(traceback.format_exc());raise
    finally:
        (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
