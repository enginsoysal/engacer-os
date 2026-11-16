"""Native file/USB identity binding and missing-type fallback on an owned install."""
import json
import os
from pathlib import Path
import sys
import traceback
from PIL import Image
import icons_native as n

c=n.c;ui=n.ui;ROOT=n.ROOT;OUT=ROOT/'build/m12/stage2/icons-files';OUT.mkdir(parents=True,exist_ok=True);c.OUT=OUT
sys.path.insert(0,str(ROOT/'tools/build'))
from media import fat32

def visit(g,p,path):
    p.desktop(40015,True);c.key(g,'ctrl','a');c.type_text(g,path);c.key(g,'ret');p.drain()

def main():
    meta=json.loads(ui.manifest_path12().read_text());native=json.loads((ROOT/'build/m12/stage2/icons-native/results.json').read_text())
    assert native['passed'] and native['build_id']==meta['build_id']
    base=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage2-icons';disk=base/native['owned_fixture']/'owned.img'
    assert disk.resolve().is_relative_to(base.resolve()) and disk.is_file()
    work=ui.q.new_work('m12-stage2-file-icons');usb=work/'owned-usb.img'
    usb.write_bytes(fat32([(2,b'HELLO   TXT',b'Owned icon test\n'),(2,b'COLOR   BMP',(ROOT/'distros/packages/apps-guide/ColorStudy.bmp').read_bytes()),(2,b'CHIME   WAV',(ROOT/'distros/packages/apps-guide/Chime.wav').read_bytes()),(2,b'SAMPLE  ZIP',(ROOT/'distros/packages/apps-guide/ArchiveSample.zip').read_bytes()),(2,b'UNKNOWN BIN',b'\0\1\2\3')]))
    extra=['-drive',f'if=none,id=removable,format=raw,file={usb}','-device','usb-storage,id=icon-usb,bus=xhci.0,drive=removable']
    report=dict(passed=False,stage='M12.2',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],comparisons=[],checks=[])
    try:
        with ui.guest(work/'files',disk,media='installed',ready='M7_DESKTOP_READY',resolution=(1280,800),extra=extra) as g:
            assert 'M7_DESKTOP_READY build='+meta['build_id'] in g.log()
            p=ui.Pointer(g);p.drain();baseline=n.windows(g)
            for folder,numbers in [('Documents',[22]),('Pictures',[23]),('Music',[24]),('Downloads',[26,25])]:
                visit(g,p,'/Users/Owner/'+folder);name=folder.lower();c.shot(g,name)
                rows=sorted((r for r in n.controls(g) if 1000<=r[5]<2024),key=lambda r:r[5]);assert len(rows)==len(numbers),(folder,len(rows))
                with Image.open(OUT/(name+'.png')) as image:
                    for row,number in zip(rows,numbers):
                        x,y,w,h,token,action=row
                        result=n.compare_icon(image.convert('RGB'),ROOT/'build/m12/stage2/icons-host.exe',number,x+10,y+5,24,c.flag(g,'scale73'),c.dark(g))
                        report['comparisons'].append(dict(surface='native-'+folder,**result))
            before=c.flag(g,'icon12_fallbacks',8);visit(g,p,'/System/Settings');c.shot(g,'unknown-file-type')
            assert c.flag(g,'icon12_fallbacks',8)>before
            row=next(r for r in n.controls(g) if r[5]==1000);x,y,*_=row
            with Image.open(OUT/'unknown-file-type.png') as image:
                report['comparisons'].append(dict(surface='native-unknown',**n.compare_icon(image.convert('RGB'),ROOT/'build/m12/stage2/icons-host.exe',0,x+10,y+5,24,2,c.dark(g))))
            assert n.windows(g)==baseline
            report['checks'].append('Native text/BMP/WAV/ZIP icons and an actual unknown binary file match physical host rows; browsing does not launch an app')
            g.wait('M10_USB_WRITABLE');p.desktop(21000,True);c.shot(g,'usb-drives');p.desktop(21101,True);c.shot(g,'usb-file-types')
            with Image.open(OUT/'usb-file-types.png') as source:
                image=source.convert('RGB')
                for index,number in enumerate([20,22,23,24,25,0]):
                    x,y,*_=c.control(g,21200+index)
                    report['comparisons'].append(dict(surface='usb-row-'+str(index),**n.compare_icon(image,ROOT/'build/m12/stage2/icons-host.exe',number,x+12,y+8,24,2,c.dark(g))))
            assert n.windows(g)==baseline;p.desktop(21006,True);g.wait('M10_USB_SAFE_TO_REMOVE');c.shot(g,'safe-removal')
            p.desktop(21001,True);c.open_settings(g,p);p.desktop(20000,True);c.shot(g,'devices')
            c.idle(g);(OUT/'journey.log').write_bytes(g.log().encode())
            report['checks'].append('Actual FAT32 USB folder/text/BMP/WAV/ZIP/unknown rows use the same shared art; safe removal confirms flush and Devices retains capability text')
        for folder,name in [('Documents','Welcome.txt'),('Pictures','ColorStudy.bmp'),('Music','Chime.wav'),('Downloads','ArchiveSample.zip')]:
            assert ui.s.s.document(disk,'/Users/Owner/'+folder+'/'+name)
        report['checks'].append('Independent metadata-bank/file CRC inspection confirms all four native sample files remain intact')
        report['passed']=True
    except Exception:
        report['error']=ui.q.clean(traceback.format_exc());raise
    finally:
        (OUT/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
