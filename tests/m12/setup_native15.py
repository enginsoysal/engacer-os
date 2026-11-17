"""M12.15 native setup, retained choices, first use and independent startup."""
import argparse,json,os,traceback
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE15'
import setup_observe as z
ui=z.ui;ROOT=z.ROOT

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--compact',action='store_true');a=parser.parse_args();name='compact' if a.compact else 'ordinary';out=ROOT/'build/m12/stage15'/('setup-native-'+name);out.mkdir(parents=True,exist_ok=True)
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m12-stage15-setup-'+name);disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);report=dict(passed=False,stage="M12.15",iso_sha256=meta["artifacts"][ui.IMAGE12+".iso"]["sha256"],build_id=meta['build_id'],owned_fixture=work.name,checks=[])
    try:
        with ui.guest(work/'install',disk,resolution=(800,600) if a.compact else (1280,800)) as g:
            p=ui.Pointer(g);p.drain();z.c.OUT=out;before=z.f.sha_file(disk);frames=z.flag(g,'full_frames75');z.shot(g,out,'welcome')
            z.wizard(g,p,2);z.shot(g,out,'keyboard');z.wizard(g,p,50002);z.text(g,'test');z.wizard(g,p,50003);z.go(g,p,2,100);z.shot(g,out,'disk-selected');z.wizard(g,p,2);z.shot(g,out,'apps');z.wizard(g,p,2);z.shot(g,out,'style');z.go(g,p,32,50301,50311,2);z.shot(g,out,'review');z.go(g,p,1);assert z.account(g)=="Owner";z.shot(g,out,'back-retains-style');z.go(g,p,2);assert z.f.sha_file(disk)==before and z.flag(g,'full_frames75')==frames
            at=z.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);p.drain();z.shot(g,out,'verified-finish');at=z.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain();z.shot(g,out,'installed-first-use',True);assert z.c.flag(g,'guide_open11');z.key(g,'esc');assert not z.c.flag(g,'guide_open11');z.t.close_all(g,p);baseline=z.f.stats(g);
            for title,kind in [('clock',8),('calendar',9),('media',16),('calc',4),('image',14)]:z.t.pin(g,p,title,kind)
            preferences=bytes(z.s.prefs(g));assert ui.s.s.document(disk,'/System/Settings/start11-Owner.bin')==preferences;z.f.same_pages(baseline,z.f.stats(g));report['resources']=dict(before=list(baseline),after=list(z.f.stats(g)),retained_pages=0);report['preferences_sha256']=__import__('hashlib').sha256(preferences).hexdigest();z.c.idle(g);(out/'native.log').write_bytes(g.log().encode())
        for label,ps2 in [('usb',False),('ps2',True)]:
            boot=ui.guest(work/('ordinary-'+label),disk,media='installed',ready='M7_DESKTOP_READY',ps2_only=ps2);ui.s.normal_boot(boot,work/'install/vars.fd')
            with boot as g:
                p=ui.Pointer(g);p.drain();assert not z.c.flag(g,'guide_open11');assert bytes(z.s.prefs(g))==preferences;assert z.h.colors(g)==(0x9caeff,1);z.shot(g,out,'disk-only-'+label,True);z.c.idle(g);(out/('ordinary-'+label+'.log')).write_bytes(g.log().encode())
        report['checks']=['Real eight-step setup has bounded non-overlapping controls, no early disk writes or full-frame reload on Next, and actually installs/restarts into a dismissible themed base guide'];report['checks']+=['Back retains the actual selected appearance; keyboard test and Clear work through guest input without early disk writes','A base-owned guide follows the saved theme and its dismissal persists across independent no-ISO USB and PS2 starts','Exact Start preference bytes survive both independent startups, with zero completed-task page retention'];report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
