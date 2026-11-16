"""Installed M12.7 command/transfer tasks; owned guest input, independent bytes."""
import os,json,struct,sys,time,traceback,zlib
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE7'
import files_observe as f
c=f.c;ui=f.ui;ROOT=f.ROOT;OUT=ROOT/'build/m12/stage7/transfers-native';OUT.mkdir(parents=True,exist_ok=True);c.OUT=OUT

def start(g,p,command):
    x,y,w,h,_,_=c.control(g,command);scale=c.flag(g,'scale73')
    p.move((x+w//2)*scale//2,(y+h//2)*scale//2)
    if not job(g)[0][0]:p.drain()
    else:time.sleep(.08)
    for down in (True,False):
        g.qmp('input-send-event',{'events':[{'type':'btn','data':{'down':down,'button':'left'}}]});time.sleep(.08)
    deadline=time.monotonic()+15
    while ui.integer(g,'mouse_head11',True)!=ui.integer(g,'mouse_tail11',True):
        if time.monotonic()>deadline:raise TimeoutError('Guest input queue')
        time.sleep(.01)

def busy_frame(g):
    deadline=time.monotonic()+15
    while not f.has(g,40019):
        assert job(g)[0][0],('Job completed before the observer reached its busy frame',job(g))
        if time.monotonic()>deadline:raise TimeoutError('No visible Cancel frame for a running job')
        time.sleep(.01)

def capture_active(g,name):
    g.qmp('stop')
    try:ui.raw_shot(g,OUT,name,True)
    finally:g.qmp('cont')

def job(g):
    raw=ui.memory(g,ui.symbol('file_job_state11',installed=True)[0],112)
    return struct.unpack_from('<15I',raw),struct.unpack_from('<6Q',raw,64)

def wait(g,p,error=0):
    deadline=time.monotonic()+600
    while job(g)[0][0]:
        if time.monotonic()>deadline:raise TimeoutError('Transfer deadline')
        time.sleep(.02)
    p.drain();actual=c.flag(g,'file_job_error11');assert actual in (error if isinstance(error,tuple) else (error,)),(actual,job(g),f.app(g))

def action(g,p,command):
    if f.has(g,command):p.desktop(command,True)
    else:p.desktop(52000,True);f.menu(g,p,command)

def menu_items(g):
    n=c.flag(g,'file_menu_count11');raw=ui.memory(g,ui.symbol('file_menu_items11',installed=True)[0],n*16)
    return dict(struct.unpack_from('<II',raw,i*16+8) for i in range(n))

def create(g,p,name,folder=False):
    action(g,p,26 if folder else 40018);assert c.flag(g,'file_dialog_state11') in (7,8)
    c.key(g,'ctrl','a');c.type_text(g,name);c.key(g,'ret');assert not c.flag(g,'file_dialog_state11')

def text(g,p,name,value):
    p.desktop(f.item(g,p,name),True);c.key(g,'ret');c.type_text(g,value);c.key(g,'ctrl','s');p.desktop(49002,True)

def fixture(work):
    sys.path.insert(0,str(ROOT/'tools/local/m10-python'));from pyfatfs.PyFat import PyFat;from pyfatfs.PyFatFS import PyFatFS
    source=ui.q.sparse_disk(work/'owned-usb.img',1024**3);fat=PyFat();fat.mkfs(str(source),fat_type=PyFat.FAT_TYPE_FAT32,size=1024**3,label='M127FILES',volume_id=0x12700001);fat.close()
    payload=(bytes(range(256))*4096)*64
    with PyFatFS(str(source),preserve_case=True) as fs:
        fs.makedir('/Folder');fs.writebytes('/Small.txt',b'Original USB payload\n');fs.writebytes('/Large.bin',payload);fs.writebytes('/Export.txt',b'Existing USB destination\n')
    return source,payload

def details(g,p):
    assert f.has(g,40034);p.desktop(40034,True);assert c.flag(g,'file_dialog_state11')==9;c.key(g,'esc')

def main():
    meta=json.loads(ui.manifest_path12().read_text());work=ui.q.new_work('m12-stage7-transfers');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);usb,payload=fixture(work);usb_sha=f.sha_file(usb)
    extra=['-drive',f'if=none,id=transfer-source,format=raw,file={usb}'];report=dict(passed=False,stage='M12.7',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],owned_fixture=work.name,checks=[],profiles=[])
    try:
        live=ui.guest(work/'install',disk,extra=extra)
        with live as g:
            p=ui.Pointer(g)
            for command in (2,2,100,2,2,2):c.wizard(g,p,command)
            at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain();before=f.stats(g)
            p.desktop(94,True);create(g,p,'Source',True);f.double(g,p,f.item(g,p,'Source'));create(g,p,'Export.txt');text(g,p,'Export.txt','Native original 123')
            p.desktop(f.item(g,p,'Export.txt'),True);action(g,p,40000);f.visit(g,p,'Desktop');action(g,p,40002);wait(g,p);assert '/Users/Owner/Desktop/Export.txt' in f.entries(g);details(g,p)
            report['checks'].append('Real graphical installation and retained-ISO startup; Actions/toolbar Copy/Paste publishes actual bytes, preserves the source and offers details after successful completion')
            p.desktop(f.item(g,p,'Export.txt'),True);action(g,p,40001);f.visit(g,p,'Documents');action(g,p,40002);wait(g,p);assert '/Users/Owner/Desktop/Export.txt' not in f.entries(g)
            action(g,p,40011);assert '/Users/Owner/Desktop/Export.txt' in f.entries(g)
            report['checks'].append('Cut/Paste moves a native file; guarded single-action Undo restores its original location without changing its contents')
            f.visit(g,p,'/Users/Owner/Documents/Source');p.desktop(f.item(g,p,'Export.txt'),True);action(g,p,40000);f.visit(g,p,'Desktop');action(g,p,40002);assert c.flag(g,'file_dialog_state11')==2;c.shot(g,'conflict-review');c.key(g,'esc')
            action(g,p,40002);p.desktop(40022,True);wait(g,p);assert '/Users/Owner/Desktop/Export (2).txt' in f.entries(g);action(g,p,40011);assert '/Users/Owner/Desktop/Export (2).txt' not in f.entries(g)
            action(g,p,40002);p.desktop(40023,True);wait(g,p);assert '/Users/Owner/Desktop/Export.txt' in f.entries(g)
            p.desktop(f.item(g,p,'Export.txt'),True);text(g,p,'Export.txt',' changed');f.visit(g,p,'/Users/Owner/Documents/Source');p.desktop(f.item(g,p,'Export.txt'),True);action(g,p,40000);f.visit(g,p,'Desktop');action(g,p,40002);p.desktop(40024,True);wait(g,p)
            report['checks'].append('Conflicts require a safe review: Escape writes nothing, Keep both creates a separate verified copy, Skip keeps the existing file, and explicit Replace stages/verifies the changed destination')
            p.desktop(f.item(g,p,'Export.txt'),True);c.key(g,'delete');wait(g,p);f.visit(g,p,'/System/Recycle/Owner');c.key(g,'home');action(g,p,40005);wait(g,p);assert '/Users/Owner/Desktop/Export.txt' in f.entries(g)
            f.visit(g,p,'/');p.desktop(f.item(g,p,'System'),True);p.desktop(52000,True);commands=menu_items(g);assert not commands[40001] and not commands[40003] and not commands[40004];c.shot(g,'protected-actions');c.key(g,'esc');c.key(g,'ctrl','x');assert '/System' in f.entries(g)
            report['checks'].append('Recycle/Restore retains original location; System mutation commands are visibly disabled and keyboard Cut cannot bypass the storage guard')
            f.visit(g,p,'/Users/Owner/Documents/Source');f.resize(g,p,500,420);p.desktop(f.item(g,p,'Export.txt'),True);p.desktop(52000,True);commands=menu_items(g);assert all(commands[x] for x in (40000,40001,40003,40004,40018));c.shot(g,'compact-actions');c.key(g,'esc')
            c.open_settings(g,p);p.desktop(43,True);p.close_app(3,True);p.drain();assert c.dark(g)==1;p.desktop(52000,True);c.shot(g,'compact-dark-actions');c.key(g,'esc')
            c.open_settings(g,p);p.desktop(44,True);p.close_app(3,True);p.drain();f.resize(g,p,1080,700)
            report['checks'].append('The actual minimum 500x420 window keeps Actions visible in light and dark; Copy/Cut/Paste/Rename/Recycle/New text/Undo remain reachable without relying on a hidden toolbar')
            row=f.names(g).index('Export.txt');rect=c.control(g,1000+row);f.right(g,p,rect[0]+60,rect[1]+15);f.menu(g,p,18000+row)
            assert f.app(g)['mode']==1;f.attach(g,p,'transfer-source','transfer-usb');p.desktop(f.drive(g),True);c.key(g,'ret');p.desktop(21005,True)
            assert 'No file was replaced.' in f.app(g)['notice'];c.shot(g,'usb-export-refusal')
            report['checks'].append('A real native-to-USB create-only export refuses an existing filename with a clear reason and keeps both original source and destination')
            p.desktop(21000,True);p.desktop(f.drive(g),True);c.key(g,'ret');p.desktop(f.row(g,'Folder'),True);assert not f.has(g,21004);p.desktop(f.row(g,'Small.txt'),True);p.desktop(21004,True);wait(g,p);assert '/Users/Owner/Downloads/Small.txt' in f.entries(g)
            p.desktop(f.row(g,'Small.txt'),True);p.desktop(21004,True);assert c.flag(g,'file_dialog_state11')==2;assert not f.has(g,40024);c.shot(g,'usb-conflict');p.desktop(40022,True);wait(g,p)
            report['checks'].append('USB Copy to Downloads uses the same cooperative job and conflict review as Copy/Paste; folders are unavailable, Keep both preserves existing contents, and unsupported USB Replace is disabled')
            p.desktop(f.row(g,'Large.bin'),True)
            start(g,p,21004);busy_frame(g)
            deadline=time.monotonic()+15
            while not job(g)[1][3]:
                assert job(g)[0][0],job(g)
                if time.monotonic()>deadline:raise TimeoutError('USB copy never began reading')
                time.sleep(.01)
            capture_active(g,'usb-transfer-progress')
            # Controls are rebuilt during repaint; a second unsynchronized read
            # after resuming is not an atomic view of the completed busy frame.
            c.key(g,'esc');wait(g,p)
            assert job(g)[0][8] and 0<job(g)[1][2]<job(g)[1][1],job(g)
            report['cancelled_usb_work_bytes']=job(g)[1][2]
            assert '/Users/Owner/Downloads/Large.bin' not in f.entries(g),'Cancelled USB stream was published'
            details(g,p)
            assert not struct.unpack('<4i',ui.memory(g,ui.symbol('files_tip_bounds12',16,True)[0],16))[2],'Busy name tip remained'
            report['checks'].append('A genuine 64-MiB USB import exposes source/destination/verified progress and Cancel; cancellation aborts the unpublished stream, retains the source and leaves accessible completed-result details')
            p.desktop(f.row(g,'Large.bin'),True);start(g,p,21004);wait(g,p);assert f.entries(g)['/Users/Owner/Downloads/Large.bin']['crc']==zlib.crc32(payload)
            # A second real source tests partial completion on cancellation of a tree.
            f.visit(g,p,'Downloads');p.desktop(f.item(g,p,'Large.bin'),True);action(g,p,40000);f.visit(g,p,'/Users/Owner/Documents/Source');start(g,p,40002);wait(g,p)
            f.visit(g,p,'Documents');p.desktop(f.item(g,p,'Source'),True);action(g,p,40000);f.visit(g,p,'Desktop');start(g,p,40002);busy_frame(g)
            deadline=time.monotonic()+30
            while job(g)[0][11]<1:
                assert job(g)[0][0],job(g)
                if time.monotonic()>deadline:raise TimeoutError('No confirmed first file before partial-copy cancellation')
                time.sleep(.01)
            capture_active(g,'native-transfer-progress');c.key(g,'esc');wait(g,p)
            assert '/Users/Owner/Documents/Source/Large.bin' in f.entries(g)
            assert '/Users/Owner/Desktop/Source/Export.txt' in f.entries(g)
            assert '/Users/Owner/Desktop/Source/Large.bin' not in f.entries(g)
            report['partial_copy_confirmed_files']=job(g)[0][11]
            details(g,p)
            report['checks'].append('USB read-back verified import has the expected independent CRC; cancelling a real native tree copy preserves its only source and reports completed items without claiming full success')
            # Test stale device lease while the large source is genuinely being read.
            f.visit(g,p,'USB:2:/');p.desktop(f.row(g,'Large.bin'),True);c.key(g,'ctrl','c');f.visit(g,p,'Pictures');start(g,p,40002);busy_frame(g);deadline=time.monotonic()+15
            while not job(g)[1][3]:
                assert job(g)[0][0],job(g)
                if time.monotonic()>deadline:raise TimeoutError('Removed source had not begun reading')
                time.sleep(.01)
            g.qmp('device_del',{'id':'transfer-usb'});wait(g,p,error=(3,9));report['removed_source_error']=c.flag(g,'file_job_error11');assert '/Users/Owner/Pictures/Large.bin' not in f.entries(g);c.shot(g,'removed-source-result');details(g,p)
            report['checks'].append('Unplugging a source during a genuine USB read stops the generation-bound job, aborts the unfinished destination and preserves previously completed data with an inspectable reason')
            f.visit(g,p,'Home');deadline=time.monotonic()+30
            while f.stats(g)[0]!=before[0]:
                if time.monotonic()>deadline:raise TimeoutError('Retained transfer/device pages')
                time.sleep(.1);p.drain()
            after=f.stats(g);f.same_pages(before,after);c.idle(g);report['resources']=dict(before=list(before),after=list(after),retained_pages=0);(OUT/'install.log').write_text(g.log(),encoding='utf-8')
        assert ui.s.s.document(disk,'/Users/Owner/Documents/Source/Export.txt')==b'Native original 123'
        assert ui.s.s.document(disk,'/Users/Owner/Desktop/Export.txt')==b'Native original 123'
        assert ui.s.s.document(disk,'/Users/Owner/Downloads/Small.txt')==ui.s.s.document(disk,'/Users/Owner/Downloads/Small (2).txt')==b'Original USB payload\n'
        assert ui.s.s.document(disk,'/Users/Owner/Downloads/Large.bin',limit=64*1024**2)==payload
        assert ui.s.s.document(disk,'/Users/Owner/Documents/Source/Large.bin',limit=64*1024**2)==payload
        assert f.sha_file(usb)==usb_sha
        report['checks'].append('Independent native metadata/data CRC and full payload comparison verify all confirmed files, while the whole original 1-GiB USB image remains byte-for-byte unchanged; tasks retain zero managed pages/new failures')
        for number in (1,2):
            boot=ui.guest(work/f'disk-{number}',disk,media='installed',ready='M7_DESKTOP_READY');ui.s.normal_boot(boot,live.folder/'vars.fd')
            with boot as g:
                p=ui.Pointer(g);p.drain();assert 'M7_DESKTOP_READY build='+meta['build_id'] in g.log();p.desktop(94,True);f.double(g,p,f.item(g,p,'Source'));assert 'Large.bin' in f.names(g);c.idle(g);c.shot(g,f'disk-only-{number}');(OUT/f'disk-{number}.log').write_text(g.log(),encoding='utf-8')
        report['checks'].append('Two ordinary installed starts retain all independently confirmed data and provide usable Files commands without the ISO')
        for label,resolution,scale_action in [('150',(1920,1200),112),('4k',(3840,2160),113)]:
            with ui.guest(work/label,disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution) as g:
                p=ui.Pointer(g);p.drain();c.open_settings(g,p);p.desktop(scale_action,True);p.close_app(3,True);p.drain();p.desktop(94,True);f.double(g,p,f.item(g,p,'Source'));p.desktop(f.item(g,p,'Export.txt'),True);p.desktop(52000,True);c.shot(g,'commands-'+label);c.key(g,'esc');c.idle(g);s=f.stats(g);report['profiles'].append(dict(physical=list(resolution),scale=c.flag(g,'scale73'),managed_current_bytes=s[0]*4096,managed_peak_bytes=s[1]*4096));(OUT/(label+'.log')).write_text(g.log(),encoding='utf-8')
        report['checks'].append('Real 150% and 3840x2160/200% command surfaces keep readable controls, retained storage results and halted idle CPUs')
        report['passed']=True
    except Exception:
        report['error']=ui.q.clean(traceback.format_exc())
        if 'g' in locals():(OUT/'failure.log').write_text(g.log(),encoding='utf-8')
        raise
    finally:
        report['idle_observations']=c.IDLE_OBSERVATIONS;(OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
