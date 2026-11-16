"""Installed Files presentation tasks through ordinary input and owned media."""
import os,json,struct,sys,time,traceback
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE6'
import files_observe as f
c=f.c;ui=f.ui;ROOT=f.ROOT;OUT=ROOT/'build/m12/stage6/presentation-native';OUT.mkdir(parents=True,exist_ok=True);c.OUT=OUT

def tip(g):return struct.unpack('<4i',ui.memory(g,ui.symbol('files_tip_bounds12',16,True)[0],16))
def count(g):return int.from_bytes(ui.memory(g,ui.symbol('model',installed=True)[0]+232,4),'little')
def hover(g,p,action):
    x,y,w,h,_,_=c.control(g,action);f.move(g,p,x+w//2,y+h//2)
def scene(g,p):p.desktop(94,True);f.double(g,p,f.item(g,p,'Scene'));assert f.app(g)['path'].endswith('/Documents/Scene')
def text(g,p,name,value):
    action=f.item(g,p,name);p.desktop(action,True);before=count(g);c.key(g,'ret');assert count(g)==before+1
    c.type_text(g,value);c.key(g,'ctrl','s');p.desktop(49002,True);assert count(g)==before
def fixture(work):
    sys.path.insert(0,str(ROOT/'tools/local/m10-python'));from pyfatfs.PyFat import PyFat;from pyfatfs.PyFatFS import PyFatFS
    source=ui.q.sparse_disk(work/'owned-usb.img',1024**3);fat=PyFat();fat.mkfs(str(source),fat_type=PyFat.FAT_TYPE_FAT32,size=1024**3,label='M126VIEWS',volume_id=0x12600001);fat.close()
    long='W'*120+'.txt'
    with PyFatFS(str(source),preserve_case=True) as fs:
        fs.makedir('/Media');fs.writebytes('/View10.txt',b'Ten\n');fs.writebytes('/View2.txt',b'Two\n');fs.writebytes('/'+long,b'Long original name\n')
    return source,long
def stored_preferences(disk):
    usb=ui.s.s.document(disk,'/System/Settings/usb-view12-Owner.bin');assert struct.unpack('<4I',usb)==(0x36565755,1,1,0)
    data=ui.s.s.document(disk,'/System/Settings/files11.bin');n=struct.unpack_from('<I',data,12)[0];assert n<=32
    matches=[struct.unpack_from('<3I',data,24+i*268+256) for i in range(n) if data[24+i*268:24+i*268+256].split(b'\0')[0]==b'/Users/Owner/Documents/Scene']
    assert matches==[(1,0,0)],matches

def main():
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m12-stage6-presentation');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);usb,usb_long=fixture(work);usb_sha=f.sha_file(usb)
    extra=['-drive',f'if=none,id=views-source,format=raw,file={usb}'];long='W'*55+'.txt'
    natural=['Folder2','Folder10','Alpha.md','File2.txt','File10.txt','Picture.bmp','Tool.exe',long]
    report=dict(passed=False,stage='M12.6',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],owned_fixture=work.name,checks=[],profiles=[])
    try:
        live=ui.guest(work/'install',disk,extra=extra)
        with live as g:
            p=ui.Pointer(g)
            for action in (2,2,100,2,2,2):c.wizard(g,p,action)
            at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain();before=f.stats(g)
            assert 'M7_DESKTOP_READY build='+meta['build_id'] in g.log();p.desktop(94,True);f.create(g,p,'Scene',True);f.double(g,p,f.item(g,p,'Scene'))
            for name in ('Folder10','Folder2'):f.create(g,p,name,True)
            for name in ('File10.txt','File2.txt','Alpha.md','Tool.exe','Picture.bmp',long):f.create(g,p,name)
            text(g,p,'File2.txt','aaaa');text(g,p,'File10.txt','abcdefghijklmnopqrst');text(g,p,'Alpha.md','abcdefgh')
            assert f.names(g)==natural,f.names(g);assert [e['size'] for e in f.listing(g) if e['path'].endswith(('File2.txt','File10.txt'))]==[4,20]
            report['checks'].append('Real installation/retained-ISO startup; ordinary dialogs and editor saves create actual different file sizes/types; natural names put File2 before File10 with folders first')
            p.desktop(f.item(g,p,'File2.txt'),True);selected=f.selected(g);p.desktop(51001,True)
            assert f.names(g)==['Folder2','Folder10','Picture.bmp','Tool.exe',long,'File2.txt','Alpha.md','File10.txt'],f.names(g);assert f.selected(g)==selected
            p.desktop(51002,True);assert f.names(g)==['Folder2','Folder10','Picture.bmp','Tool.exe','Alpha.md','File2.txt','File10.txt',long];assert f.selected(g)==selected
            p.desktop(51002,True);assert f.names(g)==['Folder10','Folder2',long,'File10.txt','File2.txt','Alpha.md','Tool.exe','Picture.bmp'];assert f.selected(g)==selected
            p.desktop(51000,True);assert f.names(g)==natural;c.key(g,'ctrl','a');all_selected=f.selected(g);assert len(all_selected)==8;p.desktop(51001,True);assert f.selected(g)==all_selected;p.desktop(51000,True);assert f.selected(g)==all_selected;c.key(g,'esc')
            c.shot(g,'native-details');report['checks'].append('Actual sortable Name/Size/Type headers and reverse direction match displayed metadata; folders stay first, and single/multiple selection stays bound to the same source IDs')
            hover(g,p,f.item(g,p,long));assert tip(g)[2]>0;c.shot(g,'native-full-name-tip')
            original_tip_owner=f.model(g)[0];c.key(g,'ctrl','n');assert tip(g)[2]==0,('Occluded owner tip',tip(g))
            c.key(g,'alt','d');c.key(g,'ctrl','a');c.type_text(g,'Home');c.key(g,'ret');assert f.app(g)['path']=='/Users/Owner' and tip(g)[2]==0
            c.shot(g,'covered-owner-no-tip');c.key(g,'alt','f4');assert f.model(g)[0]==original_tip_owner
            hover(g,p,51000);assert tip(g)[2]==0
            assert f.has(g,41000+len('/Users/Owner/Documents')),'Visible ancestor breadcrumb missing'
            p.desktop(41000+len('/Users/Owner/Documents'),True);assert f.app(g)['path'].endswith('/Documents');p.desktop(90,True);assert f.app(g)['path'].endswith('/Scene')
            p.desktop(40012,True);assert f.view(g)==(1,0,0);p.desktop(f.item(g,p,'File2.txt'),True);c.shot(g,'native-icons');hover(g,p,f.item(g,p,long));assert tip(g)[2]>0;c.shot(g,'icon-full-name-tip');hover(g,p,40012);assert tip(g)[2]==0
            report['checks'].append('Real details/icons use original artwork, bounded two-line ellipsis and a complete measured name tip; moving away removes it without a timer')
            original=f.model(g)[0];selected=f.selected(g);original_action=f.item(g,p,'File2.txt');r=c.control(g,original_action);active=c.pixel(g,r[0]+12,r[1]+12)
            c.key(g,'ctrl','n');assert f.model(g)[0]!=original;_,(x,y,w,h)=f.model(g);f.move(g,p,x+180,y+18);p.down(True);p.drain();f.move(g,p,1080,y+18);p.down(False);p.drain()
            assert f.selected(g,original)==selected,('Inactive selection identity',f.selected(g,original),selected)
            inactive=c.pixel(g,r[0]+12,r[1]+12);assert active!=inactive,(active,inactive);c.shot(g,'inactive-selection')
            # Its caption buttons are deliberately outside the viewport after this move.
            c.key(g,'alt','f4');assert f.model(g)[0]==original,('Close moved window',f.model(g))
            report['checks'].append('Selection survives a second independent Files window; real visible inactive selection differs from active selection without stealing focus')
            p.desktop(40012,True);f.resize(g,p,500,420);assert f.view(g)[0]==0 and f.has(g,51000) and f.has(g,51001) and not f.has(g,51002)
            _,bounds=f.model(g);assert all(r[1]>=bounds[1]+184 for r in f.current_controls(g) if 1000<=r[5]<2024);c.shot(g,'minimum-details')
            f.right(g,p,bounds[0]+40,bounds[1]+155);f.menu(g,p,40013);f.menu(g,p,40032);assert f.view(g)[1:]==(2,0)
            f.right(g,p,bounds[0]+40,bounds[1]+155);f.menu(g,p,40012);assert f.view(g)[0]==1 and f.has(g,1000+f.names(g).index('File2.txt'));c.shot(g,'minimum-icons');f.resize(g,p,1080,700)
            # Restore the intended persisted native view/order through actual menus.
            p.desktop(40013,True);f.menu(g,p,40030);assert f.view(g)==(1,0,0)
            report['checks'].append('Actual 500x420 minimum keeps contents below the complete toolbar; Name/Size remain readable, Type moves to the real sort menu and both views stay reachable')
            p.desktop(21000,True);assert f.view(g)[0]==0;p.desktop(40012,True);assert f.view(g)[0]==1;c.shot(g,'no-device-icons')
            f.attach(g,p,'views-source','views-usb');drive=f.drive(g);p.desktop(drive,True);assert f.app(g)['mode']==1;c.key(g,'ret');assert f.app(g)['mode']==2
            assert not f.has(g,40013) and not f.has(g,51000);original_rows=f.usb_rows(g)[:4];assert original_rows==['Media','View10.txt','View2.txt',usb_long],original_rows
            c.key(g,'home');c.key(g,'right');assert f.app(g)['selected']==2;c.key(g,'down');assert f.app(g)['selected']==4
            c.shot(g,'usb-icons');p.desktop(40012,True);assert f.view(g)[0]==0 and f.usb_rows(g)[:4]==original_rows;c.shot(g,'usb-details')
            hover(g,p,f.row(g,usb_long));assert tip(g)[2]>0;c.shot(g,'usb-full-name-tip');hover(g,p,40012);assert tip(g)[2]==0;p.desktop(40012,True)
            c.open_settings(g,p);p.desktop(43,True);p.close_app(3,True);p.drain();assert c.dark(g)==1;c.shot(g,'dark-usb-icons');c.open_settings(g,p);p.desktop(44,True);p.close_app(3,True);p.drain()
            report['checks'].append('Actual USB objects select once/open on Enter; details/icons retain original directory order and metadata, spatial arrows reach the right item, long FAT32 names remain readable and unsupported sorting stays unavailable in both themes')
            f.resize(g,p,500,420);c.shot(g,'minimum-usb-icons');g.qmp('device_del',{'id':'views-usb'});p.drain();p.desktop(50000,True);assert not any(21200<=r[5]<21206 for r in f.current_controls(g));c.shot(g,'minimum-disconnected')
            # Home remains reachable through Places at the actual minimum size.
            p.desktop(40016,True);f.menu(g,p,40200);assert f.app(g)['mode']==0
            deadline=time.monotonic()+30
            while f.stats(g)[0]!=before[0]:
                if time.monotonic()>deadline:raise TimeoutError('Presentation/device pages did not return')
                time.sleep(.1);p.drain()
            after=f.stats(g);f.same_pages(before,after);c.idle(g);report['resources']=dict(before=list(before),after=list(after),retained_pages=after[0]-before[0]);(OUT/'install.log').write_text(g.log(),encoding='utf-8')
            report['checks'].append('Minimum-size disconnected USB retains navigation and truthful empty state; detach and view/window tasks retain zero pages/new allocation failures, with idle CPUs halted')
        stored_preferences(disk)
        for name,value in [('File2.txt',b'aaaa'),('File10.txt',b'abcdefghijklmnopqrst'),('Alpha.md',b'abcdefgh')]:assert ui.s.s.document(disk,'/Users/Owner/Documents/Scene/'+name)==value
        assert ui.s.s.document(disk,'/Users/Owner/Documents/Welcome.txt')==(ROOT/'distros/packages/m12-desktop-guide/content.txt').read_bytes()
        report['checks'].append('Independent stored bytes/CRC verify real editor contents, the bundled guide and both native and 16-byte per-user USB view preferences')
        for number in (1,2):
            boot=ui.guest(work/f'disk-{number}',disk,media='installed',ready='M7_DESKTOP_READY');ui.s.normal_boot(boot,live.folder/'vars.fd')
            with boot as g:
                p=ui.Pointer(g);p.drain();assert 'M7_DESKTOP_READY build='+meta['build_id'] in g.log();scene(g,p);assert f.view(g)==(1,0,0) and f.names(g)==natural;p.desktop(21000,True);assert f.view(g)[0]==1;c.idle(g);c.shot(g,f'disk-only-{number}');(OUT/f'disk-{number}.log').write_text(g.log(),encoding='utf-8')
        report['checks'].append('Two ordinary independent installed boots restore real native view/order and the separate USB view preference, including no-device state')
        for label,resolution,scale_action in [('150',(1920,1200),112),('4k',(3840,2160),113)]:
            with ui.guest(work/label,disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution,extra=extra) as g:
                p=ui.Pointer(g);p.drain();c.open_settings(g,p);p.desktop(scale_action,True);p.close_app(3,True);p.drain();scene(g,p);assert f.view(g)==(1,0,0);c.shot(g,'native-'+label)
                p.desktop(21000,True);f.attach(g,p,'views-source','profile-usb');c.key(g,'home');c.key(g,'ret');assert f.app(g)['mode']==2 and f.view(g)[0]==1;c.shot(g,'usb-'+label);c.idle(g);s=f.stats(g);report['profiles'].append(dict(physical=list(resolution),scale=c.flag(g,'scale73'),managed_current_bytes=s[0]*4096,managed_peak_bytes=s[1]*4096,usb_attached=True));(OUT/(label+'.log')).write_text(g.log(),encoding='utf-8')
        assert f.sha_file(usb)==usb_sha;stored_preferences(disk);report['checks'].append('Actual 150% and 3840x2160/200% native/USB icon views remain legible and idle; presentation never changes the owned USB image')
        report['passed']=True
    except Exception:
        report['error']=ui.q.clean(traceback.format_exc())
        if 'g' in locals():(OUT/'failure.log').write_text(g.log(),encoding='utf-8')
        raise
    finally:
        report['idle_observations']=c.IDLE_OBSERVATIONS;(OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
