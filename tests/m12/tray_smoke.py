"""Development-only real installer/tray/provider/UI smoke for M12.12."""
import json,os,struct,traceback
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE12'
import tray_observe as q
c=q.c;f=q.f;ui=q.ui;ROOT=q.ROOT

def main():
    out=ROOT/'build/m12/stage12/tray-smoke';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m12-stage12-tray-smoke');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
    report=dict(passed=False,stage='M12.12',development_only=True,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],checks=[],owned_fixture=work.name)
    try:
        with ui.guest(work/'install',disk) as g:
            p=q.install(g);before,saved=q.basic(g,p,out,report['checks']);assert struct.unpack('<2I',ui.s.s.document(disk,'/System/Settings/audio74.bin'))==(0x41443734,saved)
            report['resources']=dict(before=list(before),after=list(f.stats(g)),retained_pages=0);(out/'native.log').write_bytes(g.log().encode())
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
