"""M12.12 real e1000 DHCP/link transitions in the open quick-settings panel."""
import json,os,time,traceback
from pathlib import Path
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE12'
import tray_observe as q
c=q.c;f=q.f;ui=q.ui;ROOT=q.ROOT

def wait(g,state):
    deadline=time.monotonic()+90
    while q.network(g)[0]!=state:
        if time.monotonic()>deadline:raise TimeoutError(('network state',state,q.network(g)))
        time.sleep(.1)
    return q.network(g)

def main():
    out=ROOT/'build/m12/stage12/tray-network';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    native=json.loads((ROOT/'build/m12/stage12/tray-native/results.json').read_text(encoding='utf-8'));meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));assert native['passed'] and native['build_id']==meta['build_id']
    work=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage12-tray'/native['owned_fixture'];report=dict(passed=False,build_id=meta['build_id'],checks=[],states=[])
    try:
        with ui.guest(work/'network',work/'owned.img',media='installed',ready='M7_DESKTOP_READY',extra=['-netdev','user,id=tray-net','-device','e1000,id=tray-nic,netdev=tray-net,mac=52:54:00:12:34:61']) as g:
            p=ui.Pointer(g);p.drain();connected=wait(g,3);assert connected[2];q.open_quick(g);p.drain();assert not q.has(g,58013);c.shot(g,'real-local-network');baseline=f.stats(g);report['states'].append(list(connected))
            g.qmp('set_link',{'name':'tray-nic','up':False});disconnected=wait(g,1);p.drain();assert not disconnected[2] and q.has(g,58013) and c.flag(g,'tray_open12')==1;c.shot(g,'real-link-disconnected');report['states'].append(list(disconnected))
            p.desktop(58013,True);wait(g,1);assert not q.network(g)[2] and c.flag(g,'tray_open12')==1
            g.qmp('set_link',{'name':'tray-nic','up':True});connected=wait(g,3);p.drain();assert connected[2] and not q.has(g,58013) and c.flag(g,'tray_open12')==1;c.shot(g,'real-link-reconnected');report['states'].append(list(connected))
            c.key(g,'esc');f.same_pages(baseline,f.stats(g));c.idle(g);report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0);(out/'native.log').write_bytes(g.log().encode())
        report['checks'].append('Real e1000 DHCP, cable disconnection, an explicit Retry with cable down and reconnection update the already-open quick panel; local addressing is observed without claiming Internet reachability')
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
