"""Distinct normal rectangles: detect shared restore state, not identical defaults."""
import json,os,struct,time,traceback
from pathlib import Path
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE11'
import taskbar_observe as t
c=t.c;f=t.f;s=t.s;ui=t.ui;ROOT=t.ROOT

def rect(g,slot):
    return struct.unpack('<4i',ui.memory(g,ui.symbol('model',installed=True)[0]+slot*28,16))

def move(g,p,window,dx,dy):
    t.focus(g,p,window);x,y,w,h=rect(g,window['slot']);scale=c.flag(g,'scale73')
    p.move((x+180)*scale//2,(y+18)*scale//2);p.drain();p.down(True);p.drain();p.move((x+180+dx)*scale//2,(y+18+dy)*scale//2);p.drain();p.down(False);p.drain()
    assert not c.flag(g,'switch_open11') and rect(g,window['slot'])==(x+dx,y+dy,w,h)

def main():
    out=ROOT/'build/m12/stage11/restore-native';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    native=json.loads((ROOT/'build/m12/stage11/multitask-native/results.json').read_text(encoding='utf-8'));meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));assert native['passed'] and not native['development_only'] and native['build_id']==meta['build_id']
    original=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m12-stage11-multitask'/native['owned_fixture'];disk=original/'owned.img';work=ui.q.new_work('m12-stage11-distinct-restore')
    report=dict(passed=False,stage='M12.11',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],checks=[])
    try:
        boot=ui.guest(work/'installed',disk,media='installed',ready='M7_DESKTOP_READY');ui.s.normal_boot(boot,original/'install/vars.fd')
        with boot as g:
            p=ui.Pointer(g);p.drain();before=f.stats(g);first=t.records(g)[0];c.key(g,'meta_l','e');assert s.windows(g,1)==2;second=next(w for w in t.records(g) if w['slot']==f.model(g)[0])
            move(g,p,first,40,20);move(g,p,second,-20,10);a=rect(g,first['slot']);b=rect(g,second['slot']);assert a!=b;c.shot(g,'different-normal-rectangles');report['normal_before']=[list(a),list(b)];report['distinct_normal_bounds']=True
            report['checks'].append('Ordinary Win+E opens a second real Files window; pointer movement gives the two live generation tokens different actual normal rectangles before any snap')
            t.focus(g,p,first);c.key(g,'alt','spc');f.menu(g,p,44006);p.desktop(44100,True);assert c.flag(g,'switch_open11')==3
            count=c.flag(g,'switch_count11');tokens=struct.unpack('<'+str(count)+'Q',ui.memory(g,ui.symbol('switch_tokens11',installed=True)[0],count*8));p.desktop(44100+tokens.index(second['token']),True)
            assert rect(g,first['slot'])==(0,0,640,740) and rect(g,second['slot'])==(640,0,640,740);c.shot(g,'distinct-windows-paired')
            c.key(g,'meta_l','down');assert rect(g,second['slot'])==b;t.focus(g,p,first);c.key(g,'meta_l','down');assert rect(g,first['slot'])==a;c.shot(g,'different-normal-rectangles-restored');report['normal_after']=[list(rect(g,first['slot'])),list(rect(g,second['slot']))];assert report['normal_after']==report['normal_before']
            report['checks'].append('Complementary snap places those two tokens in actual opposite halves; restoring in reverse order recovers each distinct independently observed rectangle exactly')
            t.focus(g,p,second);c.key(g,'meta_l','right');assert c.flag(g,'switch_open11')==3;c.key(g,'esc');c.key(g,'meta_l','up');assert rect(g,second['slot'])==(0,0,1280,740);c.key(g,'meta_l','down');assert rect(g,second['slot'])==b and rect(g,first['slot'])==a
            report['checks'].append('Snap, skip assistance, maximize and restore retain the second token\'s original rectangle without changing the first window')
            t.close_all(g,p);p.desktop(43101,True);f.same_pages(before,f.stats(g));c.idle(g);report['resources']=dict(before=list(before),after=list(f.stats(g)),retained_pages=0);(out/'native.log').write_bytes(g.log().encode())
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
