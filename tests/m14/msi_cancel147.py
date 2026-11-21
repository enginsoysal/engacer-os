"""Cancel the original MSI during staged writes, then reinstall and run it."""
import json,os,time,traceback
from pathlib import Path
from window144_native import ui,c,f,t,task
from access_fixtures16 import clone
ROOT=Path(__file__).resolve().parents[2]
def main():
 out=ROOT/'build/m14-native/stage7/msi-cancel';out.mkdir(parents=True,exist_ok=True);meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));base=json.loads((ROOT/'build/m14-native/stage7/compact/results.json').read_text(encoding='utf-8'));assert base['passed'] and base['build_id']==meta['build_id']
 source=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage7-compact'/base['owned_fixture']/'owned.img';work,disk,_=clone(ui,source,'m147-msi-cancel');report=dict(passed=False,build_id=meta['build_id'],scope='Actual original 7-Zip MSI cancellation before journal publication, complete namespace rollback and reinstall/run',canonical_observer_sha256='bfe8d1cab126fb98f238c8d056a8a2ccd10e9df820dc68643d7244b1a92a4370',source_derivation='Current stage UI/task harness, stage/output identity and actual generic staging progress marker; original functional and resource assertions retained')
 product='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}'
 try:
  boot=ui.guest(work/'cancel',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(boot)
  with boot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19)
   before=f.entries(g);pages=f.stats(g)[0];p.desktop(12001,True);at=len(g.log());p.desktop(12003,True,settle=False)
   g.wait('Staging and checking original application files.',at,120)
   committed=f.entries(g);assert any(path.startswith(product+'/') for path in committed),list(committed)[-5:]
   p.desktop(12008,True);after=f.entries(g);assert after==before,{'new':list(set(after)-set(before)),'missing':list(set(before)-set(after))}
   raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496);assert int.from_bytes(raw[:4],'little')==3 and b'cancel' in raw[304:].lower()
   delta=f.stats(g)[0]-pages;assert delta==4,delta
   report['cancel']={'committed_entries_seen':len(set(committed)-set(before)),'namespace_restored':True,'one_time_transition_pages':delta}
   stable=f.stats(g)[0];p.desktop(12001,True);task(g,p,12003);assert product+'/7z.exe' in f.entries(g);text=task(g,p,12005);assert '7-Zip' in text;assert f.stats(g)[0]==stable
   report.update(passed=True,reinstall_and_original_execution=True,subsequent_retained_pages=0);t.close_all(g,p);(out/'native.log').write_bytes(g.log().encode('utf-8'))
 except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
 finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode('utf-8'));print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
