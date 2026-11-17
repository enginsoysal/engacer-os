"""M12.18 named native device profiles, normal input and independent bytes."""
import os,json,hashlib,struct,sys,time,traceback,argparse
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE18'
import files_observe as f
import settings_observe as s
c=f.c;ui=f.ui;ROOT=f.ROOT
sys.path.insert(0,str(ROOT/'tools/build'))
from media import fat32

def main():
 a=argparse.ArgumentParser();a.add_argument('--profile',choices=['uefi','bios','low-memory','4k-hub','large-usb'],required=True);a=a.parse_args();label=a.profile
 out=ROOT/'build/m12/stage18/hardware'/label;out.mkdir(parents=True,exist_ok=True);c.OUT=out
 work=ui.q.new_work('m12-stage18-hardware-'+label);disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);usb=work/'owned-usb.img'
 firmware='bios' if label=='bios' else 'uefi';ram=64 if label=='low-memory' else 128;resolution=(3840,2160) if label=='4k-hub' else (1280,800)
 payload=bytes((i*37+11)&255 for i in range(65536+113)) if label=='large-usb' else b'Engacer OS final removable round trip.\n'
 sys.path.insert(0,str(ROOT/'tools/local/m10-python'));from pyfatfs.PyFatFS import PyFatFS
 if label=='large-usb':
  from pyfatfs.PyFat import PyFat
  ui.q.sparse_disk(usb,1024**3);writer=PyFat();writer.mkfs(str(usb),fat_type=PyFat.FAT_TYPE_FAT32,size=1024**3,label='ENGACERTEST',volume_id=0x454e4731);writer.close()
  with PyFatFS(str(usb),preserve_case=True) as fs:fs.makedirs('/EFI/BOOT');fs.writebytes('/HELLO.TXT',payload)
  with usb.open('rb') as stream:assert stream.read(512)[13]==8
 else:usb.write_bytes(fat32([(2,b'HELLO   TXT',payload)]))
 late=label=='low-memory';hub=label=='4k-hub';port={'port':'3.1'} if hub else {}
 extra=['-drive',f'if=none,id=removable,format=raw,file={usb}','-device','usb-storage,id=removable-device,bus=xhci.0,drive=removable'+(',port=3.1' if hub else '')]
 if hub:extra=['-device','usb-hub,id=hub,bus=xhci.0,port=3']+extra
 meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));report=dict(passed=False,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],profile=label,firmware=firmware,physical=list(resolution),ram_mib=ram,usb_attach_stage='after installed startup' if late else 'before firmware boot',owned_fixture=work.name,checks=[])
 try:
  candidate=ui.guest(work/'install',disk,resolution=resolution,firmware=firmware,ram=ram,extra=[] if late else extra)
  candidate.args=[v.replace('usb-kbd,bus=xhci.0','usb-kbd,id=keyboard,bus=xhci.0') for v in candidate.args]
  with candidate as g:
   p=ui.Pointer(g)
   for action in (2,2,100,2,2,2):c.wizard(g,p,action)
   at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain();c.key(g,'alt','f4');p.drain()
   assert 'M6_INSTALLED_VOLUME' in g.log()[at:];report['checks'].append('Real graphical installation and installed retained-ISO startup')
   if late:
    g.qmp('blockdev-add',{'node-name':'removable','driver':'raw','file':{'driver':'file','filename':str(usb)}});at=len(g.log());g.qmp('device_add',{'driver':'usb-storage','id':'removable-device','bus':'xhci.0','drive':'removable'});g.wait('M10_USB_WRITABLE',at,90)
   at=len(g.log());g.qmp('device_del',{'id':'keyboard'});g.wait('M45_USB_DISCONNECTED',at,90);at=len(g.log());g.qmp('device_add',{'driver':'usb-kbd','id':'keyboard-new','bus':'xhci.0'});g.wait('M4_USB_KEYBOARD_ONLINE',at,90)
   c.key(g,'ctrl','esc');assert c.flag(g,'launcher');c.key(g,'esc');assert not c.flag(g,'launcher');report['checks'].append('Actual USB keyboard reconnect and keyboard Start open/close')
   files=s.t.launch(g,p,'files',1);c.open_settings(g,p);p.desktop(59003,True);p.desktop(20000,True);p.desktop(20006,True);assert ui.integer(g,'layout10',True)==1;settings=next(w for w in s.t.records(g) if w['slot']==f.model(g)[0]);p.desktop(49000,True);p.drain()
   s.t.focus(g,p,files);p.desktop(94,True);p.desktop(26,True);c.key(g,'ctrl','a');c.key(g,'a');c.key(g,'b');c.key(g,'c');c.key(g,'ret');assert '/Users/Owner/Documents/axj' in f.entries(g)
   s.t.focus(g,p,settings);p.desktop(20005,True);assert ui.integer(g,'layout10',True)==0;c.key(g,'alt','f4');p.drain();report['checks'].append('Devices Dvorak changes actual typed folder bytes; US layout restored')
   p.desktop(21000,True);p.desktop(f.drive(g),True);c.key(g,'ret');p.desktop(f.row(g,'HELLO.TXT'),True);at=len(g.log());p.desktop(21004,True);g.wait('M12_USB_COOPERATIVE_IMPORTED',at,90);g.wait('M11_FILE_JOB_END status=0x0000000000000000',at,90);p.drain();c.shot(g,'usb-import')
   p.desktop(95,True);p.desktop(f.item(g,p,'HELLO.TXT'),True);c.key(g,'shift','f10')
   n=c.flag(g,'file_menu_count11');raw=ui.memory(g,ui.symbol('file_menu_items11',installed=True)[0],n*16);i=next(i for i in range(n) if 18000<=struct.unpack_from('<I',raw,i*16+8)[0]<19024 and struct.unpack_from('<I',raw,i*16+12)[0]);p.desktop(32000+i,True)
   p.desktop(f.drive(g),True);c.key(g,'ret');f.double(g,p,f.row(g,'EFI'));at=len(g.log());p.desktop(21005,True);g.wait('M10_USB_FILE_EXPORTED',at,90);p.drain();c.shot(g,'usb-export');report['checks'].append('Native USB import and create-only flushed export through actual Files controls')
   before=f.stats(g);at=len(g.log());p.desktop(21006,True);g.wait('M10_USB_SAFE_TO_REMOVE',at,90);g.qmp('device_del',{'id':'removable-device'});g.qmp('blockdev-add',{'node-name':'removable-again','driver':'raw','file':{'driver':'file','filename':str(usb)}});at=len(g.log());g.qmp('device_add',dict(driver='usb-storage',id='removable-reconnected',bus='xhci.0',drive='removable-again',**port));g.wait('M10_USB_WRITABLE',at,90);p.drain();p.desktop(21000,True);p.desktop(f.drive(g),True);c.key(g,'ret');after=f.stats(g);assert before[0]==after[0] and before[3]==after[3];c.idle(g);c.shot(g,'reconnected');report['resources']=dict(before=list(before),after=list(after),retained_pages=0);(out/'native.log').write_text(g.log(),encoding='utf-8')
  assert ui.s.s.document(disk,'/Users/Owner/Downloads/HELLO.TXT')==payload
  with PyFatFS(str(usb),read_only=True,preserve_case=True) as fs:assert fs.readbytes('/HELLO.TXT')==payload and fs.readbytes('/EFI/HELLO.TXT')==payload
  report['checks'].append('Independent native-volume and FAT implementations verify exact round-trip bytes and preserved original; safe removal/reconnect retains no pages')
  for turn in (1,2):
   boot=ui.guest(work/f'boot-{turn}',disk,resolution=resolution,firmware=firmware,ram=ram,media='installed',ready='M7_DESKTOP_READY');ui.s.normal_boot(boot,work/'install/vars.fd')
   with boot as g:
    p=ui.Pointer(g);p.drain();assert 'M7_DESKTOP_READY build='+meta['build_id'] in g.log() and 'M6_INSTALLED_VOLUME' in g.log();assert ui.integer(g,'layout10',True)==0;c.idle(g);c.shot(g,f'disk-only-{turn}');(out/f'disk-only-{turn}.log').write_text(g.log(),encoding='utf-8')
  report['checks'].append('Two independent disk-only starts retain actual volume and keyboard preference without forced boot order');report['payload_sha256']=hashlib.sha256(payload).hexdigest();report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
