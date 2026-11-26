"""Native installed two-app lifecycle with a migrated neighboring MSI bundle."""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

import replay7
from migration1410_native import GENERATION, PRIVATE, ensure, read, registry_effects
from private1410_native import A, B, DLL, PACKAGE
from private1410_build import build

ROOT = Path(__file__).resolve().parents[2]
EXE = A + "/7z.exe"
VERSION = b"26.07.00.0"


def main():
    replay7.REPLACEMENTS += [("EngacerOS-M14STAGE7", "EngacerOS-M14STAGE10"),
                             ("m14stage7", "m14stage10")]
    loader = replay7.ReplayLoader()
    sys.meta_path.insert(0, loader)
    try:
        from window144_native import ui, c, f, t, clone, StoppedDisk, task
        from fixture1 import library

        stage = ROOT / "build/m14-native/stage10"
        out = stage / "app-lifecycle"
        out.mkdir(parents=True, exist_ok=True)
        c.OUT = out
        meta = json.loads(ui.manifest_path12().read_text())
        base = json.loads((stage / "compact/results.json").read_text())
        assert base["passed"] and base["build_id"] == meta["build_id"]
        home = Path(os.environ["LOCALAPPDATA"])
        blank = home / "EngineOS/Tests/M6/m141-stage10-compact" / base["owned_fixture"] / "owned.img"
        work, disk, copied = clone(ui, blank, "m1410-lifecycle")
        lib = library(["remove"])
        source = (home / "EngacerOS/Research/M14/0" / PACKAGE).read_bytes()
        package_spec = subprocess.check_output(["pwsh", "-NoProfile", "-File",
            str(Path(__file__).with_name("update1410_package.ps1")),
            str(ROOT / "third_party/7zip/7z2606-x64.msi"), str(out / "update-package")])
        upgrade = json.loads(package_spec)
        update = Path(upgrade["package"])
        update_data = update.read_bytes()
        update_path = "/Users/Owner/Downloads/" + update.name
        download = "/Users/Owner/Downloads/" + PACKAGE
        report = {"passed": False, "build_id": meta["build_id"], "source_commit": meta["source_commit"],
                  "owned_fixture": work.name, "clone": copied, "runs": [],
                  "update_sha256": hashlib.sha256(update_data).hexdigest(),
                  "expected_updated_exe_sha256": upgrade["image_sha256"],
                  "observer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

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

        def select(g, pointer, path):
            row = f.entries(g)[path]["index"]
            for _ in range(128):
                if any(control[5] == 55000 + row for control in f.controls(g)):
                    pointer.desktop(55000 + row, True)
                    return
                pointer.desktop(54023, True)
            raise AssertionError("Picker path missing: " + path)

        def review(g, pointer, path):
            pointer.desktop(12013, True)
            assert c.flag(g, "picker12") == 9
            pointer.desktop(54019, True)
            c.key(g, "ctrl", "a")
            c.type_text(g, "/Users/Owner/Downloads")
            c.key(g, "ret")
            pointer.drain()
            select(g, pointer, path)
            pointer.desktop(54011, True)
            assert "M147_NATIVE_MSI_READ_ONLY_PLAN_PASS" in task(g, pointer, 12000)

        def inventory(g, pointer, root):
            pointer.desktop(12208, True)
            entries = f.entries(g)
            installed = sorted((item for item in (A, B) if item in entries),
                               key=lambda item: entries[item]["index"])
            pointer.desktop(12200 + installed.index(root), True)

        def sandbox(g, pointer, root):
            inventory(g, pointer, root)
            if root == A:
                # The legacy 7-Zip UI has the built-in console entry point.
                assert "7-Zip" in task(g, pointer, 12005)
            pointer.desktop(12301, True)
            select(g, pointer, root + "/isolation.exe")
            result = task(g, pointer, 54011)
            identity = "A" if root == A else "B"
            assert "M1410_PRIVATE_APP_" + identity + "_PASS" in result, result

        def record_b(volume):
            return {path: (entry.first, hashlib.sha256(read(volume, path)).hexdigest())
                    for entry in volume.volume.entries if entry.kind == 1
                    and (path := entry.path.decode()).startswith(B + "/")}

        def journal_version(blob):
            return blob[752:784].split(bytes(1), 1)[0]

        def save_log(g, label):
            (out / (label + ".log")).write_text(g.log(), encoding="utf-8")
            report["runs"].append(label)

        try:
            volume = StoppedDisk(disk, lib)
            try:
                volume.put(download, source)
                volume.put(update_path, update_data)
            finally:
                volume.close()

            with start("install-both") as g:
                p = front(g)
                p.desktop(12001, True)
                task(g, p, 12003)
                assert "7-Zip" in task(g, p, 12005)
                review(g, p, download)
                p.desktop(12001, True)
                task(g, p, 12003)
                assert all(root + "/product.bin" in f.entries(g) for root in (A, B))
                save_log(g, "install-both")

            fixtures = build()
            volume = StoppedDisk(disk, lib)
            try:
                initial = hashlib.sha256(read(volume, EXE)).hexdigest()
                assert initial != upgrade["image_sha256"]
                volume.put("/Users/Owner/Downloads/bundle-test.dll", (fixtures / "A/bundle-test.dll").read_bytes())
                for root, identity in [(A, "A"), (B, "B")]:
                    ensure(volume, root + "/System/System32")
                    volume.put(root + DLL, (fixtures / identity / "bundle-test.dll").read_bytes())
                    volume.put(root + "/isolation.exe", (fixtures / "isolation.exe").read_bytes())
                legacy = {}
                for suffix, value, before, _ in registry_effects(read(volume, B + "/product.bin")):
                    if before or not value:
                        continue
                    current = read(volume, PRIVATE + "/" + suffix)
                    key = read(volume, PRIVATE + "/" + suffix.rsplit("/", 1)[0] + "/$key")
                    assert current[1552:] == value
                    owner, tail = suffix.split("/", 1)
                    directory = "/Data/Windows/" + owner + "/Registry/" + tail.rsplit("/", 1)[0]
                    ensure(volume, directory)
                    volume.put(directory + "/$key", key)
                    volume.put(directory + "/" + tail.rsplit("/", 1)[1], current)
                    legacy[suffix] = current
                assert legacy
                paths = [e.path.decode() for e in volume.volume.entries if e.kind
                         and (e.path.decode() == PRIVATE or e.path.decode().startswith(PRIVATE + "/"))]
                for path in sorted(paths, key=len, reverse=True):
                    assert lib.v6_remove(ctypes.byref(volume.volume), path.encode()) == 0
                assert lib.v6_remove(ctypes.byref(volume.volume), GENERATION.encode()) == 0
            finally:
                volume.close()

            with start("migrated-baseline") as g:
                p = front(g)
                sandbox(g, p, A)
                sandbox(g, p, B)
                save_log(g, "migrated-baseline")
            volume = StoppedDisk(disk, lib)
            try:
                assert all(read(volume, PRIVATE + "/" + suffix) == record for suffix, record in legacy.items())
                neighbor = record_b(volume)
                report["migrated_values"] = len(legacy)
            finally:
                volume.close()

            with start("update-a") as g:
                p = front(g)
                review(g, p, update_path)
                p.desktop(12303, True)
                task(g, p, 12003)
                sandbox(g, p, A)
                sandbox(g, p, B)
                save_log(g, "update-a")
            volume = StoppedDisk(disk, lib)
            try:
                assert record_b(volume) == neighbor
                updated = read(volume, A + "/product.bin")
                assert journal_version(updated) == VERSION
                assert hashlib.sha256(read(volume, EXE)).hexdigest() == upgrade["image_sha256"]
                assert read(volume, A + "/.EngacerMSI/source.msi") == update_data
            finally:
                volume.close()

            with start("update-cold") as g:
                p = front(g)
                sandbox(g, p, A)
                sandbox(g, p, B)
                save_log(g, "update-cold")
            volume = StoppedDisk(disk, lib)
            try:
                assert lib.v6_remove(ctypes.byref(volume.volume), EXE.encode()) == 0
            finally:
                volume.close()
            with start("repair-a") as g:
                p = front(g)
                inventory(g, p, A)
                p.desktop(12302, True)
                task(g, p, 12003)
                sandbox(g, p, A)
                sandbox(g, p, B)
                save_log(g, "repair-a")
            volume = StoppedDisk(disk, lib)
            try:
                assert record_b(volume) == neighbor
                assert read(volume, A + "/product.bin") == updated
                assert hashlib.sha256(read(volume, EXE)).hexdigest() == upgrade["image_sha256"]
            finally:
                volume.close()

            with start("repair-cold-remove-a") as g:
                p = front(g)
                sandbox(g, p, A)
                sandbox(g, p, B)
                inventory(g, p, A)
                p.desktop(12002, True)
                task(g, p, 12003)
                assert not any(path == A or path.startswith(A + "/") for path in f.entries(g))
                sandbox(g, p, B)
                save_log(g, "repair-cold-remove-a")
            with start("remove-cold") as g:
                p = front(g)
                sandbox(g, p, B)
                save_log(g, "remove-cold")
            volume = StoppedDisk(disk, lib)
            try:
                assert record_b(volume) == neighbor
                report["neighbor_sha256"] = hashlib.sha256(
                    json.dumps(neighbor, sort_keys=True).encode()).hexdigest()
                report["neighbor_files"] = len(neighbor)
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
