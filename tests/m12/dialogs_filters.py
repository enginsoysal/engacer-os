"""Real extension filters and refused saves must preserve the open document."""
import json,os,traceback
from pathlib import Path
import dialogs_native as d
c=d.c;f=d.f;ui=d.ui;ROOT=d.ROOT

def frozen_digest(g,disk):
    g.qmp('stop')
    try:return ui.q.digest(disk)
    finally:g.qmp('cont')

def main():
    out=ROOT/'build/m12/stage8/dialogs-filters';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    native=json.loads((ROOT/'build/m12/stage8/dialogs-native/results.json').read_text());meta=json.loads(ui.manifest_path12().read_text());assert native['passed'] and native['build_id']==meta['build_id']
    work=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage8-dialogs'/native['owned_fixture'];disk=work/'owned.img'
    report=dict(passed=False,build_id=meta['build_id'],checks=[])
    try:
        with ui.guest(work/'filter-refusals',disk,media='installed',ready='M7_DESKTOP_READY') as g:
            p=ui.Pointer(g);p.drain();before=f.stats(g);f.visit(g,p,'Documents');p.desktop(f.item(g,p,'Existing.txt'),True);c.key(g,'ret');original=f.app(g)['path'];text=bytes(d.appview(g).text);baseline=frozen_digest(g,disk)
            def retained():
                assert c.flag(g,'file_dialog_state11')==10 and d.picker(g).error and f.app(g)['path']==original and bytes(d.appview(g).text)==text and not d.appview(g).dirty
            c.key(g,'ctrl','o');p.desktop(54017,True);index=f.entries(g)['/Users/Owner/Downloads/ArchiveSample.zip']['index'];state=d.picker(g);assert not state.filter and index not in state.order[:state.count]
            p.desktop(54021,True);state=d.picker(g);assert state.filter==1 and index in state.order[:state.count];d.choose(g,p,'ArchiveSample.zip');c.key(g,'ret');retained();assert b'8191' in d.picker(g).error;c.shot(g,'all-files-size-refusal')
            p.desktop(54021,True);state=d.picker(g);assert not state.filter and index not in state.order[:state.count];p.desktop(54010,True)
            report['checks'].append('Text filter excludes ZIP; All files reveals the actual source but retains the original document on its explicit native size-limit refusal')
            c.key(g,'ctrl','o');d.location(g,p,'/Users/Owner/AppData');p.desktop(54021,True);d.choose(g,p,'file-dialogs12.bin');c.key(g,'ret');retained();assert b'ASCII' in d.picker(g).error;c.shot(g,'binary-text-refusal');p.desktop(54010,True)
            report['checks'].append('An actual CRC-valid small binary file is refused as unsupported ASCII without changing the current text or app path')
            c.key(g,'ctrl','shift','s');d.location(g,p,'/System');d.field(g,p,54020,'NeverCreated.txt');p.desktop(54011,True);retained();assert '/System/NeverCreated.txt' not in f.entries(g);c.shot(g,'protected-save-refusal');p.desktop(54010,True)
            report['checks'].append('A protected native destination explains the refused save and never publishes a file or changes the original document')
            c.key(g,'ctrl','shift','s');assert d.picker(g).path==b'/Users/Owner/Documents';p.desktop(54021,True)
            for name in ('Bad.','Bad/Name'):
                d.field(g,p,54020,name);p.desktop(54011,True);retained()
            p.desktop(54010,True);assert frozen_digest(g,disk)==baseline;report['disk_unchanged']=True
            report['checks'].append('Invalid All-files names are refused; cancelled navigation and every rejected Open/Save leave the complete owned native disk unchanged')
            d.close_focused(g,p);f.same_pages(before,f.stats(g));report['retained_pages']=0;c.idle(g);(out/'boot.log').write_bytes(g.log().encode())
        report['passed']=True
    except Exception:
        report['error']=ui.q.clean(traceback.format_exc())
        if 'g' in locals():(out/'failure.log').write_bytes(g.log().encode())
        raise
    finally:
        (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
