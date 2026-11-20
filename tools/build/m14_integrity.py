"""Verify exact committed build bytes, including line endings, before compilation."""
import hashlib
import subprocess
from pathlib import Path


def verify_committed_inputs(root, records, ref='HEAD'):
    root = Path(root)
    commit = subprocess.check_output(['git', 'rev-parse', ref+'^{commit}'], cwd=root).decode().strip()
    paths = list(records)
    result = subprocess.run(['git', 'cat-file', '--batch'], cwd=root,
                            input=''.join(commit+':'+p+'\n' for p in paths).encode(),
                            capture_output=True, check=True).stdout
    at = 0
    for path in paths:
        end = result.index(b'\n', at)
        header = result[at:end].split()
        if len(header) != 3 or header[1] != b'blob':
            raise RuntimeError('Uncommitted build input: '+path)
        size = int(header[2])
        body = result[end+1:end+1+size]
        at = end+size+2
        if hashlib.sha256(body).hexdigest() != records[path]:
            raise RuntimeError('Build bytes differ from commit (including line endings): '+path)
    verify_working_inputs(root, records)
    return commit


def verify_working_inputs(root, records):
    for path, expected in records.items():
        if hashlib.sha256((Path(root)/path).read_bytes()).hexdigest() != expected:
            raise RuntimeError('Build input changed during compilation: '+path)
