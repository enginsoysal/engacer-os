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
    for source in ['user/windows8/msi_db.c','user/windows8/msi-plan147.c','runtime/sha256.c','tests/m14/plan147_host.c']:
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
    lib.init147.argtypes=[alloc_type,free_type,failure_type];lib.open147.argtypes=[ctypes.c_void_p,ctypes.c_uint];lib.action147.argtypes=[ctypes.c_uint];lib.action147.restype=ctypes.POINTER(Action);lib.get147.argtypes=[ctypes.c_char_p];lib.get147.restype=ctypes.c_char_p;lib.set147.argtypes=[ctypes.c_char_p,ctypes.c_char_p];lib.property147.argtypes=[ctypes.c_uint];lib.condition147.argtypes=[ctypes.c_char_p];lib.init147(allocate,release,failure);buf=ctypes.create_string_buffer(data);checks=0;cycles=[]
    def check(yes):
        nonlocal checks
        assert yes;checks+=1
    tables=original['tables'];expected_sequence=sorted(tables['InstallExecuteSequence'],key=lambda x:int(x[2]));custom=tables['CustomAction'];custom={}if isinstance(custom,dict)else{row[0]:row for row in custom}
    for cycle in range(21):
        count=lib.open147(buf,len(data));check(mutation=='normal'and count==len(expected_sequence))
        for name,value in tables['Property']:check(lib.get147(name.encode()).decode()==value)
        for i,expected in enumerate(expected_sequence):
            action=lib.action147(i).contents;name=action.name.decode();check([name,action.condition.decode(),str(action.sequence)]==expected)
            if name in custom:
                row=custom[name];check(action.kind==int(row[1])and action.source.decode()==row[2]and action.target.decode()==row[3])
            else:check(action.kind==0 and action.source is None and action.target is None)
        if index==1:
            # Explicitly supplied cost results: directory costing and actual
            # file/standard/custom-action execution are separate native work.
            for name,value in {'SystemFolder':'C:\\Windows\\System32\\','LocalizationFolder':'C:\\Program Files\\Notepad++\\localization\\','INSTALLFOLDER':'C:\\Program Files\\Notepad++\\','NPP_LANG':'english'}.items():check(lib.set147(name.encode(),value.encode())==0)
            for i in range(count):
                action=lib.action147(i).contents
                if action.kind==51:check(lib.property147(i)==0)
                elif action.kind==3137:check(lib.condition147(action.condition)==(1 if action.name==b'CopyNativeLangAction'else 0))
            check(lib.get147(b'CopyNativeLangAction')==b'"C:\\Windows\\System32\\xcopy.exe" "C:\\Program Files\\Notepad++\\localization\\english.xml" "C:\\Program Files\\Notepad++\\nativeLang.xml*" /Y /Q')
            check(lib.get147(b'DeleteNativeLangAction')==b'"C:\\Windows\\System32\\cmd.exe" /C del /F /Q "C:\\Program Files\\Notepad++\\nativeLang.xml"')
            check(lib.set147(b'Installed',b'1')==0 and lib.set147(b'REMOVE',b'ALL')==0)
            for i in range(count):
                action=lib.action147(i).contents
                if action.kind==3137:check(lib.condition147(action.condition)==(1 if action.name==b'DeleteNativeLangAction'else 0))
        for condition in [b'%PATH',b'$Component=3',b'&Feature=3']:check(lib.condition147(condition)==3)
        lib.close147();check(not live and state['bytes']==0 and not state['bad_free']);cycles.append(dict(cycle=cycle+1,retained_allocations=0,ordered_actions=count))
    target.write_bytes((json.dumps(dict(passed=True,package=path.name,package_sha256=original['sha256'],checks=checks,cycles=cycles,peak_host_allocated_bytes=state['peak'],scope='Original database-derived action/property plan and Type51 formatted values vs independent read-only MSI tables. No target mutation, directory costing, standard actions or original WiX execution.',limits=['Conditions using environment/component/feature prefixes refuse until cost/state resolvers are implemented','Only the selected Type51 and Type3137 custom-action metadata profiles are admitted; admission is not execution']),indent=2)+'\n').encode())

def main():
    if len(sys.argv)>1:
        assert sys.argv[1]=='--worker';worker(int(sys.argv[2]),sys.argv[3]);return
    build();reports=[]
    for index in range(2):
        for mutation in ['normal','unknown','bad-shift','bad-directory-count','mini-fat-overquota','fat-cycle','truncated-sector']:
            run=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker',str(index),mutation],cwd=ROOT,capture_output=True);report=OUT/(str(index)+'-'+mutation+'.json')
            if run.returncode:raise RuntimeError('Owned MSI plan test failed '+str(run.returncode)+' '+(report.read_text()if report.exists()else run.stderr.decode(errors='replace')))
            result=json.loads(report.read_text());assert result['passed'];reports.append(result)
    sources=['user/windows8/msi-plan147.c','user/windows8/msi-plan147.h','user/windows8/msi_db.c','user/windows8/msi_db.h','user/windows8/msi-properties147.h','user/windows8/msi-condition147.h','runtime/sha256.c','include/engine/sha256.h','tests/m14/plan147_host.c','tests/m14/plan147_host.py'];result=dict(passed=True,scope='Supporting original MSI plan/condition/Type51/close tests, with unknown mandatory actions refused in isolated test processes. Not native MSI installation.',reports=reports,sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources});(OUT/'results.json').write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PASS original MSI plan tests',sum(r.get('checks',1)for r in reports))

if __name__=='__main__':main()
