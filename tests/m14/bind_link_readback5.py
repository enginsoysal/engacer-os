"""Bind a live link check to a freshly read public link graph with no unverified additions."""
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 work=ROOT/'build/m14-native/stage5';out=ROOT/'evidence/M14/5'
 def load(path):return json.loads(path.read_text(encoding='utf-8'))
 old=load(work/'website-readback.json');current=load(out/'website-readback.json');checked=load(work/'website-links-preflight.json')
 assert current['passed'] and checked['passed'] and not checked['broken']
 assert checked['source_commit']==old['source_commit']
 def edges(report):return sorted({url for page in report['pages'] for url in page.get('links',[])})
 before,after=edges(old),edges(current);assert set(after)<=set(before),'New links require a fresh link validation'
 age=(datetime.now(timezone.utc)-datetime.fromisoformat(checked['checked_at'])).total_seconds();assert 0<=age<=900,'Link check expired'
 checked.update(original_source_commit=checked['source_commit'],source_commit=current['source_commit'],link_graph_sha256=hashlib.sha256(('\n'.join(after)+'\n').encode()).hexdigest(),verified_link_count=len(after),removed_links=sorted(set(before)-set(after)),readback_binding='Every URL in the complete fresh current-source readback belongs to the independently live-checked link set; removed URLs are recorded, and any unverified addition refuses this binding',original_check='development/public-source-refresh/website-links-preflight.json')
 target=out/'website-links.json';assert not target.exists()
 target.write_bytes((json.dumps(checked,indent=2)+'\n').encode())
 print('PASS fully covered fresh public link graph:',len(after),'URLs; zero known broken targets')
if __name__=='__main__':main()
