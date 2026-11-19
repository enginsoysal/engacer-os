"""Inspect original PE bytes through ordinary native file-picker input."""
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
from fixture1 import library,StoppedDisk

def fingerprint(data):
    pe=struct.unpack_from('<I',data,60)[0]
    sections=struct.unpack_from('<H',data,pe+6)[0]
    options=struct.unpack_from('<H',data,pe+20)[0]
    header=struct.unpack_from('<I',data,pe+24+60)[0]
    value=2166136261
    ranges=[data[:header]]
    for i in range(sections):
        size,offset=struct.unpack_from('<II',data,pe+24+options+i*40+16)
        ranges.append(data[offset:offset+size])
    for block in ranges:
        for byte in block:value=((value^byte)*16777619)&0xffffffff
    return value

def output(g):
    raw=ui.memory(g,ui.symbol('info8',installed=True)[0],496+16384)
    return struct.unpack_from('<4I',raw),raw[304:496].split(b'\0')[0].decode(errors='replace'),raw[496:].split(b'\0')[0].decode(errors='replace')

def check(g,p,path):
    p.desktop(12012,True)
    p.desktop(54019,True);c.key(g,'ctrl','a');c.type_text(g,'/Users/Owner/Downloads');c.key(g,'ret');p.drain()
    entries=f.entries(g);index=entries[path]['index']
    for _ in range(128):
        if any(row[5]==55000+index for row in f.controls(g)):break
        p.desktop(54023,True)
    else:raise AssertionError('The selected test file is not reachable')
    p.desktop(55000+index,True)
    start=len(g.log());p.desktop(54011,True)
    deadline=time.monotonic()+120
    while time.monotonic()<deadline:
        if 'M8_JOB_DONE' in g.log()[start:] or 'M8_JOB_FAILED' in g.log()[start:]:
            p.drain();return output(g)
        time.sleep(.05)
    raise TimeoutError('Native Windows inspection did not finish')

def main():
    out=ROOT/'build/m14-native/stage1/inspection';out.mkdir(parents=True,exist_ok=True)
    meta=json.loads(ui.manifest_path12().read_text())
    baseline=json.loads((ROOT/'build/m14-native/stage1/ordinary/results.json').read_text())
    assert baseline['passed'] and baseline['build_id']==meta['build_id']
    original=Path(os.environ['LOCALAPPDATA'])/'EngineOS/Tests/M6/m141-stage1-ordinary'/baseline['owned_fixture']/'owned.img'
    work,disk,cloned=clone(ui,original,'m141-inspection')
    research=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0'
    sources={'Notepad.exe':research/'notepadpp/notepad++.exe','Sumatra.exe':research/'sumatra/SumatraPDF-3.6.1-64.exe'}
    report=dict(passed=False,stage='M14.1',build_id=meta['build_id'],clone=cloned,checks=[])
    mounted=StoppedDisk(disk,library())
    try:
        data={name:path.read_bytes() for name,path in sources.items()}
        for name,body in data.items():mounted.put('/Users/Owner/Downloads/'+name,body)
        mounted.put('/Users/Owner/Downloads/Invalid.exe',b'MZ'+bytes(62))
    finally:mounted.close()
    try:
        boot=ui.guest(work/'inspect',disk,media='installed',ready='M7_DESKTOP_READY',resolution=(1920,1080),ram=512)
        ui.s.normal_boot(boot)
        with boot as g:
            p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p)
            t.launch(g,p,'windows apps',19)
            initial=f.stats(g)[0]
            warm=check(g,p,'/Users/Owner/Downloads/Notepad.exe')
            report['first_worker_initialization_pages']=f.stats(g)[0]-initial
            assert warm[0][0]==2 and 0<=report['first_worker_initialization_pages']<=4,(warm,report)
            for name,body in data.items():
                before=f.stats(g)[0]
                state,message,text=check(g,p,'/Users/Owner/Downloads/'+name)
                expected=fingerprint(body)
                assert state[0]==2 and state[2]==0,(state,message,text)
                assert 'source-fnv32='+str(expected) in text and 'No app code was executed.' in text,text
                assert f.stats(g)[0]==before,'Inspection retained managed pages'
                report['checks'].append(dict(file=name,original_sha256=hashlib.sha256(body).hexdigest(),source_fnv32=expected,output=text,retained_pages=0))
                g.qmp('stop')
                try:ui.raw_shot(g,out,name.replace('.exe',''),True)
                finally:g.qmp('cont')
            before=f.stats(g)[0]
            state,message,text=check(g,p,'/Users/Owner/Downloads/Invalid.exe')
            assert state[0]==3 and f.stats(g)[0]==before,(state,message,text)
            report['checks'].append(dict(file='Invalid.exe',refused=True,message=message,retained_pages=0))
            (out/'serial.log').write_text(g.log())
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:
        (out/'results.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
