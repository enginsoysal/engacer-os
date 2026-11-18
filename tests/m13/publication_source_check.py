"""Verify current document/image bytes against every pinned publication source."""
import argparse,json,re,subprocess
from pathlib import Path
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[2]

def main():
 p=argparse.ArgumentParser();p.add_argument('--payload',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();payload=json.loads(a.payload.read_text(encoding='utf-8'));ref=payload['source_commit'];records=[];docs=0;images=0
 for post in payload['page']['blog']['posts']:
  meta={m['key']:m['value'] for m in post['meta']};path=meta['engine_source_path'];source=meta['engine_source_commit']
  if path.endswith('.md'):
   assert re.fullmatch('[0-9a-f]{40}',source);url='https://github.com/enginsoysal/engacer-os/blob/'+source+'/'+path
   assert url in post['blocks'][0]['props']['html'];records.append((source,path,'document'));docs+=1
  for block in post['blocks']:
   if block['type']!='image':continue
   u=block['props'].get('url','');m=re.fullmatch(r'https://raw.githubusercontent.com/enginsoysal/engacer-os/([0-9a-f]{40})/(.+)',u)
   if m:records.append((m[1],unquote(m[2]),'image'));images+=1
 requests=sorted({commit+':'+path for commit,path,_ in records}|{ref+':'+path for _,path,_ in records})
 raw=subprocess.check_output(['git','cat-file','--batch-check'],cwd=ROOT,input=('\n'.join(requests)+'\n').encode()).decode().splitlines();objects={request:line.split() for request,line in zip(requests,raw)};assert len(objects)==len(requests)
 for commit,path,kind in records:
  left,right=objects[commit+':'+path],objects[ref+':'+path];assert len(left)==3 and left[1]=='blob',(kind,path,'missing pinned source');assert left==right,(kind,path,'pinned bytes differ from current source')
 result=dict(passed=True,source_commit=ref,document_bytes_verified=docs,pinned_image_bytes_verified=images,scope='Every generated Markdown article and pinned relative image has the same Git blob at its actual edit revision and the current publication revision')
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes((json.dumps(result,indent=2)+'\n').encode());print(json.dumps(result))
if __name__=='__main__':main()
