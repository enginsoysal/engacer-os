"""Real partition tools, whole-disk consent, foreign disk preservation and recovery."""
import hashlib,json,struct,traceback,shutil
import setup as s
ui=s.ui;ROOT=s.ROOT
fixture=ui.module('fixture71',ROOT/'tests/m71/native.py')
out=ROOT/'build/m11/setup/safety';out.mkdir(parents=True,exist_ok=True)

def control(g,action):
 n=s.flag(g,'controls');raw=ui.memory(g,ui.symbol('buttons',480)[0],n*20)
 return any(struct.unpack_from('<I',raw,i*20+16)[0]==action for i in range(n))

def go(g,p,*commands):
 for c in commands:s.wizard(g,p,c)

def apply(g,p,operation):
 s.wizard(g,p,226);start=s.wizard(g,p,228);g.wait('M71_DISK_APPLIED op=0x'+format(operation,'016x'),start,120)

def main():
 work=ui.q.new_work('m115-safety');meta=json.loads((ui.manifest_path11()).read_text());report={'passed':False,'build_id':meta['build_id'],'checks':[]}
 try:
  disk=ui.q.sparse_disk(work/'target.img',2*1024**3);parts=fixture.fixture(disk);foreign=ui.q.sparse_disk(work/'foreign.img',2*1024**3);fixture.fixture(foreign)
  keep=ui.q.digest(disk,parts[0][0]*512,(parts[0][1]-parts[0][0]+1)*512);whole=ui.q.digest(disk);untouched=ui.q.digest(foreign)
  extra=['-drive','if=none,id=foreign,format=raw,file='+str(foreign),'-device','ide-hd,bus=ide.1,drive=foreign']
  with ui.guest(work/'partitions',disk,extra=extra) as g:
   p=ui.Pointer(g);go(g,p,2,2,100);assert not control(g,2);s.shot(g,out,'existing-disk-guidance');assert ui.q.digest(disk)==whole
   go(g,p,90);s.shot(g,out,'partitions');go(g,p,301,212,224);s.shot(g,out,'format-review');go(g,p,228);assert ui.q.digest(disk)==whole
   go(g,p,227);assert ui.q.digest(disk)==whole
   go(g,p,301,212,224);apply(g,p,5)
   with disk.open('rb') as stream:stream.seek(parts[1][0]*512);assert stream.read(512)[82:90]==b'FAT32   '
   go(g,p,301,212,225);apply(g,p,6)
   with disk.open('rb') as stream:stream.seek(parts[1][0]*512);assert stream.read(8)==b'ENGINEV6'
   go(g,p,301,211);apply(g,p,4);go(g,p,301,210,223);apply(g,p,3);s.shot(g,out,'created-partition')
   assert ui.q.digest(disk,parts[0][0]*512,(parts[0][1]-parts[0][0]+1)*512)==keep and ui.q.digest(foreign)==untouched
   report['checks'].append('Native FAT32 and native-volume format, partition delete/create and separate unchecked/cancelled consent preserve foreign partition payload and every byte of the other equal-capacity disk')
   go(g,p,200,91,2,2,2);assert s.flag(g,'step')==4 and not control(g,2);s.shot(g,out,'whole-disk-consent');before=ui.q.digest(disk)
   go(g,p,92);assert control(g,2);go(g,p,1,2);assert not control(g,2) and s.flag(g,'replace_consent')==0;assert ui.q.digest(disk)==before
   go(g,p,92);start=s.wizard(g,p,2);g.wait('M6_INSTALL_PASS',start,240);assert ui.q.digest(foreign)==untouched
   start=s.wizard(g,p,84);g.wait('M7_DESKTOP_READY',start,180);ui.Pointer(g).drain();s.shot(g,out,'replacement-installed',True);(out/'partition-install.log').write_bytes(g.log().encode())
  report['checks'].append('Whole-disk replacement needs fresh separate Review consent after Back; actual copy/readback/reset succeeds and the unselected disk remains byte-identical')
  small=ui.q.sparse_disk(work/'small.img',512*1024**2)
  with ui.guest(work/'small',small) as g:
   p=ui.Pointer(g);go(g,p,2,2,100);assert not control(g,2);s.shot(g,out,'small-disk-readable-refusal')
  absent=ui.guest(work/'absent',small);at=next(i for i,x in enumerate(absent.args) if x.startswith('ide-hd,bus=ide.0,drive=target'));del absent.args[at-1:at+1]
  with absent as g:
   p=ui.Pointer(g);go(g,p,2,2);assert not control(g,2);s.shot(g,out,'no-disk-guidance')
  report['checks'].append('Missing and undersized disks retain actionable guidance and disabled Next without pretending installation is possible')
  failed=ui.q.sparse_disk(work/'fault.img',2*1024**3)
  with ui.guest(work/'fault',failed,fault={'event':'write_aio','errno':5,'once':True,'immediately':True}) as g:
   p=ui.Pointer(g);go(g,p,2,2,100,2,2,2);start=s.wizard(g,p,2);g.wait('M6_INSTALL_FAILED',start,180);assert 'M6_INSTALL_PASS' not in g.log();s.shot(g,out,'write-failure-readable')
   go(g,p,63);assert s.flag(g,'step')==1 and s.flag(g,'replace_consent')==0;assert ui.memory(g,ui.symbol('preferences',40)[0],6)==b'Owner\0'
   go(g,p,100);assert not control(g,2),'A quarantined controller must not advertise writable installation';s.shot(g,out,'faulted-controller-refuses-next');fault_variables=g.folder/'vars.fd';(out/'failure.log').write_bytes(g.log().encode())
  # Removing the external injected fault does not undo the driver's safe quarantine.
  # Power-cycle the same owned disk/firmware variables before a real installation retry.
  retry=ui.guest(work/'retry',failed);shutil.copyfile(fault_variables,retry.folder/'vars.fd')
  with retry as g:
   p=ui.Pointer(g);go(g,p,2,2,100,2,2,2);start=s.wizard(g,p,2);g.wait('M6_INSTALL_PASS',start,240);s.shot(g,out,'write-failure-retry-succeeded');(out/'failure-retry.log').write_bytes(g.log().encode())
  report['checks'].append('Injected first-write failure never reports success; Back keeps choices and clears consent, quarantined I/O cannot enable Next, and a real retry on the same disk/NVRAM succeeds after removing the external fault and power-cycling')
  # Corrupt only an owned installed BIOS payload, then use the original verified recovery slot.
  with failed.open('r+b') as stream:stream.seek(2112*512+511);value=stream.read(1);stream.seek(-1,1);stream.write(bytes([value[0]^255]))
  repair=ui.guest(work/'repair',failed);wait_original=repair.wait
  def recovery_wait(text,after=0,timeout=90):
   if text==repair.ready:
    wait_original('M115_RECOVERY_WINDOW',after,timeout);ui.h.key(repair,'esc');wait_original('M75_SETUP_OVERRIDE',after,10)
   return wait_original(text,after,timeout)
  repair.wait=recovery_wait
  with repair as g:
   p=ui.Pointer(g);assert 'M75_SETUP_OVERRIDE' in g.log();go(g,p,50,80,100,2);assert s.flag(g,'step')==4;start=s.wizard(g,p,2);g.wait('M6_MAINTENANCE_PASS',start,240);s.shot(g,out,'recovery-complete');(out/'recovery.log').write_bytes(g.log().encode())
  with ui.guest(work/'repaired-bios',failed,firmware='bios',media='installed',ready='M7_DESKTOP_READY') as g:
   assert 'M7_DESKTOP_READY build='+meta['build_id'] in g.log();(out/'repaired-boot.log').write_bytes(g.log().encode())
  report['checks'].append('The ISO recovery route restores a deliberately corrupted owned BIOS payload from the checked slot, followed by actual disk-only installed desktop startup')
  report['untouched_disk_sha256']=untouched;report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
