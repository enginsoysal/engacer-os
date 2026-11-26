"""Check the installed generation across a native MSI lifecycle on M14.10."""
from pathlib import Path
import sys

import replay7

ROOT = Path(__file__).resolve().parents[2]
observer = ROOT / "tests/m14/generic147_native.py"
replay7.REPLACEMENTS += [("EngacerOS-M14STAGE7", "EngacerOS-M14STAGE10"),
                         ("m14stage7", "m14stage10")]
source = observer.read_text(encoding="utf-8")
source = source.replace("stage7", "stage10").replace("m147-generic-", "m1410-generation-")
marker = "  def snapshot(g):"
assert source.count(marker) == 1
source = source.replace(marker, """  def verify_generation(expected):
   record = '/Data/Windows/InstallGenerations/' + root.rsplit('/', 1)[-1]
   value = struct.unpack('<Q', document(record, 8))[0]
   assert value == expected, (value, expected)
   report.setdefault('installation_generations', []).append(value)
""" + marker)
for operation, epoch in [('install', 1), ('remove without original download after independent restart', 1),
                         ('reinstall original selection', 2), ('remove unchanged reinstalled product', 2)]:
    marker = "report['tasks'].append(dict(operation=" + repr(operation)
    assert source.count(marker) == 1
    source = source.replace(marker, f"verify_generation({epoch});" + marker)
exec(compile(source, str(observer), "exec"), {"__file__": __file__, "__name__": "__main__"})
