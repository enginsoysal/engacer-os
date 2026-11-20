"""Add M14.6 tasks to all seventy-four retained M14.5 orchestration tasks."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    listing = '--list' in sys.argv
    if listing:
        sys.argv.remove('--list')
    canonical = ROOT / 'tests/m14/suite5.py'
    raw = canonical.read_bytes()
    source = raw.decode('utf-8')
    replacements = [('M14.5', 'M14.6'), ('STAGE5', 'STAGE6'), ('stage5', 'stage6'),
                    ('replay5.py', 'replay6.py'), ("'--stage','5'", "'--stage','6'"),
                    ("default='revision17'", "default='full1'")]
    for before, after in replacements:
        assert before in source, before
        source = source.replace(before, after)
    before = ' assert len(tasks)==74,len(tasks)'
    assert source.count(before) == 1
    addition = ''' assert len(tasks)==74,len(tasks)
 # Retain the original dialog parser corpus, adding actual helper templates.
 tasks['dialog145-host']['command']=[sys.executable,'tests/m14/replay6.py','dialog146_host']
 for profile in ('compact','ordinary','4k'):
  dependency=('apps-'+profile,)
  add('original-clipboard146-'+profile,'tests/m14/original_clipboard146_run.py',('--profile',profile),dependency,4)
  add('original-picker146-'+profile,'tests/m14/original_picker146_run.py',('--profile',profile),dependency,4)
  add('font146-'+profile,'tests/m14/font146_run.py',('--profile',profile,'--cycles','21'if profile=='compact'else'1'),dependency,4)
 for name,script,arguments in (
  ('global146','global146_run.py',()),('clipboard146','clipboard146_run.py',()),
  ('chords146','chords146_run.py',()),('mapping146','mapping146_run.py',('--cycles','21')),
  ('picker146','picker146_run.py',('--cycles','21')),
  ('picker-lifetime146','picker_lifetime146_run.py',('--cycles','21'))):
  add(name,'tests/m14/'+script,arguments,('apps-compact',),4)
 for name,script in (
  ('global146-host','global146_host.py'),('mapping146-host','mapping146_host.py'),
  ('document146-host','document146_host.py'),('pack146-host','pack146_host.py'),('font146-host','font146_host.py')):
  add(name,'tests/m14/'+script,priority=30)
 assert len(tasks)==94,len(tasks)'''
    source = source.replace(before, addition)
    before = " assert all(t['dependencies']<=tasks.keys()for t in tasks.values())"
    assert source.count(before) == 1
    source = source.replace(before, before + '''
 if suite_list146:
  print(json.dumps({name:{'command':value['command'][1:],'dependencies':sorted(value['dependencies'])}for name,value in tasks.items()},indent=2));return''')
    before = ' source_tree=hashlib.sha256(json.dumps(tree,sort_keys=True).encode()).hexdigest()'
    assert source.count(before) == 1
    source = source.replace(before, before + '''
 (out/'observer-tree.json').write_bytes((json.dumps({'files':tree,'source_tree_sha256':source_tree,'suite_derivation':suite_derivation146},indent=2)+'\\n').encode())''')
    derivation = dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),
                      executed_sha256=hashlib.sha256(source.encode()).hexdigest(),
                      adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      replacements=replacements, retained_tasks=74, total_tasks=94)
    namespace = dict(__name__='m146_suite_derivation', __file__=str(canonical), suite_derivation146=derivation, suite_list146=listing)
    exec(compile(source, str(canonical), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
