"""Original console lifecycle and honest browser-choice UI on an owned guest."""
import hashlib,json,os,struct,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
os.environ['ENGACER12_IMAGE']='EngacerOS-M14STAGE1'
sys.path[:0]=[str(ROOT/'tests/m12'),str(ROOT/'tests/m13')]
import taskbar_observe as t
ui=t.ui;c=t.c;f=t.f
import capture14,observer8
capture14.bind(ui);observer8.bind(ui)
from access_fixtures16 import clone

def task(g,p,action):
    start=len(g.log());p.desktop(action,True,settle=False)
    g.wait('M8_CPL3_CREATED',start)
    deadline=time.monotonic()+240
    while time.monotonic()<deadline:
        log=g.log()[start:]
        if 'M8_JOB_DONE' in log:break
        if 'M8_JOB_FAILED' in log:
            raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384)
            raise AssertionError(raw[304:].split(b'\0',1)[0].decode(errors='replace')+' OUTPUT '+raw[496:].split(b'\0',1)[0].decode(errors='replace'))
        time.sleep(.05)
    else:raise TimeoutError('The Windows worker did not finish')
    p.drain()
    raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384)
    assert struct.unpack_from('<III',raw)==(2,struct.unpack_from('<I',raw,4)[0],0),raw[:16]
    return raw[496:].split(b'\0')[0].decode(errors='replace')

def main():
    out=ROOT/'build/m14-native/stage1/apps';out.mkdir(parents=True,exist_ok=True);c.OUT=out
    meta=json.loads(ui.manifest_path12().read_text())
    baseline=json.loads((ROOT/'build/m14-native/stage1/ordinary/results.json').read_text())
    assert baseline['passed'] and baseline['build_id']==meta['build_id']
    original=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage1-ordinary'/baseline['owned_fixture']/'owned.img'
    work,disk,cloned=clone(ui,original,'m141-apps')
    report=dict(passed=False,stage='M14.1',build_id=meta['build_id'],clone=cloned,owned_fixture=work.name,checks=[])
    try:
        boot=ui.guest(work/'apps',disk,media='installed',ready='M7_DESKTOP_READY',resolution=(1920,1080),ram=512)
        ui.s.normal_boot(boot)
        with boot as g:
            p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p)
            t.launch(g,p,'windows apps',19)
            p.desktop(12001,True);task(g,p,12003)
            text=task(g,p,12005);assert '7-Zip' in text,text
            task(g,p,12006);task(g,p,12007);c.shot(g,'original-console')
            product='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}'
            provenance=json.loads((ROOT/'third_party/7zip/provenance.json').read_text())
            sys.path.insert(0,str(ROOT/'tests/m8'))
            from database import original_tables
            tables=original_tables();components={row[0]:row[2] for row in tables['Component']}
            verified={}
            for row in tables['File']:
                identifier,component,filename=row[:3]
                path=product+('/Lang/' if components[component]=='MyLang' else '/')+filename.split('|')[-1]
                digest=hashlib.sha256(ui.s.s.document(disk,path,8*1024**2)).hexdigest()
                assert digest==provenance['original_payload_sha256'][identifier],path
                verified[path]=digest
            report['original_payload_sha256']=verified
            p.desktop(12002,True);task(g,p,12003)
            assert product+'/7z.exe' not in f.entries(g)
            p.desktop(12001,True);task(g,p,12003);task(g,p,12005)
            report['checks'].append('Original 7-Zip MSI install/run/archive/extract/remove/reinstall and all 106 original payload hashes pass')
            t.close_all(g,p);t.launch(g,p,'browser',17)
            p.desktop(15009,True);c.shot(g,'browser-choices')
            assert any(row[5]==15010 for row in f.controls(g))
            p.desktop(15009,True);p.desktop(15009,True)
            report['checks'].append('Browser choices opens and returns through ordinary controls; Firefox explicitly remains download-only')
            (out/'serial.log').write_text(g.log())
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:
        (out/'results.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({k:v for k,v in report.items() if k!='original_payload_sha256'},indent=2),flush=True)

if __name__=='__main__':main()
