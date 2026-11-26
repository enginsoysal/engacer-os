"""Repair a damaged MSI application while its neighboring bundle keeps working."""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import sys
import traceback

import replay7
from private1410_native import A, B
from migration1410_native import read

ROOT = Path(__file__).resolve().parents[2]


def main():
    replay7.REPLACEMENTS += [("EngacerOS-M14STAGE7", "EngacerOS-M14STAGE10"),
                             ("m14stage7", "m14stage10")]
    loader = replay7.ReplayLoader()
    sys.meta_path.insert(0, loader)
    try:
        from window144_native import ui, c, f, t, clone, StoppedDisk, task
        from fixture1 import library

        stage = ROOT / "build/m14-native/stage10"
        out = stage / "repair"
        out.mkdir(parents=True, exist_ok=True)
        c.OUT = out
        meta = json.loads(ui.manifest_path12().read_text())
        base = json.loads((stage / "private-ab/results.json").read_text())
        assert base["passed"] and base["build_id"] == meta["build_id"]
        disk = Path(os.environ["LOCALAPPDATA"]) / "EngineOS/Tests/M6/m1410-private-ab" / base["owned_fixture"] / "owned.img"
        work, disk, _ = clone(ui, disk, "m1410-repair-ab")
        lib = library(["remove"])
        report = {"passed": False, "build_id": meta["build_id"], "source_commit": meta["source_commit"],
                  "owned_fixture": work.name}

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

        def run_b(g, p):
            p.desktop(12208, True)
            entries = f.entries(g)
            roots = sorted((A, B), key=lambda root: entries[root]["index"])
            p.desktop(12200 + roots.index(B), True)
            p.desktop(12301, True)
            row = f.entries(g)[B + "/isolation.exe"]["index"]
            for _ in range(128):
                if any(control[5] == 55000 + row for control in f.controls(g)):
                    p.desktop(55000 + row, True)
                    assert "M1410_PRIVATE_APP_B_PASS" in task(g, p, 54011)
                    return
                p.desktop(54023, True)
            raise AssertionError("B executable unavailable")

        def bundle_digest(volume, root):
            result = hashlib.sha256()
            for entry in volume.volume.entries:
                path = entry.path.decode()
                if entry.kind == 1 and path.startswith(root + "/"):
                    result.update(path.encode() + bytes(1))
                    result.update(hashlib.sha256(read(volume, path)).digest())
            return result.hexdigest()

        try:
            volume = StoppedDisk(disk, lib)
            try:
                other = bundle_digest(volume, B)
                header = read(volume, A + "/product.bin")
                at = 1024
                expected = None
                while at < len(header):
                    kind = int.from_bytes(header[at:at+4], "little")
                    length = int.from_bytes(header[at+4:at+8], "little")
                    if kind == 1 and header[at+8:at+264].split(bytes(1), 1)[0] == b"7z.exe":
                        expected = header[at+264:at+296].hex()
                        break
                    at += length
                assert expected and hashlib.sha256(read(volume, A + "/7z.exe")).hexdigest() != expected
                assert lib.v6_remove(ctypes.byref(volume.volume), (A + "/7z.exe").encode()) == 0
            finally:
                volume.close()
            with start("repair") as g:
                p = front(g)
                p.desktop(12302, True)
                task(g, p, 12003)
                assert "7-Zip" in task(g, p, 12005)
                (out / "serial-repair.log").write_text(g.log(), encoding="utf-8")
            volume = StoppedDisk(disk, lib)
            try:
                assert bundle_digest(volume, B) == other
                assert hashlib.sha256(read(volume, A + "/7z.exe")).hexdigest() == expected
                assert read(volume, A + "/product.bin") == header
            finally:
                volume.close()
            with start("cold-start") as g:
                p = front(g)
                assert "7-Zip" in task(g, p, 12005)
                run_b(g, p)
                (out / "serial-cold.log").write_text(g.log(), encoding="utf-8")
            report.update(passed=True, restored_sha256=expected, neighbor_bundle_sha256=other,
                          observer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
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
