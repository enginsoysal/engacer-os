"""Generate the pinned compact Unicode simple-fold data; never fetch during OS boot."""
import argparse
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def generate(source):
    provenance = json.loads((ROOT/'third_party/unicode/provenance.json').read_text(encoding='utf-8'))
    raw = source.read_bytes()
    expected = provenance['sources']['case_folding']
    assert len(raw) == expected['bytes'] and hashlib.sha256(raw).hexdigest() == expected['sha256']
    pairs = []
    for line in raw.decode('utf-8').splitlines():
        row = line.split('#', 1)[0].strip()
        if not row:
            continue
        code, status, mapping, *_ = [part.strip() for part in row.split(';')]
        if status in ('C', 'S'):
            points = mapping.split()
            assert len(points) == 1
            pairs.append((int(code, 16), int(points[0], 16)))
    assert pairs == sorted(set(pairs))
    runs = []
    at = 0
    while at < len(pairs):
        first, target = pairs[at]
        delta, stride = target-first, 1
        if at+1 < len(pairs):
            following, value = pairs[at+1]
            if following-first in (1, 2) and value-following == delta:
                stride = following-first
        end = at+1
        while (end < len(pairs) and pairs[end][0]-pairs[end-1][0] == stride
               and pairs[end][1]-pairs[end][0] == delta):
            end += 1
        runs.append((first, pairs[end-1][0], delta, stride))
        at = end
    assert len(runs)*16 <= 4096
    text = ('/* Generated from Unicode 17.0.0 CaseFolding C/S records.\n'
            ' * Unicode-3.0: third_party/unicode/LICENSE.txt.\n'
            ' * Regenerate with tools/build/unicode143.py; full/Turkic folds are excluded. */\n'
            'typedef struct {uint32_t first,last;int32_t delta;uint16_t stride,pad;} unicode_run143;\n'
            'static const unicode_run143 unicode_runs143[]={\n')
    text += ''.join(f' {{{a:#x},{b:#x},{delta},{stride},0}},\n' for a,b,delta,stride in runs)
    text += '};\n_Static_assert(sizeof(unicode_runs143)<=4096,"Simple-fold data exceeds its component budget");\n'
    data = text.encode('utf-8')
    manifest = dict(version='17.0.0', mapping='Simple case folding, C/S records only; no normalization',
                    source_sha256=expected['sha256'], pairs=len(pairs), runs=len(runs),
                    record_bytes=16, read_only_component_bytes=len(runs)*16,
                    generated_sha256=hashlib.sha256(data).hexdigest(),
                    windows_nls_equivalence_claimed=False)
    return data, (json.dumps(manifest, indent=2)+'\n').encode('utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path,
        default=Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Research/M14/3/CaseFolding-17.0.0.txt')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data, manifest = generate(args.source)
    outputs = {ROOT/'kernel/windows8/unicode-table143.inc': data,
               ROOT/'third_party/unicode/case-map143.json': manifest}
    for path, body in outputs.items():
        if args.check:
            assert path.read_bytes() == body, path
        else:
            path.write_bytes(body)
    print('Verified' if args.check else 'Generated', 'pinned compact Unicode 17 simple-fold data')


if __name__ == '__main__':
    main()
