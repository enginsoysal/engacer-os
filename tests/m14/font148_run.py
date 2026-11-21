"""Observe real CPL3 GDI font pixels and lifecycle; not vendor qualification."""
import hashlib,json,os,struct,sys,traceback
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]

def ink(image,color,box):
 points=[];levels=set()
 for y in range(box[1],box[3]):
  for x in range(box[0],box[2]):
   r,g,b=image.getpixel((x,y));primary=b if color=='blue' else r
   if primary>180 and primary-max(g,r if color=='blue' else b)>45:
    points.append((x,y));levels.add((r,g,b))
 assert points,color
 return dict(pixels=len(points),width=max(x for x,y in points)-min(x for x,y in points)+1,height=max(y for x,y in points)-min(y for x,y in points)+1,coverage_colors=len(levels))

def main():
 from exe148_probe_build import build
 private,inputs=build();production=private.parent/'WINDOWS8.ELF'
 import replay8
 loader=replay8.ReplayLoader();sys.meta_path.insert(0,loader)
 try:
  from window144_native import ui,c,f,t,clone,library,StoppedDisk,task,output,wait
  from font148_build import build as build_fixture
  fixture=build_fixture();meta=json.loads(ui.manifest_path12().read_text());base=json.loads((ROOT/'build/m14-native/stage8/apps/results.json').read_text());assert base['passed'] and base['build_id']==meta['build_id']==inputs['kernel_build_id']
  source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m148-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m148-font-raster');mounted=StoppedDisk(disk,library())
  try:
   mounted.put('/System/Windows/runtime8.elf',production.read_bytes())
   mounted.put('/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',fixture.read_bytes())
  finally:mounted.close()
  out=ROOT/'build/m14-native/stage8/font-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out
  report=dict(passed=False,scope=__doc__,build_id=meta['build_id'],production_inputs=inputs,fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest(),observer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),clone=cloned)
  try:
   boot=ui.guest(work/'font',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
   with boot as g:
    p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19);task(g,p,12005);before=f.stats(g)[0];samples=[]
    for cycle in range(3):
     at=len(g.log());p.desktop(12100,True);g.wait('M8_CPL3_CREATED',at);wait(g,'M148_FONT_RASTER_WAITING');p.drain();assert len(t.records(g))==2
     name='font-raster-'+str(cycle+1);c.shot(g,name);image=Image.open(out/(name+'.png')).convert('RGB');scale=c.flag(g,'scale73');assert scale==2,scale
     assert image.getpixel((650,420))==(255,255,255),'GDI+ client clear did not replace the gray background'
     assert image.getpixel((650,390))==(255,0,0),'GDI+ solid client rectangle did not draw red pixels'
     assert image.getpixel((650,320))==(127,255,127) and image.getpixel((690,320))==(0,0,255),'Copied image pixels changed after source disposal/mutation or premultiplied alpha was lost'
     assert image.getpixel((631,250))==(2,2,2),('Straight-ARGB window blend differs from owned Windows HDC reference',image.getpixel((631,250)))
     green=[image.getpixel((xx,yy))for yy in range(210,240)for xx in range(631,811)];assert sum(1 for rr,gg,bb in green if gg>rr+25 and gg>bb+25)>80 and len(set(green))>8,'Actual GDI+ bitmap glyphs are missing'
     brown=[image.getpixel((xx,yy))for yy in range(170,200)for xx in range(631,821)];assert sum(1 for rr,gg,bb in brown if rr>gg+30 and gg>bb+15)>80 and len(set(brown))>8,'Actual GDI+ client glyphs are missing'
     large=[(xx,yy)for yy in range(310,405)for xx in range(425,615)if (lambda rgb:rgb[0]>160 and 40<rgb[1]<160 and rgb[2]<70)(image.getpixel((xx,yy)))];assert len(large)>300 and max(y for x,y in large)-min(y for x,y in large)>50 and max(x for x,y in large)-min(x for x,y in large)>50,'Actual large canonical font coverage is absent or still quantized to a small strike'
     purple=[(xx,yy)for yy in range(320,420)for xx in range(740,841)if (lambda rgb:rgb[2]>rgb[0]+30 and rgb[0]>rgb[1]+30)(image.getpixel((xx,yy)))];assert len(purple)>100 and max(yy for xx,yy in purple)-min(yy for xx,yy in purple)>2*(max(xx for xx,yy in purple)-min(xx for xx,yy in purple)),'Actual rotated glyphs are missing or not vertical'
     assert image.getpixel((250,420))==(42,157,143) and image.getpixel((430,420))!=(42,157,143),'Progress does not show its actual 60-percent position'
     blue=ink(image,'blue',(205,185,870,230));red=ink(image,'red',(205,250,875,305));assert red['height']>blue['height']*1.5 and red['width']>blue['width']*1.5,(blue,red);assert blue['coverage_colors']>8 and red['coverage_colors']>8,(blue,red)
     shield_colors=[image.getpixel((xx,yy)) for yy in range(340,380) for xx in range(211,391)];assert shield_colors.count((35,134,200))>5 and shield_colors.count((239,193,88))>5,'Native shield glyph is missing'
     c.key(g,'a');wait(g,'M148_SHIELD_CLEARED');assert 'M148_ASSOCIATION_REFRESH_WITH_LIVE_WINDOW_PASS' in output(g);assert g.log().count('M148_NATIVE_SHELL_ASSOCIATIONS_REFRESH')==cycle+1;assert 'M148_ACTUAL_FOREGROUND_KEYBOARD_PASS' in output(g);p.drain();c.shot(g,name+'-shield-cleared');cleared=Image.open(out/(name+'-shield-cleared.png')).convert('RGB');assert not any(cleared.getpixel((xx,yy)) in ((35,134,200),(239,193,88))for yy in range(340,380)for xx in range(211,391)),'Shield remained visible after clearing';assert cleared.getpixel((430,420))==(42,157,143),'Progress did not repaint the actual 90-percent update'
     p.desktop(49002,True);g.wait('M8_JOB_DONE',at);p.drain();assert 'M148_FONT_RASTER_LIFETIME_PASS' in output(g),output(g);assert len(t.records(g))==1 and t.records(g)[0]['token']==front['token'];assert ui.integer(g,'ui_resident144',True)==0
     retained=f.stats(g)[0]-before;assert retained==0,retained;samples.append(dict(cycle=cycle+1,blue14=blue,red28_underlined=red,actual_gdiplus_client_clear=True,actual_gdiplus_client_rectangle=True,actual_copied_image_after_source_disposal=True,actual_shield_show_hide=True,retained_pages=retained))
    report.update(passed=True,cycles=samples,native_shell_refresh_deliveries=3);(out/'serial.log').write_bytes(g.log().encode())
  except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
  finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
 finally:sys.meta_path.remove(loader)
if __name__=='__main__':main()
