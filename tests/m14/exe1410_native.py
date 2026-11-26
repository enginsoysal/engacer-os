"""Replay the unchanged original EXE lifecycle on the M14.10 candidate."""
from pathlib import Path

import replay8

observer = Path(__file__).with_name("exe148_chain_native.py")
replay8.REPLACEMENTS += [("EngacerOS-M14STAGE8", "EngacerOS-M14STAGE10"),
                         ("m14stage8", "m14stage10")]
source = observer.read_text(encoding="utf-8")
source = source.replace("stage8", "stage10")
# The EXE observer timed out while parallel guests ran and registry writes continued.
# Run this observer alone and leave time for its original completion marker.
assert source.count("predicate,seconds=240)") == 1
source = source.replace("predicate,seconds=240)", "predicate,seconds=600)")
source = source.replace("m148-ordinary-exe-chain", "m1410-ordinary-exe-chain")
exec(compile(source, str(observer), "exec"), {"__file__": __file__, "__name__": "__main__"})
