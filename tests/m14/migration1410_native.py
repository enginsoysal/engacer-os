"""Seed an interrupted legacy registry migration on an owned stopped disk."""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import struct
import sys
import traceback

import replay7
from private1410_native import A, B

ROOT = Path(__file__).resolve().parents[2]
TEST_ROOT = ROOT / "build/m14-native/stage10"
USER = "/Users/Owner"
PRIVATE = B + "/.Engacer/Registry"
STAGE = B + "/.Engacer/Migration"
GENERATION = "/Data/Windows/InstallGenerations/" + B.rsplit("/", 1)[-1]


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()[:32]


def registry_effects(journal):
    at = 1024
    while at < len(journal):
        kind, length = struct.unpack_from("<II", journal, at)
        assert length >= 8 and length % 8 == 0 and at + length <= len(journal)
        if kind == 2:
            root, view, _, _, size, _, key_size, name_size, before, _ = struct.unpack_from("<10I", journal, at + 8)
            start = at + 48
            key = journal[start:start + key_size - 1].decode().lower()
            start += key_size
            name = journal[start:start + name_size - 1].decode().lower()
            start += name_size
            principal = USER if root == 1 else "/Machine/" + str(view)
            suffix = digest(principal) + "/k" + digest(key) + "/v" + digest(name)
            yield suffix, journal[start:start + size], before, journal[at:at + length]
        at += length


def read(mounted, path):
    entry = next(e for e in mounted.volume.entries if e.kind == 1 and e.path == path.encode())
    assert mounted.lib.v6_verify(ctypes.byref(mounted.volume), entry.path) == 0
    mounted.file.seek(mounted.offset + entry.first * 4096)
    return mounted.file.read(entry.size)


def ensure(mounted, path):
    volume = ctypes.byref(mounted.volume)
    parts = path.split("/")[1:]
    directories = {e.path.decode() for e in mounted.volume.entries if e.kind == 2}
    directory = ""
    for part in parts:
        directory += "/" + part
        if directory not in directories:
            assert mounted.lib.v6_mkdir(volume, directory.encode()) == 0


def main():
    replay7.REPLACEMENTS += [("EngacerOS-M14STAGE7", "EngacerOS-M14STAGE10"),
                             ("m14stage7", "m14stage10")]
    loader = replay7.ReplayLoader()
    sys.meta_path.insert(0, loader)
    try:
        from window144_native import ui, c, f, t, clone, StoppedDisk, task
        from fixture1 import library

        meta = json.loads(ui.manifest_path12().read_text())
        earlier = json.loads((TEST_ROOT / "private-ab/results.json").read_text())
        assert earlier["passed"] and earlier["build_id"] == meta["build_id"]
        source = Path(os.environ["LOCALAPPDATA"]) / "EngineOS/Tests/M6/m1410-private-ab" / earlier["owned_fixture"] / "owned.img"
        work, disk, _ = clone(ui, source, "m1410-migration")
        lib = library(["remove"])
        out = TEST_ROOT / "migration"
        out.mkdir(parents=True, exist_ok=True)
        c.OUT = out
        report = {"passed": False, "build_id": meta["build_id"],
                  "source_commit": meta["source_commit"], "owned_fixture": work.name,
                  "observer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
        try:
            volume = StoppedDisk(disk, lib)
            try:
                journal = read(volume, B + "/product.bin")
                digest_expected = hashlib.sha256(journal[:72] + bytes(32) + journal[104:]).digest()
                assert journal[72:104] == digest_expected
                selected = [(suffix, payload, effect) for suffix, payload, before, effect
                            in registry_effects(journal) if not before and payload]
                assert len(selected) >= 3
                # Preserve A's product/principal binding while giving its checked
                # ownership journal one competing claim on B's legacy value.
                rival = bytearray(read(volume, A + "/product.bin"))
                assert rival[72:104] == hashlib.sha256(rival[:72] + bytes(32) + rival[104:]).digest()
                rival += selected[2][2]
                struct.pack_into("<I", rival, 12, len(rival))
                for field in (16, 24):
                    struct.pack_into("<I", rival, field, struct.unpack_from("<I", rival, field)[0] + 1)
                rival[72:104] = hashlib.sha256(rival[:72] + bytes(32) + rival[104:]).digest()
                volume.put(A + "/product.bin", bytes(rival))
                original = {}
                for index, (suffix, payload, _) in enumerate(selected):
                    record = read(volume, PRIVATE + "/" + suffix)
                    assert record[1552:] == payload
                    principal, tail = suffix.split("/", 1)
                    legacy = "/Data/Windows/" + principal + "/Registry/" + tail
                    ensure(volume, legacy.rsplit("/", 1)[0])
                    if index == 1:
                        record = record[:1552] + bytes([record[1552] ^ 1]) + record[1553:]
                    original[suffix] = (legacy, record)
                    volume.put(legacy, record)
                api = ctypes.byref(volume.volume)
                old_paths = [e.path.decode() for e in volume.volume.entries
                             if e.kind and (e.path.decode() == PRIVATE or e.path.decode().startswith(PRIVATE + "/"))]
                for path in sorted(old_paths, key=len, reverse=True):
                    assert lib.v6_remove(api, path.encode()) == 0
                assert lib.v6_remove(api, GENERATION.encode()) == 0
                ensure(volume, STAGE + "/unfinished")
                volume.put(STAGE + "/unfinished/stale", b"Interruption before private registry publication")
            finally:
                volume.close()

            for index in range(2):
                boot = ui.guest(work / ("start-" + str(index)), disk, media="installed", ready="M7_DESKTOP_READY", ram=128)
                ui.s.normal_boot(boot)
                with boot as g:
                    pointer = ui.Pointer(g)
                    pointer.drain()
                    c.key(g, "esc")
                    t.close_all(g, pointer)
                    t.launch(g, pointer, "windows apps", 19)
                    pointer.desktop(12208, True)
                    entries = f.entries(g)
                    roots = [p for p in entries if p.startswith("/Applications/Windows/{") and p.count("/") == 3]
                    roots.sort(key=lambda p: entries[p]["index"])
                    pointer.desktop(12200 + roots.index(B), True)
                    pointer.desktop(12301, True)
                    row = f.entries(g)[B + "/isolation.exe"]["index"]
                    for _ in range(128):
                        if any(control[5] == 55000 + row for control in f.controls(g)):
                            break
                        pointer.desktop(54023, True)
                    pointer.desktop(55000 + row, True)
                    assert "M1410_PRIVATE_APP_B_PASS" in task(g, pointer, 54011)
                    (out / ("serial-" + str(index) + ".log")).write_text(g.log(), encoding="utf-8")

                volume = StoppedDisk(disk, lib)
                try:
                    names = {e.path.decode() for e in volume.volume.entries if e.kind}
                    assert not any(path == STAGE or path.startswith(STAGE + "/") for path in names)
                    assert read(volume, PRIVATE + "/$legacy-migration") == digest_expected
                    for entry_index, (suffix, (legacy, record)) in enumerate(original.items()):
                        assert read(volume, legacy) == record
                        if entry_index in (1, 2):
                            assert PRIVATE + "/" + suffix not in names
                        else:
                            assert read(volume, PRIVATE + "/" + suffix) == record
                finally:
                    volume.close()

            report.update(passed=True, interrupted_state="staged and unpublished",
                          original_values_preserved=len(original),
                          migrated_values=len(original)-2, changed_values_skipped=1,
                          competing_values_skipped=1,
                          independent_disk_starts=2, receipt_sha256=digest_expected.hex())
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
