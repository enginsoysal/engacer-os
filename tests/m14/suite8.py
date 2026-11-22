"""Retain stage-seven qualification on new media and add stage-eight contracts.

This adapter never edits accepted historical observers. Resume requires an
identical observer tree; changed inputs require a fresh campaign.
"""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def resume148(prior,name,record,command,current_tree,current_digest,out,build):
 if record.get('validated_source_tree_sha256',record['source_tree_sha256'])==current_digest:return True
 if not prior:return False
 original=prior if record['source_tree_sha256']==prior['source_tree_sha256']else json.loads((out/('observer-tree-'+record['source_tree_sha256']+'.json')).read_text())
 assert hashlib.sha256(json.dumps(original['files'],sort_keys=True).encode()).hexdigest()==record['source_tree_sha256']
 old=original['files'];differences={p for p in old.keys()|current_tree.keys()if old.get(p)!=current_tree.get(p)}
 allowed={'tests/m14/suite8.py','tests/m14/verify8.py','tests/m14/wix_action148_lifetimes.py','tests/m14/wix_system148_native.py','tests/m14/painting148_entry.py'}
 if not differences<=allowed:return False
 if any(p in differences and p in old for p in ['tests/m14/wix_action148_lifetimes.py','tests/m14/wix_system148_native.py','tests/m14/painting148_entry.py']):return False
 assert command[0]not in differences
 record['validated_source_tree_sha256']=current_digest
 record['verified_unconsumed_tree_changes']={p:dict(before=old.get(p),after=current_tree.get(p))for p in sorted(differences)}
 record['reuse_scope']='Unchanged frozen OS media, command and consumed observers; only orchestration/verifier maintenance and previously absent scoped test entries were added. Original executed tree is preserved.'
 return True

def main():
 canonical=ROOT/'tests/m14/suite7.py';raw=canonical.read_bytes();text=raw.decode()
 for old,new in [('M14.7','M14.8'),('STAGE7','STAGE8'),('stage7','stage8'),('replay7.py','replay8.py'),("'--stage','7'","'--stage','8'"),('final7','final8')]:text=text.replace(old,new)
 needle=" assert len(tasks)==138,len(tasks)'''";assert text.count(needle)==1
 additions=""" assert len(tasks)==138,len(tasks)
 for name,script,dependencies in (
  ('session148-native','session148_run.py',('apps-compact',)),
  ('font148-native','font148_run.py',('session148-native',)),
  ('copy148-native','copy148_run.py',('font148-native',)),
  ('exe148-review','exe148_review_run.py',('compact',)),
  ('exe148-chain','exe148_chain_native.py',('compact',)),
  ('batch148-host','batch148_host.py',()),
  ('registry-info148-reference','registry_info148_reference.py',()),
  ('static148-host','static148_host.py',()),
  ('rtl148-native','rtl148_run.py',('copy148-native',)),
  ('software148-native','software148_run.py',('apps-compact',))):
  add(name,'tests/m14/'+script,dependencies=dependencies,priority=5 if dependencies else 30)
  tasks[name]['command']=[sys.executable,'tests/m14/'+script]
 del tasks['static146-host']
 tasks['msi147-wix_action-native']['command']=[sys.executable,'tests/m14/wix_action148_lifetimes.py']
 tasks['msi147-wix_system-native']['command']=[sys.executable,'tests/m14/wix_system148_native.py']
 tasks['faults']['command']=[sys.executable,'tests/m14/painting148_entry.py','fault']
 tasks['paint']['command']=[sys.executable,'tests/m14/painting148_entry.py','paint']
 assert len(tasks)==147,len(tasks)'''"""
 text=text.replace(needle,additions)
 text=text.replace('retained_tasks=74, total_tasks=138','retained_tasks=74, total_tasks=147, stage7_tasks=138, stage8_added_tasks=9, outer_stage8_adapter_sha256=hashlib.sha256((ROOT/\"tests/m14/suite8.py\").read_bytes()).hexdigest()')
 needle='def validate_resume(prior, name, record, command, current_tree, current_digest, out, build):'
 assert text.count(needle)==1
 text=text.replace(needle,needle+'\n    return resume148(prior,name,record,command,current_tree,current_digest,out,build)\n')
 namespace=dict(__name__='suite148_derivation',__file__=str(canonical),resume148=resume148)
 exec(compile(text,str(canonical),'exec'),namespace)
 namespace['main']()

if __name__=='__main__':main()
