"""Native disk-tool layout/input/transport tasks on explicitly owned fixtures."""
import argparse,json,os,struct,sys,traceback,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];os.environ['ENGACER12_IMAGE']='EngacerOS-M13STAGE3';sys.path.insert(0,str(ROOT/'tests/m12'))
import setup_observe as s
ui=s.ui;fixture=ui.module('fixture13_disk',ROOT/'tests/m71/native.py')
def controls(g):return [r[4] for r in s.controls(g)]
def go(g,p,action,keyboard):
 if not keyboard:return s.wizard(g,p,action)
 for _ in range(25):
  rows=controls(g);focus=s.flag(g,'focus')
  if focus<len(rows) and rows[focus]==action:s.key(g,'ret');return
  s.key(g,'tab')
 raise AssertionError(('Unreachable keyboard control',action,rows))
def apply(g,p,op,keyboard):
 go(g,p,226,keyboard);at=len(g.log());go(g,p,228,keyboard);g.wait('M71_DISK_APPLIED op=0x'+format(op,'016x'),at,120);p.drain()
def table(disk):
 with disk.open('rb') as f:
  f.seek(512);header=bytearray(f.read(512));assert header[:8]==b'EFI PART';size=struct.unpack_from('<I',header,12)[0];expected=struct.unpack_from('<I',header,16)[0];struct.pack_into('<I',header,16,0);assert zlib.crc32(header[:size])==expected
  lba,count,entry_size,crc=struct.unpack_from('<QIII',header,72);f.seek(lba*512);entries=f.read(count*entry_size);assert zlib.crc32(entries)==crc
  return [entries[i*entry_size:(i+1)*entry_size] for i in range(count)]
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--profile',choices=['compact','ordinary','150','4k'],default='ordinary');parser.add_argument('--controller',choices=['sata','ide','mptsas','pvscsi','nvme','virtio'],default='sata');parser.add_argument('--keyboard',action='store_true');parser.add_argument('--blank',action='store_true');args=parser.parse_args()
 label=args.profile+'-'+args.controller+('-keyboard' if args.keyboard else '')+('-blank' if args.blank else '')
 out=ROOT/'build/m13/stage3'/('disk-'+label);out.mkdir(parents=True,exist_ok=True);work=ui.q.new_work('m133-'+label);disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
 resolution,ram,choice={'compact':((1024,768),128,50011),'ordinary':((1280,800),256,50011),'150':((1920,1200),512,50012),'4k':((3840,2160),1024,50013)}[args.profile]
 parts=fixture.fixture(disk) if not args.blank else None;whole=ui.q.digest(disk);keep=ui.q.digest(disk,parts[0][0]*512,(parts[0][1]-parts[0][0]+1)*512) if parts else None;entry=fixture.original_entry(disk,0) if parts else None
 meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));report=dict(passed=False,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],physical=list(resolution),controller=args.controller,keyboard_only=args.keyboard,blank=args.blank,checks=[])
 try:
  with ui.guest(work/'tools',disk,resolution=resolution,ram=ram,controller=args.controller) as g:
   p=ui.Pointer(g);p.drain();act=lambda a:go(g,p,a,args.keyboard)
   act(2);act(choice);act(2);act(100);act(90);s.shot(g,out,'partitions');assert 211 not in controls(g) and 212 not in controls(g)
   if args.blank:
    act(213);s.shot(g,out,'initialize-review');assert 228 not in controls(g);assert ui.q.digest(disk)==whole;apply(g,p,2,args.keyboard);assert not any(row[:16]!=bytes(16) for row in table(disk));row=300
   else:assert ui.q.digest(disk)==whole;row=302
   act(row);act(210);act(220);s.text(g,'128');assert ui.memory(g,ui.symbol('u71_size',16)[0],16).split(b'\0')[0]==b'128'
   act(222);s.text(g,'Temporary');s.key(g,'ctrl','a');s.text(g,'Shared data');assert ui.memory(g,ui.symbol('u71_name',37)[0],37).split(b'\0')[0]==b'Shared data';s.shot(g,out,'create-fields')
   act(223);s.shot(g,out,'create-review');assert 228 not in controls(g);apply(g,p,3,args.keyboard);rows=table(disk);found=[row for row in rows if row[56:78]=='Shared data'.encode('utf-16-le')];assert len(found)==1;first,last=struct.unpack_from('<QQ',found[0],32);assert last-first+1==128*2048
   assert s.flag(g,'u71_mode')==1;s.shot(g,out,'created');selected=300 if args.blank else 302;act(selected);act(212);s.shot(g,out,'formats');act(224);s.shot(g,out,'format-review');assert 228 not in controls(g);apply(g,p,5,args.keyboard)
   with disk.open('rb') as f:f.seek(first*512);boot=f.read(512);assert boot[82:90]==b'FAT32   ' and boot[510:]==b'\x55\xaa'
   if parts:assert fixture.original_entry(disk,0)==entry and ui.q.digest(disk,parts[0][0]*512,(parts[0][1]-parts[0][0]+1)*512)==keep
   if args.blank:
    act(300);act(211);apply(g,p,4,args.keyboard);assert not any(row[:16]!=bytes(16) for row in table(disk));act(214);assert 228 not in controls(g);s.shot(g,out,'clear-review');apply(g,p,1,args.keyboard)
    with disk.open('rb') as f:assert f.read(512)==bytes(512);f.seek(-512,2);assert f.read(512)==bytes(512)
   report['checks']=['Native bounded non-overlapping targets and readable physical capture dimensions','No active Format/Delete without partition selection; no active Apply before consent','Ordinary field activation replaces suggested size; Ctrl+A and a real space in the partition name work','Independent GPT header/table CRC, 128-MiB named entry and actual FAT32 bytes verified','Blank GPT/create/format/delete/clear lifecycle passes' if args.blank else 'Unrelated partition entry and payload remain byte-identical'];report['passed']=True;(out/'tools.log').write_bytes(g.log().encode())
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report),flush=True)
if __name__=='__main__':main()
