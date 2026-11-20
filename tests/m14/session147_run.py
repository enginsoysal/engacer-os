"""Qualify new cores in an owned clone on immutable accepted M14.6 media.

Exact derivation retains 21 complete close/cleanup cycles and original console
afterward. This qualifies the owned core PE, not a new OS or MSI installation.
"""
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]

def main():
    import replay6
    loader=replay6.ReplayLoader();sys.meta_path.insert(0,loader)
    try:
        from session147_build import build
        # Reuse only the retained input/lifetime protocol. All new output and
        # injected executable bytes are isolated under stage7 and a new clone.
        source=ROOT/'tests/m14/global146_run.py';raw=source.read_bytes();text=raw.decode()
        replacements=[('from global146_build import build','from session147_build import build'),("stage6/global-native","stage7/session-native"),('m146-global-native','m147-session-native'),("M146_GLOBAL_MEMORY_OWNERSHIP_QUOTA_THREADS_PASS","M147_MSI_SESSION_CONDITIONS_PROPERTIES_FORMATTING_PASS"),("concurrent_alloc_free_rounds=200","selected_core_assertions=22"),("Owned global-memory ABI, handle/LocalAlloc separation, allocation quota and native thread concurrency; not original application qualification","Owned MSI condition/property/scalar-formatting cores on accepted M14.6 media; not new OS, reusable MSI installation or custom-action qualification")]
        for before,after in replacements:
            assert text.count(before)==1,(before,text.count(before));text=text.replace(before,after)
        out=ROOT/'build/m14-native/stage7/session-native';out.mkdir(parents=True,exist_ok=True)
        (out/'observer.json').write_bytes((json.dumps(dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),replacements=replacements),indent=2)+'\n').encode())
        namespace={'__file__':str(source),'__name__':'session147_derived'};exec(compile(text,str(source),'exec'),namespace);namespace['main']()
    finally:
        sys.meta_path.remove(loader)
        out=ROOT/'build/m14-native/stage7/session-native';out.mkdir(parents=True,exist_ok=True);(out/'dependencies.json').write_bytes((json.dumps(replay6.observed,indent=2)+'\n').encode())

if __name__=='__main__':main()
