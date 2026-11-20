"""Exact installed original file-manager window profile; broader app tasks remain open."""
import argparse,hashlib,json,os,struct,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tests/m14'))
from window144_native import ui,c,f,t,clone,task,output,drag
from original_window_trace4 import views,controls,wait_for
import capture14
capture14.bind(ui)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--profile',choices=['compact','ordinary','4k'],default='compact');parser.add_argument('--cycles',type=int,default=21);args=parser.parse_args();assert 1<=args.cycles<=21
 out=ROOT/'build/m14-native/stage4'/('original-native-'+args.profile);out.mkdir(parents=True,exist_ok=True);c.OUT=out;meta=json.loads(ui.manifest_path12().read_text());base=json.loads((ROOT/'build/m14-native/stage4/apps/results.json').read_text());assert base['passed']and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m144-window-apps'/base['owned_fixture']/'owned.img';work,disk,cloned=clone(ui,source,'m144-original-'+args.profile);original=ui.s.s.document(disk,'/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/7zFM.exe',8*1024**2);digest=hashlib.sha256(original).hexdigest();assert digest=='a12710799d5cb9b3076b86dd0f92d4a503b7062bc3efac62b7f4cb8a74e05931'
 report=dict(passed=False,original_gui_qualified=False,scope='M14.4 original file-manager window/input/lifetime profile only; NOT complete app tasks or general Windows compatibility',build_id=meta['build_id'],original_sha256=digest,profile=args.profile,clone=cloned,cycles=[])
 try:
  resolution,ram={'compact':((1280,800),128),'ordinary':((1920,1080),512),'4k':((3840,2160),1024)}[args.profile];boot=ui.guest(work/'original',disk,media='installed',ready='M7_DESKTOP_READY',resolution=resolution,ram=ram);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);front=t.launch(g,p,'windows apps',19);task(g,p,12005);before=f.stats(g)[0]
   for cycle in range(args.cycles):
    at=len(g.log());p.desktop(12100,True,settle=False);g.wait('M8_CPL3_CREATED',at);wait_for(g,lambda:len(t.records(g))==2);p.drain();root=next(v for v in views(g)if not v['parent']and v['class_name']=='7-Zip::FM');handle=root['handle'];row=lambda:next(v for v in views(g)if v['handle']==handle)
    wait_for(g,lambda:g.qmp('human-monitor-command',{'command-line':'info registers -a'}).count('HLT=1')==2);sample={'cycle':cycle+1,'halted_cpus_at_message_wait':2,'initial_bounds':list(f.model(g)[1])}
    if cycle==0:c.shot(g,'original-file-manager')
    edit=next(v for v in views(g)if v['class_name']=='Edit'and v['visible']);old=edit['title'];table={v['handle']:v for v in views(g)};x=y=0;node=edit
    while node['parent']:
     border=1 if node['style']&0x800000 else 0;x+=node['bounds'][0]+border;y+=node['bounds'][1]+border;node=table[node['parent']]
    x+=node['bounds'][0]+1;y+=node['bounds'][1]+40;scale=c.flag(g,'scale73')/2;p.move(int((x+8)*scale),int((y+8)*scale));p.down(True);p.down(False);p.drain();c.key(g,'z');wait_for(g,lambda:next(v for v in views(g)if v['handle']==edit['handle'])['title']!=old);c.key(g,'backspace');wait_for(g,lambda:next(v for v in views(g)if v['handle']==edit['handle'])['title']==old);sample['actual_original_edit_input']=True
    x,y,w,h=f.model(g)[1];direction=1 if cycle%2==0 else -1;drag(g,p,x+180,y+20,x+180+direction*30,y+20+direction*20);moved=f.model(g)[1];assert moved[:2]!=(x,y),(cycle,moved);sample['moved_bounds']=list(moved)
    x,y,w,h=moved;drag(g,p,x+w-4,y+h-4,x+w-4+direction*24,y+h-4+direction*18);resized=f.model(g)[1];assert resized[2:]!=(w,h),(cycle,resized);sample['resized_bounds']=list(resized)
    target=next(v for v in t.records(g)if v['slot']==f.model(g)[0]);owner=target['token'];minimum=next(r for r in controls(g)if r[5]==49000 and r[4]==owner);p.logical(minimum[0]+minimum[2]//2,minimum[1]+minimum[3]//2,True);p.drain();wait_for(g,lambda:next(v for v in t.records(g)if v['token']==owner)['minimized']and row()['style']&0x20000000);t.focus(g,p,target);p.drain();wait_for(g,lambda:not next(v for v in t.records(g)if v['token']==owner)['minimized']and not(row()['style']&0x20000000));sample['native_minimize_restore']=True
    normal=f.model(g)[1];p.desktop(49001,True);p.drain();wait_for(g,lambda:row()['style']&0x01000000);maximum=f.model(g)[1];sample['maximized_bounds']=list(maximum);p.desktop(49000,True);p.drain();wait_for(g,lambda:row()['style']&0x20000000);t.focus(g,p,target);p.drain();wait_for(g,lambda:row()['style']&0x01000000);assert f.model(g)[1]==maximum;p.desktop(49001,True);p.drain();wait_for(g,lambda:not(row()['style']&0x21000000));assert f.model(g)[1]==normal,(normal,f.model(g)[1]);sample['native_maximize_minimize_restore_consistency']=True
    if cycle==0:c.shot(g,'original-restored-window')
    p.desktop(49002,True);g.wait('M8_JOB_DONE',at);p.drain();state,command,status=struct.unpack('<3I',ui.memory(g,ui.symbol('info8',installed=True)[0],12));assert state==2 and not status,(state,status,output(g));assert len(t.records(g))==1 and t.records(g)[0]['token']==front['token'];assert ui.integer(g,'ui_resident144',True)==0
    retained=f.stats(g)[0]-before;assert retained==(1 if cycle==0 else 0),(cycle,retained);assert ui.integer(g,'clipboard_resident144',True)==1
    if cycle==0:before=f.stats(g)[0]
    sample['retained_pages']=retained;sample['exit_status']=status;report['cycles'].append(sample)
   report['output']=output(g);report['passed']=True;report['original_window_profile_passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps({k:v for k,v in report.items()if k!='cycles'},indent=2),flush=True)
if __name__=='__main__':main()
