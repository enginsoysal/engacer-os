"""Own atom core vs independent model and bounded private Windows atom references."""
import ctypes as c,hashlib,json,random,sys,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import command,pinned_tools

def main():
 out=ROOT/'build/m14-native/stage7/atom-host';out.mkdir(parents=True,exist_ok=True);t=pinned_tools();command([t['clang'],'--target=x86_64-pc-windows-msvc','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector','-mno-stack-arg-probe','-I',ROOT/'include','-c',ROOT/'tests/m14/atom147_host.c','-o',out/'atom.obj']);command([t['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0','/out:'+str(out/'atom.dll'),out/'atom.obj']);lib=c.CDLL(str(out/'atom.dll'));U=c.c_uint;P=c.c_void_p
 for fn in ['add147','find147']:getattr(lib,fn).argtypes=[P,U]
 lib.name147.argtypes=[U,P,U];checks=0
 def check(value):
  nonlocal checks
  assert value;checks+=1
 def ascii_swap(text):return ''.join(chr(ord(ch)^32)if 'A'<=ch<='Z' or 'a'<=ch<='z'else ch for ch in text)
 def call(fn,text):
  raw=text.encode('utf-16-le');return getattr(lib,fn)(c.create_string_buffer(raw),len(raw)//2)
 kernel=c.WinDLL('kernel32',use_last_error=True);kernel.GlobalAddAtomW.argtypes=[c.c_wchar_p];kernel.GlobalAddAtomW.restype=c.c_ushort;kernel.GlobalFindAtomW.argtypes=[c.c_wchar_p];kernel.GlobalFindAtomW.restype=c.c_ushort;kernel.GlobalDeleteAtom.argtypes=[c.c_ushort];kernel.GlobalGetAtomNameW.argtypes=[c.c_ushort,P,c.c_int]
 # These are only our uniquely named transient reference atoms, released in finally.
 reference=[]
 for spelling in ['Engacer.DevTest.'+uuid.uuid4().hex,'Engacer.DevTest.Éλ.'+uuid.uuid4().hex,'E'*255]:
  owned=[];atom=0
  try:
   atom=kernel.GlobalAddAtomW(spelling);check(atom>=0xc000);owned.append(atom);lib.reset147();own=call('add147',spelling);check(own>=0xc000);second=kernel.GlobalAddAtomW(ascii_swap(spelling));
   if second:owned.append(second)
   check(second==atom);check(call('add147',ascii_swap(spelling))==own and lib.references147(own)==2);check(kernel.GlobalFindAtomW(ascii_swap(spelling))==atom and call('find147',ascii_swap(spelling))==own)
   for cap in [0,1,2,3,len(spelling),len(spelling)+1,len(spelling)+2]:
    a=(c.c_ushort*300)(*([0x9b9b]*300));b=(c.c_ushort*300)(*([0x9b9b]*300));c.set_last_error(0);expected=kernel.GlobalGetAtomNameW(atom,b,cap);error=c.get_last_error();actual=lib.name147(own,a,cap);check(actual==(expected if expected else -error)and bytes(a)==bytes(b));reference.append(dict(units=len(spelling),capacity=cap,copied=expected,error=error))
   check(kernel.GlobalDeleteAtom(atom)==0);owned.remove(atom);check(lib.delete147(own)==0 and call('find147',spelling)==own);check(kernel.GlobalFindAtomW(spelling)==atom)
   check(kernel.GlobalDeleteAtom(atom)==0);owned.remove(atom);check(lib.delete147(own)==0 and call('find147',spelling)==-2 and lib.used147()==0 and lib.valid147())
  finally:
   for reference_atom in owned:kernel.GlobalDeleteAtom(reference_atom)
 lib.reset147()
 for text in ['#0','#1','#49151','#49152','#65535','#00001','#999999999999999999999999']:
  c.set_last_error(0);result=kernel.GlobalFindAtomW(text);error=c.get_last_error();check(call('find147',text)==(result if result else -error));check(lib.used147()==0)
 for atom in [1,7,1234,49151]:
  for cap in range(9):
   a=(c.c_ushort*16)(*([0x9b9b]*16));b=(c.c_ushort*16)(*([0x9b9b]*16));c.set_last_error(0);expected=kernel.GlobalGetAtomNameW(atom,b,cap);error=c.get_last_error();check(lib.name147(atom,a,cap)==(expected if expected else -error)and bytes(a)==bytes(b))
 # Independent reference-count/state model with arbitrary packed-pool removal order.
 model={};rng=random.Random(147)
 for turn in range(15000):
  name='Atom-%02d'%rng.randrange(48);key=name.casefold();operation=rng.randrange(3)
  if operation==0:
   atom=call('add147',name.swapcase()if rng.randrange(2)else name);check(atom>=0xc000)
   if key in model:check(atom==model[key][0]);model[key][1]+=1
   else:check(atom not in [v[0]for v in model.values()]);model[key]=[atom,1]
  elif operation==1:check(call('find147',name)==(model[key][0]if key in model else -2))
  elif key in model:
   atom,count=model[key];check(lib.delete147(atom)==0);model[key][1]-=1
   if count==1:del model[key]
  check(lib.valid147());check(lib.used147()==sum(len(name)+1 for name in model))
 for atom,count in list(model.values()):
  for _ in range(count):check(lib.delete147(atom)==0)
 check(lib.used147()==0 and lib.valid147());lib.reset147();atoms=[call('add147','quota-'+str(i))for i in range(64)];check(len(set(atoms))==64 and call('add147','quota-over')==-1816)
 for atom in atoms[::2]+atoms[1::2]:check(lib.delete147(atom)==0 and lib.valid147())
 check(lib.used147()==0);large=[]
 for i in range(7):large.append(call('add147',chr(65+i)*255));check(large[-1]>=0xc000)
 check(call('add147','Z'*255)==-1816 and lib.valid147())
 for atom in reversed(large):check(lib.delete147(atom)==0 and lib.valid147())
 check(call('add147','X'*256)==-87 and lib.used147()==0)
 invalid=(c.c_ushort*1)(0xd800);check(lib.add147(invalid,1)==-87 and lib.used147()==0)
 atom=call('add147','reference-limit')
 for _ in range(65534):check(call('add147','REFERENCE-LIMIT')==atom)
 check(lib.references147(atom)==65535 and call('add147','reference-limit')==-1816)
 for _ in range(65535):check(lib.delete147(atom)==0)
 check(lib.used147()==0 and lib.valid147());sources=['include/engine/winatom147.h','tests/m14/atom147_host.c','tests/m14/atom147_host.py'];report=dict(passed=True,scope=__doc__,checks=checks,private_reference_atoms_released=True,reference=reference,table_bytes=4096,slot_quota=64,name_pool_utf16_units=1854,sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources});(out/'results.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print('PASS global atom core checks',checks)
if __name__=='__main__':main()
