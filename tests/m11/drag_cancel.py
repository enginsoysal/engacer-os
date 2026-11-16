"""Regression: Ctrl+Escape cancels a file drag before ordinary Start dispatch."""
import hashlib,json,os,struct,traceback
from pathlib import Path
import files as f
ui=f.ui;ROOT=ui.ROOT

def main():
 prior=json.loads((ROOT/'build/m11/files/results.json').read_text(encoding='utf-8'));assert prior['passed']
 sha=hashlib.sha256(ui.iso_path11().read_bytes()).hexdigest();assert prior['iso_sha256']==sha
 base=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m11-files'
 owned=max(base.iterdir(),key=lambda p:p.stat().st_mtime_ns);disk=owned/'owned.img';assert disk.resolve().is_relative_to(base.resolve())
 path='/Users/Owner/Documents/Welcome.txt';payload=ui.s.s.document(disk,path)
 work=ui.q.new_work('m116-drag-cancel');out=ROOT/'build/m11/files/drag-cancel';out.mkdir(parents=True,exist_ok=True)
 report={'passed':False,'iso_sha256':sha,'checks':[]}
 try:
  for ps2 in (False,True):
   label='ps2' if ps2 else 'usb'
   with ui.guest(work/label,disk,media='installed',ready='M7_DESKTOP_READY',ps2_only=ps2) as g:
    p=ui.Pointer(g);p.drain();f.nav(g,p,'/Users/Owner/Documents');f.select(g,p,path)
    slot=next(i for i,w in enumerate(f.s.windows(g)) if w[6] and w[5]==1)
    row=f.s.listing(g,slot).index(f.rows(g)[path][0]);x,y=f.control(g,1000+row);scale=ui.integer(g,'scale73',True)
    before=struct.unpack('<4Q',ui.memory(g,ui.symbol('stats',32,True)[0],32))
    for held in (True,False):
     p.move(x*scale//2,y*scale//2);p.drain();f.s.modifier(g,'ctrl',True,1)
     p.down(True);p.drain();p.move((x+24)*scale//2,y*scale//2);p.drain();assert f.flag(g,'file_drag11')
     if not held:f.s.modifier(g,'ctrl',False,0)
     f.key(g,'esc');assert not f.flag(g,'file_drag11') and not f.flag(g,'launcher')
     p.down(False)
     if held:f.s.modifier(g,'ctrl',False,0)
     p.drain();assert ui.s.s.document(disk,path)==payload
    after=struct.unpack('<4Q',ui.memory(g,ui.symbol('stats',32,True)[0],32));assert after[0]==before[0] and after[3]==before[3]
    (out/(label+'.log')).write_bytes(g.log().encode())
    report['checks'].append(label.upper()+': Escape and held-Ctrl Escape cancel genuine pointer file capture without opening Start, changing source bytes or retaining pages')
  report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
if __name__=='__main__':main()
