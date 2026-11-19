"""Supporting compiled wildcard checks against an independent official-data oracle."""
import ctypes as c,hashlib,json,os,random,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command

def main():
 out=ROOT/'build/m14-native/stage3/find-host';out.mkdir(parents=True,exist_ok=True);tools=pinned_tools()
 obj=out/'find.obj';dll=out/'find.dll'
 command([tools['clang'],'--target=x86_64-pc-windows-msvc','-std=c17','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-I',ROOT/'include','-c',ROOT/'tests/m14/find143_host.c','-o',obj])
 command([tools['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/export:find_host143',obj,'/out:'+str(dll)])
 library=c.CDLL(str(dll));function=library.find_host143;function.argtypes=[c.c_char_p,c.c_uint,c.c_char_p,c.c_uint,c.POINTER(c.c_uint)];function.restype=c.c_uint
 class Result(c.Structure):_fields_=[('before',c.c_uint64),('matched',c.c_uint),('pad',c.c_uint),('after',c.c_uint64)]
 raw=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/3/CaseFolding-17.0.0.txt';data=raw.read_bytes()
 assert hashlib.sha256(data).hexdigest()=='ff8d8fefbf123574205085d6714c36149eb946d717a0c585c27f0f4ef58c4183'
 mapping={}
 for line in data.decode('utf-8').splitlines():
  fields=line.split('#')[0].strip().split(';')
  if len(fields)>=3 and fields[1].strip() in ['C','S']:mapping[int(fields[0],16)]=int(fields[2].strip(),16)
 def fold(text):return ''.join(chr(mapping.get(ord(ch),ord(ch)))for ch in text)
 def oracle(pattern,name):
  variants=[fold(pattern)];target=fold(name)
  if pattern.endswith('.*'):variants.append(fold(pattern[:-2]))
  return any(re.fullmatch(''.join('.*'if ch=='*'else'.'if ch=='?'else re.escape(ch)for ch in item),target,re.DOTALL)is not None for item in variants)
 def call(pattern,name):
  p=pattern.encode('utf-8')if isinstance(pattern,str)else pattern;n=name.encode('utf-8')if isinstance(name,str)else name
  result=Result(0x1431431431431431,0x12345678,0x87654321,0x1431431431431431)
  status=function(p,len(p),n,len(n),c.cast(c.byref(result,Result.matched.offset),c.POINTER(c.c_uint)))
  assert result.before==result.after==0x1431431431431431 and result.pad==0x87654321
  return status,result.matched
 cases=[('*.*','noextension'),('m143-?.txt','M143-🙂.TXT'),('[a]','[A]'),('strasse','Straße'),('*é?','XÉ🙂'),('*.txt','A.TXT'),('prefix.*','prefix'),('prefix.*','prefix.a'),('*'+'a'*200+'b','a'*255)]
 for pattern,name in cases:assert call(pattern,name)==(0,int(oracle(pattern,name))),(pattern,name,call(pattern,name))
 rng=random.Random(14303);alphabet=['a','A','x','X','.','é','É','Σ','ς','ß','ẞ','🙂','𐐀','𐐨','[',']','-',' ']
 for turn in range(10000):
  pattern=''.join(rng.choice(alphabet+['*','?'])for _ in range(rng.randrange(13)));name=''.join(rng.choice(alphabet)for _ in range(rng.randrange(13)))
  assert call(pattern,name)==(0,int(oracle(pattern,name))),(turn,pattern,name,call(pattern,name))
 invalid=[b'\xed\xa0\x80',b'\xe2\x82',b'\xc0\xaf',b'\xf4\x90\x80\x80',b'\x80']
 for item in invalid:assert call(b'*',item)==call(item,b'name')==(1113,0x12345678)
 names=['kernel/windows8/find-core143.inc','kernel/windows8/unicode143.inc','kernel/windows8/unicode-table143.inc','tests/m14/find143_host.c','tests/m14/find143_host.py','tests/m14/path143_host.c']
 report=dict(passed=True,scope='Host-compiled pure matcher supporting checks, not native Windows API qualification',explicit_cases=len(cases),independent_random_cases=10000,malformed_input_cases=len(invalid)*2,guarded_results=True,official_case_data_sha256=hashlib.sha256(data).hexdigest(),source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in names})
 (out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
