"""Recheck the named-object and surviving-helper contract on M14.10 media."""
import importlib.abc
import importlib.util
from pathlib import Path
import sys

DIRECTORY = Path(__file__).resolve().parent
MODULES = {"thread_native2", "named_sync_native2", "named_sync_fixtures2"}


class CandidateLoader(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def find_spec(self, fullname, path=None, target=None):
        if fullname in MODULES:
            source = DIRECTORY / (fullname + ".py")
            return importlib.util.spec_from_loader(fullname, self, origin=str(source))
        return None

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        source = Path(module.__spec__.origin)
        module.__file__ = str(source)
        code = source.read_text(encoding="utf-8")
        code = code.replace("EngacerOS-M14STAGE2", "EngacerOS-M14STAGE10")
        code = code.replace("m14-native/stage2", "m14-native/stage10")
        code = code.replace("m141-stage2-compact", "m141-stage10-compact")
        code = code.replace("m142-named-sync", "m1410-named-sync")
        exec(compile(code, str(source), "exec"), module.__dict__)


if __name__ == "__main__":
    loader = CandidateLoader()
    sys.meta_path.insert(0, loader)
    try:
        from named_sync_native2 import main

        main()
    finally:
        sys.meta_path.remove(loader)
