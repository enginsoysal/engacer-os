"""Ordinary unchanged x64 EXE GUI install, cold removal and reinstall on production media."""
import argparse,hashlib,json,os,struct,sys,time,traceback,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PRODUCT='/Applications/Windows/{D6E9EC8F-75FD-5D1F-8990-8DE725154FFF}'
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--development-worker',type=Path);args=parser.parse_args()
 import replay8
 loader=replay8.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  from window144_native import ui,c,f,t,clone,library,StoppedDisk,task,output
  out=ROOT/'build/m14-native/stage8/exe-chain-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out;meta=json.loads(ui.manifest_path12().read_text());base=json.loads((ROOT/'build/m14-native/stage8/compact/results.json').read_text());assert base['passed']and base['build_id']==meta['build_id']
  source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage8-compact'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m148-ordinary-exe-chain');original=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/SumatraPDF-3.6.1-64-install.exe';data=original.read_bytes();assert hashlib.sha256(data).hexdigest()=='1eee71cccd2ea6e94d5bcea54ee2f759844da3e1a0ee2f6045035b1d17b94381';download='/Users/Owner/Downloads/'+original.name;sentinel='/Users/Owner/Documents/EXE-personal-sentinel148.txt'
  mounted=StoppedDisk(disk,library())
  try:
   mounted.put(download,data);mounted.put(sentinel,b'Personal document preserved across original EXE lifecycle')
   if args.development_worker:mounted.put('/System/Windows/runtime8.elf',args.development_worker.read_bytes())
  finally:mounted.close()
  report=dict(passed=False,scope=__doc__,build_id=meta['build_id'],compiled_source=meta.get('source_commit'),observer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),clone=cloned,owned_fixture=work.name,cycles=[],full_production_media=not args.development_worker,development_worker_sha256=hashlib.sha256(args.development_worker.read_bytes()).hexdigest()if args.development_worker else None)
  previous_output='';observed_output=''
  def state(g):
   raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496);return dict(state=struct.unpack_from('<I',raw)[0],status=struct.unpack_from('<I',raw,8)[0],message=raw[304:496].split(b'\0')[0].decode(errors='replace'))
  def wait_condition(g,p,predicate,seconds=240):
   nonlocal previous_output,observed_output
   deadline=time.monotonic()+seconds
   while time.monotonic()<deadline:
    current_output=output(g)
    if current_output!=previous_output:
     overlap=min(len(previous_output),len(current_output))
     while overlap and not current_output.startswith(previous_output[-overlap:]):overlap-=1
     observed_output+=current_output[overlap:];previous_output=current_output;(out/'observed-original-output.log').write_bytes(observed_output.encode())
    if predicate():return
    current=state(g)
    if current['state']==3:
     report['last_state']=current;report['last_output']=output(g);(out/'failure-serial.log').write_bytes(g.log().encode());raise AssertionError((current,output(g)))
    time.sleep(.05)
   report['last_state']=state(g);report['last_output']=output(g);(out/'failure-serial.log').write_bytes(g.log().encode());raise TimeoutError((state(g),output(g)))
  def choose(g,p):
   p.desktop(12013,True);assert c.flag(g,'picker12')==9;p.desktop(54019,True);c.key(g,'ctrl','a');c.type_text(g,'/Users/Owner/Downloads');c.key(g,'ret');p.drain();row=f.entries(g)[download]['index']
   for _ in range(128):
    if any(r[5]==55000+row for r in f.controls(g)):break
    p.desktop(54023,True)
   else:raise AssertionError('Original installer not reachable in picker')
   p.desktop(55000+row,True);p.desktop(54011,True);before=f.entries(g);task(g,p,12000);assert before==f.entries(g);c.shot(g,'source-review-'+str(len(report['cycles'])))
  for cycle in range(3):
   removing=cycle==1;boot=ui.guest(work/('cycle-'+str(cycle)),disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
   with boot as g:
    p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19)
    if removing:p.desktop(12208,True);assert any(r[5]==12300 for r in f.controls(g));p.desktop(12300,True)
    else:choose(g,p)
    before=f.stats(g)[0];p.desktop(12002 if removing else 12001,True);c.shot(g,'confirmation-'+str(cycle));at=len(g.log());p.desktop(12003,True,settle=False);g.wait('M8_CPL3_CREATED',at)
    def originals():return[w for w in t.records(g)if w['token']!=front['token']]
    wait_condition(g,p,lambda:len(originals())==1,45);window=originals()[0];t.focus(g,p,window);p.drain();c.shot(g,'original-before-click-'+str(cycle));x,y,width,height=f.model(g)[1];scale=c.flag(g,'scale73');p.click((x+width-100)*scale//2,(y+height-25)*scale//2);p.drain()
    marker='OnUninstallationFinished'if removing else'OnInstallationFinished:';start=time.monotonic();wait_condition(g,p,lambda:marker in output(g));duration=round(time.monotonic()-start,3);p.drain();c.shot(g,'original-after-operation-'+str(cycle));assert originals();t.focus(g,p,originals()[0]);p.desktop(49002,True)
    wait_condition(g,p,lambda:state(g)['state']!=1);assert state(g)['state']==2 and state(g)['status']==0,(state(g),output(g));assert('M148_ORDINARY_ORIGINAL_REMOVE_VERIFIED'if removing else'M148_ORDINARY_ORIGINAL_INSTALL_VERIFIED')in output(g)
    after=f.stats(g)[0];entries=f.entries(g);assert (PRODUCT in entries)==(not removing);assert ui.s.s.document(disk,sentinel,4096)==b'Personal document preserved across original EXE lifecycle';assert hashlib.sha256(ui.s.s.document(disk,download,16*1024*1024)).hexdigest()==hashlib.sha256(data).hexdigest();report['cycles'].append(dict(cycle=cycle,removing=removing,observed_original_seconds=duration,retained_pages=after-before,state=state(g),original_output=output(g)));(out/('serial-'+str(cycle)+'.log')).write_bytes(g.log().encode());c.shot(g,'verified-'+str(cycle))
   mounted=StoppedDisk(disk,library())
   try:
    if not removing:
     reference=json.loads((ROOT/'evidence/M14/8/development/native-original-registration-completion/archive-reference.json').read_text());assert reference['passed'];expected=reference['payloads']+[dict(name='SumatraPDF.exe',bytes=len(data),sha256=hashlib.sha256(data).hexdigest())];verified=[]
     for item in expected:
      matches=[e for e in mounted.volume.entries if e.kind==1 and e.path==(PRODUCT+'/'+item['name']).encode()];assert len(matches)==1;entry=matches[0];assert entry.size==item['bytes'];mounted.file.seek(mounted.offset+entry.first*4096);remaining=entry.size;sha=hashlib.sha256();crc=0
      while remaining:
       block=mounted.file.read(min(remaining,1024*1024));assert block;remaining-=len(block);sha.update(block);crc=zlib.crc32(block,crc)
      assert sha.hexdigest()==item['sha256']and crc==entry.crc;verified.append(dict(name=item['name'],bytes=entry.size,sha256=sha.hexdigest(),crc32=crc))
     from shell148_reference import read
     links=[]
     for i,path in enumerate(['/Users/Owner/Desktop/SumatraPDF.lnk','/Users/Owner/AppData/Roaming/Microsoft/Windows/Start Menu/SumatraPDF.lnk']):
      matches=[e for e in mounted.volume.entries if e.kind==1 and e.path==path.encode()];assert len(matches)==1;entry=matches[0];assert 76<entry.size<=4096;mounted.file.seek(mounted.offset+entry.first*4096);link=mounted.file.read(entry.size);saved=out/('original-shortcut-'+str(cycle)+'-'+str(i)+'.lnk');saved.write_bytes(link);metadata=read(saved);assert metadata['target']==r'C:\Program Files\SumatraPDF\SumatraPDF.exe';links.append(dict(path=path,sha256=hashlib.sha256(link).hexdigest(),metadata=metadata))
     report['cycles'][-1].update(cold_payload_readback=verified,windows_original_shortcut_readback=links)
    else:assert not any(e.kind and(e.path.decode()==PRODUCT or e.path.decode().startswith(PRODUCT+'/'))for e in mounted.volume.entries)
   finally:mounted.close()
   (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
  report['passed']=True
 except Exception:
  if 'report'in locals():
   report['error']=traceback.format_exc()
   if 'g'in locals():
    try:report['last_state']=state(g);report['last_output']=output(g);(out/'failure-serial.log').write_bytes(g.log().encode())
    except Exception:pass
  raise
 finally:
  if 'report'in locals():(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
  sys.meta_path.remove(loader)
if __name__=='__main__':main()
