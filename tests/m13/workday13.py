"""Exact VMware eight-real-hour gate; ordinary input, visible output and native logs.

Preflight is explicitly diagnostic and can never qualify duration. No guest RAM
writes, clock acceleration, automatic restart or user/host VM manipulation.
"""
import argparse, ctypes, hashlib, json, msvcrt, re, shutil, struct, subprocess, time, traceback, uuid, zipfile
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageChops
import vmware_stage12 as observer
from close_stage import verify_inputs_at_commit

ROOT=observer.ROOT;v=observer.v
HOURS=8*3600;IDLE=2*3600
SAVED=b'engacer stability saved baseline'
DRAFT=SAVED+b' retained unsaved text'
DOCUMENT='/Users/Owner/Documents/Note1.txt'


def utc():return datetime.now(timezone.utc).isoformat()
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def chord(g,modifier,key):
    d=g.connect_display();d.key(modifier,True)
    try:d.press(key)
    finally:d.key(modifier,False)
    g.read();time.sleep(.2)
def text(g,value):
    for char in value:
        if char.isupper():chord(g,0xffe1,ord(char.lower()))
        else:v.key(g,ord(char))
    g.read();time.sleep(.25)
def pointer(g,x,y,mask=0):g.connect_display().socket.sendall(struct.pack('!BBHH',5,mask,x,y));g.read()
def click(g,x,y,mask=1):
    pointer(g,x,y);time.sleep(.07);pointer(g,x,y,mask);time.sleep(.07);pointer(g,x,y);time.sleep(.3)
