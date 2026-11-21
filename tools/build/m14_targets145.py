"""Generate compact refusal keys for the frozen x64 app and selected WiX helper imports, not APIs."""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2]
BASE=['','kernel32.dll','msvcrt.dll','oleaut32.dll','user32.dll','advapi32.dll','comctl32.dll','comdlg32.dll','gdi32.dll','ole32.dll','shell32.dll','mpr.dll']

def key(provider,name,ordinal):
    data=provider.to_bytes(2,'little')+bytes([not bool(name)])+(name.encode() if name else ordinal.to_bytes(2,'little'))
    value=14695981039346656037
    for byte in data:value=((value^byte)*1099511628211)&((1<<64)-1)
    return value

def generate():
    inventory=json.loads((ROOT/'evidence/M14/0/binary-inventory.json').read_text(encoding='utf-8'))
    records=[r for r in inventory['binaries'] if (r['app']=='notepadpp' and r['relative_path']=='notepad++.exe')or(r['app']=='sumatra'and r['relative_path']=='SumatraPDF-3.6.1-64.exe')]
    assert len(records)==2
    # Preserve every existing provider ID; append helper-only namespaces.
    providers=BASE+sorted({v['dll']for r in records for v in r['imports']}-set(BASE))
    helper=next(r for r in inventory['binaries']if r['sha256']=='54febbd1f0a3875df16a4b88621cc0a10729b3c94b9a68639aab27d36fe39381')
    records.append(helper);providers+=sorted({v['dll']for v in helper['imports']}-set(providers)-{'msi.dll'})
    assert len(providers)<=64
    api=(ROOT/'user/windows8/api.c').read_text(encoding='utf-8')
    real={(int(provider),name,0)for name,provider in re.findall(r'API8\((\w+),(\d+)\)',api)}
    real.update((3,name,0)for name in ('SysAllocString','SysAllocStringLen','SysFreeString','SysStringLen','SysStringByteLen','SysAllocStringByteLen','VariantClear','VariantCopy'))
    real.update((3,'',ordinal)for ordinal in (2,4,6,7,9,10,149,150))
    # MSI is a real lazy PE, not a synthetic provider. Only missing static
    # imports may resolve to a fatal refusal after its real export lookup.
    from msi147 import ORDINALS147
    real.update((0,'',ordinal)for ordinal in ORDINALS147)
    existing={(int(provider),name,int(ordinal))for provider,ordinal,name in re.findall(r'\{(\d+),(\d+),"([^"]*)",', (ROOT/'user/windows8/guarded-ui144.inc').read_text(encoding='utf-8'))}
    existing.update((int(provider),'',int(ordinal))for provider,ordinal in re.findall(r'\{(\d+),(\d+),0,', (ROOT/'user/windows8/guarded-ui144.inc').read_text(encoding='utf-8')))
    keys={};rows=[]
    for record in records:
        for imported in record['imports']:
            provider=0 if imported['dll']=='msi.dll'else providers.index(imported['dll'])
            for symbol in imported['symbols']:
                ordinal=int(symbol[1:])if symbol.startswith('#')else 0;name=''if ordinal else symbol
                assert not name or re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',name),('Review function versus data import',symbol)
                identity=(provider,name,ordinal)
                if identity in real or identity in existing or(provider==6 and ordinal==17):continue
                value=key(*identity)
                assert value not in keys or keys[value]==identity,'Refusal-key collision'
                keys[value]=identity
                rows.append(dict(app=record['app'],dll=imported['dll'],symbol=symbol,key=f'{value:016x}',status='Refusal diagnostic only; no implementation or execution qualification'))
    names='/* Stable existing provider IDs; additional names are ABI refusal namespaces. */\nstatic const char*const provider_names145[]={'+','.join(json.dumps(p)for p in providers)+'};\n#define PROVIDERS145 '+str(len(providers))+'u\n'
    values='/* Generated refusal keys, never evidence of API compatibility. */\nstatic const uint64_t target_refusals145[]={\n'
    ordered=sorted(keys)
    for at in range(0,len(ordered),4):values+=' '+','.join('UINT64_C(0x'+f'{v:016x}'+')'for v in ordered[at:at+4])+',\n'
    values+='};\n'
    result=dict(scope='Frozen original main-image and selected WiX helper static function imports; diagnostic refusal only, not API or custom-action compatibility',provider_ids={p:i for i,p in enumerate(providers)if p},refusal_keys=len(keys),table_bytes=8*len(keys),imports=rows,inventory_sha256=hashlib.sha256((ROOT/'evidence/M14/0/binary-inventory.json').read_bytes()).hexdigest())
    return {'user/windows8/providers145.inc':names.encode(),'user/windows8/target-refusals145.inc':values.encode(),'docs/roadmap/target-import-refusals145.json':(json.dumps(result,indent=2)+'\n').encode()}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    for path,data in generate().items():
        target=ROOT/path
        if args.check:assert target.read_bytes()==data,('Generated refusal data is stale',path)
        else:target.write_bytes(data)
    print('PASS compact target refusal generation'if args.check else'Generated compact refusal data; no API implementation claimed')

if __name__=='__main__':main()
