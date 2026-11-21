"""Data-only utility reference in an owned temporary directory; no vendor installer executes."""
import hashlib,json,os,re,shutil,subprocess,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 base=(Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Tests/M14Helpers').resolve();base.mkdir(parents=True,exist_ok=True);work=base/uuid.uuid4().hex;work.mkdir();assert work.resolve().is_relative_to(base)and re.fullmatch('[0-9a-f]{32}',work.name)
 system=Path(os.environ['SystemRoot'])/'System32';source=work/'source language.xml';body=b'<lang>owned reference</lang>\r\n';source.write_bytes(body);result=dict(passed=False,scope=__doc__,source_sha256=hashlib.sha256(body).hexdigest(),copies=[],deletes=[])
 try:
  for target in ['nativeLang.xml*','copy.txt*','nativeLang.*']:
   destination=work/target;call=subprocess.run([str(system/'xcopy.exe'),str(source),str(destination),'/Y','/Q'],input=b'',capture_output=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW);files=sorted(p.name for p in work.iterdir()if p.is_file()and p!=source);entry=dict(pattern=target,status=call.returncode,files=files,stdout=call.stdout.decode(errors='replace').replace(str(work),'<owned-reference>'),stderr=call.stderr.decode(errors='replace').replace(str(work),'<owned-reference>'));result['copies'].append(entry)
   if target=='nativeLang.xml*':assert call.returncode==0 and (work/'nativeLang.xml').read_bytes()==body
  for cycle in range(2):
   target=work/'nativeLang.xml';call=subprocess.run([str(system/'cmd.exe'),'/d','/c','del','/F','/Q',str(target)],capture_output=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW);result['deletes'].append(dict(initially_present=cycle==0,status=call.returncode,exists=target.exists(),stdout=call.stdout.decode(errors='replace').replace(str(work),'<owned-reference>'),stderr=call.stderr.decode(errors='replace').replace(str(work),'<owned-reference>')));assert call.returncode==0 and not target.exists()
  assert source.read_bytes()==body;result['passed']=True
 finally:
  assert work.resolve().is_relative_to(base)and work.parent.resolve()==base;shutil.rmtree(work);result['owned_fixture_removed']=not work.exists();out=ROOT/'build/m14-native/stage7/helpers-reference';out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_bytes((json.dumps(result,indent=2)+'\n').encode());print(json.dumps(result,indent=2))
if __name__=='__main__':main()
