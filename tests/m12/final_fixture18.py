"""Prepare a separate native default-effects fixture and verify reverse pane focus."""
import hashlib,json,os,traceback
from pathlib import Path
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE18'
import access_observe16 as a
from access_fixtures16 import clone
c=a.c;f=a.f;h=a.h;t=a.t;ui=a.ui;ROOT=a.ROOT

def main():
 out=ROOT/'build/m12/stage18/performance-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out;meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));native=json.loads((ROOT/'build/m12/stage18/access-native/results.json').read_text(encoding='utf-8'));assert native['passed'] and native['build_id']==meta['build_id'];source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage18-access'/native['owned_fixture']/'owned.img';original=f.sha_file(source);work,disk,cloned=clone(ui,source,'m12-stage18-performance');report=dict(passed=False,stage='M12.18',build_id=meta['build_id'],iso_sha256=native['iso_sha256'],owned_fixture=work.name,clone=cloned,checks=[])
 try:
  appearance=h.record(disk);start=ui.s.s.document(disk,'/System/Settings/start11-Owner.bin')
  with ui.guest(work/'prepare',disk,media='installed',ready='M7_DESKTOP_READY') as g:
   p=ui.Pointer(g);p.drain();c.open_settings(g,p);p.desktop(59004,True);p.desktop(60012,True);assert not c.flag(g,'access_flags16');h.close(g,p);assert h.record(disk)==appearance and ui.s.s.document(disk,'/System/Settings/start11-Owner.bin')==start
   if not t.records(g):a.launch(g,'files',1)
   files=next(w for w in t.records(g) if w['app']==1);assert len(t.records(g))==1
   a.key(g,'f6');assert c.flag(g,'access_region16')==1;a.key(g,'shift','f6');assert not c.flag(g,'access_region16') and a.focus(g)[1]==files['token'];a.key(g,'shift','f6');assert c.flag(g,'access_region16')==2;a.key(g,'f6');assert not c.flag(g,'access_region16') and a.focus(g)[1]==files['token'];a.key(g,'f1');assert a.semantic(g,'access_help_item16')['owner']==files['token'];c.shot(g,'reverse-pane-help');a.key(g,'esc');a.key(g,'esc');c.idle(g);(out/'native.log').write_bytes(g.log().encode())
  record=ui.s.s.document(disk,'/System/Settings/accessibility16-Owner.bin');assert record.hex()=='55413136010000000000000000000000';assert f.sha_file(source)==original;report['accessibility_record_hex']=record.hex();report['checks']=['A separately cloned installed fixture disables accessibility effects through actual Settings Reset, retaining exact appearance and Start bytes so native movement exercises the ordinary shadow-rendering path','Actual Shift+F6 reverses Taskbar → Window → Desktop, ordinary F6 returns to the window, and F1 describes its real owner without allocating a new application'];report['passed']=True
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
