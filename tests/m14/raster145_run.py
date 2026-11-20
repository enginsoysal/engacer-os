"""Independent physical-pixel and ordinary-input checks on the M14.5 candidate."""
import argparse,hashlib,json,os,re,struct,sys,traceback
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
from window144_native import ui,c,f,t,clone,library,StoppedDisk,task,output,wait
from original_window_trace4 import wait_for
from raster145_build import build
from resource144_build import build as resource_build

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--profile',choices=['compact','4k'],default='compact');parser.add_argument('--cycles',type=int,default=21);args=parser.parse_args();assert 1<=args.cycles<=21
 out=ROOT/'build/m14-native/stage5'/('raster-native-'+args.profile);out.mkdir(parents=True,exist_ok=True);c.OUT=out
 fixture=build();resources=resource_build()/'resources144.dll'
 meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage5'/('apps' if args.profile=='compact' else 'apps-4k')/'results.json').read_text(encoding='utf-8'));assert base['passed'] and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/('EngineOS/Tests/M6/m145-window-apps'+('' if args.profile=='compact' else '-4k'))/base['owned_fixture']/'owned.img'
 work,disk,cloned=clone(ui,source,'m145-raster-'+args.profile);mounted=StoppedDisk(disk,library())
 folder='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/'
 try:mounted.put(folder+'7zFM.exe',fixture.read_bytes());mounted.put(folder+'resources144.dll',resources.read_bytes())
 finally:mounted.close()
 report=dict(passed=False,stage='M14.5',scope='Owned pixel/control fixture, not original application task qualification',build_id=meta['build_id'],fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest(),resource_sha256=hashlib.sha256(resources.read_bytes()).hexdigest(),clone=cloned,profile=args.profile,cycles=[])
 try:
  resolution,ram=((1280,800),128)if args.profile=='compact'else((3840,2160),1024)
  boot=ui.guest(work/'raster',disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution,ram=ram);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19);task(g,p,12005);before=f.stats(g)[0]
   for cycle in range(args.cycles):
    at=len(g.log());p.desktop(12100,True,settle=False);g.wait('M8_CPL3_CREATED',at);wait(g,'M145_RASTER_READY');wait_for(g,lambda:len(t.records(g))==2);p.drain()
    text=output(g);assert 'M145_RASTER_FAIL'not in text,text
    root_x,root_y,width,height=f.model(g)[1];scale=c.flag(g,'scale73')/2
    if cycle==0:
     c.shot(g,'native-raster-and-toolbar');image=Image.open(out/'native-raster-and-toolbar.png').convert('RGB')
     def pixel(x,y):return list(image.getpixel((int((root_x+1+x)*scale),int((root_y+40+y)*scale))))
     expected={'transparent':(20,20,[0,120,199]),'magenta':(21,20,[255,0,255]),'black':(22,20,[0,0,0]),'scaled_transparent':(40,20,[0,120,199]),'scaled_magenta':(42,20,[255,0,255]),'copied_list':(73,20,[255,0,255]),'negative_child_clip':(100,20,[0,0,0]),'child_right_edge':(101,20,[255,0,255]),'outside_child':(102,20,[0,120,199])}
     expected.update(static_transparent=(200,20,[255,255,255]),static_native_magenta=(201,20,[255,0,255]),static_center_magenta=(289,39,[255,0,255]),static_stretch_magenta=(322,20,[255,0,255]))
     report['physical_dimensions']=list(image.size);report['pixel_checks']={}
     for name,(x,y,rgb)in expected.items():actual=pixel(x,y);assert actual==rgb,(name,actual,rgb);report['pixel_checks'][name]=actual
    def click_marker(marker):
     match=re.search(marker+r' (\d+) (\d+)',text);assert match,text
     x,y=map(int,match.groups());p.move(int((root_x+1+x)*scale),int((root_y+40+y)*scale));p.down(True);p.down(False);p.drain()
    click_marker('M145_DISABLED_CENTER');assert 'M145_TOOLBAR_COMMAND_PASS'not in output(g) and 'M145_RASTER_FAIL'not in output(g),output(g)
    click_marker('M145_BUTTON_CENTER');wait(g,'M145_TOOLBAR_COMMAND_PASS')
    p.desktop(49002,True);g.wait('M8_JOB_DONE',at);p.drain();state,command,status=struct.unpack('<3I',ui.memory(g,ui.symbol('info8',installed=True)[0],12));assert state==2 and status==0,(state,command,status,output(g));assert 'M145_RASTER_LIFETIME_PASS'in output(g)
    retained=f.stats(g)[0]-before;assert retained==0,(cycle,retained)
    assert len(t.records(g))==1 and t.records(g)[0]['token']==front['token']
    report['cycles'].append(dict(cycle=cycle+1,retained_pages=retained,disabled_command_refused=True,ordinary_input_command=True,exit_status=status))
   report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
