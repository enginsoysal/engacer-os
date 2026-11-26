"""Exercise identical DLL, registry and temporary names in two installed bundles."""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import struct
import sys
import traceback

import replay7
from private1410_build import build

ROOT = Path(__file__).resolve().parents[2]
APP = "/Applications/Windows/"
A = APP + "{23170F69-40C1-2702-2606-000001000000}"
B = APP + "{A23B657D-838B-4C9B-8F9D-386E50C1A76B}"
DLL = "/System/System32/bundle-test.dll"
PACKAGE = "npp.8.9.9.1.Installer.x64.msi"


def main():
    replay7.REPLACEMENTS += [("EngacerOS-M14STAGE7", "EngacerOS-M14STAGE10"),
                             ("m14stage7", "m14stage10")]
    loader = replay7.ReplayLoader()
    sys.meta_path.insert(0, loader)
    try:
        from window144_native import ui, c, f, t, clone, StoppedDisk, task
        from fixture1 import library

        meta = json.loads(ui.manifest_path12().read_text(encoding="utf-8"))
        base = json.loads((ROOT / "build/m14-native/stage10/compact/results.json").read_text(encoding="utf-8"))
        assert base["passed"] and base["build_id"] == meta["build_id"]
        home = Path(os.environ["LOCALAPPDATA"])
        source = home / "EngineOS/Tests/M6/m141-stage10-compact" / base["owned_fixture"] / "owned.img"
        work, disk, _ = clone(ui, source, "m1410-private-ab")
        package = (home / "EngacerOS/Research/M14/0" / PACKAGE).read_bytes()
        download = "/Users/Owner/Downloads/" + PACKAGE
        out = ROOT / "build/m14-native/stage10/private-ab"
        out.mkdir(parents=True, exist_ok=True)
        c.OUT = out
        disk_lib = library()
        report = {"passed": False, "build_id": meta["build_id"],
                  "source_commit": meta["source_commit"], "owned_fixture": work.name,
                  "markers": [], "backing": {}}

        def start(name):
            boot = ui.guest(work / name, disk, media="installed", ready="M7_DESKTOP_READY", ram=128)
            ui.s.normal_boot(boot)
            return boot

        def front(g):
            pointer = ui.Pointer(g)
            pointer.drain()
            c.key(g, "esc")
            t.close_all(g, pointer)
            t.launch(g, pointer, "windows apps", 19)
            return pointer

        def choose_file(g, pointer, path):
            row = f.entries(g)[path]["index"]
            for _ in range(128):
                if any(control[5] == 55000 + row for control in f.controls(g)):
                    pointer.desktop(55000 + row, True)
                    return
                pointer.desktop(54023, True)
            raise AssertionError("File missing from the picker: " + path)

        try:
            volume = StoppedDisk(disk, disk_lib)
            try:
                volume.put(download, package)
            finally:
                volume.close()

            with start("install") as g:
                p = front(g)
                p.desktop(12001, True)
                task(g, p, 12003)
                assert A + "/product.bin" in f.entries(g)
                p.desktop(12013, True)
                assert c.flag(g, "picker12") == 9
                p.desktop(54019, True)
                c.key(g, "ctrl", "a")
                c.type_text(g, "/Users/Owner/Downloads")
                c.key(g, "ret")
                p.drain()
                choose_file(g, p, download)
                p.desktop(54011, True)
                task(g, p, 12000)
                p.desktop(12001, True)
                task(g, p, 12003)
                assert B + "/product.bin" in f.entries(g)

            fixtures = build()
            native = (fixtures / "isolation.exe").read_bytes()
            volume = StoppedDisk(disk, disk_lib)
            try:
                for root, marker, image in [(A, "A", "7z.exe"), (B, "B", "isolation.exe")]:
                    for part in ["/System", "/System/System32"]:
                        path = (root + part).encode()
                        assert volume.lib.v6_mkdir(ctypes.byref(volume.volume), path) == 0
                    volume.put(root + "/" + image, native)
                    volume.put(root + DLL, (fixtures / marker / "bundle-test.dll").read_bytes())
            finally:
                volume.close()

            for index in range(2):
                with start("observe-" + str(index)) as g:
                    p = front(g)
                    assert "M1410_PRIVATE_APP_A_PASS" in task(g, p, 12005)
                    report["markers"].append("A")
                    p.desktop(12208, True)
                    entries = f.entries(g)
                    roots = sorted((A, B), key=lambda root: entries[root]["index"])
                    p.desktop(12200 + roots.index(B), True)
                    p.desktop(12301, True)
                    choose_file(g, p, B + "/isolation.exe")
                    assert "M1410_PRIVATE_APP_B_PASS" in task(g, p, 54011)
                    report["markers"].append("B")
                    (out / ("serial-" + str(index) + ".log")).write_text(g.log(), encoding="utf-8")

            owner = hashlib.sha256(b"/Users/Owner").hexdigest()[:32]
            key = hashlib.sha256(b"software\\engacerbundleisolation").hexdigest()[:32]
            value = hashlib.sha256(b"marker").hexdigest()[:32]
            volume = StoppedDisk(disk, disk_lib)
            try:
                records = {e.path.decode(): e for e in volume.volume.entries if e.kind == 1}
                for root, marker in [(A, "A"), (B, "B")]:
                    paths = [root + DLL, root + "/.Engacer/Temp/" + owner + "/bundle-test.bin",
                             root + "/.Engacer/Registry/" + owner + "/k" + key + "/v" + value]
                    contents = []
                    for path in paths:
                        entry = records[path]
                        assert volume.lib.v6_verify(ctypes.byref(volume.volume), entry.path) == 0
                        volume.file.seek(volume.offset + entry.first * 4096)
                        contents.append(volume.file.read(entry.size))
                    assert contents[0] == (fixtures / marker / "bundle-test.dll").read_bytes()
                    assert contents[1] == contents[2][-4:] == struct.pack("<I", ord(marker))
                    report["backing"][marker] = {"paths": paths, "first_blocks": [records[p].first for p in paths],
                                                 "dll_sha256": hashlib.sha256(contents[0]).hexdigest()}
                blocks = [block for result in report["backing"].values() for block in result["first_blocks"]]
                assert len(set(blocks)) == len(blocks)
            finally:
                volume.close()
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
