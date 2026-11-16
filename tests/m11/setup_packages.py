"""The actual No optional apps install can add/run/remove an app offline."""
import json,os,struct,traceback
from pathlib import Path
import setup as s
ui=s.ui;f=s.f;ROOT=s.ROOT
def main():
 meta=json.loads((ui.manifest_path11()).read_text());prior=json.loads((ROOT/'build/m11/setup/150/results.json').read_text());assert prior['passed'] and prior['build_id']==meta['build_id']
 base=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m115-setup-150';owned=max(base.iterdir(),key=lambda p:p.stat().st_mtime_ns);disk=owned/'owned.img';assert disk.is_file() and disk.resolve().is_relative_to(base.resolve())
 work=ui.q.new_work('m115-packages');out=ROOT/'build/m11/setup/packages';out.mkdir(parents=True,exist_ok=True);report={'passed':False,'build_id':meta['build_id'],'iso_sha256':meta['artifacts'][ui.IMAGE11+'.iso']['sha256'],'checks':[]}
 try:
  g=ui.guest(work/'installed',disk,media='installed',ready='M7_DESKTOP_READY',resolution=(1920,1200));ui.s.normal_boot(g,owned/'install/vars.fd')
  with g:
   p=ui.Pointer(g);p.drain();assert s.flag(g,'layout10',True)==1 and s.flag(g,'scale73',True)==3 and s.flag(g,'guide_open11',True)==0
   p.logical(60,335,True);s.key(g,'ret');assert f.s.count(g,3)==1;p.desktop(10000,True)
   before=struct.unpack('<4Q',ui.memory(g,ui.symbol('stats',32,True)[0],32));p.desktop(10304,True)
   assert s.document(disk,'/Applications/Calculator/program.elf').startswith(b'\x7fELF');p.desktop(10204,True);assert f.s.count(g,4)==1;s.shot(g,out,'offline-calculator-launched',True)
   p.close_app(4,True);p.drain();p.desktop(10304,True);s.shot(g,out,'remove-calculator-review',True);p.desktop(10004,True)
   rows=f.rows(g);assert '/Applications/Calculator/program.elf' not in rows and '/System/Packages/Calculator.elf' in rows
   after=struct.unpack('<4Q',ui.memory(g,ui.symbol('stats',32,True)[0],32));assert after[0]==before[0]
   p.close_app(3,True);p.drain();p.desktop(94,True);f.create(g,p,'123',26);assert '/Users/Owner/Documents/123' in ui.s.directories(disk);s.shot(g,out,'files-after-app-removal',True)
   (out/'native.log').write_bytes(g.log().encode());report.update(managed_current_bytes=after[0]*4096,managed_peak_bytes=after[1]*4096,retained_page_delta=after[0]-before[0])
  report['checks']=['The actual minimal installed disk restores active Dvorak and 150-percent providers after firmware startup, not just stored preference bytes','Base Settings installs Calculator from the offline cache; the original native worker launches; reviewed removal preserves cache, files and base services','Calculator launch/close/removal retains no managed pages; required Files still creates a real persistent directory afterward'];report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
