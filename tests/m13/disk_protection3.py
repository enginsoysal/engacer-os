"""Protected GPT attributes and actual verified-copy repair on owned disks."""
import json,struct,traceback,zlib
from PIL import Image
import disk_profiles3 as d
ui=d.ui;s=d.s;ROOT=d.ROOT
def protect(path):
 with path.open('r+b') as f:
  for lba in (1,path.stat().st_size//512-1):
   f.seek(lba*512);h=bytearray(f.read(512));table_lba=struct.unpack_from('<Q',h,72)[0];f.seek(table_lba*512);t=bytearray(f.read(16384));struct.pack_into('<Q',t,48,1);struct.pack_into('<I',h,88,zlib.crc32(t));struct.pack_into('<I',h,16,0);struct.pack_into('<I',h,16,zlib.crc32(h[:92]));f.seek(lba*512);f.write(h);f.seek(table_lba*512);f.write(t)
def main():
 out=ROOT/'build/m13/stage3/disk-protection';out.mkdir(parents=True,exist_ok=True);work=ui.q.new_work('m133-disk-protection');owned=ui.q.sparse_disk(work/'protected.img',2*1024**3);repair=ui.q.sparse_disk(work/'repair.img',2*1024**3);d.fixture.fixture(owned);protect(owned);d.fixture.fixture(repair)
 with repair.open('r+b') as f:f.seek(-512+16,2);f.write(b'\0'*4)
 with repair.open('rb') as f:f.seek(-512+16,2);assert f.read(4)==bytes(4),'Fixture corruption did not persist'
 protected_hash=ui.q.digest(owned);repair_hash=ui.q.digest(repair);data_hash=ui.q.digest(repair,34*512,repair.stat().st_size-67*512);meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));report=dict(passed=False,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'])
 try:
  extra=['-drive','if=none,id=repair,format=raw,file='+str(repair),'-device','ide-hd,bus=ide.1,drive=repair']
  with ui.guest(work/'tools',owned,extra=extra,firmware='bios') as g:
   p=ui.Pointer(g);p.drain();s.go(g,p,2,2,100,90,300);assert 211 not in d.controls(g) and 212 not in d.controls(g);s.shot(g,out,'protected-selection')
   s.go(g,p,202,300);s.shot(g,out,'damaged-backup');report['observed_second_disk']=dict(index=s.flag(g,'u71_disk'),state=list(struct.unpack('<3I',ui.memory(g,ui.symbol('u71_state')[0],12))),actions=d.controls(g));assert 211 not in d.controls(g) and 212 not in d.controls(g),report['observed_second_disk']
   s.go(g,p,215);assert 229 in d.controls(g) and 230 not in d.controls(g);s.shot(g,out,'verified-copy-choice');s.go(g,p,229);assert 228 not in d.controls(g)
   assert ui.q.digest(owned)==protected_hash and ui.q.digest(repair)==repair_hash;d.apply(g,p,7,False);s.shot(g,out,'repair-complete');state=struct.unpack('<3I',ui.memory(g,ui.symbol('u71_state')[0],12));assert state[1:]==(3,1),state;d.table(repair)
   assert s.flag(g,'scale73')==2
   with Image.open(out/'repair-complete.png') as image:
    pixels=image.convert('RGB').crop((s.flag(g,'body')+12,s.flag(g,'bottom')-42,s.flag(g,'left')+s.flag(g,'width')-24,s.flag(g,'bottom')-14))
    assert not any(r>g*1.3 and r>b*1.3 and r-g>30 for r,g,b in pixels.getdata()),'Successful completion is painted as a red error'
   assert ui.q.digest(owned)==protected_hash and ui.q.digest(repair,34*512,repair.stat().st_size-67*512)==data_hash
   report.update(passed=True,checks=['Protected selected GPT partition has no active Format/Delete','Damaged backup retains read-only partition actions and only verified primary repair is offered','No disk bytes change during inspect/review; explicit consent repairs both verified copies','Every protected-disk byte and all repaired-disk bytes outside GPT metadata stay identical']);(out/'boot.log').write_bytes(g.log().encode())
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report),flush=True)
if __name__=='__main__':main()
