"""Check the installed generation across a native MSI lifecycle on M14.10."""
from pathlib import Path
import sys

import replay7

ROOT = Path(__file__).resolve().parents[2]
observer = ROOT / "tests/m14/generic147_native.py"
replay7.REPLACEMENTS += [("EngacerOS-M14STAGE7", "EngacerOS-M14STAGE10"),
                         ("m14stage7", "m14stage10")]
if "--private-registry" in sys.argv:
    sys.argv.remove("--private-registry")
    class RegistryObserver(replay7.ReplayLoader):
        def exec_module(self, module):
            if module.__name__ != "registry_readback147":
                return super().exec_module(module)
            path = DIRECTORY / "registry_readback147.py"
            module.__file__ = str(path)
            code = path.read_text(encoding="utf-8")
            old = "path.startswith(b'/Data/Windows/') and b'/Registry/'in path"
            new = "path.startswith(b'/Applications/Windows/{A23B657D-838B-4C9B-8F9D-386E50C1A76B}/.Engacer/Registry/')"
            assert code.count(old) == 1
            exec(compile(code.replace(old, new), str(path), "exec"), module.__dict__)

    DIRECTORY = Path(__file__).resolve().parent
    replay7.ReplayLoader = RegistryObserver

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
