"""Derive nested accepted observers with explicit current-stage path mappings."""
from pathlib import Path
import hashlib
import replay7

def load_adapter(name):
    canonical = Path(__file__).with_name(name + '.py')
    raw = canonical.read_bytes()
    source = raw.decode('utf-8').replace('from replay6 import REPLACEMENTS', 'from replay7 import REPLACEMENTS')
    for before, after in replay7.REPLACEMENTS:
        source = source.replace(before, after)
    needle = 'def derive(source):'
    assert source.count(needle) == 1
    source = source.replace(needle, needle + '\n    for before, after in nested_replacements147:\n        source = source.replace(before, after)')
    scope = dict(__file__=str(canonical), __name__='nested147_' + name, nested_replacements147=replay7.REPLACEMENTS)
    exec(compile(source, str(canonical), 'exec'), scope)
    scope['derivation147'] = dict(canonical_sha256=hashlib.sha256(raw).hexdigest(), executed_sha256=hashlib.sha256(source.encode()).hexdigest(), replacements=replay7.REPLACEMENTS)
    return scope
