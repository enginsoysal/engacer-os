"""Exercise compiled path authorization policy without pretending it booted an OS."""
import ctypes as c
import hashlib
import json
from pathlib import Path
import random
import sys
import uuid
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command

class Entry(c.Structure):
    _fields_=[('path',c.c_char*256),('first',c.c_uint64),('size',c.c_uint64),('crc',c.c_uint32),('kind',c.c_uint32)]
class Result(c.Structure):
    _fields_=[('native',c.c_char*256),('windows',c.c_uint16*512)]
class Guarded(c.Structure):
    _fields_=[('before',c.c_uint64*2),('result',Result),('after',c.c_uint64*2)]

def main():
    out=ROOT/'build/m14-native/stage7/helper-path-host';work=out/uuid.uuid4().hex;work.mkdir(parents=True)
    tools=pinned_tools();obj=work/'path.obj';dll=work/'path.dll'
    command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-DENGINE_M14','-ffreestanding','-fno-builtin',
             '-fno-stack-protector','-mno-stack-arg-probe','-Wall','-Wextra','-Werror',
             '-I',ROOT/'include','-c',ROOT/'tests/m14/path143_host.c','-o',obj])
    command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(dll),obj])
    lib=c.CDLL(str(dll));lib.normalize_host143.argtypes=[c.c_char_p,c.c_char_p,c.c_uint,c.c_char_p,
        c.c_char_p,c.c_char_p,c.POINTER(Entry),c.c_uint,c.POINTER(Result)]
    paths=[('/Users/Owner/Documents',2),('/Users/Owner/Downloads',2),
           ('/Users/Owner/Documents/Résumé.txt',1),('/Users/Owner/Documents/FOLDER',2),
           ('/Users/Owner/Documents/FOLDER/child.txt',1),('/Users/Owner/Documents/smile-🙂.txt',1),
           ('/Users/Owner/Documents/literal',1),('/Users/Owner/Documents/literal. ',1)]
    entries=(Entry*len(paths))()
    for row,(path,kind) in zip(entries,paths):row.path=path.encode('utf-8');row.kind=kind
    def call(text,flags=0,custom=entries):
        raw=text.encode('utf-8') if isinstance(text,str) else text
        guard=Guarded();guard.before[:]=[0xa5a5a5a5a5a5a5a5]*2;guard.after[:]=list(guard.before)
        code=lib.normalize_host143(raw,b'C:\\Users\\Owner\\Documents',flags,b'/Users/Owner',
            b'/Applications/Windows/App',b'C:\\Program Files\\7-Zip',custom,len(custom),c.byref(guard.result))
        assert list(guard.before)==list(guard.after)==[0xa5a5a5a5a5a5a5a5]*2
        wide=bytes(guard.result.windows);zero=next((i for i in range(0,len(wide),2) if wide[i:i+2]==b'\0\0'),len(wide))
        return code,guard.result.native.decode('utf-8'),wide[:zero].decode('utf-16-le')
    checks=[]
    corpus=[(r'c:/users/OWNER/documents/rÉsumÉ.TXT',0,0,'/Users/Owner/Documents/Résumé.txt'),
            (r'..\Downloads\new.txt',0,0,'/Users/Owner/Downloads/new.txt'),
            (r'C:..\Downloads\new.txt',0,0,'/Users/Owner/Downloads/new.txt'),
            ('\\Users\\OWNER\\Documents\\smile-🙂.txt',0,0,'/Users/Owner/Documents/smile-🙂.txt'),
            (r'C:\Users\Owner\Documents\folder\CHILD.TXT',0,0,'/Users/Owner/Documents/FOLDER/child.txt'),
            (r'C:\Users\Owner\Documents\folder\CHILD.TXT',4,0,'/Users/Owner/Documents/FOLDER/CHILD.TXT'),
            ('C:\\Users\\Owner\\Documents\\literal. ',0,0,'/Users/Owner/Documents/literal'),
            ('\\\\?\\C:\\Users\\Owner\\Documents\\literal. ',0,0,'/Users/Owner/Documents/literal. '),
            (r'\\server\share\file',0,50,''),(r'\\.\PhysicalDrive0',0,50,''),
            (r'C:\Users\Owner\Documents\NUL.txt',0,50,''),
            ('C:\\Users\\Owner\\Documents\\COM¹.txt',0,50,''),
            (r'C:\Users\Owner\Documents\x:stream',0,50,''),
            (r'C:\Users\Owner\..\Other\private',0,5,''),
            (r'C:\Windows\..\Data\file',2,0,''),
            (r'C:\Users\Owner\Documents\*.txt',1,0,'/Users/Owner/Documents/*.txt'),
            (r'C:\Users\Owner\*\file',1,123,''),
            (r'\\?\C:\Users\Owner\Documents\..\file',0,50,''),
            (r'D:\file',2,15,''),('',0,3,''),('',2,87,''),
            ('C:\\Users\\Owner\\Documents\\'+'a'*64,0,206,''),
            (b'C:\\Users\\Owner\\Documents\\\xed\xa0\x80',0,1113,'')]
    for text,flags,expected,native in corpus:
        code,path,wide=call(text,flags);assert (code,path if not code else '')==(expected,native),(text,code,path,wide)
        if text==r'C:\Windows\..\Data\file':assert wide==r'C:\Data\file'
        checks.append(dict(input=text if isinstance(text,str) else text.hex(),flags=flags,status=code))
    for directory in ['System32','SysWOW64']:
        for name in ['cmd.exe','xcopy.exe']:
            for leaf in [name,name.upper()]:
                value='C:\\Windows\\'+directory+'\\'+leaf
                code,native,_=call(value)
                assert code==0 and native=='/System/Windows/Tools/'+name
        for leaf in ['other.exe','cmd.exe\\child','cmd.exe.bak','*','xcopy.exe:stream']:
            assert call('C:\\Windows\\'+directory+'\\'+leaf)[0]!=0
    assert call(r'C:\Windows\System32\..\other.exe')[0]!=0
    for tail in ['',r'\Notepad++.lnk',r'\7-Zip\7-Zip File Manager.lnk']:
        code,native,_=call(r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs'+tail)
        assert code==0 and native=='/Data/Windows/Common/Programs'+tail.replace('\\','/')
    assert call(r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\..\outside')[0]==5
    ambiguous=(Entry*3)()
    ambiguous[0].path=b'/Users/Owner/Documents';ambiguous[0].kind=2
    for row,name in zip(ambiguous[1:],['Alpha','alpha']):row.path=('/Users/Owner/Documents/'+name).encode();row.kind=1
    assert call(r'C:\Users\Owner\Documents\ALPHA',custom=ambiguous)[0]==123
    rng=random.Random(143);statuses={}
    atoms=['a','..','.','folder','Résumé','🙂','NUL','name. ','x:stream','*','?',' ']
    for _ in range(5000):
        value=r'C:\Users\Owner\Documents'+'\\'+'\\'.join(rng.choice(atoms) for _ in range(rng.randrange(1,12)))
        code,native,_=call(value,rng.randrange(2));statuses[code]=statuses.get(code,0)+1
        assert code in [0,3,5,50,123,206,1113]
        if not code:
            assert native.startswith('/Users/Owner/') or native=='/Users/Owner'
            assert len(native.encode('utf-8'))<256 and '\\' not in native
            assert not any(part in ('.','..','') for part in native.split('/')[1:])
    sources=['kernel/windows8/path-core143.inc','kernel/windows8/unicode143.inc',
             'kernel/windows8/unicode-table143.inc','include/engine/windows8.h',
             'tests/m14/path143_host.c','tests/m14/helper_paths147_host.py']
    report=dict(passed=True,scope='Host compiled path policy, not native syscall or Windows app qualification',
                checks=checks,ambiguous_native_case_refused=True,mutation_cases=5000,statuses=statuses,
                source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources})
    (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode('utf-8'));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
