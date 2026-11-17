"""Real cooperative USB transfer keeps removal and preference writes guarded."""
import json,os,struct,sys,time,traceback
from pathlib import Path
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE14'
import tray_observe as q
c=q.c;f=q.f;s=q.s;t=q.t;ui=q.ui;ROOT=q.ROOT

def job(g):
    raw=ui.memory(g,ui.symbol('file_job_state11',installed=True)[0],112)
    return struct.unpack_from('<15I',raw),struct.unpack_from('<6Q',raw,64)

def active_key(g,*keys):
    g.qmp('send-key',{'keys':[{'type':'qcode','data':name} for name in keys],'hold-time':40});time.sleep(.1)

def active_click(g,p,command):
    deadline=time.monotonic()+15
    while True:
        matches=[r for r in f.controls(g) if r[5]==command]
        if matches:break
        if time.monotonic()>deadline:raise AssertionError(('Missing active control',command,job(g)))
        time.sleep(.01)
    x,y,w,h,*_=matches[-1];scale=c.flag(g,'scale73');p.move((x+w//2)*scale//2,(y+h//2)*scale//2)
    if not job(g)[0][0]:p.drain()
    else:time.sleep(.08)
    for down in (True,False):g.qmp('input-send-event',{'events':[{'type':'btn','data':{'down':down,'button':'left'}}]});time.sleep(.08)
    deadline=time.monotonic()+15
    while ui.integer(g,'mouse_head11',True)!=ui.integer(g,'mouse_tail11',True):
        if time.monotonic()>deadline:raise TimeoutError('Active guest input queue')
        time.sleep(.01)

def main():
    out=ROOT/'build/m12/stage14/feedback-busy';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    native=json.loads((ROOT/'build/m12/stage14/feedback-native/results.json').read_text(encoding='utf-8'));meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));assert native['passed'] and native['build_id']==meta['build_id']
    work=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage14-feedback'/native['owned_fixture'];disk=work/'owned.img';attempt=ui.q.new_work('m12-stage14-feedback-busy');report=dict(passed=False,build_id=meta['build_id'],checks=[],owned_fixture=attempt.name)
    try:
        sys.path.insert(0,str(ROOT/'tools/local/m10-python'));from pyfatfs.PyFat import PyFat;from pyfatfs.PyFatFS import PyFatFS
        source=ui.q.sparse_disk(attempt/'owned-usb.img',1024**3);fat=PyFat();fat.mkfs(str(source),fat_type=PyFat.FAT_TYPE_FAT32,size=1024**3,label='M1214BUSY',volume_id=0x12140001);fat.close()
        payload=(bytes(range(256))*4096)*64
        with PyFatFS(str(source),preserve_case=True) as fs:fs.writebytes('/Large.bin',payload)
        source_hash=f.sha_file(source)
        with ui.guest(attempt/'guest',disk,media='installed',ready='M7_DESKTOP_READY',extra=['-drive',f'if=none,id=feedback-large,format=raw,file={source}']) as g:
            p=ui.Pointer(g);p.drain();t.close_all(g,p);editor=t.launch(g,p,'text editor',2);c.type_text(g,'Keep my active transfer document');editor_path=f.app(g)['path'];assert editor_path not in f.entries(g);p.desktop(49000,True)
            f.attach(g,p,'feedback-large','feedback-large-device');q.open_quick(g);p.desktop(58002,True);drive=next(r for r in f.controls(g) if 58200<=r[5]<58216);p.desktop(drive[5],True);files=next(w for w in t.records(g) if w['slot']==f.model(g)[0]);p.desktop(f.row(g,'Large.bin'),True);p.desktop(40000,True)
            active_click(g,p,21004);assert job(g)[0][0];active_key(g,'alt','ret');assert not c.flag(g,'file_dialog_state11') and job(g)[0][0] and 'file operation' in f.app(g)['notice'];active_click(g,p,43102);assert f.model(g)[0]==editor['slot'];active_click(g,p,54001);assert not c.flag(g,'file_dialog_state11') and job(g)[0][0] and 'file operation' in f.app(g)['notice'];active_click(g,p,20);assert job(g)[0][0] and 'unsaved text' in f.app(g)['notice'] and editor_path not in f.entries(g) and bytes(t.app_view(g).text)==b'Keep my active transfer document'
            painted=c.flag(g,'paints');deadline=time.monotonic()+15
            while c.flag(g,'paints')==painted:
                assert job(g)[0][0]
                if time.monotonic()>deadline:raise TimeoutError('Busy feedback paint')
                time.sleep(.01)
            g.qmp('stop')
            try:ui.raw_shot(g,out,'busy-dialog-and-save-refused',True)
            finally:g.qmp('cont')
            active_click(g,p,43101);active_click(g,p,40019);deadline=time.monotonic()+90
            while job(g)[0][0]:
                if time.monotonic()>deadline:raise TimeoutError('Transfer cancellation')
                time.sleep(.02)
            p.drain();assert job(g)[0][8] and not c.flag(g,'file_job_error11') and '/Users/Owner/Downloads/Large.bin' not in f.entries(g)
            t.focus(g,p,editor);p.desktop(54001,True);assert c.flag(g,'file_dialog_state11')==10;owner=int.from_bytes(ui.memory(g,ui.symbol('file_dialog_state11',installed=True)[0]+32,8),'little');t.focus(g,p,files);f.visit(g,p,'/Users/Owner/Downloads');c.key(g,'ctrl','v');assert not job(g)[0][0] and c.flag(g,'file_dialog_state11')==10 and int.from_bytes(ui.memory(g,ui.symbol('file_dialog_state11',installed=True)[0]+32,8),'little')==owner;c.shot(g,'existing-dialog-kept');t.focus(g,p,editor);assert bytes(t.app_view(g).text)==b'Keep my active transfer document';p.desktop(54010,True);t.focus(g,p,files);f.visit(g,p,'USB drives');p.desktop(f.drive(g),True);p.desktop(f.row(g,'Large.bin'),True);active_click(g,p,21004);assert job(g)[0][0];g.qmp('device_del',{'id':'feedback-large-device'});deadline=time.monotonic()+90
            while job(g)[0][0]:
                if time.monotonic()>deadline:raise TimeoutError('Removed USB transfer failure')
                time.sleep(.02)
            p.drain();assert c.flag(g,'file_job_error11') and '/Users/Owner/Downloads/Large.bin' not in f.entries(g);c.shot(g,'removed-source-transfer-failed');t.close_all(g,p)
            assert f.sha_file(source)==source_hash;baseline=f.stats(g);c.idle(g);report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0);(out/'native.log').write_bytes(g.log().encode())
        report['checks'].append('During a real 64-MiB cooperative USB import, Save As and Save refuse without changing the active job, publishing the unsaved document or losing text; Cancel leaves the destination unpublished and source byte-identical')
        report['checks'].append('After cancellation an actual Save As opens; another Files window cannot start a paste or replace that dialog owner, and exact unsaved text survives')
        report['checks'].append('Removing the actual USB source during another active import reports failure and leaves its destination unpublished; the original source image remains byte-identical')
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
