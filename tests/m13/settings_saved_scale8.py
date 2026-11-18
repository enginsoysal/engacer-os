"""A previously valid saved scale falls back before new Settings windows open."""
import hashlib,json,os,struct,sys,traceback,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
os.environ['ENGACER12_IMAGE']='EngacerOS-M13STAGE8'
sys.path.insert(0,str(ROOT/'tests/m12'))
import settings_observe as h
import capture14,observe6,observer8
c=h.c;f=h.f;t=h.t;ui=h.ui
capture14.bind(ui);observe6.bind(ui);observer8.bind(ui)


def old_scale_record(disk):
    """Only an owned, stopped fixture: retain valid file/bank/GPT checksums."""
    assert disk.name=='owned.img' and disk.resolve().is_relative_to(Path(ui.q.BASE).resolve())
    changed=0
    with disk.open('r+b') as stream:
        stream.seek(512);gpt=stream.read(512);assert gpt[:8]==b'EFI PART'
        stream.seek(struct.unpack_from('<Q',gpt,72)[0]*512);table=stream.read(16384);start=struct.unpack_from('<Q',table,4*128+32)[0]*512
        for bank in range(2):
            offset=start+bank*71*4096;stream.seek(offset);head=bytearray(stream.read(4096));entries=bytearray(stream.read(1024*280))
            if head[:8]!=b'ENGINEV6' or zlib.crc32(head[:4092])!=struct.unpack_from('<I',head,4092)[0]:continue
            assert zlib.crc32(entries)==struct.unpack_from('<I',head,36)[0]
            for index in range(1024):
                row=index*280
                if entries[row:row+256].split(b'\0')[0].decode()!=h.APPEARANCE:continue
                first,size,crc,kind=struct.unpack_from('<QQII',entries,row+256);assert size==352 and kind==1
                stream.seek(start+first*4096);record=bytearray(stream.read(size));assert struct.unpack_from('<I',record,28)[0]==0
                struct.pack_into('<I',record,16,4);stream.seek(start+first*4096);stream.write(record);struct.pack_into('<I',entries,row+272,zlib.crc32(record));changed+=1
            struct.pack_into('<I',head,36,zlib.crc32(entries));struct.pack_into('<I',head,4092,zlib.crc32(head[:4092]));stream.seek(offset);stream.write(head);stream.write(entries)
    assert changed and struct.unpack_from('<I',h.record(disk),16)[0]==4
    return changed


def main():
    out=ROOT/'build/m13/stage8/saved-scale';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m138-saved-scale');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
    report=dict(passed=False,stage='M13.8',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],physical=[1920,1200],owned_fixture=work.name,checks=[])
    try:
        with ui.guest(work/'install',disk,resolution=(1920,1200),ram=512) as g:
            p=ui.Pointer(g)
            for action in (2,50012,2,100,2,2,2):c.wizard(g,p,action)
            at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain();t.close_all(g,p)
            t.launch(g,p,'settings',3);p.desktop(43,True);h.save(g,p);h.close(g,p);(out/'install.log').write_text(g.log(),encoding='utf-8')
        personal=ui.s.s.document(disk,'/Users/Owner/Documents/Welcome.txt');report['legacy_scale_records']=old_scale_record(disk);legacy=h.record(disk)
        boot=ui.guest(work/'fallback',disk,resolution=(1920,1200),ram=512,media='installed',ready='M7_DESKTOP_READY');ui.s.normal_boot(boot,work/'install/vars.fd')
        with boot as g:
            p=ui.Pointer(g);p.drain();assert c.flag(g,'scale73')==2 and c.flag(g,'choice73')==0 and c.flag(g,'settings_invalid13')==2 and h.colors(g)[1]==1
            t.close_all(g,p);baseline=f.stats(g);t.launch(g,p,'settings',3);assert 'saved size' in f.app(g)['notice'].lower() and 'Automatic' in f.app(g)['notice'];assert f.model(g)[1][3]>=600 and h.record(disk)==legacy;c.shot(g,'saved-size-fallback')
            h.save(g,p);saved=h.record(disk);assert struct.unpack_from('<I',saved,16)[0]==0 and not c.flag(g,'settings_invalid13');h.close(g,p);f.same_pages(baseline,f.stats(g));c.idle(g)
            report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0);(out/'fallback.log').write_text(g.log(),encoding='utf-8')
        boot=ui.guest(work/'saved-startup',disk,resolution=(1920,1200),ram=512,media='installed',ready='M7_DESKTOP_READY');ui.s.normal_boot(boot,work/'install/vars.fd')
        with boot as g:
            p=ui.Pointer(g);p.drain();assert c.flag(g,'scale73')==2 and not c.flag(g,'settings_invalid13') and ui.memory(g,ui.symbol('appearance11',352,True)[0],352)==saved
            t.close_all(g,p);t.launch(g,p,'settings',3);assert 'saved size' not in f.app(g)['notice'].lower();c.shot(g,'saved-size-corrected-startup');h.close(g,p);c.idle(g);(out/'saved-startup.log').write_text(g.log(),encoding='utf-8')
        assert ui.s.s.document(disk,'/Users/Owner/Documents/Welcome.txt')==personal
        report['replacement_sha256']=hashlib.sha256(saved).hexdigest()
        report['checks'].append('A CRC-valid legacy 200% preference on a real 1920x1200 framebuffer falls back to Automatic before windows open, preserves dark appearance/personal bytes, explains the session fallback in Settings and leaves the original record unchanged until Apply')
        report['checks'].append('Actual Apply saves Automatic; a second independent no-ISO start reloads the exact corrected appearance without the warning, and completed tasks retain zero managed pages and halt at idle')
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':main()
