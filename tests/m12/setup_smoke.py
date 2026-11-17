"""Development-only real setup layout and installed-first-use smoke."""
import argparse,json,os,traceback
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE15'
import setup_observe as z
ui=z.ui;ROOT=z.ROOT

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--compact',action='store_true');a=parser.parse_args();name='compact' if a.compact else 'ordinary';out=ROOT/'build/m12/stage15'/('setup-smoke-'+name);out.mkdir(parents=True,exist_ok=True)
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m12-stage15-setup-smoke-'+name);disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);report=dict(passed=False,development_only=True,build_id=meta['build_id'],owned_fixture=work.name,checks=[])
    try:
        with ui.guest(work/'install',disk,resolution=(800,600) if a.compact else (1280,800)) as g:
            p=ui.Pointer(g);p.drain();before=z.f.sha_file(disk);frames=z.flag(g,'full_frames75');z.shot(g,out,'welcome')
            z.wizard(g,p,2);z.shot(g,out,'keyboard');z.go(g,p,2,100);z.shot(g,out,'disk-selected');z.wizard(g,p,2);z.shot(g,out,'apps');z.wizard(g,p,2);z.shot(g,out,'style');z.go(g,p,32,50301,50311,2);z.shot(g,out,'review');assert z.f.sha_file(disk)==before and z.flag(g,'full_frames75')==frames
            at=z.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);p.drain();z.shot(g,out,'verified-finish');at=z.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain();z.shot(g,out,'installed-first-use',True);assert z.c.flag(g,'guide_open11');z.key(g,'esc');assert not z.c.flag(g,'guide_open11');z.c.idle(g);(out/'native.log').write_bytes(g.log().encode())
        report['checks']=['Real eight-step setup has bounded non-overlapping controls, no early disk writes or full-frame reload on Next, and actually installs/restarts into a dismissible themed base guide'];report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
