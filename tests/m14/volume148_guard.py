"""Host execution of production volume mutation-policy boundaries, not native EXE-broker qualification."""
import ctypes as C,hashlib,importlib.util,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/build'))
from m1 import pinned_tools,command
spec=importlib.util.spec_from_file_location('volume148_types',ROOT/'tests/m11/volume_host.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
def main():
 out=ROOT/'build/m14-native/stage8/volume-guard-host';out.mkdir(parents=True,exist_ok=True);t=pinned_tools();source=ROOT/'kernel/storage/volume6.c'
 command([t['clang'],'--target=x86_64-pc-windows-msvc','-std=c17','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-fno-stack-protector',*['-DENGINE_'+x for x in['M7','M8','M11','M14']],'-I',ROOT/'include','-c',source,'-o',out/'volume.obj'])
 names=['format','mount','mkdir','put','read','remove','rename','move_tree11','remove_tree11','stream_begin','stream_append','stream_finish','stream_abort','set_guard148'];command([t['lld-link'],'/dll','/noentry','/nodefaultlib','/timestamp:0',*['/export:v6_'+x for x in names],out/'volume.obj','/out:'+str(out/'volume.dll')]);lib=C.CDLL(str(out/'volume.dll'));Volume=base.Volume;Entry=base.types.Entry;vp=C.POINTER(Volume)
 for name in['format','mount','stream_finish','stream_abort']:getattr(lib,'v6_'+name).argtypes=[vp]
 lib.v6_stream_abort.restype=None
 for name in['mkdir','remove','remove_tree11']:getattr(lib,'v6_'+name).argtypes=[vp,C.c_char_p]
 for name in['rename','move_tree11']:getattr(lib,'v6_'+name).argtypes=[vp,C.c_char_p,C.c_char_p,C.c_uint]
 lib.v6_put.argtypes=[vp,C.c_char_p,C.c_uint64,base.SOURCE,C.c_void_p];lib.v6_stream_begin.argtypes=[vp,C.c_char_p,C.c_uint64];lib.v6_stream_append.argtypes=[vp,C.c_void_p,C.c_uint]
 Guard=C.CFUNCTYPE(C.c_uint,vp,C.c_char_p,C.POINTER(Entry));lib.v6_set_guard148.argtypes=[Guard]
 disk=base.Disk();volume=disk.volume();p=C.byref(volume);assert lib.v6_format(p)==0 and lib.v6_mkdir(p,b'/protected')==0
 @base.SOURCE
 def content(ctx,offset,out,n):C.memmove(out,b'Original image'[offset:offset+n],n);return 0
 def put(path):return lib.v6_put(p,path,14,content,None)
 assert put(b'/protected/source.exe')==0 and put(b'/other.exe')==0
 index=next(i for i,e in enumerate(volume.entries)if e.path==b'/protected/source.exe');active=[True];extra=[None];calls=[]
 @Guard
 def guard(v,path,pending):
  calls.append('commit'if pending else 'path'if path else'format')
  if not active[0]:return 0
  if pending:return 9 if bytes(v.contents.entries[index])!=bytes(pending[index])else 0
  return 9 if path is None or path in[b'/protected/source.exe',extra[0]]else 0
 lib.v6_set_guard148(guard);checks=[]
 def refused(name,operation):
  generation=volume.generation;before=bytes(volume.entries);io=disk.calls;assert operation()==9,name;assert volume.generation==generation and bytes(volume.entries)==before and not volume.readonly and disk.calls==io,name;checks.append(name)
 refused('write pinned image before I/O',lambda:put(b'/protected/source.exe'));refused('delete pinned image',lambda:lib.v6_remove(p,b'/protected/source.exe'));refused('rename pinned source',lambda:lib.v6_rename(p,b'/protected/source.exe',b'/renamed.exe',0));refused('replace pinned destination',lambda:lib.v6_rename(p,b'/other.exe',b'/protected/source.exe',1));refused('move ancestor tree at commit',lambda:lib.v6_move_tree11(p,b'/protected',b'/moved',0));refused('remove ancestor tree at commit',lambda:lib.v6_remove_tree11(p,b'/protected'));refused('format before header writes',lambda:lib.v6_format(p))
 active[0]=False;assert lib.v6_stream_begin(p,b'/staged.exe',4096)==0;assert lib.v6_stream_append(p,C.c_char_p(b'abc'),3)==0;active[0]=True;extra[0]=b'/staged.exe';refused('finish earlier stream after policy change',lambda:lib.v6_stream_finish(p));assert lib.v6_stream_begin(p,b'/next.exe',4096)==0;lib.v6_stream_abort(p);checks.append('refused stream releases its reservation')
 assert put(b'/unrelated.exe')==0;checks.append('unrelated writes remain allowed');active[0]=False;assert lib.v6_remove(p,b'/protected/source.exe')==0;checks.append('released image can be removed');lib.v6_set_guard148(Guard());assert lib.v6_mount(p)==0
 inputs=[source,ROOT/'include/engine/storage/volume6.h',Path(__file__)];report=dict(passed=True,scope=__doc__,checks=checks,guard_calls=len(calls),source_sha256={x.relative_to(ROOT).as_posix():hashlib.sha256(x.read_bytes()).hexdigest()for x in inputs});(out/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,checks=checks),indent=2))
if __name__=='__main__':main()
