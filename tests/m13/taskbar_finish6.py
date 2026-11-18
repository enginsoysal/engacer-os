"""Complete only the final disk-start phase after the corrected capacity assertion."""
import hashlib,json,os,struct,traceback
from pathlib import Path
import taskbar_native6 as t
import observe6
observe6.bind(t.ui)
c=t.c;f=t.f;s=t.s;ui=t.ui;ROOT=t.ROOT
out=ROOT/'build/m13/stage6/taskbar-native';c.OUT=out
old=json.loads((out/'task-phase-original.json').read_text(encoding='utf-8'));meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));assert old['build_id']==meta['build_id'] and not old['passed'] and 'group_order(g)==[1,7,2,4,8,9]' in old['error']
assert len(old['checks'])==6 and old['checks'][-1].startswith('Eight pins and eight distinct running apps') and old['resources']['retained_pages']==0
work=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m136-taskbar'/old['owned_fixture'];disk=work/'owned.img';assert disk.is_file() and (work/'install/vars.fd').is_file()
report=dict(old);report.pop('error');report['passed']=False;report['continuation']=dict(reason='Only the final startup capacity assertion changed, from six to eight visible groups. Retain original failed observation; repeat both disk-only starts without modifying the frozen media or preceding task phase.',original_failed_report='diagnostics/initial-taskbar-order.json',native_task_phase_source='7714f5d',boot_checks=[])
try:
 saved=ui.s.s.document(disk,'/System/Settings/start11-Owner.bin');assert hashlib.sha256(saved).hexdigest()==old['preferences_sha256']
 for n in (1,2):
  boot=ui.guest(work/('capacity-corrected-'+str(n)),disk,media='installed',ready='M7_DESKTOP_READY');ui.s.normal_boot(boot,work/'install/vars.fd')
  with boot as g:
   p=ui.Pointer(g);p.drain();assert bytes(s.prefs(g))==saved;actual=t.group_order(g);assert actual==[1,7,2,4,8,9,14,16] and len(t.group_controls(g))==8,(actual,t.group_controls(g));c.shot(g,'ordinary-'+str(n));p.desktop(43101,True);assert t.records(g)[0]['minimized'];p.desktop(43101,True);c.idle(g);(out/('ordinary-'+str(n)+'.log')).write_text(g.log(),encoding='utf-8');report['continuation']['boot_checks'].append(dict(start=n,pins=actual,sha256=hashlib.sha256(bytes(s.prefs(g))).hexdigest(),minimize_restore=True))
 report['checks'].append('Two fresh ordinary no-ISO starts preserve exact independently read eight-pin preferences, show all eight groups and minimize/restore the real Files window')
 report['passed']=True
except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
finally:(out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
