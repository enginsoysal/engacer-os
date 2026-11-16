"""Early native ZIP/keyboard regression probe; never full stage acceptance."""
import json,traceback,zipfile
import dialogs_native as d
c=d.c;f=d.f;ui=d.ui;ROOT=d.ROOT

def main():
    out=ROOT/'build/m12/stage8/dialogs-formats-smoke';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    meta=json.loads(ui.manifest_path12().read_text());work=ui.q.new_work('m12-stage8-dialogs-formats-smoke');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
    report=dict(passed=False,development_only=True,build_id=meta['build_id'],owned_fixture=work.name,checks=[])
    try:
        with ui.guest(work/'install',disk) as g:
            p=ui.Pointer(g)
            for command in (2,2,100,2,2,2):c.wizard(g,p,command)
            at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain();before=f.stats(g)
            d.start_app(g,p,'Text Editor');c.key(g,'right');token=c.control(g,49002)[4];actions=[r[5] for r in f.controls(g) if r[4]==token and r[5]!=70];assert len(actions)>2
            c.key(g,'tab');assert c.flag(g,'focused_action')==actions[0]
            c.key(g,'tab');assert c.flag(g,'focused_action')==actions[1]
            c.key(g,'shift','tab');assert c.flag(g,'focused_action')==actions[0]
            c.key(g,'shift','tab');assert c.flag(g,'focused_action')==actions[-1]
            c.key(g,'tab');assert c.flag(g,'focused_action')==actions[0]
            d.close_focused(g,p);report['checks'].append('Generic native Tab and Shift+Tab preserve control order and both wrap directions without the control-index stack array')
            d.start_app(g,p,'Image Viewer');p.desktop(10502,True);p.desktop(54018,True);d.choose(g,p,'ColorStudy.bmp');c.key(g,'ret');assert not c.flag(g,'file_dialog_state11') and f.app(g)['path'].endswith('/ColorStudy.bmp');c.shot(g,'image-open');d.close_focused(g,p)
            d.start_app(g,p,'Archive Manager');p.desktop(54000,True);p.desktop(54017,True);d.choose(g,p,'ArchiveSample.zip');c.key(g,'ret');assert not c.flag(g,'file_dialog_state11') and f.app(g)['path'].endswith('/ArchiveSample.zip');c.shot(g,'zip-open')
            p.desktop(54002,True);p.desktop(54016,True);p.desktop(54011,True);assert not c.flag(g,'file_dialog_state11');c.shot(g,'zip-extracted');report['extracted_folder']=next(path for path,e in f.entries(g).items() if e['kind']==2 and path.startswith('/Users/Owner/Documents/Extracted') and '/' not in path[len('/Users/Owner/Documents/'):]);d.close_focused(g,p);f.same_pages(before,f.stats(g));c.idle(g);(out/'install.log').write_bytes(g.log().encode())
        with zipfile.ZipFile(ROOT/'distros/packages/apps-guide/ArchiveSample.zip') as archive:
            for item in archive.infolist():
                if not item.is_dir():assert ui.s.s.document(disk,report['extracted_folder']+'/'+item.filename)==archive.read(item)
        report['checks'].append('Ordinary keyboard Enter opens real BMP and ZIP, chosen-folder extraction matches every independently decoded archive member and tasks retain zero pages')
        report['passed']=True
    except Exception:
        report['error']=ui.q.clean(traceback.format_exc())
        if 'g' in locals():(out/'failure.log').write_bytes(g.log().encode())
        raise
    finally:
        (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
