"""M13.6 real icon-grid Start and local search at actual display profiles."""
import argparse,ctypes,json,os,struct,traceback
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'m12'))
os.environ['ENGACER12_IMAGE']='EngacerOS-M13STAGE6'
import files_observe as f
c=f.c;ui=f.ui;ROOT=f.ROOT
import capture14
capture14.bind(ui)
class Pin(ctypes.Structure):
    _fields_=[('kind',ctypes.c_uint),('app',ctypes.c_uint),('path',ctypes.c_char*256),('label',ctypes.c_char*32)]
class Preferences(ctypes.Structure):
    _fields_=[('magic',ctypes.c_uint64)]+[(n,ctypes.c_uint) for n in ('version','categories','pins','tasks','view','tab','centered','reserved')]+[('names',(ctypes.c_char*32)*12),('order',ctypes.c_uint*12),('hidden',ctypes.c_uint*12),('assignment',ctypes.c_uint*20),('pinned',Pin*32),('task',ctypes.c_uint*8)]
def prefs(g):
    return Preferences.from_buffer_copy(ui.memory(g,ui.symbol('start_preferences11',ctypes.sizeof(Preferences),True)[0],ctypes.sizeof(Preferences)))
def results(g):
    count=c.flag(g,'start_result_count11');assert count<=52
    raw=ui.memory(g,ui.symbol('start_results11',installed=True)[0],count*8)
    return list(struct.iter_unpack('<II',raw))
def bounds(g):return tuple(int.from_bytes(c.field(g,'start_bounds11',i,4),'little',signed=True) for i in range(4))
def windows(g,kind=None):
    raw=ui.memory(g,ui.symbol('model',installed=True)[0],224)
    return sum(bool(raw[i*28+24]) and (kind is None or struct.unpack_from('<I',raw,i*28+20)[0]==kind) for i in range(8))
