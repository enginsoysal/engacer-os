"""Ordinary native text/resize cursor tasks on exact owned M13.10 fixtures."""
import argparse,json,os,struct,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
os.environ['ENGACER12_IMAGE']='EngacerOS-M13STAGE10'
sys.path.insert(0,str(ROOT/'tests/m12'))
import taskbar_observe as t
import observer8,capture14
from access_fixtures16 import clone
c=t.c;f=t.f;ui=t.ui
observer8.bind(ui);capture14.bind(ui)

def main():
 p=argparse.ArgumentParser();p.add_argument('--profile',choices=['ordinary','compact','1024','150','4k'],required=True);a=p.parse_args()
 physical,ram={'ordinary':((1920,1080),512),'compact':((1280,800),128),'1024':((1024,768),128),'150':((1920,1200),512),'4k':((3840,2160),1024)}[a.profile]
 meta=json.loads(ui.manifest_path12().read_text());native=json.loads((ROOT/'build/m13/stage10'/a.profile/'results.json').read_text());assert native['passed'] and native['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6'/('m13-stage10-'+a.profile)/native['owned_fixture']/'owned.img'
 work,disk,cloned=clone(ui,source,'m1310-cursors-'+a.profile)
 out=ROOT/'build/m13/stage10'/('cursors-'+a.profile);out.mkdir(parents=True,exist_ok=True);c.OUT=out
 report=dict(passed=False,build_id=meta['build_id'],iso_sha256=meta['artifacts']['EngacerOS-M13STAGE10.iso']['sha256'],physical=list(physical),clone=cloned,checks=[],observations=[])
 try:
  with ui.guest(work/'installed',disk,resolution=physical,ram=ram,media='installed',ready='M7_DESKTOP_READY') as g:
   pointer=ui.Pointer(g);pointer.drain();c.key(g,'esc');t.close_all(g,pointer);baseline=f.stats(g)
   files=t.launch(g,pointer,'files',1)
   x,y,w,h=struct.unpack('<4i',ui.memory(g,ui.symbol('model',installed=True)[0]+files['slot']*28,16));scale=c.flag(g,'scale73')
   def hover(px,py,kind,name):
    pointer.move(px*scale//2,py*scale//2);pointer.drain()
    actual=ui.integer(g,'cursor_kind19',True);assert actual==kind,(name,actual,kind)
    assert (c.flag(g,'pointer_x'),c.flag(g,'pointer_y'))==(px*scale//2*2//scale,py*scale//2*2//scale)
    c.shot(g,name);report['observations'].append(dict(name=name,kind=actual,logical_position=[px,py]))
   hover(x+1,y+h//2,2,'horizontal-resize')
   hover(x+w//2,y+1,3,'vertical-resize')
   hover(x+1,y+1,4,'northwest-resize')
   hover(x+w-1,y+1,5,'northeast-resize')
   hover(x+w-2,y+h-2,4,'southeast-resize')
   pointer.down(True);pointer.drain();pointer.move((x+w+8)*scale//2,(y+h+8)*scale//2);pointer.drain()
   resized=struct.unpack('<4i',ui.memory(g,ui.symbol('model',installed=True)[0]+files['slot']*28,16));assert resized[2:]!=(w,h)
   c.key(g,'esc');pointer.down(False);pointer.drain();assert struct.unpack('<4i',ui.memory(g,ui.symbol('model',installed=True)[0]+files['slot']*28,16))==(x,y,w,h)
   hover(x+160,y+18,0,'caption-arrow')
   report['checks'].append('Native edge/corner hover shows both axial and diagonal resize cursors; real resize changes bounds and Escape restores the exact original geometry')
   c.key(g,'meta_l');count=ui.integer(g,'control_count',True);raw=ui.memory(g,ui.symbol('controls',65536,True)[0],count*32)
   fields=[struct.unpack_from('<iiiiQI',raw,i*32) for i in range(count) if struct.unpack_from('<I',raw,i*32+24)[0]==42004];assert len(fields)==1
   fx,fy,fw,fh,_,_=fields[0];hover(fx+fw//2,fy+fh//2,1,'start-search-text')
   position=(c.flag(g,'pointer_x'),c.flag(g,'pointer_y'))
   c.key(g,'esc');assert ui.integer(g,'cursor_kind19',True)==0 and position==(c.flag(g,'pointer_x'),c.flag(g,'pointer_y'));c.shot(g,'keyboard-closed-start')
   report['observations'].append(dict(name='keyboard-closed-start',kind=0,unchanged_pointer=list(position)))
   c.key(g,'meta_l');assert ui.integer(g,'cursor_kind19',True)==1 and position==(c.flag(g,'pointer_x'),c.flag(g,'pointer_y'));c.shot(g,'keyboard-opened-start')
   report['observations'].append(dict(name='keyboard-opened-start',kind=1,unchanged_pointer=list(position)))
   c.key(g,'esc');t.launch(g,pointer,'settings',3);pointer.desktop(59003,True);pointer.desktop(59007,True)
   fx,fy,fw,fh,*_=c.control(g,60102);hover(fx+fw//2,fy+fh//2,1,'preview-field-text')
   report['checks'].append('Keyboard closing/reopening Start refreshes arrow/text context at an independently unchanged pointer position; the shared preview field also exposes its real text cursor')
   t.close_all(g,pointer);f.same_pages(baseline,f.stats(g));c.idle(g)
   report['checks'].append('Actual Start search field uses a scalable text cursor at the unchanged native hit coordinate; leaving it restores context, and completed cursor tasks retain zero managed pages')
   report['resources']=dict(retained_pages=0,all_cpus_halted_when_idle=True,cursor_kind_fixed_bytes=4)
   (out/'native.log').write_text(g.log(),encoding='utf-8')
  report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
