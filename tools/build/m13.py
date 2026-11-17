"""Build isolated M13 native stages after the preceding public delivery."""
import argparse,json
from pathlib import Path
from m6 import build
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--stage',type=int,required=True,choices=range(1,13));a=p.parse_args()
 previous=ROOT/f'evidence/M13/{a.stage-1}/publication-results.json'
 if a.stage==1:previous=ROOT/'evidence/M13/0/closure-publication.json'
 proof=json.loads(previous.read_text(encoding='utf-8'));assert proof['passed'] and proof.get('stage')==f'M13.{a.stage-1}','Close the preceding public delivery first'
 assert not (ROOT/f'evidence/M13/{a.stage}/publication-results.json').exists(),'Accepted media are immutable'
 profile=ROOT/'distros/engacer-desktop-m13.json';assert json.loads(profile.read_text())['version']==f'0.13.{a.stage}'
 build('stage'+str(a.stage),profile,m13=True)
if __name__=='__main__':main()