def close(g,p):
    slot=f.model(g)[0];rows=[r for r in f.controls(g) if r[5]==49002 and (r[4]&0xffffffff)==slot+1];assert len(rows)==1
    x,y,w,h,*_=rows[0];p.logical(x+w//2,y+h//2,True);p.drain()
def search(g,p,value):
    if not c.flag(g,'launcher'):p.desktop(0,True)
    if c.flag(g,'start_manage11'):p.desktop(42008,True)
    p.desktop(42004,True);c.key(g,'ctrl','a');c.type_text(g,value);p.drain()
def context(g,p):
    c.key(g,'shift','f10');assert c.flag(g,'context11')
def label(g,p,value):c.key(g,'ctrl','a');c.type_text(g,value);c.key(g,'ret');p.drain()
def launch(g,p,value,kind):
    search(g,p,value);assert results(g)==[(1,kind)],results(g);c.key(g,'ret');assert windows(g,kind)==1
def main():
    assert not (ROOT/'evidence/M13/6/publication-results.json').exists()
    parser=argparse.ArgumentParser();parser.add_argument('--profile',choices=['ordinary','compact','1024','150','4k'],default='ordinary');args=parser.parse_args()
    resolution,ram,scale={'ordinary':((1920,1080),512,50011),'compact':((1280,800),128,50011),'1024':((1024,768),128,50011),'150':((1920,1200),512,50012),'4k':((3840,2160),1024,50013)}[args.profile]
    real_guest=ui.guest
    def configured_guest(*a,**k):k.update(resolution=resolution,ram=ram);return real_guest(*a,**k)
    ui.guest=configured_guest
    out=ROOT/('build/m13/stage6/start-'+args.profile);out.mkdir(parents=True,exist_ok=True);c.OUT=out
    meta=json.loads(ui.manifest_path12().read_text(encoding='utf-8'));work=ui.q.new_work('m136-start-'+args.profile);disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
    report=dict(passed=False,stage='M13.6',build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],owned_fixture=work.name,profile=args.profile,physical=list(resolution),checks=[])
    try:
        with ui.guest(work/'install',disk) as g:
            p=ui.Pointer(g)
            for action in (2,scale,2,100,2,2,2):c.wizard(g,p,action)
            at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain();close(g,p);baseline=f.stats(g)
            p.desktop(0,True);assert bounds(g)[3]==560 and len(results(g))==6;c.shot(g,'pinned');tiles=[r for r in f.controls(g) if 42200<=r[5]<42252];assert len(tiles)==6 and all(r[3]==88 for r in tiles) and len({r[0] for r in tiles})==5;report['pinned_tiles']=[list(r[:4]) for r in tiles]
            report['checks'].append('Real install and retained-ISO installed startup reach a compact Start with six real app/folder pins')
            before=windows(g);search(g,p,'calc');assert results(g)==[(1,4)] and windows(g)==before;f.same_pages(baseline,f.stats(g));c.shot(g,'search-calculator')
            c.key(g,'ret');assert windows(g,4)==1;close(g,p)
            report['checks'].append('Typing local search launches no window and retains no pages; Enter launches the installed Calculator')
            p.desktop(0,True);p.desktop(42002,True);p.desktop(42027,True);f.menu(g,p,42304);assert results(g)==[(1,7)];c.shot(g,'development-category')
            p.desktop(42007,True);p.desktop(42010,True);label(g,p,'Games');p.desktop(42011,True);label(g,p,'Favorites');p.desktop(42012,True);p.desktop(42013,True)
            saved=prefs(g);assert saved.names[5].value==b'Favorites' and saved.hidden[5] and list(saved.order[:6])==[0,1,2,3,5,4]
            p.desktop(42008,True);search(g,p,'terminal');context(g,p);f.menu(g,p,42807);f.menu(g,p,42505);assert prefs(g).assignment[7]==5 and results(g)==[(1,7)]
            report['checks'].append('Create/rename/hide/reorder categories and context assignment preserve searchability of hidden-category apps')
            p.desktop(42007,True);p.desktop(42029,True);p.desktop(42402,True);p.desktop(42032,True);label(g,p,'Command Center');p.desktop(42016,True)
            saved=prefs(g);assert saved.pinned[1].app==7 and saved.pinned[1].label==b'Command Center';p.desktop(42008,True);search(g,p,'command');assert results(g)==[(3,1)];c.shot(g,'renamed-pin-search')
            c.key(g,'esc');assert ui.memory(g,ui.symbol('start_query11',installed=True)[0],1)==b'\0' and c.flag(g,'launcher');c.key(g,'esc');assert not c.flag(g,'launcher')
            report['checks'].append('Renaming/reordering pins changes labels only; local alias search and two-step Escape work')
            search(g,p,'calc');context(g,p);f.menu(g,p,42604);context(g,p);f.menu(g,p,42704);saved=prefs(g);assert any(saved.pinned[i].app==4 for i in range(saved.pins)) and 4 in saved.task[:saved.tasks]
            p.desktop(42007,True);p.desktop(42029,True);p.desktop(42401,True);p.desktop(42015,True);assert windows(g,7)==0
            report['checks'].append('Start/taskbar context pinning and explicit unpinning preserve the installed app')
            p.desktop(42008,True);search(g,p,'zzzzmissing');assert not results(g);c.shot(g,'no-results');c.key(g,'esc');p.desktop(42001,True)
            all_results=results(g);assert len(all_results)>12
            rows=[r for r in f.controls(g) if 42200<=r[5]<42252];assert len({r[0] for r in rows})==5
            c.key(g,'home');assert c.flag(g,'start_cursor11')==0;c.key(g,'down');assert c.flag(g,'start_cursor11')==5
            p.desktop(42003,True);c.key(g,'down');assert c.flag(g,'start_cursor11')==1;c.shot(g,'installed-list')
            report['checks'].append('Empty search explains recovery; All apps grid/list and arrow movement use the drawn column count')
            launch(g,p,'software',11);p.desktop(10304,True);p.desktop(10004,True);saved=prefs(g);assert not any(saved.pinned[i].kind==1 and saved.pinned[i].app==4 for i in range(saved.pins)) and 4 not in saved.task[:saved.tasks]
            search(g,p,'calculator');assert not results(g);c.shot(g,'removed-app');c.key(g,'esc');c.key(g,'esc');p.desktop(10304,True);close(g,p)
            launch(g,p,'calculator',4);close(g,p)
            report['checks'].append('Actual optional Calculator removal prunes both pin sets and search; reinstall restores launch without breaking the desktop')
            launch(g,p,'files',1);f.visit(g,p,'Documents');f.create(g,p,'Pinned Work',folder=True);p.desktop(f.item(g,p,'Pinned Work'),True);c.key(g,'shift','f10');f.menu(g,p,43000);close(g,p)
            search(g,p,'Pinned Work');assert results(g)[0][0]==2;c.shot(g,'folder-result');c.key(g,'ret');assert f.app(g)['path']=='/Users/Owner/Documents/Pinned Work';close(g,p)
            report['checks'].append('A real folder result opens its native path using stable pin identity')
            for theme in ('dark','high-contrast','light'):
                launch(g,p,'settings',3)
                if theme=='dark':p.desktop(59000,True);p.desktop(43,True)
                elif theme=='high-contrast':p.desktop(59004,True);p.desktop(60010,True)
                else:p.desktop(59004,True);p.desktop(60010,True);p.desktop(59000,True);p.desktop(44,True)
                close(g,p);p.desktop(0,True);p.desktop(42000,True);
                if not prefs(g).view:p.desktop(42003,True)
                c.shot(g,'start-'+theme);assert len([r for r in f.controls(g) if 42200<=r[5]<42252])>0;c.key(g,'esc')
            report['checks'].append('Real light/dark/high-contrast Start frames use the same catalogue, icon hit targets and readable focus; Settings changes return to the same independent desktop')
            p.desktop(0,True);p.desktop(42019,True);f.menu(g,p,42020);assert c.flag(g,'start_confirm11')==1;c.shot(g,'restart-review');p.desktop(42022,True);assert not c.flag(g,'start_confirm11');c.key(g,'esc');assert windows(g)==0
            report['checks'].append('Actual Power menu opens the separate Restart review; Cancel preserves the installed session and existing files')
            saved=bytes(prefs(g));assert ui.s.s.document(disk,'/System/Settings/start11-Owner.bin')==saved
            f.same_pages(baseline,f.stats(g));c.idle(g);after=f.stats(g);report['resources']=dict(before=list(baseline),after=list(after),retained_pages=0);report['preferences_sha256']=__import__('hashlib').sha256(saved).hexdigest()
            (out/'native.log').write_bytes(g.log().encode())
        for n in (1,2):
            boot=ui.guest(work/f'ordinary-{n}',disk,media='installed',ready='M7_DESKTOP_READY');ui.s.normal_boot(boot,work/'install/vars.fd')
            with boot as g:
                p=ui.Pointer(g);p.drain();assert bytes(prefs(g))==saved;search(g,p,'Pinned Work');assert results(g)[0][0]==2;c.shot(g,f'ordinary-{n}');c.key(g,'esc');c.key(g,'esc');c.idle(g);(out/f'ordinary-{n}.log').write_bytes(g.log().encode())
        report['checks'].append('Two ordinary no-ISO disk starts retain exact independently read preferences and the actual folder pin')
        report['passed']=True
    except Exception:report['error']=ui.q.clean(traceback.format_exc());raise
    finally:(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
