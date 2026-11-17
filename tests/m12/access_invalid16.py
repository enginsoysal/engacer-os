"""Semantically invalid accessibility records with valid native filesystem CRCs."""
import json,os,struct,traceback,zlib
from pathlib import Path
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE16'
import access_observe16 as a
from access_fixtures16 import clone
c=a.c;f=a.f;h=a.h;s=a.s;ui=a.ui;ROOT=a.ROOT
PATH='/System/Settings/accessibility16-Owner.bin'

def replace_record(disk,payload):
 with disk.open('r+b') as stream:
  stream.seek(512);gpt=stream.read(512);assert gpt[:8]==b'EFI PART';stream.seek(struct.unpack_from('<Q',gpt,72)[0]*512);table=stream.read(16384);start=struct.unpack_from('<Q',table,4*128+32)[0]*512;changed=0
  for bank in range(2):
   offset=start+bank*71*4096;stream.seek(offset);head=bytearray(stream.read(4096));entries=bytearray(stream.read(1024*280))
   if head[:8]!=b'ENGINEV6' or zlib.crc32(head[:4092])!=struct.unpack_from('<I',head,4092)[0]:continue
   assert zlib.crc32(entries)==struct.unpack_from('<I',head,36)[0]
   for index in range(1024):
    row=index*280
    if entries[row:row+256].split(b'\0')[0].decode()!=PATH:continue
    first,size,crc,kind=struct.unpack_from('<QQII',entries,row+256);assert kind==1 and len(payload)<=4096;stream.seek(start+first*4096);stream.write(payload);struct.pack_into('<Q',entries,row+264,len(payload));struct.pack_into('<I',entries,row+272,zlib.crc32(payload));changed+=1
   struct.pack_into('<I',head,36,zlib.crc32(entries));struct.pack_into('<I',head,4092,zlib.crc32(head[:4092]));stream.seek(offset);stream.write(head);stream.write(entries)
 assert changed and ui.s.s.document(disk,PATH)==payload;return changed

def main():
 out=ROOT/'build/m12/stage16/access-invalid';out.mkdir(parents=True,exist_ok=True);c.OUT=out;meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));native=json.loads((ROOT/'build/m12/stage16/access-native/results.json').read_text(encoding='utf-8'));assert native['passed'] and native['build_id']==meta['build_id'];source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage16-access'/native['owned_fixture']/'owned.img';original=f.sha_file(source);report=dict(passed=False,build_id=meta['build_id'],checks=[],cases=[])
 try:
  good=struct.pack('<4I',0x36314155,1,3,0)
  for label,payload in [('magic',struct.pack('<4I',0,1,3,0)),('version',struct.pack('<4I',0x36314155,2,3,0)),('flags',struct.pack('<4I',0x36314155,1,4,0)),('reserved',struct.pack('<4I',0x36314155,1,3,1)),('short',good[:12]),('long',good+b'x')]:
   work,disk,cloned=clone(ui,source,'m12-stage16-invalid');appearance=h.record(disk);preferences=ui.s.s.document(disk,'/System/Settings/start11-Owner.bin');changed=replace_record(disk,payload);before=f.sha_file(disk)
   with ui.guest(work/'refused',disk,media='installed',ready='M7_DESKTOP_READY') as g:
    p=ui.Pointer(g);p.drain();assert c.flag(g,'access_invalid16')==1 and c.flag(g,'access_flags16')==0,label;c.open_settings(g,p);p.desktop(59004,True);c.shot(g,'safe-'+label);assert ui.s.s.document(disk,PATH)==payload and f.sha_file(disk)==before;a.activate(g,60012,space=True);assert not c.flag(g,'access_invalid16') and not c.flag(g,'access_flags16');a.close(g);c.idle(g);(out/(label+'.log')).write_bytes(g.log().encode())
   replacement=struct.pack('<4I',0x36314155,1,0,0);assert ui.s.s.document(disk,PATH)==replacement and h.record(disk)==appearance and ui.s.s.document(disk,'/System/Settings/start11-Owner.bin')==preferences
   with ui.guest(work/'valid-startup',disk,media='installed',ready='M7_DESKTOP_READY') as g:
    ui.Pointer(g).drain();assert not c.flag(g,'access_invalid16') and not c.flag(g,'access_flags16');c.idle(g)
   report['cases'].append(dict(name=label,bytes=len(payload),valid_filesystem_banks=changed,clone=cloned,replacement_hex=replacement.hex()));print('PASS semantic refusal and reset: '+label,flush=True)
  assert f.sha_file(source)==original;report['checks']=['Six independently CRC-valid bad magic/version/flags/reserved/short/long records activate safe defaults without silent disk writes; real keyboard Reset writes valid defaults, independent startup reloads them, and appearance/Start/source fixture bytes remain exact'];report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
