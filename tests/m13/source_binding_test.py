"""A documentation-only commit may advance; changed compiled bytes cannot qualify."""
import hashlib,subprocess,tempfile,unittest
from pathlib import Path
from close_stage import verify_inputs_at_commit

class SourceBinding(unittest.TestCase):
 def test_documentation_advance_and_changed_runtime(self):
  with tempfile.TemporaryDirectory(prefix='engacer-source-binding-') as folder:
   root=Path(folder)
   def git(*args):return subprocess.check_output(['git',*args],cwd=root,stderr=subprocess.DEVNULL).decode().strip()
   def commit(message):
    git('add','.');git('-c','user.name=Engacer test','-c','user.email=test@example.invalid','commit','-m',message);return git('rev-parse','HEAD')
   git('init');(root/'runtime.c').write_bytes(b'original compiled bytes\n');(root/'README.md').write_bytes(b'original docs\n');release=commit('release')
   records={'runtime.c':hashlib.sha256((root/'runtime.c').read_bytes()).hexdigest()}
   (root/'README.md').write_bytes(b'updated publication status\n');docs=commit('documentation only')
   self.assertEqual(verify_inputs_at_commit(release,records,root),release);self.assertEqual(verify_inputs_at_commit(docs,records,root),docs)
   (root/'runtime.c').write_bytes(b'different runtime\n');changed=commit('changed native source')
   with self.assertRaisesRegex(AssertionError,'Compiled source differs'):verify_inputs_at_commit(changed,records,root)
   with self.assertRaisesRegex(AssertionError,'Missing compiled source'):verify_inputs_at_commit(release,{'missing.c':'0'*64},root)

if __name__=='__main__':unittest.main()
