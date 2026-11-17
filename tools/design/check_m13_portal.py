"""Verify current public source provenance against the exact generated M13 payload."""
import argparse
import importlib.util
import json
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('portal_audit',ROOT/'website/brix/audit.py')
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--payload',type=Path,required=True)
    p.add_argument('--audit',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    payload=json.loads(a.payload.read_text(encoding='utf-8'))
    report=json.loads(a.audit.read_text(encoding='utf-8'))
    assert report['passed'], 'Full public crawl must pass before provenance closure'
    rows={row['url']:row for row in report['pages']}
    errors=[];refreshes=[]
    for post in payload['page']['blog']['posts']:
        source=next(m['value'] for m in post['meta'] if m['key']=='engine_source_path')
        url=audit.SITE+'/blog/'+post['slug']
        expected='https://github.com/enginsoysal/engacer-os/'+('tree/'+payload['source_commit'] if source.startswith('@') else 'blob/'+payload['source_commit']+'/'+source)
        row=rows.get(url,{})
        for attempt in range(3):
            if row.get('status')==200 and expected in row.get('links',[]):break
            if attempt:time.sleep(2*attempt)
            row=audit.fetch(url);refreshes.append({'url':url,'attempt':attempt+1,'status':row.get('status')})
        if row.get('status')!=200 or expected not in row.get('links',[]):errors.append({'url':url,'expected_source':expected,'status':row.get('status')})
    result={'passed':not errors,'source_commit':payload['source_commit'],'articles_checked':len(payload['page']['blog']['posts']),'pages_checked':report['pages_checked'],'unique_links':report['unique_links'],'provenance_errors':errors,'fresh_reads':refreshes,'current_native_download':'M12.18','design_only':'M13.0','production_overlay':False}
    a.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    assert result['passed'],errors
    print(f"PASS: all {result['articles_checked']} articles identify the final exact source")

if __name__=='__main__':main()
