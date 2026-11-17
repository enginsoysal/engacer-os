"""Fresh anonymous source readback for the final M13.0 publication, bounded to four workers."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
from pathlib import Path
import re
import time

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('closure_audit',ROOT/'website/brix/audit.py')
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--payload',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    payload=json.loads(a.payload.read_text(encoding='utf-8'))
    ref=payload['source_commit'];assert re.fullmatch('[0-9a-f]{40}',ref)
    def read(post):
        source=next(m['value'] for m in post['meta'] if m['key']=='engine_source_path')
        url=audit.SITE+'/blog/'+post['slug']
        expected='https://github.com/enginsoysal/engacer-os/'+('tree/'+ref if source.startswith('@') else 'blob/'+ref+'/'+source)
        attempts=[]
        for attempt in range(3):
            if attempt:time.sleep(2*attempt)
            row=audit.fetch(url)
            matched=row.get('status')==200 and not row.get('soft_404') and expected in row.get('links',[])
            attempts.append({'status':row.get('status'),'source_matches':matched})
            if matched:break
        return {'url':url,'expected_source':expected,'passed':matched,'attempts':attempts}
    results=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for row in pool.map(read,payload['page']['blog']['posts']):
            results.append(row)
            if len(results)%50==0:print(f'Checked {len(results)} public article sources',flush=True)
    errors=[r for r in results if not r['passed']]
    result={'passed':not errors,'publication_source':ref,'fresh_anonymous_articles_checked':len(results),'workers':4,'provenance_errors':errors,'results':results,'structure_audit':'website-audit.json','structure_audit_source':'5e1149d1896ab1c0c98d97e31dc828e8b4ff5751','scope':'Final closure changes source stamps, completion text, recovery export documentation and the additional design release; the previously crawled task routes remain unchanged.'}
    a.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    assert result['passed'],errors
    print(f'PASS: {len(results)} fresh public articles match the final closure source')

if __name__=='__main__':main()
