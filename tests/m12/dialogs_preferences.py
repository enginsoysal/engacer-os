"""An invalid optional picker record must not prevent ordinary installed use."""
import json,os,struct,subprocess,traceback,zlib
from pathlib import Path
import dialogs_fault as fault
d=fault.d;c=d.c;f=d.f;ui=d.ui;ROOT=d.ROOT

def corrupt_owned_record(path,wanted):
    with path.open('r+b') as stream:
        stream.seek(512);header=bytearray(stream.read(512));assert header[:8]==b'EFI PART'
        crc=struct.unpack_from('<I',header,16)[0];struct.pack_into('<I',header,16,0);assert zlib.crc32(header[:92])==crc
        stream.seek(struct.unpack_from('<Q',header,72)[0]*512);table=stream.read(16384);assert zlib.crc32(table)==struct.unpack_from('<I',header,88)[0]
        start=struct.unpack_from('<Q',table,4*128+32)[0]*512;banks=[]
        for bank in range(2):
            stream.seek(start+bank*71*4096);head=stream.read(4096);raw=stream.read(1024*280)
            if head[:8]==b'ENGINEV6' and zlib.crc32(head[:4092])==struct.unpack_from('<I',head,4092)[0] and zlib.crc32(raw)==struct.unpack_from('<I',head,36)[0]:banks.append((struct.unpack_from('<Q',head,24)[0],raw))
        assert banks;raw=max(banks)[1]
        for i in range(1024):
            record=raw[i*280:(i+1)*280]
            if record[:256].split(b'\0')[0].decode()!=wanted:continue
            first,size,crc,kind=struct.unpack_from('<QQII',record,256);assert kind==1 and size==792
            position=start+first*4096;stream.seek(position);value=stream.read(size);assert zlib.crc32(value)==crc
            stream.seek(position);stream.write(bytes([value[0]^255]));return
    raise AssertionError('Expected owned optional record not found')

def main():
    out=ROOT/'build/m12/stage8/dialogs-preferences';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    native=json.loads((ROOT/'build/m12/stage8/dialogs-native/results.json').read_text());meta=json.loads(ui.manifest_path12().read_text());assert native['build_id']==meta['build_id']
    base=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage8-dialogs'/native['owned_fixture']/'owned.img';before=fault.digest(base)
    work=ui.q.new_work('m12-stage8-dialogs-preferences');clone=work/'owned-clone.img';qimg=Path(ui.q.qemu_tools()['qemu-system-x86_64']).with_name('qemu-img.exe')
    subprocess.run([str(qimg),'convert','-f','raw','-O','raw','-S','4k',str(base),str(clone)],check=True,capture_output=True);assert fault.digest(clone)==before
    corrupt_owned_record(clone,'/Users/Owner/AppData/file-dialogs12.bin');report=dict(passed=False,build_id=meta['build_id'],owned_fixture=work.name,base_sha256=before,checks=[])
    try:
        with ui.guest(work/'bad-preference',clone,media='installed',ready='M7_DESKTOP_READY') as g:
            p=ui.Pointer(g);p.drain();p.desktop(94,True);p.desktop(f.item(g,p,'Existing.txt'),True);c.key(g,'ret');text=bytes(d.appview(g).text);p.desktop(54001,True)
            assert d.picker(g).path==b'/Users/Owner/Documents' and c.flag(g,'file_dialog_state11')==10
            c.shot(g,'invalid-preference-fallback');p.desktop(54010,True);assert bytes(d.appview(g).text)==text;c.idle(g);(out/'boot.log').write_bytes(g.log().encode())
        assert fault.digest(base)==before;report['passed']=True;report['checks'].append('Corrupt optional preference payload falls back to usable Documents after ordinary installed startup; Cancel retains real text and the base disk remains unchanged')
    except Exception:
        report['error']=ui.q.clean(traceback.format_exc());raise
    finally:
        (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
