"""Installed common Files/provider tasks through normal guest input and owned media."""
import ctypes,json,os,struct,sys,time,traceback,hashlib
from pathlib import Path
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE5'
import components as c
from focus_ownership import View
ui=c.ui;ROOT=ui.ROOT;OUT=ROOT/'build/m12/stage5/files-native';OUT.mkdir(parents=True,exist_ok=True);c.OUT=OUT

def model(g):
    base=ui.symbol('model',installed=True)[0];slot=int.from_bytes(ui.memory(g,base+236,4),'little');assert slot<8
    return slot,struct.unpack('<4i',ui.memory(g,base+slot*28,16))
def app(g,slot=None):
    if slot is None:slot=model(g)[0]
    address,size=ui.symbol('apps',installed=True);raw=ui.memory(g,address+slot*(size//8)+ctypes.sizeof(View),1164)
    values=struct.unpack_from('<6I',raw,628)
    return dict(slot=slot,path=raw[:256].split(b'\0')[0].decode(),notice=raw[256:352].split(b'\0')[0].decode(),offset=struct.unpack_from('<I',raw,356)[0],mode=values[1],disk=values[2],part=values[3],context=values[4],selected=values[5],usb_path=raw[652:908].split(b'\0')[0].decode())
def controls(g):
    count=ui.integer(g,'control_count',True);raw=ui.memory(g,ui.symbol('controls',65536,True)[0],count*32)
    return [struct.unpack_from('<iiiiQI',raw,i*32) for i in range(count)]
def current_controls(g):
    slot=model(g)[0];return [r for r in controls(g) if r[4]&0xffffffff==slot+1]
def has(g,action):return any(r[5]==action for r in current_controls(g))
def history(g):
    raw=ui.memory(g,ui.symbol('navigation',8*2216,True)[0]+model(g)[0]*2216,2216);count,position=struct.unpack_from('<II',raw,2208)
    assert count<=8 and position<count
    return dict(count=count,position=position,locations=[dict(zip(('path','provider','disk','context','part','offset'),(path.split(b'\0')[0].decode(),*values))) for path,*values in struct.iter_unpack('<256s5I',raw[:count*276])])
def address(g):
    address,size=ui.symbol('file_windows11',installed=True);stride=size//8;assert stride==296
    raw=ui.memory(g,address+model(g)[0]*stride,stride)
    return raw[16:288].split(b'\0')[0].decode(),struct.unpack_from('<I',raw,12)[0]
def type_text(g,text):
    for ch in text:
        if ch==':':c.key(g,'shift','semicolon')
        else:c.type_text(g,ch)
def visit(g,p,text):
    p.desktop(40015,True);c.key(g,'ctrl','a');type_text(g,text);c.key(g,'ret');p.drain()
def usb_rows(g):
    raw=ui.memory(g,ui.symbol('usb_rows10',6*264,True)[0],6*264)
    return [name.split(b'\0')[0].decode() for name,kind,size in struct.iter_unpack('<256sII',raw)]
def row(g,name):
    values=usb_rows(g);index=values.index(name);assert index<6 and has(g,21200+index),(name,values);return 21200+index
def drive(g):return next(r[5] for r in current_controls(g) if 21100<=r[5]<21116)
def double(g,p,action):
    x,y,w,h,_,_=c.control(g,action);scale=c.flag(g,'scale73');p.move((x+w//2)*scale//2,(y+h//2)*scale//2);p.drain();start=time.monotonic()
    for down in (True,False,True,False):g.qmp('input-send-event',{'events':[{'type':'btn','data':{'down':down,'button':'left'}}]});time.sleep(.06)
    assert time.monotonic()-start<.5,'Host did not deliver the double-click in time';p.drain()
def stats(g):return struct.unpack('<4Q',ui.memory(g,ui.symbol('stats',32,True)[0],32))
def same_pages(a,b):assert a[0]==b[0] and a[3]==b[3],(a,b)
def attach(g,p,node,identity):
    at=len(g.log());g.qmp('device_add',{'driver':'usb-storage','id':identity,'bus':'xhci.0','drive':node});g.wait('M10_USB_WRITABLE',at,90);p.drain()
def wait_selected_clear(g,p):
    deadline=time.monotonic()+30
    while app(g)['selected']:
        if time.monotonic()>deadline:raise TimeoutError('Removed drive selection was retained')
        time.sleep(.05);p.drain()
def sha_file(path):
    digest=hashlib.sha256()
    with path.open('rb') as stream:
        for data in iter(lambda:stream.read(1024**2),b''):digest.update(data)
    return digest.hexdigest()
def fixture(work):
    sys.path.insert(0,str(ROOT/'tools/local/m10-python'))
    from pyfatfs.PyFat import PyFat
    from pyfatfs.PyFatFS import PyFatFS
    usb=ui.q.sparse_disk(work/'owned-usb.img',1024**3);writer=PyFat();writer.mkfs(str(usb),fat_type=PyFat.FAT_TYPE_FAT32,size=1024**3,label='M125FILES',volume_id=0x12500001);writer.close()
    long_path='/'+'/'.join('x'*62 for _ in range(4));payload=b'Owned M12.5 provider input\n'
    with PyFatFS(str(usb),preserve_case=True) as fs:
        fs.makedirs('/Games/Arcade');fs.writebytes('/Games/Arcade/HELLO.TXT',payload)
        for i in range(15):fs.writebytes('/PAGE%02d.TXT'%i,b'Page item\n')
        fs.makedirs(long_path)
    sys.path.insert(0,str(ROOT/'tools/build'));from media import fat32
    other=work/'owned-replacement.img';other.write_bytes(fat32([(2,b'OTHER   TXT',b'Different owned device\n')]))
    return usb,other,long_path,payload

def main():
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m12-stage5-files');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
    usb,other,long_path,payload=fixture(work);original_usb=sha_file(usb);original_other=sha_file(other)
    report=dict(passed=False,stage='M12.5',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],owned_fixture=work.name,checks=[],profiles=[])
    extra=['-drive',f'if=none,id=files-source,format=raw,file={usb}']
    try:
        live=ui.guest(work/'install',disk,extra=extra)
        with live as g:
            p=ui.Pointer(g)
            for action in (2,2,100,2,2,2):c.wizard(g,p,action)
            at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain()
            assert 'M7_DESKTOP_READY build='+meta['build_id'] in g.log();baseline=stats(g)
            assert app(g)['mode']==0 and history(g)['count']==1 and not has(g,90) and not has(g,91)
            p.desktop(94,True);assert app(g)['path']=='/Users/Owner/Documents'
            p.desktop(21000,True);assert app(g)['mode']==1 and has(g,90) and not has(g,24) and has(g,50000)
            c.shot(g,'no-device-common-frame');p.desktop(90,True);assert app(g)['mode']==0 and app(g)['path'].endswith('/Documents');p.desktop(91,True);assert app(g)['mode']==1
            p.desktop(92,True);assert app(g)['mode']==0;visit(g,p,'/Applications');assert has(g,47000)
            p.desktop(21000,True);assert not has(g,47000);c.key(g,'home');c.key(g,'end');assert app(g)['offset']==0
            same_pages(baseline,stats(g));report['checks'].append('Real installed startup and a single common frame retain Back/Forward/Home/Refresh in no-device state; hidden native scrollbars cannot steal USB keys')
            attach(g,p,'files-source','files-usb');p.desktop(21000,True);command=drive(g);p.desktop(command,True);assert app(g)['mode']==1 and app(g)['selected']==command-21100+1
            c.key(g,'ret');assert app(g)['mode']==2 and app(g)['usb_path']=='/';leased=app(g)['context'];attached=stats(g)
            assert has(g,99);p.desktop(99,True);assert app(g)['offset']>0;offset=app(g)['offset'];p.desktop(94,True);p.desktop(90,True);assert app(g)['mode']==2 and app(g)['offset']==offset;p.desktop(98,True);assert app(g)['offset']==0
            report['checks'].append('USB drive objects select once and Enter opens their actual lease; item pages and native/USB history restore the prior scroll offset')
            double(g,p,row(g,'Games'));assert app(g)['usb_path']=='/Games';p.desktop(row(g,'Arcade'),True);assert app(g)['usb_path']=='/Games';c.key(g,'ret');assert app(g)['usb_path']=='/Games/Arcade'
            p.desktop(row(g,'HELLO.TXT'),True);assert app(g)['usb_path']=='/Games/Arcade';p.desktop(21004,True);assert 'Copied to Downloads' in app(g)['notice'];c.shot(g,'usb-folder-common-frame')
            p.desktop(24,True);assert app(g)['usb_path']=='/Games';p.desktop(50001,True);assert app(g)['usb_path']=='/';p.desktop(90,True);assert app(g)['usb_path']=='/Games';p.desktop(91,True);assert app(g)['usb_path']=='/'
            report['checks'].append('Real FAT32 folders obey single-select/double-click/Enter; copy-to-Downloads, Up, drive-root breadcrumbs and Back/Forward use the same frame')
            uri='USB:'+str(app(g)['disk']+1)+':'+long_path;assert len(uri)>255
            visit(g,p,uri);assert app(g)['usb_path']==long_path;p.desktop(40015,True);assert address(g)[0]==uri;c.key(g,'ctrl','a');c.key(g,'ctrl','c');c.key(g,'esc')
            p.desktop(94,True);p.desktop(40015,True);c.key(g,'ctrl','a');c.key(g,'ctrl','v');assert address(g)[0]==uri;c.key(g,'ret');assert app(g)['mode']==2 and app(g)['usb_path']==long_path
            p.desktop(40015,True);c.key(g,'ctrl','a');c.key(g,'ctrl','v');c.key(g,'home')
            for _ in range(len('USB:'+str(app(g)['disk']+1)+':')):c.key(g,'delete')
            c.key(g,'end');type_text(g,'zzzz');assert len(address(g)[0])==256;c.key(g,'ret');assert app(g)['usb_path']==long_path and address(g)[1];c.key(g,'esc');c.shot(g,'long-usb-address')
            report['checks'].append('A real 258-byte USB address survives edit/copy/paste and cross-provider navigation; an overlong native address preserves the prior location and remains editable')
            original_slot=model(g)[0];before_history=history(g);c.key(g,'ctrl','n');assert model(g)[0]!=original_slot and app(g)['usb_path']==long_path and history(g)['count']==1
            p.desktop(92,True);assert app(g)['mode']==0 and app(g,original_slot)['usb_path']==long_path;p.desktop(49002,True);assert model(g)[0]==original_slot and history(g)==before_history
            same_pages(attached,stats(g));report['checks'].append('Ctrl+N copies the real provider into an independent bounded history; closing that window preserves its original owner and retains no pages')
            p.desktop(50001,True);c.key(g,'ctrl','n');assert history(g)['count']==1;old_context=app(g)['context'];p.desktop(21000,True);p.desktop(drive(g),True);assert app(g)['selected']
            g.qmp('device_del',{'id':'files-usb'});wait_selected_clear(g,p)
            g.qmp('blockdev-add',{'node-name':'files-replacement','driver':'raw','file':{'driver':'file','filename':str(other)}});attach(g,p,'files-replacement','files-usb-new')
            c.key(g,'ret');assert app(g)['mode']==1,'A replaced drive inherited an old selection'
            p.desktop(90,True);assert app(g)['context']==old_context and app(g)['mode']==2;assert not any(21200<=r[5]<21206 for r in current_controls(g));p.desktop(50000,True);assert app(g)['context']==old_context;c.shot(g,'disconnected-history')
            p.desktop(91,True);c.key(g,'home');c.key(g,'ret');assert app(g)['context']!=old_context and 'OTHER.TXT' in usb_rows(g);new_context=app(g)['context'];assert app(g,original_slot)['context']==old_context
            p.desktop(90,True);p.desktop(90,True);assert app(g)['context']==old_context and not any(21200<=r[5]<21206 for r in current_controls(g));p.desktop(91,True);p.desktop(91,True);assert app(g)['context']==new_context
            same_pages(attached,stats(g));report['checks'].append('Actual detach/replacement clears drive selection; stale generation history and Refresh never retarget the new device, while explicit re-selection opens its different real contents in only that window')
            p.desktop(21006,True);g.wait('M10_USB_SAFE_TO_REMOVE');g.qmp('device_del',{'id':'files-usb-new'});p.desktop(49002,True);p.desktop(92,True)
            deadline=time.monotonic()+30
            while stats(g)[0]!=baseline[0]:
                if time.monotonic()>deadline:raise TimeoutError('USB driver pages did not return after physical detach')
                time.sleep(.1);p.drain()
            after=stats(g);same_pages(baseline,after);c.idle(g);report['resources']=dict(before=list(baseline),after=list(after),attached_before=list(attached),retained_pages=after[0]-baseline[0]);c.shot(g,'native-home-after-detach');(OUT/'install.log').write_text(g.log(),encoding='utf-8')
            report['checks'].append('Safe remove plus physical detach releases device pages; browsing, long addresses and multiple windows retain zero pages and no new allocation failures; idle CPUs halt')
        assert ui.s.s.document(disk,'/Users/Owner/Downloads/HELLO.TXT')==payload
        assert ui.s.s.document(disk,'/Users/Owner/Documents/Welcome.txt')==(ROOT/'distros/packages/m12-desktop-guide/content.txt').read_bytes()
        assert sha_file(usb)==original_usb and sha_file(other)==original_other
        report['checks'].append('Independent stored bytes/CRC verify the imported original file and bundled guide; both owned USB images remain byte-identical after browsing/import')
        for number in (1,2):
            boot=ui.guest(work/f'disk-{number}',disk,media='installed',ready='M7_DESKTOP_READY');ui.s.normal_boot(boot,live.folder/'vars.fd')
            with boot as g:
                p=ui.Pointer(g);p.drain();assert 'M7_DESKTOP_READY build='+meta['build_id'] in g.log();p.desktop(94,True);p.desktop(21000,True);p.desktop(90,True);assert app(g)['path'].endswith('/Documents');c.idle(g);c.shot(g,f'disk-only-{number}');(OUT/f'disk-{number}.log').write_text(g.log(),encoding='utf-8')
        report['checks'].append('Two ordinary independent installed starts preserve real data and the common provider navigation without forced boot order')
        for label,resolution,scale_action in [('150',(1920,1200),112),('4k',(3840,2160),113)]:
            with ui.guest(work/label,disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution,extra=extra) as g:
                p=ui.Pointer(g);p.drain();assert 'M7_DESKTOP_READY build='+meta['build_id'] in g.log();c.open_settings(g,p);p.desktop(scale_action,True);p.close_app(3,True);p.drain();assert c.flag(g,'scale73')==(3 if label=='150' else 4)
                p.desktop(21000,True);c.shot(g,'native-'+label+'-no-device');attach(g,p,'files-source','profile-usb');c.key(g,'home');c.key(g,'ret');double(g,p,row(g,'Games'));assert app(g)['usb_path']=='/Games';c.shot(g,'native-'+label);c.idle(g);s=stats(g);report['profiles'].append(dict(physical=list(resolution),scale=c.flag(g,'scale73'),managed_current_bytes=s[0]*4096,managed_peak_bytes=s[1]*4096,usb_attached=True));(OUT/(label+'.log')).write_text(g.log(),encoding='utf-8')
        report['checks'].append('Actual 150% and 3840x2160/200% frames exercise both no-device and real USB folder navigation, with native Inter/vector graphics and idle halt')
        report['passed']=True
    except Exception:
        report['error']=ui.q.clean(traceback.format_exc())
        if 'g' in locals():(OUT/'failure.log').write_text(g.log(),encoding='utf-8')
        raise
    finally:
        report['idle_observations']=c.IDLE_OBSERVATIONS;(OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
