"""Replay the nested original picker observer against the frozen stage-7 fixture."""
from pathlib import Path
import replay7

def main():
    canonical = Path(__file__).with_name('original_picker146_run.py')
    source = canonical.read_bytes().decode('utf-8')
    for before, after in replay7.REPLACEMENTS:
        source = source.replace(before, after)
    needle = "    source = canonical.read_bytes().decode('utf-8')"
    assert source.count(needle) == 1
    source = source.replace(needle, needle + "\n    for before, after in nested_replacements147:\n        source = source.replace(before, after)")
    scope = dict(__file__=str(canonical), __name__='nested_picker147', nested_replacements147=replay7.REPLACEMENTS)
    exec(compile(source, str(canonical), 'exec'), scope)
    scope['main']()
