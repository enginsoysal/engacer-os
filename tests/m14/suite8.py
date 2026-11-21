"""Retain stage-seven qualification on new media and add stage-eight contracts.

This adapter never edits accepted historical observers. Resume requires an
identical observer tree; changed inputs require a fresh campaign.
"""
import hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 canonical=ROOT/'tests/m14/suite7.py';raw=canonical.read_bytes();text=raw.decode()
 for old,new in [('M14.7','M14.8'),('STAGE7','STAGE8'),('stage7','stage8'),('replay7.py','replay8.py'),("'--stage','7'","'--stage','8'"),('final7','final8')]:text=text.replace(old,new)
 needle=" assert len(tasks)==138,len(tasks)'''";assert text.count(needle)==1
 additions=""" assert len(tasks)==138,len(tasks)
 for name,script,dependencies in (
  ('session148-native','session148_run.py',('apps-compact',)),
  ('font148-native','font148_run.py',('session148-native',)),
  ('copy148-native','copy148_run.py',('apps-compact',)),
  ('exe148-review','exe148_review_run.py',('compact',)),
  ('exe148-chain','exe148_chain_native.py',('compact',)),
  ('batch148-host','batch148_host.py',()),
  ('registry-info148-reference','registry_info148_reference.py',()),
  ('static148-host','static148_host.py',()),
  ('rtl148-native','rtl148_run.py',('apps-compact',)),
  ('software148-native','software148_run.py',('apps-compact',))):
  add(name,'tests/m14/'+script,dependencies=dependencies,priority=5 if dependencies else 30)
  tasks[name]['command']=[sys.executable,'tests/m14/'+script]
 del tasks['static146-host']
 assert len(tasks)==147,len(tasks)'''"""
 text=text.replace(needle,additions)
 needle='def validate_resume(prior, name, record, command, current_tree, current_digest, out, build):'
 assert text.count(needle)==1
 text=text.replace(needle,needle+'\n    return record.get("source_tree_sha256")==current_digest\n')
 namespace=dict(__name__='suite148_derivation',__file__=str(canonical))
 exec(compile(text,str(canonical),'exec'),namespace)
 namespace['main']()

if __name__=='__main__':main()
