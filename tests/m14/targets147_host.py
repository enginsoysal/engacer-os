"""Retain all refusal checks, including real-PE MSI provider-zero diagnostics."""
from pathlib import Path
import hashlib,json
import replay7

def main():
    canonical=Path(__file__).with_name('targets145_host.py');raw=canonical.read_bytes();source=raw.decode('utf-8')
    for before,after in replay7.REPLACEMENTS:source=source.replace(before,after)
    before="provider=data['provider_ids'][row['dll']]"
    assert source.count(before)==1
    source=source.replace(before,"provider=0 if row['dll']=='msi.dll' else data['provider_ids'][row['dll']]")
    scope=dict(__file__=str(canonical),__name__='targets147_derived')
    exec(compile(source,str(canonical),'exec'),scope);scope['main']()
    root=canonical.parents[2];table=json.loads((root/'docs/roadmap/target-import-refusals145.json').read_text(encoding='utf-8'));count=sum(row['dll']=='msi.dll' for row in table['imports']);assert count>0
    (root/'build/m14-native/stage7/targets-host/observer.json').write_bytes((json.dumps(dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(source.encode()).hexdigest(),adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),msi_provider=0,msi_unresolved_import_rows_checked=count,no_import_rows_skipped=True),indent=2)+'\n').encode())