def close(g):chord(g,0xffe9,0xffc1)
def drag(g,x,y,xx,yy):
    pointer(g,x,y);time.sleep(.1);pointer(g,x,y,1);time.sleep(.1)
    pointer(g,(x+xx)//2,(y+yy)//2,1);time.sleep(.1);pointer(g,xx,yy,1);time.sleep(.2);pointer(g,xx,yy);time.sleep(.3)
def pixels(a,b,crop=None):
    with Image.open(a) as x,Image.open(b) as y:
        assert x.size==y.size
        if crop is None:crop=(100,70,x.width-100,x.height-100)
        d=ImageChops.difference(x.convert('RGB').crop(crop),y.convert('RGB').crop(crop)).convert('L')
        return d.width*d.height-d.histogram()[0]


def main():
    p=argparse.ArgumentParser();p.add_argument('--preflight',action='store_true');a=p.parse_args()
    assert not (ROOT/'evidence/M13/13/publication-results.json').exists()
    meta=json.loads((ROOT/'dist/m13stage13-build-manifest.json').read_text(encoding='utf-8'))
    starter=json.loads((ROOT/'dist/m13stage13-starter-manifest.json').read_text(encoding='utf-8'))
    archive=ROOT/'dist'/starter['archive'];assert sha(archive)==starter['sha256']
    verify_inputs_at_commit('HEAD',meta['source_sha256'])
    frozen=sha(Path(__file__));manifest=sha(ROOT/'dist/m13stage13-build-manifest.json')
    dependencies={n:sha(ROOT/n) for n in ['tests/m13/workday13.py','tests/m13/vmware_stage12.py','tests/m13/close_stage.py','tests/m10/vmware.py','tests/m9/rfb.py','tests/m71/vmware.py','tests/m7/vmware.py','tests/m7/rfb.py','tests/m6/vmware.py']}
    stamp=uuid.uuid4().hex;work=ROOT/'build/m13-native/stage13/workday'/stamp
    out=ROOT/'build/m13/stage13'/('preflight' if a.preflight else 'workday')/stamp
    work.mkdir(parents=True);out.mkdir(parents=True)
    report=dict(passed=False,diagnostic_only=a.preflight,status='starting',stage='M13.13',build_id=meta['build_id'],iso_sha256=meta['artifacts']['EngacerOS-M13STAGE13.iso']['sha256'],starter_sha256=starter['sha256'],owned_fixture=stamp,requested_seconds=HOURS,requested_uninterrupted_idle_seconds=IDLE,frames=[],launches=[],resources=[],cycles=[],idle_intervals=[],checks=[],started_at=utc(),harness_sha256=frozen,dependencies_sha256=dependencies)
    def save():
        (out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        (out.parent/'current.json').write_text(json.dumps(dict(report=(out/'results.json').relative_to(ROOT).as_posix(),owned_fixture=stamp,status=report['status']),indent=2)+'\n',encoding='utf-8')
    def frame(g,name):
        target=out/(name+'.png');v.shot(g,out,name);report['frames'].append(dict(name=name,png=target.name,sha256=sha(target),observed_at=utc(),monotonic=time.monotonic()));return target
    def launch(g,query,kind,label):
        before=frame(g,label+'-before');v.key(g,0xffeb);text(g,query);at=len(g.read());v.enter(g)
        g.wait('M7_WINDOW_OPEN app='+f'0x{kind:016x}',offset=at,timeout=30)
        deadline=time.monotonic()+10
        while True:
            after=frame(g,label+'-after');changed=pixels(before,after)
            if changed>=10000:break
            if time.monotonic()>deadline:raise AssertionError('Serial launch without visible central change: '+label)
            time.sleep(.1)
        report['launches'].append(dict(label=label,kind=kind,changed_central_pixels=changed,serial_event=True,visible=True));save()
    def resource(g,label):
        at=len(g.read());launch(g,'system monitor',6,label)
        rows=re.findall(r'M7_DESKTOP_STATS current=(0x[0-9a-f]+) peak=(0x[0-9a-f]+) allocation_failures=(0x[0-9a-f]+) paints=(0x[0-9a-f]+) pixels=(0x[0-9a-f]+) visible_framebuffer=(0x[0-9a-f]+) framebuffer_range=(0x[0-9a-f]+)',g.read()[at:])
        assert rows,'No fresh native resource record'
        row=dict(zip(['current_bytes','peak_bytes','allocation_failures','paints','pixels','visible_framebuffer_bytes','framebuffer_range_bytes'],map(lambda n:int(n,16),rows[-1])))
        row.update(label=label,observed_at=utc());report['resources'].append(row);close(g);return row
    def navigate(g,path):
        chord(g,0xffe9,ord('d'));chord(g,0xffe3,ord('a'));text(g,path);at=len(g.read());v.enter(g)
        g.wait('M125_LOCATION native '+path,offset=at,timeout=30)
    def new_folder(g,name):
        d=g.connect_display();d.key(0xffe3,True);d.key(0xffe1,True)
        try:d.press(ord('n'))
        finally:d.key(0xffe1,False);d.key(0xffe3,False)
        time.sleep(.2);chord(g,0xffe3,ord('a'));text(g,name);v.enter(g);time.sleep(.3)
    def idle(g,seconds,label,uninterrupted=False):
        began=time.monotonic();last=began;sample=began+60;changed_at=began;last_hash=None;observations=[];max_gap=0;boot_at=len(g.read())
        while time.monotonic()-began<seconds:
            now=time.monotonic();max_gap=max(max_gap,now-last);assert now-last<=15,'Host/observer gap cannot qualify uninterrupted execution';last=now
            log=g.read();assert not any(x in log for x in ['KERNEL_PANIC','KERNEL_REJECT:','LOADER_REJECT:']), 'Native failure during duration gate'
            assert not any(x in log[boot_at:] for x in ['ENGINE_OS_KERNEL_ENTRY','M7_DESKTOP_READY','M6_WIZARD_READY','M75_USER_RESTART']),'Unexpected native restart during duration gate'
            if now>=sample:
                target=frame(g,label+'-'+str(len(observations)))
                with Image.open(target) as image:clock_hash=hashlib.sha256(image.convert('RGB').crop((image.width-250,image.height-60,image.width,image.height)).tobytes()).hexdigest()
                if last_hash!=clock_hash:changed_at=now
                assert now-changed_at<180,'Visible idle clock/presentation stopped progressing'
                last_hash=clock_hash;observations.append(dict(elapsed_seconds=now-began,png=target.name,clock_region_sha256=clock_hash))
                report['elapsed_seconds']=now-report.get('gate_monotonic',began);report['status']=label;save();sample=now+60
                print(label+' real seconds '+str(int(report['elapsed_seconds']))+'/'+str(HOURS),flush=True)
            time.sleep(min(1,max(0,seconds-(time.monotonic()-began))))
        elapsed=time.monotonic()-began;report['idle_intervals'].append(dict(label=label,actual_seconds=elapsed,uninterrupted_no_input=uninterrupted,maximum_observer_gap_seconds=max_gap,observations=observations));save();return elapsed
    before=v.old.v.inventory();save()
    try:
        with zipfile.ZipFile(archive) as z:assert z.testzip() is None;z.extractall(work)
        source=work/'EngacerOS';original=(source/'EngacerOS.vmx').read_text(encoding='utf-8');g=v.Guest(work/'same-vm',source/'EngacerOS.vmdk','efi')
        g.rfb_port,report['observation_port_policy']=observer.observer_port8()
        cfg=g.vmx.read_text(encoding='utf-8');cfg=re.sub(r'(?m)^RemoteDisplay\.vnc\.port\s*=.*$','RemoteDisplay.vnc.port = '+json.dumps(str(g.rfb_port)),cfg)
        observation='\n'.join(line for line in cfg.splitlines() if line.startswith(('serial0.','RemoteDisplay.')))+'\n'
        for f in source.iterdir():shutil.copyfile(f,g.folder/f.name)
        g.vmx=g.folder/'EngacerOS.vmx';g.vmx.write_bytes((original+observation).encode('utf-8'))
        assert 'bios.bootOrder' not in original and all(x in original for x in ['ethernet0.present = "TRUE"','sound.present = "TRUE"','usb_xhci.present = "TRUE"','pciBridge4.virtualDev = "pcieRootPort"'])
        with g:
            v.enter(g);v.enter(g);v.enter(g);v.tab(g,3);v.enter(g);v.enter(g);v.enter(g);v.enter(g);g.wait('M6_INSTALL_PASS',timeout=240)
            at=len(g.read());v.enter(g);g.wait('M7_DESKTOP_READY build='+meta['build_id'],offset=at,timeout=180);g.wait('M7_DHCP_CONFIGURED',offset=at,timeout=90)
            g.rfb.close();g.rfb=None;v.key(g,0xff1b)
            boot_failures=re.findall(r'M7_DESKTOP_STATS current=0x[0-9a-f]+ peak=0x[0-9a-f]+ allocation_failures=(0x[0-9a-f]+)',g.read());assert boot_failures;report['boot_allocation_failures']=int(boot_failures[-1],16)
            d=g.connect_display();width,height=d.width,d.height;assert 1000<=width<2000 and 760<=height<1500
            report['physical']=[width,height];fw=1080 if width>1200 else width-112;fh=720 if height>900 else height-100;fx=(width-fw)//2;fy=(height-60-fh)//2
            navigate(g,'/Users/Owner/Documents')
            for i in range(24):new_folder(g,'stability-'+format(i,'02d'))
            navigate(g,'/Users/Owner/Documents/stability-00');chord(g,0xffe9,0xff52);navigate(g,'/Users/Owner/Documents');close(g)
            launch(g,'text editor',2,'seed-editor');text(g,SAVED.decode());at=len(g.read());chord(g,0xffe3,ord('s'));g.wait('M7_DOCUMENT_SAVED',offset=at)
            text(g,DRAFT[len(SAVED):].decode());pointer(g,20,20);body=frame(g,'retained-draft-seed');body_crop=(194,216,846,440)
            baseline=resource(g,'baseline');assert baseline['allocation_failures']==report['boot_allocation_failures'];report['managed_peak_budget_bytes']=baseline['peak_bytes']+8*1024**2
            def retained(label):
                pointer(g,20,20);target=frame(g,label);difference=pixels(body,target,body_crop);assert difference<=100,('Dirty document body changed',label,difference)
                return difference
            def cycle(number):
                start=time.monotonic();prefix='cycle-'+str(number);retained(prefix+'-draft-before')
                launch(g,'files',1,prefix+'-files');navigate(g,'/Users/Owner/Documents/stability-00');chord(g,0xffe9,0xff51);time.sleep(.3);navigate(g,'/Users/Owner/Documents')
                first=frame(g,prefix+'-page-before');click(g,fx+86,fy+fh-30);second=frame(g,prefix+'-page-after');assert pixels(first,second)>=500,'Visible file page did not change';click(g,fx+38,fy+fh-30)
                first=frame(g,prefix+'-menu-before');click(g,fx+fw-110,fy+fh-150,4);second=frame(g,prefix+'-menu-after');assert pixels(first,second)>=500,'Context menu did not appear';v.key(g,0xff1b)
                first=frame(g,prefix+'-move-before');drag(g,fx+220,fy+18,fx+244,fy+34);second=frame(g,prefix+'-move-after');assert pixels(first,second)>=1000,'Window did not visibly move';drag(g,fx+244,fy+34,fx+220,fy+18)
                first=frame(g,prefix+'-size-before');drag(g,fx+fw-2,fy+fh-2,fx+fw+6,fy+fh+6);second=frame(g,prefix+'-size-after');assert pixels(first,second)>=500,'Window did not visibly resize';close(g)
                launch(g,'settings',3,prefix+'-settings');sx=(width-800)//2+24;sy=(height-60-650)//2+56
                chord(g,0xffe3,ord('f'));text(g,'contrast');frame(g,prefix+'-search');click(g,sx+692,sy+54)
                before_theme=frame(g,prefix+'-theme-before');click(g,sx+234,sy+270);after_theme=frame(g,prefix+'-theme-after');assert pixels(before_theme,after_theme)>=10000,'Appearance preview did not visibly change'
                click(g,sx+258,(height-60-650)//2+650-98);click(g,sx+74,sy+270)
                at=len(g.read());click(g,sx+82,sy+496);g.wait('M11_APPEARANCE_SAVED',offset=at);close(g)
                launch(g,'calculator',4,prefix+'-calculator');close(g);difference=retained(prefix+'-retained-draft')
                memory=resource(g,prefix+'-resources');assert memory['current_bytes']==baseline['current_bytes'] and memory['allocation_failures']==baseline['allocation_failures'],('Unexplained retention/failure',memory,baseline)
                assert memory['peak_bytes']<=report['managed_peak_budget_bytes'],'Native task peak exceeded the declared baseline + 8 MiB budget'
                report['cycles'].append(dict(number=number,actual_active_seconds=time.monotonic()-start,dirty_body_changed_pixels=difference,retained_managed_bytes=0,visible_and_serial=True));save()
            cycle(0)
            report['checks'].append('Fresh exact enabled-device starter installs, retains ISO, types/saves a real original document and retains its dirty suffix through full visible file/window/menu/settings/search/preview/cancel/apply/app/resource tasks')
            if not a.preflight:
                report.update(status='uninterrupted-idle',gate_started_at=utc(),gate_monotonic=time.monotonic());save()
                idle(g,IDLE,'uninterrupted-idle',True);retained('after-two-hour-idle')
                number=1
                while time.monotonic()-report['gate_monotonic']<HOURS:
                    began=time.monotonic();cycle(number);number+=1
                    remaining=HOURS-(time.monotonic()-report['gate_monotonic'])
                    if remaining>0:idle(g,min(max(1,300-(time.monotonic()-began)),remaining),'active-idle-'+str(number))
                report['elapsed_seconds']=time.monotonic()-report['gate_monotonic'];assert report['elapsed_seconds']>=HOURS
                assert report['idle_intervals'][0]['actual_seconds']>=IDLE and len(report['cycles'])>=13
                report['checks'].append('At least eight REAL hours include two uninterrupted no-input idle hours and repeated native visible active/idle tasks; clock/presentation, independent serial launches, unchanged dirty text and zero unexplained resource retention pass')
            retained('before-final-save');at=len(g.read());chord(g,0xffe3,ord('s'));g.wait('M7_DOCUMENT_SAVED',offset=at);close(g)
            launch(g,'terminal',7,'final-readback');at=len(g.read());text(g,'cat '+DOCUMENT);v.enter(g);g.wait(DRAFT.decode(),offset=at);frame(g,'final-native-readback');close(g)
            (out/'native.log').write_text(g.read(),encoding='utf-8')
        config=g.vmx.read_text(encoding='utf-8');g.vmx.write_bytes(re.sub(r'(?im)^ide1:0.startConnected\s*=.*$','ide1:0.startConnected = "FALSE"',config).encode());g.installed=True
        report['independent_starts']=[]
        for number in range(2):
            g.output='';g.pipe=None;g.rfb=None
            with g:
                g.wait('M7_DESKTOP_READY build='+meta['build_id'],timeout=180);assert 'M6_INSTALLED_VOLUME' in g.read();v.key(g,0xff1b)
                launch(g,'terminal',7,'disk-only-'+str(number));at=len(g.read());text(g,'cat '+DOCUMENT);v.enter(g);g.wait(DRAFT.decode(),offset=at);frame(g,'disk-only-'+str(number)+'-actual-readback');(out/('disk-only-'+str(number)+'.log')).write_text(g.read(),encoding='utf-8')
            report['independent_starts'].append(dict(number=number+1,no_iso=True,ordinary_firmware=True,actual_native_readback=True))
        raw=work/'independent.img';assert raw.resolve().is_relative_to(work.resolve()) and not raw.exists()
        with raw.open('xb'):pass
        subprocess.run(['fsutil','sparse','setflag',str(raw)],capture_output=True,check=True,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        with raw.open('r+b',buffering=0) as stream:
            handle=ctypes.wintypes.HANDLE(msvcrt.get_osfhandle(stream.fileno()));assert v.workspace.api.SetFilePointerEx(handle,20*1024**3,None,0) and v.workspace.api.SetEndOfFile(handle)
        subprocess.run(['C:/Program Files/qemu/qemu-img.exe','convert','-n','--target-is-zero','-f','vmdk','-O','raw','-S','4k',str(g.folder/'EngacerOS.vmdk'),str(raw)],capture_output=True,check=True,timeout=120,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        assert observer.m.s.s.document(raw,DOCUMENT)==DRAFT
        directories=observer.m.s.directories(raw);assert all('/Users/Owner/Documents/stability-'+format(i,'02d') in directories for i in range(24))
        report['saved_document_sha256']=hashlib.sha256(DRAFT).hexdigest();report['checks'].append('Explicit final GUI Save, two independent ordinary no-ISO starts, actual native file readback and independent stopped-image CRC/data inspection preserve all exact saved/dirty bytes and created folders')
        report['preflight_successful']=True;report['passed']=not a.preflight;report['status']='diagnostic-preflight-complete' if a.preflight else 'duration-gate-passed'
    except Exception:report.update(status='failed',error=v.old.v.redact(traceback.format_exc()));raise
    finally:
        if 'g' in locals():
            target=out/('last-session-native.log' if (out/'native.log').exists() else 'native.log');target.write_text(g.output,encoding='utf-8')
        for name,digest in dependencies.items():assert sha(ROOT/name)==digest,('Qualification dependency changed',name)
        assert sha(Path(__file__))==frozen and sha(ROOT/'dist/m13stage13-build-manifest.json')==manifest and sha(archive)==starter['sha256'],'Frozen qualification bytes changed'
        after=v.old.v.inventory();deadline=time.monotonic()+20
        while 'g' in locals() and str(g.vmx) in after and time.monotonic()<deadline:time.sleep(.2);after=v.old.v.inventory()
        report['existing_vm_inventory_unchanged']=before==after;report['passed']=report['passed'] and before==after;report['completed_at']=utc();save()
        print(json.dumps({k:report.get(k) for k in ['passed','diagnostic_only','status','owned_fixture','elapsed_seconds','error']},indent=2),flush=True)


if __name__=='__main__':main()
