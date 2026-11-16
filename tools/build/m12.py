"""Build the next isolated M12 stage only after its predecessor was published."""
import argparse
import json
from pathlib import Path
from m6 import build

ROOT = Path(__file__).resolve().parents[2]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', type=int, required=True, choices=range(1,19))
    args = parser.parse_args()
    previous = ROOT / f'evidence/M12/{args.stage-1}/publication-results.json'
    proof = json.loads(previous.read_text(encoding='utf-8'))
    assert proof['passed'] and proof['stage'] == f'M12.{args.stage-1}', 'Close the previous stage first'
    accepted = ROOT / f'evidence/M12/{args.stage}/publication-results.json'
    assert not accepted.exists(), 'Published stage outputs are immutable; use the next stage'
    profile = ROOT / 'distros/engacer-desktop-m12.json'
    assert json.loads(profile.read_text(encoding='utf-8'))['version'] == f'0.12.{args.stage}'
    build('stage'+str(args.stage), profile, m12=True)

if __name__ == '__main__':
    main()
