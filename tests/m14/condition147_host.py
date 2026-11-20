"""Production MSI conditions: original requirements, truth tables and parser bounds.

Supporting host evidence only. No Windows Installer/application execution.
"""
import ctypes
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command

def main():
    out=ROOT/'build/m14-native/stage7/condition-host';out.mkdir(parents=True,exist_ok=True)
    tools=pinned_tools()
    command([tools['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-c',ROOT/'tests/m14/condition147_host.c','-o',out/'condition.obj'])
    command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'condition.dll'),out/'condition.obj'])
    lib=ctypes.CDLL(str(out/'condition.dll'))
    class Pair(ctypes.Structure):
        _fields_=[('name',ctypes.c_char_p),('value',ctypes.c_char_p),('prefix',ctypes.c_uint)]
    call=lib.evaluate147;call.argtypes=[ctypes.c_char_p,ctypes.POINTER(Pair),ctypes.c_uint];call.restype=ctypes.c_int
    checks=0
    def evaluate(text,values=None):
        rows=[(name.encode(),value.encode(),prefix) for (prefix,name),value in (values or {}).items()]
        pairs=(Pair*len(rows))(*(Pair(*row) for row in rows))
        return call(text.encode() if text is not None else None,pairs,len(rows))
    def check(text,expected,values=None):
        nonlocal checks
        actual=evaluate(text,values);assert actual==expected,(text,expected,actual);checks+=1
    for text in [None,'',' \t\r\n']:check(text,2)
    for text in ['0','-0','+0','Missing','""']:check(text,0)
    for text in ['1','-1','"0"','"False"']:check(text,1)
    for text,expected in [('2>1',1),('2>=2',1),('2<=1',0),('"12">"2"',0),('12>"2"',1),('3><1',1),('4><1',0),('65537<<1',1),('65537>>1',1),('-2147483648<0',1),('2147483647>0',1),('"abc"><"b"',1),('"abc"<<"a"',1),('"abc">>"bc"',1),('"AbC"~="abc"',1),('"AbC"="abc"',0),('"AbC"~><"B"',1),('"é"="é"',1),('"é"~="é"',3),('"é">"e"',3),('1="text"',0),('1<>"text"',1),('"text"<>1',1),('"text">1',0)]:check(text,expected)
    # Exercise exact selected original sequence/feature/launch conditions.
    for lang,installed,remove,downgrade in itertools.product([False,True],repeat=4):
        props={(0,'NPP_LANG'):'english' if lang else '',(0,'Installed'):'1' if installed else '',(0,'REMOVE'):'ALL' if remove else '',(0,'WIX_DOWNGRADE_DETECTED'):'1' if downgrade else ''}
        check('NPP_LANG AND NOT Installed',int(lang and not installed),props)
        check('NPP_LANG AND Installed AND REMOVE="ALL"',int(lang and installed and remove),props)
        check('NOT WIX_DOWNGRADE_DETECTED',int(not downgrade),props)
    for a,b,c in itertools.product([False,True],repeat=3):
        props={(0,'A'):'1' if a else '',(0,'B'):'1' if b else '',(0,'C'):'1' if c else ''}
        for text,expected in [('A OR B AND C',a or b and c),('(A OR B) AND C',(a or b) and c),('NOT A AND B',not a and b),('A XOR B',a!=b),('A EQV B',a==b),('A IMP B',not a or b),('A OR B XOR C',(a or b)!=c)]:check(text,int(expected),props)
    for prefix in '$?&!':check(prefix+'Item=3',1,{(ord(prefix),'Item'):'3'})
    check('%pAtH="value"',1,{(ord('%'),'PATH'):'value'})
    check('A',0,{(0,'a'):'1'});check('A',1,{(0,'A'):'0'})
    for text in ['NOT','(',')','A B','A == 1','A < = 1','"unclosed','"a""b"','2147483648','-2147483649','1 + 2','1.2','&','A ~ B','A AND','@bad','(' * 33+'1'+')'*33,'NOT '*33+'1','x'*73,'1'*4097]:check(text,3)
    check('('*30+'1'+')'*30,1)
    # Independently generated boolean workloads, including syntactically valid
    # false branches: parsing cannot use short-circuiting to hide an error.
    rng=random.Random(147)
    for _ in range(2000):
        terms=[tuple(rng.randrange(2) for _ in range(3)) for _ in range(4)]
        text=' OR '.join('('+' AND '.join(str(x) for x in term)+')' for term in terms)
        check(text,int(any(all(term) for term in terms)))
    check('1 OR (bad AND)',3);check('0 AND (bad OR)',3)
    for _ in range(10000):
        text=''.join(rng.choice(' ()0123456789+-~<>=!$%?&ABCDEFGHIJKLMNOPQRSTUVWXYZ_"\t') for _ in range(rng.randrange(128)))
        result=evaluate(text);assert result in range(4);checks+=1
    sources=['user/windows8/msi-condition147.h','tests/m14/condition147_host.c','tests/m14/condition147_host.py']
    report=dict(passed=True,checks=checks,scope='Supporting hosted production parser, exact original selected conditions and malformed-input bounds; not native MSI/custom-action or original installation qualification',limits=['4096 condition bytes, 2048 lexer steps, 32 unary/parenthesis levels, 72-byte symbol names','Case-insensitive and ordered text comparisons currently require ASCII; unsupported non-ASCII comparisons return condition error'],sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources})
    (out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS MSI condition host checks',checks)

if __name__=='__main__':main()
