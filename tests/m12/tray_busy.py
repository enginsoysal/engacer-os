"""Real cooperative USB transfer keeps removal and preference writes guarded."""
import json,os,struct,sys,time,traceback
from pathlib import Path
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE12'
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
    out=ROOT/'build/m12/stage12/tray-busy';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    native=json.loads((ROOT/'build/m12/stage12/tray-native/results.json').read_text(encoding='utf-8'));meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));assert native['passed'] and native['build_id']==meta['build_id']
    work=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage12-tray'/native['owned_fixture'];disk=work/'owned.img';attempt=ui.q.new_work('m12-stage12-tray-busy');report=dict(passed=False,build_id=meta['build_id'],checks=[],owned_fixture=attempt.name)
    try:
        sys.path.insert(0,str(ROOT/'tools/local/m10-python'));from pyfatfs.PyFat import PyFat;from pyfatfs.PyFatFS import PyFatFS
        source=ui.q.sparse_disk(attempt/'owned-usb.img',1024**3);fat=PyFat();fat.mkfs(str(source),fat_type=PyFat.FAT_TYPE_FAT32,size=1024**3,label='M1212BUSY',volume_id=0x12120001);fat.close()
        payload=(bytes(range(256))*4096)*64
        with PyFatFS(str(source),preserve_case=True) as fs:fs.writebytes('/Large.bin',payload)
        source_hash=f.sha_file(source)
        with ui.guest(attempt/'guest',disk,media='installed',ready='M7_DESKTOP_READY',extra=['-drive',f'if=none,id=tray-large,format=raw,file={source}']) as g:
            p=ui.Pointer(g);p.drain();t.close_all(g,p);f.attach(g,p,'tray-large','tray-large-device');q.open_quick(g);p.desktop(58002,True);drive=next(r for r in f.controls(g) if 58200<=r[5]<58216);p.desktop(drive[5],True);p.desktop(f.row(g,'Large.bin'),True)
            saved_audio=ui.s.s.document(disk,'/System/Settings/audio74.bin');active_click(g,p,21004)
            assert job(g)[0][0],('Transfer completed before busy observation',job(g));active_key(g,'meta_l','a');active_click(g,p,58002);assert job(g)[0][0]
            at=len(g.log());active_click(g,p,drive[5]+20);assert 'transfer' in q.notice(g).lower() and 'M10_USB_SAFE_TO_REMOVE' not in g.log()[at:] and dict(q.disks(g))[drive[5]-58200][4]
            active_click(g,p,58001);active_click(g,p,58010);assert 'session' in q.notice(g).lower() and ui.s.s.document(disk,'/System/Settings/audio74.bin')==saved_audio and job(g)[0][0]
            g.qmp('stop')
            try:ui.raw_shot(g,out,'busy-provider-guards',True)
            finally:g.qmp('cont')
            active_key(g,'esc');active_click(g,p,40019);deadline=time.monotonic()+90
            while job(g)[0][0]:
                if time.monotonic()>deadline:raise TimeoutError('Real transfer cancellation')
                time.sleep(.02)
            p.drain();assert job(g)[0][8] and c.flag(g,'file_job_error11')==0,(job(g),c.flag(g,'file_job_error11'));assert '/Users/Owner/Downloads/Large.bin' not in f.entries(g);q.open_quick(g);p.desktop(58002,True);at=len(g.log());p.desktop(drive[5]+20,True);g.wait('M10_USB_SAFE_TO_REMOVE',at,90);c.shot(g,'after-cancel-safe-removal');c.key(g,'esc');t.close_all(g,p)
            assert f.sha_file(source)==source_hash;baseline=f.stats(g);q.open_quick(g);c.key(g,'esc');f.same_pages(baseline,f.stats(g));c.idle(g);report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0);report['cancel_error']=c.flag(g,'file_job_error11');(out/'native.log').write_bytes(g.log().encode())
        report['checks'].append('During an actual 64-MiB cooperative USB import, safe removal is refused and PCM changes do not write preferences; explicit Cancel completes before removal becomes available, and the complete USB source image remains byte-identical')
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:
        serial=attempt/'guest/serial.log'
        if serial.exists():(out/'native.log').write_bytes(ui.q.clean(serial.read_text(encoding='utf-8',errors='replace')).encode())
        (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
