"""Derive nested accepted observers with explicit current-stage path mappings."""
from pathlib import Path
import hashlib
import replay7

def map_source(source):
    for before, after in replay7.REPLACEMENTS:
        source = source.replace(before, after)
    # Guest leaf names are an ABI fixture contract, not stage ownership paths.
    for leaf in ('open-', 'save-', 'hidden.bin'):
        source = source.replace('m' + str(147) + '-' + leaf, 'm' + str(146) + '-' + leaf)
    return source


def load_adapter(name):
    canonical = Path(__file__).with_name(name + '.py')
    raw = canonical.read_bytes()
    source = raw.decode('utf-8').replace('from replay6 import REPLACEMENTS', 'from replay7 import REPLACEMENTS')
    for before, after in replay7.REPLACEMENTS:
        source = source.replace(before, after)
    needle = 'def derive(source):'
    assert source.count(needle) == 1
    source = source.replace(needle, needle + '\n    source = map_source147(source)')
    scope = dict(__file__=str(canonical), __name__='nested147_' + name, map_source147=map_source)
    exec(compile(source, str(canonical), 'exec'), scope)
    scope['derivation147'] = dict(canonical_sha256=hashlib.sha256(raw).hexdigest(), executed_sha256=hashlib.sha256(source.encode()).hexdigest(), replacements=replay7.REPLACEMENTS)
    return scope
