"""Execute current-stage adapters once; their own nested replay remains recorded."""
import argparse,hashlib,sys
from pathlib import Path
import replay7

SCENARIOS = {name + '147_run' for name in ('api','codepage','atom','fls','machine','pipe','slist','version','wix_system')} | {'wix_action147_lifetimes'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--scenario',choices=sorted(SCENARIOS),required=True);args=parser.parse_args()
    source=Path(__file__).with_name(args.scenario+'.py');raw=source.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    replay7.observed[source.relative_to(source.parents[2]).as_posix()]=dict(canonical_sha256=digest,executed_sha256=digest,execution_mode='canonical-stage7-entry')
    scope=dict(__file__=str(source),__name__='canonical147_'+args.scenario)
    exec(compile(raw.decode('utf-8'),str(source),'exec'),scope)
    previous_argv=sys.argv;sys.argv=[str(source)]
    try:scope['main']()
    finally:sys.argv=previous_argv
