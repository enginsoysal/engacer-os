"""BIOS regression for the exact M12 candidate, with unforced independent boots."""
import argparse
import os
import json
import traceback
parser=argparse.ArgumentParser();parser.add_argument('--stage',type=int,required=True);stage=parser.parse_args().stage
assert 2<=stage<=18
os.environ['ENGACER12_IMAGE']=f'EngacerOS-M12STAGE{stage}'
import components as c

ui=c.ui;ROOT=ui.ROOT

def main():
    c.OUT=ROOT/f'build/m12/stage{stage}/bios';c.OUT.mkdir(parents=True,exist_ok=True)
    meta=json.loads(ui.manifest_path12().read_text())
    report=dict(passed=False,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],firmware='BIOS',checks=[])
    work=ui.q.new_work(f'm12-stage{stage}-bios');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
    try:
        with ui.guest(work/'install',disk,firmware='bios') as g:
            p=ui.Pointer(g)
            for action in (2,2,100,2,2,2):c.wizard(g,p,action)
            at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240)
            at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180)
            ui.Pointer(g).drain();c.shot(g,'retained-iso-installed');c.idle(g)
            (c.OUT/'install.log').write_text(g.log(),encoding='utf-8')
        report['checks'].append('BIOS ISO traverses setup, installs and resets into the real installed desktop with matching media retained')
        for number in (1,2):
            candidate=ui.guest(work/f'independent-{number}',disk,firmware='bios',media='installed',ready='M7_DESKTOP_READY')
            ui.s.normal_boot(candidate)
            with candidate as g:
                ui.Pointer(g).drain();c.shot(g,f'disk-only-{number}');c.idle(g)
                assert 'M6_INSTALLED_VOLUME' in g.log()
                (c.OUT/f'disk-only-{number}.log').write_text(g.log(),encoding='utf-8')
            report['checks'].append(f'BIOS disk-only startup {number} uses ordinary firmware discovery and reaches idle native desktop')
        report['passed']=True
    except Exception as error:
        report['error']=str(error)
        (c.OUT/'failure.txt').write_text(traceback.format_exc().replace(str(ROOT),'<project-root>'),encoding='utf-8')
        raise
    finally:
        (c.OUT/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
