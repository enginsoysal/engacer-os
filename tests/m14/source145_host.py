"""Reject normalized Git-clean CRLF drift and edits made after source capture."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools/build'))
from m14_integrity import verify_committed_inputs, verify_working_inputs


def main():
    base = Path(os.environ['LOCALAPPDATA'])/'EngacerOS/Tests/M14/source-integrity'
    base.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=base) as temporary:
        root = Path(temporary).resolve()
        assert root.is_relative_to(base.resolve())
        def git(*args):
            return subprocess.check_output(['git', *args], cwd=root, stderr=subprocess.PIPE)
        git('init', '-q')
        git('config', 'user.name', 'Owned integrity fixture')
        git('config', 'user.email', 'fixture@example.invalid')
        git('config', 'core.autocrlf', 'false')
        (root/'.gitattributes').write_bytes(b'*.c text eol=lf\n')
        path = root/'fixture.c'
        path.write_bytes(b'original\n')
        git('add', '.')
        git('commit', '-qm', 'Owned source fixture')
        def record():
            return {'fixture.c': hashlib.sha256(path.read_bytes()).hexdigest()}
        hashes = record()
        commit = verify_committed_inputs(root, hashes)
        assert commit == git('rev-parse', 'HEAD').decode().strip()
        path.write_bytes(b'original\r\n')
        assert not git('diff', '--name-only'), 'Git normalizes the line endings'
        try:
            verify_committed_inputs(root, record())
        except RuntimeError as error:
            assert 'including line endings' in str(error)
        else:
            raise AssertionError('CRLF byte drift accepted')
        path.write_bytes(b'changed\n')
        try:
            verify_working_inputs(root, hashes)
        except RuntimeError as error:
            assert 'changed during compilation' in str(error)
        else:
            raise AssertionError('Post-capture source mutation accepted')
        try:
            verify_committed_inputs(root, {'absent.c': '0'*64})
        except RuntimeError as error:
            assert 'Uncommitted build input' in str(error)
        else:
            raise AssertionError('Missing committed input accepted')
    result = dict(passed=True, scope='Host build-integrity checks, not OS compatibility',
                  exact_bytes=True, git_clean_crlf_drift_refused=True,
                  post_capture_mutation_refused=True, missing_input_refused=True)
    out = ROOT/'build/m14-native/stage5/source-host'
    out.mkdir(parents=True, exist_ok=True)
    (out/'results.json').write_bytes((json.dumps(result, indent=2)+'\n').encode())
    print(json.dumps(result))


if __name__ == '__main__':
    main()
