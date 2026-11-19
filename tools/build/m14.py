"""Build isolated M14 native stages after the preceding public delivery."""
import argparse
import json
from pathlib import Path
from m6 import build

ROOT = Path(__file__).resolve().parents[2]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', type=int, required=True, choices=range(1, 16))
    args = parser.parse_args()
    previous = ROOT / f'evidence/M14/{args.stage-1}/publication-results.json'
    proof = json.loads(previous.read_text(encoding='utf-8'))
    assert proof['passed'] and proof.get('stage') == f'M14.{args.stage-1}', 'Close the preceding public delivery first'
    assert not (ROOT / f'evidence/M14/{args.stage}/publication-results.json').exists(), 'Accepted media are immutable'
    profile = ROOT / 'distros/engacer-desktop-m14.json'
    assert json.loads(profile.read_text())['version'] == f'0.14.{args.stage}'
    build('stage'+str(args.stage), profile, m14=True)

if __name__ == '__main__':
    main()
