"""Actual M12.8 native dialogs, ordinary input and independent persistent bytes."""
import argparse,ctypes,json,os,struct,time,traceback,zlib
os.environ['ENGACER12_IMAGE']='EngacerOS-M12STAGE8'
import files_observe as f
c=f.c;ui=f.ui;ROOT=f.ROOT
from focus_ownership import View

class Picker(ctypes.Structure):
    _fields_=[(n,ctypes.c_uint32) for n in ('purpose','phase','filter','selected','offset','count','rows','history_count','history_position','address_cursor','address_anchor','name_cursor','name_anchor')]+[(n,ctypes.c_uint64) for n in ('generation','target_first','target_size','selected_first','selected_size')]+[(n,ctypes.c_uint32) for n in ('target_crc','selected_crc','selected_kind')]+[(n,ctypes.c_char*256) for n in ('path','address','name','pending','selected_path')]+[('error',ctypes.c_char*160),('history',(ctypes.c_char*256)*8),('order',ctypes.c_uint16*1024)]

def picker(g):
    address,size=ui.symbol('picker12',installed=True);assert size==ctypes.sizeof(Picker),(size,ctypes.sizeof(Picker))
    return Picker.from_buffer_copy(ui.memory(g,address,size))

def appview(g,slot=None):
    if slot is None:slot=f.model(g)[0]
    address,size=ui.symbol('apps',installed=True)
    return View.from_buffer_copy(ui.memory(g,address+slot*(size//8),ctypes.sizeof(View)))

def count_windows(g):return int.from_bytes(ui.memory(g,ui.symbol('model',installed=True)[0]+232,4),'little')

def task(g,p,token):
    rows=[r for r in f.controls(g) if r[4]==token and r[5]==70];assert len(rows)==1,(token,rows)
    x,y,w,h,*_=rows[0];p.logical(x+w//2,y+h//2,True);p.drain()

def owner(g):return c.control(g,54010)[4]

def field(g,p,action,value):p.desktop(action,True);c.key(g,'ctrl','a');f.type_text(g,value)

def location(g,p,value):field(g,p,54019,value);c.key(g,'ret');p.drain()

def choose(g,p,name,open_item=False):
    state=picker(g);entries=f.entries(g);index=next(e['index'] for path,e in entries.items() if path==state.path.decode().rstrip('/')+'/'+name)
    for _ in range(128):
        if any(r[5]==55000+index for r in f.controls(g)):break
        p.desktop(54023,True)
    else:raise AssertionError(('Picker item not visible',name))
    if open_item:f.double(g,p,55000+index)
    else:p.desktop(55000+index,True)

def start_app(g,p,name):
    p.desktop(0,True);p.desktop(42004,True);c.key(g,'ctrl','a');c.type_text(g,name);c.key(g,'ret');p.drain()

def create_text(g,p,name,value):
    p.desktop(52000,True);f.menu(g,p,40018);c.key(g,'ctrl','a');c.type_text(g,name);c.key(g,'ret')
    p.desktop(f.item(g,p,name),True);c.key(g,'ret');c.type_text(g,value);c.key(g,'ctrl','s');p.desktop(49002,True)

def close_focused(g,p):p.desktop(49002,True);p.drain()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--smoke',action='store_true');args=parser.parse_args()
    out=ROOT/('build/m12/stage8/dialogs-smoke' if args.smoke else 'build/m12/stage8/dialogs-native');out.mkdir(parents=True,exist_ok=True);c.OUT=out
    meta=json.loads(ui.manifest_path12().read_text());work=ui.q.new_work('m12-stage8-dialogs-smoke' if args.smoke else 'm12-stage8-dialogs');disk=ui.q.sparse_disk(work/'owned.img',2*1024**3)
    report=dict(passed=False,stage='M12.8',development_only=args.smoke,build_id=meta['build_id'],iso_sha256=meta['artifacts'][ui.IMAGE12+'.iso']['sha256'],owned_fixture=work.name,checks=[],profiles=[])
    text=b'Original native text';saved=text+b' edited'
    try:
        live=ui.guest(work/'install',disk)
        with live as g:
            p=ui.Pointer(g)
            for command in (2,2,100,2,2,2):c.wizard(g,p,command)
            at=c.wizard(g,p,2);g.wait('M6_INSTALL_PASS',at,240);at=c.wizard(g,p,84);g.wait('M7_DESKTOP_READY',at,180);p=ui.Pointer(g);p.drain();before=f.stats(g)
            file_token=c.control(g,94)[4];p.desktop(94,True);create_text(g,p,'First.txt',text.decode());create_text(g,p,'Existing.txt','Keep original target')
            p.desktop(f.item(g,p,'First.txt'),True);c.key(g,'ret');c.key(g,'end');c.type_text(g,' edited');assert appview(g).dirty
            windows=count_windows(g);p.desktop(54001,True);assert c.flag(g,'file_dialog_state11')==10 and picker(g).purpose==2 and count_windows(g)==windows
            c.shot(g,'save-as-initial');p.desktop(54017,True);field(g,p,54020,'Saved.txt');p.desktop(54011,True)
            assert not c.flag(g,'file_dialog_state11') and f.app(g)['path']=='/Users/Owner/Downloads/Saved.txt' and bytes(appview(g).text)==saved and not appview(g).dirty
            report['checks'].append('Actual installation/retained-ISO startup; shared Save as chooses Downloads, persists exact text and keeps the original source without consuming another window slot')
            p.desktop(54001,True);assert picker(g).path==b'/Users/Owner/Downloads';p.desktop(54018,True);field(g,p,54020,'Cancelled.txt');p.desktop(54010,True)
            assert f.app(g)['path']=='/Users/Owner/Downloads/Saved.txt' and bytes(appview(g).text)==saved and '/Users/Owner/Pictures/Cancelled.txt' not in f.entries(g)
            p.desktop(54001,True);assert picker(g).path==b'/Users/Owner/Downloads';p.desktop(54010,True)
            report['checks'].append('Cancel preserves the document/path, creates no destination and does not change the remembered successful Save location')
            p.desktop(54000,True);assert picker(g).purpose==1;p.desktop(54016,True);choose(g,p,'First.txt');assert c.flag(g,'file_dialog_state11')==10 and f.app(g)['path']=='/Users/Owner/Downloads/Saved.txt';c.shot(g,'open-selected');c.key(g,'ret')
            assert not c.flag(g,'file_dialog_state11') and f.app(g)['path']=='/Users/Owner/Documents/First.txt' and bytes(appview(g).text)==text
            report['checks'].append('One click selects without replacing the app document; Enter opens the actual selected validated native text file')
            p.desktop(54000,True);p.desktop(54016,True);choose(g,p,'Welcome.txt');c.key(g,'ret');assert bytes(appview(g).text)==(ROOT/'distros/packages/m12-desktop-guide/content.txt').read_bytes()
            report['checks'].append('The real CPL3 Editor loads the checked multi-page included guide through existing IPC pages without a large kernel stack buffer')
            if not args.smoke:
                # Each operation uses visible controls and checks the real owner state.
                p.desktop(54001,True)
                for command in (54016,54017,54018,54015,54016,54017,54018,54015,54016):p.desktop(command,True)
                assert picker(g).history_count==8
                p.desktop(54012,True);assert picker(g).history_position==6
                p.desktop(54017,True);assert picker(g).history_position==7 and picker(g).history_count==8
                previous=bytes(picker(g).path);location(g,p,'/Users/Owner/DoesNotExist');assert picker(g).path==previous and picker(g).error
                location(g,p,'usb://0/');assert picker(g).path==previous and picker(g).error
                p.desktop(54016,True);field(g,p,54020,'Nested');p.desktop(54024,True);assert picker(g).phase==3
                field(g,p,54020,'Bad/Name');p.desktop(54011,True);assert picker(g).phase==3 and picker(g).error
                p.desktop(54026,True);assert picker(g).name==b'Nested'
                p.desktop(54024,True);field(g,p,54020,'Projects');p.desktop(54011,True);assert picker(g).path==b'/Users/Owner/Documents/Projects'
                p.desktop(54011,True);assert f.app(g)['path']=='/Users/Owner/Documents/Projects/Nested.txt' and not c.flag(g,'file_dialog_state11')
                report['checks'].append('Bounded eight-location history, history branching, missing/USB locations, invalid folder name, separate folder creation and automatic text extension use ordinary controls')
                p.desktop(54001,True);p.desktop(54016,True);field(g,p,54020,'Existing.txt');p.desktop(54011,True);assert picker(g).phase==1
                c.shot(g,'replace-review');c.key(g,'ret');assert picker(g).phase==0 and c.flag(g,'file_dialog_state11')==10
                p.desktop(54011,True);assert picker(g).phase==1;p.desktop(54010,True)
                assert f.app(g)['path']=='/Users/Owner/Documents/Projects/Nested.txt'
                report['checks'].append('Existing target requires an explicit replacement; default Enter returns to the picker and Cancel retains the original path')
                c.key(g,'end');c.type_text(g,' unsaved');dirty=bytes(appview(g).text);assert appview(g).dirty
                p.desktop(54000,True);p.desktop(54016,True);choose(g,p,'First.txt');c.key(g,'ret');assert picker(g).phase==2
                c.shot(g,'dirty-review');p.desktop(54026,True);assert appview(g).dirty and bytes(appview(g).text)==dirty
                choose(g,p,'First.txt');c.key(g,'ret');assert picker(g).phase==2;p.desktop(54028,True)
                assert not c.flag(g,'file_dialog_state11') and f.app(g)['path']=='/Users/Owner/Documents/First.txt' and bytes(appview(g).text)==text
                report['checks'].append('Dirty Open has a separate Save/Discard/Back/Cancel review; Back retains unsaved work and explicit Discard opens the selected original source')
                c.key(g,'end');c.type_text(g,' saved before open');p.desktop(54000,True);p.desktop(54017,True);choose(g,p,'Saved.txt');c.key(g,'ret');assert picker(g).phase==2;p.desktop(54027,True)
                assert f.app(g)['path']=='/Users/Owner/Downloads/Saved.txt' and bytes(appview(g).text)==saved and not appview(g).dirty
                text+=b' saved before open'
                report['checks'].append('Explicit Save and open persists the old modified document before loading the selected new source')
                p.desktop(54001,True);p.desktop(54016,True);field(g,p,54020,'Existing.txt');p.desktop(54011,True);assert picker(g).phase==1
                editor_token=owner(g);task(g,p,file_token);p.desktop(40015,True);c.key(g,'ctrl','a');c.type_text(g,'/Users/Owner/Documents');c.key(g,'ret');assert f.app(g)['path']=='/Users/Owner/Documents'
                p.desktop(f.item(g,p,'Existing.txt'),True);c.key(g,'ret');c.key(g,'end');c.type_text(g,' changed');c.key(g,'ctrl','s');close_focused(g,p)
                task(g,p,editor_token);assert picker(g).phase==1;p.desktop(54025,True);assert picker(g).phase==0 and picker(g).error and f.app(g)['path']=='/Users/Owner/Downloads/Saved.txt'
                c.shot(g,'changed-target-refused');p.desktop(54011,True);assert picker(g).phase==1;p.desktop(54025,True);assert not c.flag(g,'file_dialog_state11') and f.app(g)['path']=='/Users/Owner/Documents/Existing.txt'
                report['checks'].append('Another window remains usable during review; changing and saving the target invalidates the old replacement review, followed by a fresh explicit replacement')
                close_focused(g,p)
                start_app(g,p,'Image Viewer');p.desktop(74,True);assert picker(g).purpose==3
                p.desktop(54018,True);choose(g,p,'ColorStudy.bmp');c.key(g,'ret');assert not c.flag(g,'file_dialog_state11') and f.app(g)['path'].endswith('/ColorStudy.bmp')
                c.shot(g,'image-opened');close_focused(g,p)
                report['checks'].append('Image Viewer uses the common picker to open an actual native BMP while retaining its existing format checks')
                start_app(g,p,'Archive Manager');p.desktop(74,True);assert picker(g).purpose==4
                p.desktop(54017,True);choose(g,p,'ArchiveSample.zip');c.key(g,'ret');assert not c.flag(g,'file_dialog_state11') and f.app(g)['path'].endswith('/ArchiveSample.zip')
                p.desktop(54002,True);assert picker(g).purpose==5;p.desktop(54016,True);c.shot(g,'choose-extraction-folder');p.desktop(54011,True)
                assert not c.flag(g,'file_dialog_state11') and '/Users/Owner/Documents/Extracted' in f.entries(g)
                c.shot(g,'chosen-extraction-result');close_focused(g,p)
                report['checks'].append('Archive Manager opens a real ZIP and extracts into a newly created subfolder at the destination chosen through the shared folder dialog')
                p.desktop(94,True);p.desktop(f.item(g,p,'Existing.txt'),True);c.key(g,'ret')
                # Fault, display and restart profiles remain explicit pending gates.
                raise AssertionError('Remaining M12.8 fault/display/restart qualification is not yet complete')
            close_focused(g,p);assert count_windows(g)==1;f.same_pages(before,f.stats(g));c.idle(g);report['resources']=dict(before=list(before),after=list(f.stats(g)),retained_pages=0);(out/'install.log').write_bytes(g.log().encode())
        assert ui.s.s.document(disk,'/Users/Owner/Documents/First.txt')==text
        assert ui.s.s.document(disk,'/Users/Owner/Downloads/Saved.txt')==saved
        assert ui.s.s.document(disk,'/Users/Owner/Documents/Existing.txt')==b'Keep original target'
        report['passed']=True
    except Exception:
        report['error']=ui.q.clean(traceback.format_exc())
        if 'g' in locals():(out/'failure.log').write_bytes(g.log().encode())
        raise
    finally:
        (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
