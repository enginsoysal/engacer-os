"""Add M14.6 tasks to all seventy-four retained M14.5 orchestration tasks."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def validate_resume(prior, name, record, command, current_tree, current_digest, out, build):
    """Reuse only proven unmodified tasks; preserve their actual original tree hash."""
    if record.get('validated_source_tree_sha256',record.get('source_tree_sha256')) == current_digest:
        return True
    assert prior and record.get('validated_source_tree_sha256',record.get('source_tree_sha256')) == prior['source_tree_sha256']
    original = prior
    if record['source_tree_sha256'] != prior['source_tree_sha256']:
        original = json.loads((out / ('observer-tree-' + record['source_tree_sha256'] + '.json')).read_text())
        assert hashlib.sha256(json.dumps(original['files'],sort_keys=True).encode()).hexdigest()==record['source_tree_sha256']
    old = original['files']
    differences = {path for path in old.keys() | current_tree.keys() if old.get(path) != current_tree.get(path)}
    allowed = {'tests/m14/verify6.py','tests/m14/suite6.py','tests/m14/public_site6_scoped.mjs',
               'tests/m14/close6_scoped.py','tests/m14/picker_lifetime146_run.py',
               'tests/m14/window146_run.py','tests/m14/picker_restart146_run.py'}
    assert differences <= allowed, ('Unreviewed campaign input changes', sorted(differences))
    if name == 'picker-lifetime146' and 'tests/m14/picker_lifetime146_run.py' in differences:
        return False
    if command[0] == 'tests/m14/replay6.py':
        import re
        target, arguments = command[1], command[2:]
        suffix = '-'.join(re.sub('[^a-zA-Z0-9_-]','',a) for a in arguments)
        path = out.parent.parent / 'replay-observers' / (target + ('-' + suffix if suffix else '') + '.json')
        observed = json.loads(path.read_text())
        assert observed['passed'] and observed['build_id'] == build
        assert not (differences & observed['observer_sources'].keys()), ('A consumed observer changed', name)
        for path, row in observed['observer_sources'].items():
            assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == row['canonical_sha256'], (name,path)
    else:
        assert command[0] in ('tests/m14/native1.py','tools/release/vmware_starter14.py')
    record['validated_source_tree_sha256'] = current_digest
    record['verified_unconsumed_tree_changes'] = {path: {'before':old.get(path),'after':current_tree.get(path)} for path in sorted(differences)}
    record['reuse_scope'] = 'Identical frozen OS artifacts and consumed observers; changed pending-dialog observer reruns, public/orchestration/verifier changes do not execute in this retained task'
    return True


def main():
    listing = '--list' in sys.argv
    if listing:
        sys.argv.remove('--list')
    canonical = ROOT / 'tests/m14/suite5.py'
    raw = canonical.read_bytes()
    source = raw.decode('utf-8')
    replacements = [('M14.5', 'M14.6'), ('STAGE5', 'STAGE6'), ('stage5', 'stage6'),
                    ('replay5.py', 'replay6.py'), ("'--stage','5'", "'--stage','6'"),
                    ("default='revision17'", "default='full2'")]
    for before, after in replacements:
        assert before in source, before
        source = source.replace(before, after)
    before = ' assert len(tasks)==74,len(tasks)'
    assert source.count(before) == 1
    addition = ''' assert len(tasks)==74,len(tasks)
 # Retain the original dialog parser corpus, adding actual helper templates.
 tasks['dialog145-host']['command']=[sys.executable,'tests/m14/replay6.py','dialog146_host']
 tasks['windows']['command']=[sys.executable,'tests/m14/replay6.py','window146_run']
 add('picker-restart146','tests/m14/picker_restart146_run.py',('--cycles','1'),('apps-compact',),4)
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
  ('document146-host','document146_host.py'),('pack146-host','pack146_host.py'),('font146-host','font146_host.py'),('static146-host','static146_host.py')):
  add(name,'tests/m14/'+script,priority=30)
 assert len(tasks)==96,len(tasks)'''
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
    prior_tree = None
    if '--resume' in sys.argv:
        revision = sys.argv[sys.argv.index('--revision') + 1] if '--revision' in sys.argv else 'full2'
        tree_path = ROOT / 'build/m14-native/stage6/development' / revision / 'observer-tree.json'
        prior_tree = json.loads(tree_path.read_text())
        assert hashlib.sha256(json.dumps(prior_tree['files'], sort_keys=True).encode()).hexdigest() == prior_tree['source_tree_sha256']
        backup = tree_path.with_name('observer-tree-' + prior_tree['source_tree_sha256'] + '.json')
        if not backup.exists():
            backup.write_bytes(tree_path.read_bytes())
    needle = "   if r.get('source_tree_sha256')!=source_tree:continue"
    assert source.count(needle) == 1
    source = source.replace(needle, "   if not validate_resume146(name,r,tasks[name]['command'][1:],tree,source_tree,out,build):continue")
    derivation = dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),
                      executed_sha256=hashlib.sha256(source.encode()).hexdigest(),
                      adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      replacements=replacements, retained_tasks=74, total_tasks=96)
    namespace = dict(__name__='m146_suite_derivation', __file__=str(canonical), suite_derivation146=derivation, suite_list146=listing, validate_resume146=lambda *args: validate_resume(prior_tree,*args))
    exec(compile(source, str(canonical), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
