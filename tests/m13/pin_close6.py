"""Diagnose only the owned native pin/close sequence without changing guest memory."""
import json,traceback
import taskbar_native6 as t
c=t.c;f=t.f;s=t.s;ui=t.ui;ROOT=t.ROOT
out=ROOT/'build/m13/stage6/pin-close-diagnostic';out.mkdir(parents=True,exist_ok=True);c.OUT=out
meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m136-pin-close');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);report=dict(passed=False,build_id=meta['build_id'],steps=[])
def record(g,name):
 r=dict(name=name,records=t.records(g),launcher=c.flag(g,'launcher'),context=c.flag(g,'context11'));report['steps'].append(r)
 if r['records']:
  r.update(dirty=t.app_view(g).dirty,text=bytes(t.app_view(g).text).decode(errors='replace'),closing=t.closing(g))
 c.shot(g,name)
try:
 with ui.guest(work/'install',disk) as g:
  p=ui.Pointer(g)
  for action in (2,2,100,2,2,2):c.wizard(g,p,action)
  at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain();s.close(g,p);record(g,'initial')
  t.right_group(g,p,2);f.menu(g,p,42702);record(g,'unpinned');assert not t.records(g)
  editor=t.launch(g,p,'text editor',2);record(g,'editor-opened')
  t.right_group(g,p,2);f.menu(g,p,42702);record(g,'repinned');t.focus(g,p,editor);record(g,'focused');assert any(r[5]==60002 for r in f.controls(g));p.desktop(60002,True);record(g,'notice-dismissed');s.close(g,p);record(g,'close-requested');assert not t.records(g),report['steps'][-1]
  report['passed']=True
except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
