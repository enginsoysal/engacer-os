"""Development-only real M12.13 visual preview and exact preference-byte smoke."""
import json,os,struct,traceback
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE13'
import tray_observe as q
c=q.c;f=q.f;s=q.s;t=q.t;ui=q.ui;ROOT=q.ROOT

def preview(g):return struct.unpack_from('<Q5I',ui.memory(g,ui.symbol('settings_preview13',32,True)[0],32))

def main():
    out=ROOT/'build/m12/stage13/settings-smoke';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m12-stage13-settings-smoke');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3);report=dict(passed=False,stage='M12.13',development_only=True,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],owned_fixture=work.name,checks=[])
    try:
        with ui.guest(work/'install',disk) as g:
            p=q.install(g);baseline=f.stats(g);original=c.dark(g);before=f.sha_file(disk);c.open_settings(g,p);c.shot(g,'appearance');p.desktop(43,True);assert c.dark(g)==1 and preview(g)[0];p.desktop(59005,True);assert c.dark(g)==original and not preview(g)[0] and f.sha_file(disk)==before
            p.desktop(45001,True);p.desktop(40,True);c.shot(g,'appearance-preview');p.desktop(47,True);assert not preview(g)[0] and 'saved' in f.app(g)['notice'].lower();record=ui.s.s.document(disk,'/System/Settings/appearance11-Owner.bin');values=struct.unpack_from('<8I',record);assert len(record)==352 and values[2]==0x62e5bd and values[5]==0x182039
            p.desktop(59001,True);c.shot(g,'display');p.desktop(59002,True);c.shot(g,'input');p.desktop(59003,True);c.shot(g,'system');s.close(g,p);f.same_pages(baseline,f.stats(g));c.idle(g);report['resources']=dict(before=list(baseline),after=list(f.stats(g)),retained_pages=0);(out/'native.log').write_bytes(g.log().encode())
        report['checks'].append('Real install/retained-ISO startup, four Settings categories, disk-identical Cancel, explicit Apply with independently verified 352-byte preferences, zero retained pages and idle halt')
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
