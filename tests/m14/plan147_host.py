"""Parse original MSI plans, compare independent tables, close/reopen and refuse.

Own metadata code only; no original installer, custom action or app executes.
Fatal parser refusals run in separate owned host test processes.
"""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import subprocess
import struct
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command
OUT=ROOT/'build/m14-native/stage7/plan-host'

def build():
    OUT.mkdir(parents=True,exist_ok=True);tools=pinned_tools();objects=[]
    for source in ['user/windows8/msi_db.c','user/windows8/msi-plan147.c','user/windows8/msi-cost147.c','runtime/sha256.c','tests/m14/plan147_host.c']:
        obj=OUT/(Path(source).stem+'.obj');command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-I',ROOT/'include','-c',ROOT/source,'-o',obj]);objects.append(obj)
    command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(OUT/'plan147.dll'),*objects])

def worker(index,mutation):
    inputs=[ROOT/'third_party/7zip/7z2606-x64.msi',Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/0/npp.8.9.9.1.Installer.x64.msi'];path=inputs[index];data=path.read_bytes();inventory=json.loads((ROOT/'evidence/M14/0/msi-inventory.json').read_text(encoding='utf-8-sig'));original=next(x for x in inventory['packages']if x['file']==path.name);assert hashlib.sha256(data).hexdigest()==original['sha256'];target=OUT/(str(index)+'-'+mutation+'.json')
    refusal={'unknown':'MSI requires an unknown standard/custom action.','bad-shift':'MSI compound-file geometry is unsupported.','bad-directory-count':'MSI directory-sector count is invalid.','mini-fat-overquota':'MSI mini FAT exceeds its bound.','fat-cycle':'MSI directory chain is invalid.','truncated-sector':'MSI compound-file sector length is invalid.'}
    if mutation=='unknown':
        assert data.count(b'InstallFiles')==1;data=data.replace(b'InstallFiles',b'UnsupportedX')
    elif mutation in refusal:
        data=bytearray(data);sector=1<<struct.unpack_from('<H',data,30)[0]
        if mutation=='bad-shift':struct.pack_into('<H',data,30,12 if sector==512 else 9)
        elif mutation=='bad-directory-count':struct.pack_into('<I',data,40,struct.unpack_from('<I',data,40)[0]+1)
        elif mutation=='mini-fat-overquota':struct.pack_into('<I',data,64,65536//sector+1)
        elif mutation=='fat-cycle':
            directory=struct.unpack_from('<I',data,48)[0];fat=struct.unpack_from('<I',data,76+(directory//(sector//4))*4)[0];struct.pack_into('<I',data,(fat+1)*sector+(directory%(sector//4))*4,directory)
        elif mutation=='truncated-sector':data=data[:-1]
        data=bytes(data)
    elif mutation!='normal':raise ValueError(mutation)
    lib=ctypes.CDLL(str(OUT/'plan147.dll'));alloc_type=ctypes.CFUNCTYPE(ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t);free_type=ctypes.CFUNCTYPE(None,ctypes.c_void_p,ctypes.c_void_p);failure_type=ctypes.CFUNCTYPE(None,ctypes.c_char_p);live={};state={'bytes':0,'peak':0,'bad_free':False}
    @alloc_type
    def allocate(context,n):
        buf=ctypes.create_string_buffer(n);address=ctypes.addressof(buf);live[address]=(buf,n);state['bytes']+=n;state['peak']=max(state['peak'],state['bytes']);return address
    @free_type
    def release(context,address):
        if address not in live:state['bad_free']=True;return
        state['bytes']-=live.pop(address)[1]
    @failure_type
    def failure(message):
        text=message.decode();expected=mutation in refusal and text==refusal[mutation];target.write_bytes((json.dumps(dict(passed=expected,package=path.name,scope='Owned metadata refusal before any target mutation',expected_refusal=text,mutation=mutation),indent=2)+'\n').encode());os._exit(0 if expected else 87)
    class Action(ctypes.Structure):
        _fields_=[('name',ctypes.c_char_p),('condition',ctypes.c_char_p),('source',ctypes.c_char_p),('target',ctypes.c_char_p),('kind',ctypes.c_uint),('sequence',ctypes.c_uint)]
    class File(ctypes.Structure):
        _fields_=[('id',ctypes.c_char_p),('name',ctypes.c_char_p),('component',ctypes.c_uint),('size',ctypes.c_uint),('sequence',ctypes.c_uint),('attributes',ctypes.c_uint),('selected',ctypes.c_uint),('sha256',ctypes.c_ubyte*32)]
    lib.init147.argtypes=[alloc_type,free_type,failure_type];lib.open147.argtypes=[ctypes.c_void_p,ctypes.c_uint];lib.action147.argtypes=[ctypes.c_uint];lib.action147.restype=ctypes.POINTER(Action);lib.get147.argtypes=[ctypes.c_char_p];lib.get147.restype=ctypes.c_char_p;lib.set147.argtypes=[ctypes.c_char_p,ctypes.c_char_p];lib.property147.argtypes=[ctypes.c_uint];lib.condition147.argtypes=[ctypes.c_char_p];lib.init147(allocate,release,failure);buf=ctypes.create_string_buffer(data);checks=0;cycles=[]
    def check(yes):
        nonlocal checks
        assert yes;checks+=1
    lib.cost147.argtypes=[ctypes.c_char_p];lib.path147.argtypes=[ctypes.c_uint,ctypes.c_void_p];lib.file147.argtypes=[ctypes.c_uint];lib.file147.restype=ctypes.POINTER(File);lib.alias147.restype=ctypes.c_char_p;lib.format147.argtypes=[ctypes.c_char_p,ctypes.c_void_p,ctypes.c_uint]
    complete=json.loads((ROOT/'evidence/M14/7/development/msi-tables147.json').read_text(encoding='utf-8-sig'));metadata=next(x for x in complete['packages']if x['file']==path.name);assert metadata['sha256']==original['sha256']
    tables=original['tables'];cost_tables=metadata['tables'];expected_sequence=sorted(tables['InstallExecuteSequence'],key=lambda x:int(x[2]));custom=tables['CustomAction'];custom={}if isinstance(custom,dict)else{row[0]:row for row in custom}
    directories={row[0]:row for row in cost_tables['Directory']};roots=[row[0]for row in cost_tables['Directory']if row[1]in('ProgramFiles64Folder','ProgramFilesFolder')];assert len(roots)==1;root_id=roots[0];components={row[0]:row for row in cost_tables['Component']};expected_files={row[0]:row for row in cost_tables['File']};product_code=dict(tables['Property'])['ProductCode'].upper()
    def target_name(field):return field.split(':')[0].split('|')[-1]
    def relative(directory):
        if directory==root_id:return ''
        row=directories[directory];parent=relative(row[1]);leaf=target_name(row[2]);return '/'.join(x for x in [parent,''if leaf=='.'else leaf]if x)
    for cycle in range(21):
        count=lib.open147(buf,len(data));check(mutation=='normal'and count==len(expected_sequence))
        for name,value in tables['Property']:check(lib.get147(name.encode()).decode()==value)
        for i,expected in enumerate(expected_sequence):
            action=lib.action147(i).contents;name=action.name.decode();check([name,action.condition.decode(),str(action.sequence)]==expected)
            if name in custom:
                row=custom[name];check(action.kind==int(row[1])and action.source.decode()==row[2]and action.target.decode()==row[3])
            else:check(action.kind==0 and action.source is None and action.target is None)
        language=index==1 and cycle%4 in (1,3);no_updater=index==1 and cycle%4 in (2,3)
        blank=ctypes.create_string_buffer(512);check(lib.format147(b'[#BeforeCost]',blank,len(blank))==0 and blank.value==b'')
        check(lib.set147(b'Privileged',b'1')==0)
        if index==1:
            check(lib.set147(b'NPP_LANG',b'english'if language else b'')==0);check(lib.set147(b'NOUPDATER',b'1'if no_updater else b'')==0)
        lib.cost147(b'C:\\Users\\Owner');check(lib.files147()==len(expected_files));check(lib.alias147().decode()=='C:\\Program Files\\'+target_name(directories[root_id][2]))
        check(lib.get147(b'SystemFolder')==b'C:\\Windows\\SysWOW64\\'and lib.get147(b'System64Folder')==b'C:\\Windows\\System32\\'and lib.get147(b'WindowsFolder')==b'C:\\Windows\\')
        selected_features={'Program','Complete','LanguageFiles'}if index==0 else {'MainApplication'}|({'AutoUpdaterFeature'}if not no_updater else set())|({'NativeLangFeature'}if language else set())
        expected_components={row[1]for row in cost_tables['FeatureComponents']if row[0]in selected_features};selected_count=selected_bytes=0
        for i in range(lib.files147()):
            file=lib.file147(i).contents;row=expected_files[file.id.decode()];component=components[row[1]];check(file.size==int(row[3])and file.sequence==int(row[7])and file.attributes==int(row[6]));wanted=row[1]in expected_components;check(bool(file.selected)==wanted)
            output=ctypes.create_string_buffer(256);check(lib.path147(i,output)==0);expected_path='/Applications/Windows/'+product_code+'/'+'/'.join(x for x in [relative(component[2]),target_name(row[2])]if x);check(output.value.decode()==expected_path)
            windows_dir=lib.alias147().decode()+'\\'+(relative(component[2]).replace('/','\\')+'\\'if relative(component[2])else'');formatted=ctypes.create_string_buffer(512);check(lib.format147(('[#'+row[0]+']').encode(),formatted,len(formatted))==0 and formatted.value.decode()==(windows_dir+target_name(row[2])if wanted else''));check(lib.format147(('[$'+row[1]+']').encode(),formatted,len(formatted))==0 and formatted.value.decode()==(windows_dir if wanted else''))
            if wanted:selected_count+=1;selected_bytes+=int(row[3])
        check(lib.selected147()==selected_count and lib.selected_bytes147()==selected_bytes)
        if index==1:
            for i in range(count):
                action=lib.action147(i).contents
                if action.kind==51:check(lib.property147(i)==0)
                elif action.kind==3137:check(lib.condition147(action.condition)==(1 if language and action.name==b'CopyNativeLangAction'else 0))
            check(lib.get147(b'CopyNativeLangAction')==b'"C:\\Windows\\SysWOW64\\xcopy.exe" "C:\\Program Files\\Notepad++\\localization\\'+(b'english'if language else b'')+b'.xml" "C:\\Program Files\\Notepad++\\nativeLang.xml*" /Y /Q')
            check(lib.get147(b'DeleteNativeLangAction')==b'"C:\\Windows\\SysWOW64\\cmd.exe" /C del /F /Q "C:\\Program Files\\Notepad++\\nativeLang.xml"')
            check(lib.set147(b'Installed',b'1')==0 and lib.set147(b'REMOVE',b'ALL')==0)
            for i in range(count):
                action=lib.action147(i).contents
                if action.kind==3137:check(lib.condition147(action.condition)==(1 if language and action.name==b'DeleteNativeLangAction'else 0))
        for condition in [b'%PATH',b'$Component=3',b'&Feature=3']:check(lib.condition147(condition)==3)
        for text in [b'[%PATH]',b'[!ShortFile]']:
            refused=ctypes.create_string_buffer(b'unchanged',512);check(lib.format147(text,refused,len(refused))==87 and refused.value==b'')
        lib.close147();check(not live and state['bytes']==0 and not state['bad_free']);cycles.append(dict(cycle=cycle+1,retained_allocations=0,ordered_actions=count,selected_files=selected_count,selected_bytes=selected_bytes,language=language,no_updater=no_updater))
    target.write_bytes((json.dumps(dict(passed=True,package=path.name,package_sha256=original['sha256'],checks=checks,cycles=cycles,peak_host_allocated_bytes=state['peak'],scope='Original database-derived action/property plan, clean-install feature/directory/component/file costing and Type51 values vs independent read-only MSI tables. No target mutation, remaining standard actions or original WiX execution.',limits=['Conditions using environment/component/feature prefixes refuse until their full state resolvers are implemented','Only selected Type51/Type3137 metadata is admitted; admission is not execution','ASCII payload leaves, one isolated program root, selected component/feature attributes and one embedded cabinet; other profiles refuse']),indent=2)+'\n').encode())

def main():
    if len(sys.argv)>1:
        assert sys.argv[1]=='--worker';worker(int(sys.argv[2]),sys.argv[3]);return
    build();reports=[]
    for index in range(2):
        for mutation in ['normal','unknown','bad-shift','bad-directory-count','mini-fat-overquota','fat-cycle','truncated-sector']:
            run=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker',str(index),mutation],cwd=ROOT,capture_output=True);report=OUT/(str(index)+'-'+mutation+'.json')
            if run.returncode:raise RuntimeError('Owned MSI plan test failed '+str(run.returncode)+' '+(report.read_text()if report.exists()else run.stderr.decode(errors='replace')))
            result=json.loads(report.read_text());assert result['passed'];reports.append(result)
    sources=['user/windows8/msi-plan147.c','user/windows8/msi-plan147.h','user/windows8/msi-cost147.c','user/windows8/msi_db.c','user/windows8/msi_db.h','user/windows8/msi-properties147.h','user/windows8/msi-condition147.h','runtime/sha256.c','include/engine/sha256.h','tests/m14/plan147_host.c','tests/m14/plan147_host.py'];result=dict(passed=True,scope='Supporting original MSI plan/condition/costing/Type51/close tests, with unknown mandatory actions refused in isolated test processes. Not native MSI installation.',reports=reports,sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources});(OUT/'results.json').write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PASS original MSI plan tests',sum(r.get('checks',1)for r in reports))

if __name__=='__main__':main()
