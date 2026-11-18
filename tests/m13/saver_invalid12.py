"""Real native refusal of CRC-valid malformed optional screensaver records."""
import hashlib,json,os,struct,traceback,zlib
from pathlib import Path
import saver_native12 as n
from access_fixtures16 import clone
c=n.c;f=n.f;h=n.h;t=n.t;ui=n.ui;ROOT=n.ROOT


def replace_record(disk,payload):
    assert disk.resolve().is_relative_to((Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6').resolve())
    with disk.open('r+b') as stream:
        stream.seek(512);gpt=stream.read(512);assert gpt[:8]==b'EFI PART';stream.seek(struct.unpack_from('<Q',gpt,72)[0]*512);table=stream.read(16384);start=struct.unpack_from('<Q',table,4*128+32)[0]*512;changed=0
        for bank in range(2):
            offset=start+bank*71*4096;stream.seek(offset);head=bytearray(stream.read(4096));entries=bytearray(stream.read(1024*280))
            if head[:8]!=b'ENGINEV6' or zlib.crc32(head[:4092])!=struct.unpack_from('<I',head,4092)[0]:continue
            assert zlib.crc32(entries)==struct.unpack_from('<I',head,36)[0]
            for index in range(1024):
                row=index*280
                if entries[row:row+256].split(b'\0')[0].decode()!=n.PATH:continue
                first,size,crc,kind=struct.unpack_from('<QQII',entries,row+256);assert kind==1 and len(payload)<=4096;stream.seek(start+first*4096);stream.write(payload);struct.pack_into('<Q',entries,row+264,len(payload));struct.pack_into('<I',entries,row+272,zlib.crc32(payload));changed+=1
            struct.pack_into('<I',head,36,zlib.crc32(entries));struct.pack_into('<I',head,4092,zlib.crc32(head[:4092]));stream.seek(offset);stream.write(head);stream.write(entries)
    assert changed and ui.s.s.document(disk,n.PATH)==payload;return changed


def main():
    out=ROOT/'build/m13/stage12/screensaver-invalid';out.mkdir(parents=True,exist_ok=True);c.OUT=out;meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m13/stage12/screensaver-native/results.json').read_text(encoding='utf-8'));assert base['passed'] and base['build_id']==meta['build_id']
    source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m1312-saver'/base['owned_fixture']/'owned.img';original=f.sha_file(source)
    report=dict(passed=False,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],checks=[],cases=[])
    try:
        good=[0x31325345,1,1,60,0];cases=[]
        for label,index,value in [('magic',0,0),('version',1,2),('enabled',2,2),('timeout',3,0),('style',4,3)]:
            fields=good.copy();fields[index]=value;cases.append((label,struct.pack('<5I',*fields)))
        data=struct.pack('<5I',*good);cases.extend([('short',data[:16]),('long',data+b'x')])
        for label,payload in cases:
            work,disk,cloned=clone(ui,source,'m1312-invalid');welcome=ui.s.s.document(disk,'/Users/Owner/Documents/Welcome.txt');changed=replace_record(disk,payload);before=f.sha_file(disk)
            with ui.guest(work/'refused',disk,media='installed',ready='M7_DESKTOP_READY') as g:
                p=ui.Pointer(g);p.drain();assert c.flag(g,'saver_invalid21') and n.saved(g)==(0x31325345,1,0,60,0);n.open_saver(g,p);c.shot(g,'safe-'+label);assert f.sha_file(disk)==before
                p.desktop(60212,True);p.desktop(60210,True);assert not c.flag(g,'saver_invalid21');replacement=struct.pack('<5I',0x31325345,1,0,60,0);assert ui.s.s.document(disk,n.PATH)==replacement;h.close(g,p);c.idle(g)
            with ui.guest(work/'valid-startup',disk,media='installed',ready='M7_DESKTOP_READY') as g:
                p=ui.Pointer(g);p.drain();assert not c.flag(g,'saver_invalid21') and n.saved(g)==struct.unpack('<5I',replacement);c.idle(g)
            assert ui.s.s.document(disk,'/Users/Owner/Documents/Welcome.txt')==welcome
            report['cases'].append(dict(name=label,bytes=len(payload),valid_filesystem_banks=changed,clone=cloned,replacement_hex=replacement.hex()));print('PASS actual semantic refusal and defaults: '+label,flush=True)
        assert f.sha_file(source)==original;report['checks']=['Seven independent CRC-valid malformed magic/version/enabled/timeout/style/short/long records activate Off without silent writes; actual Restore defaults/Apply and ordinary startup recover valid choices while preserving personal and source bytes'];report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':main()
