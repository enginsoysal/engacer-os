"""Execute an i386 PE from a Win64 parent on the installed candidate."""
import hashlib
import json
import os
from pathlib import Path
import sys
import traceback

import replay7
from x86_build1410 import build

ROOT = Path(__file__).resolve().parents[2]
PRODUCT = "/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}"


def main():
    replay7.REPLACEMENTS += [("EngacerOS-M14STAGE7", "EngacerOS-M14STAGE10"),
                             ("m14stage7", "m14stage10")]
    loader = replay7.ReplayLoader()
    sys.meta_path.insert(0, loader)
    try:
        from window144_native import ui, c, f, t, clone, StoppedDisk, task
        from fixture1 import library

        stage = ROOT / "build/m14-native/stage10"
        out = stage / "x86-native"
        out.mkdir(parents=True, exist_ok=True)
        c.OUT = out
        meta = json.loads(ui.manifest_path12().read_text())
        smoke = json.loads((stage / "compact/results.json").read_text())
        assert smoke["passed"] and smoke["build_id"] == meta["build_id"]
        disk = Path(os.environ["LOCALAPPDATA"]) / "EngineOS/Tests/M6/m141-stage10-compact" / smoke["owned_fixture"] / "owned.img"
        work, disk, _ = clone(ui, disk, "m1410-native-x86")
        report = {"passed": False, "build_id": meta["build_id"], "source_commit": meta["source_commit"],
                  "owned_fixture": work.name, "observer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

        def start(name):
            boot = ui.guest(work / name, disk, media="installed", ready="M7_DESKTOP_READY", ram=128)
            ui.s.normal_boot(boot)
            return boot

        def front(g):
            p = ui.Pointer(g)
            p.drain()
            c.key(g, "esc")
            t.close_all(g, p)
            t.launch(g, p, "windows apps", 19)
            return p

        try:
            with start("install") as g:
                p = front(g)
                p.desktop(12001, True)
                task(g, p, 12003)
                assert PRODUCT + "/product.bin" in f.entries(g)
            files = build()
            volume = StoppedDisk(disk, library())
            try:
                report["images"] = {}
                for fixture, target in (("x86-parent.exe", "7z.exe"),
                                        ("helper32.exe", "helper32.exe"), ("fault32.exe", "fault32.exe")):
                    data = (files / fixture).read_bytes()
                    volume.put(PRODUCT + "/" + target, data)
                    report["images"][fixture] = hashlib.sha256(data).hexdigest()
            finally:
                volume.close()
            with start("probe") as g:
                p = front(g)
                try:
                    result = task(g, p, 12005)
                    assert "M1410_NATIVE_I386_THUNK_PASS" in result, result
                    assert "M1410_X64_PARENT_I386_CHILD_PASS" in result, result
                    serial = g.log()
                    assert "M8_PROCESS_FAULT vector=0x0000000000000006" in serial, serial[-5000:]
                    report["output"] = result
                finally:
                    (out / "serial.log").write_text(g.log(), encoding="utf-8")
            report["passed"] = True
        except Exception:
            report["error"] = ui.q.clean(traceback.format_exc())
            raise
        finally:
            (out / "results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            print(json.dumps(report, indent=2), flush=True)
    finally:
        sys.meta_path.remove(loader)


if __name__ == "__main__":
    main()
