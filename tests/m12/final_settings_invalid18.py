"""Owned disk semantic preference corruption with independently valid filesystem CRCs."""
import hashlib,json,os,struct,traceback,zlib
from pathlib import Path
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE18'
import settings_observe as h
c=h.c;f=h.f;ui=h.ui;ROOT=h.ROOT

def corrupt_semantic_record(disk):
    with disk.open('r+b') as stream:
        stream.seek(512);gpt=stream.read(512);assert gpt[:8]==b'EFI PART';stream.seek(struct.unpack_from('<Q',gpt,72)[0]*512);table=stream.read(16384);start=struct.unpack_from('<Q',table,4*128+32)[0]*512;changed=0
        for bank in range(2):
            offset=start+bank*71*4096;stream.seek(offset);head=bytearray(stream.read(4096));entries=bytearray(stream.read(1024*280))
            if head[:8]!=b'ENGINEV6' or zlib.crc32(head[:4092])!=struct.unpack_from('<I',head,4092)[0]:continue
            assert zlib.crc32(entries)==struct.unpack_from('<I',head,36)[0]
            for index in range(1024):
                row=index*280
                if entries[row:row+256].split(b'\0')[0].decode()!=h.APPEARANCE:continue
                first,size,crc,kind=struct.unpack_from('<QQII',entries,row+256);assert size==352 and kind==1;stream.seek(start+first*4096);record=bytearray(stream.read(size));struct.pack_into('<I',record,8,0x123456);struct.pack_into('<I',record,28,1);stream.seek(start+first*4096);stream.write(record);struct.pack_into('<I',entries,row+272,zlib.crc32(record));changed+=1
            struct.pack_into('<I',head,36,zlib.crc32(entries));struct.pack_into('<I',head,4092,zlib.crc32(head[:4092]));stream.seek(offset);stream.write(head);stream.write(entries)
    assert changed;invalid=h.record(disk);assert struct.unpack_from('<I',invalid,28)[0]==1;return changed

def main():
    out=ROOT/'build/m12/stage18/settings-invalid';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    native=json.loads((ROOT/'build/m12/stage18/settings-native/results.json').read_text(encoding='utf-8'));meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));assert native['passed'] and native['build_id']==meta['build_id'];base=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage18-settings';work=base/native['owned_fixture'];disk=work/'owned.img';assert disk.resolve().is_relative_to(base.resolve());attempt=ui.q.new_work('m12-stage18-settings-invalid');report=dict(passed=False,build_id=meta['build_id'],owned_fixture=attempt.name,checks=[])
    try:
        personal=ui.s.s.document(disk,'/Users/Owner/Documents/Welcome.txt');report['malformed_records']=corrupt_semantic_record(disk)
        with ui.guest(attempt/'refused',disk,media='installed',ready='M7_DESKTOP_READY') as g:
            p=ui.Pointer(g);p.drain();assert c.flag(g,'settings_invalid13')==1 and h.colors(g)[0]!=0x123456;c.open_settings(g,p);assert 'could not be read' in f.app(g)['notice'];c.shot(g,'malformed-record-safe-fallback');h.save(g,p);replacement=h.record(disk);assert struct.unpack_from('<I',replacement,28)[0]==0 and not c.flag(g,'settings_invalid13');c.shot(g,'valid-replacement-saved');h.close(g,p);c.idle(g);(out/'native.log').write_bytes(g.log().encode())
        with ui.guest(attempt/'valid-startup',disk,media='installed',ready='M7_DESKTOP_READY') as g:
            p=ui.Pointer(g);p.drain();assert not c.flag(g,'settings_invalid13') and ui.memory(g,ui.symbol('appearance11',352,True)[0],352)==replacement and h.click_interval(g)==900;c.open_settings(g,p);assert 'could not be read' not in f.app(g)['notice'];c.shot(g,'valid-replacement-startup');h.close(g,p);c.idle(g);(out/'ordinary.log').write_bytes(g.log().encode())
        assert ui.s.s.document(disk,'/Users/Owner/Documents/Welcome.txt')==personal;report['replacement_sha256']=hashlib.sha256(replacement).hexdigest();report['checks'].append('An owned appearance file with independently valid GPT/native-bank/file CRCs but an invalid reserved field is semantically refused; Settings explains safe fallback, real Apply saves a valid record, and ordinary startup loads it without changing personal content or input preferences');report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
