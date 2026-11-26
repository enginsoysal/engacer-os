"""Migrate the reviewed EXE effects from the accepted M14.8 disk fixture."""
import hashlib
import json
import os
from pathlib import Path
import sys

import replay7
from migration1410_native import digest, ensure, read
from private1410_build import build

ROOT = Path(__file__).resolve().parents[2]
SUITE = ROOT / "build/m14-native/stage10"
CODE = "{D6E9EC8F-75FD-5D1F-8990-8DE725154FFF}"
PRODUCT = "/Applications/Windows/" + CODE
PRIVATE = PRODUCT + "/.Engacer/Registry"
OWNER = digest("/Users/Owner")
LEGACY = "/Data/Windows/" + OWNER
RECORD = LEGACY + "/EXE/" + CODE + ".bin"
CLAIMS = [
    ("software\\classes\\.pdf", "content type", "application/pdf\0"),
    ("software\\classes\\mime\\database\\content type\\application/pdf", "extension", ".pdf\0"),
]


def main():
    replay7.REPLACEMENTS += [("EngacerOS-M14STAGE7", "EngacerOS-M14STAGE10"),
                             ("m14stage7", "m14stage10")]
    loader = replay7.ReplayLoader()
    sys.meta_path.insert(0, loader)
    try:
        from window144_native import ui, c, f, t, clone, StoppedDisk, task
        from fixture1 import library

        out = SUITE / "exe-migration"
        out.mkdir(parents=True, exist_ok=True)
        c.OUT = out
        meta = json.loads(ui.manifest_path12().read_text())
        smoke = json.loads((SUITE / "compact/results.json").read_text())
        assert smoke["passed"] and smoke["build_id"] == meta["build_id"]
        home = Path(os.environ["LOCALAPPDATA"]) / "EngineOS/Tests/M6"
        accepted = json.loads((ROOT / "evidence/M14/8/exe-chain-native/results.json").read_text())
        legacy = home / "m148-ordinary-exe-chain" / accepted["owned_fixture"] / "owned.img"
        blank = home / "m141-stage10-compact" / smoke["owned_fixture"] / "owned.img"
        legacy_work, legacy_clone, legacy_hash = clone(ui, legacy, "m1410-legacy-exe-input")
        work, disk, _ = clone(ui, blank, "m1410-exe-migration")
        report = {"passed": False, "build_id": meta["build_id"],
                  "source_commit": meta["source_commit"], "owned_fixture": work.name,
                  "legacy_build": accepted["build_id"], "legacy_input_sha256": legacy_hash["source_sha256"]}
        lib = library()
        source = StoppedDisk(legacy_clone, lib)
        fixture_dir = build()
        try:
            owner_record = read(source, RECORD)
            assert int.from_bytes(owner_record[16:20], "little") == 2
            committed = hashlib.sha256(owner_record[:56] + bytes(32) + owner_record[88:]).digest()
            assert owner_record[56:88] == committed
            values = {}
            for key, name, expected in CLAIMS:
                leaf = "k" + digest(key) + "/v" + digest(name)
                raw = read(source, LEGACY + "/Registry/" + leaf)
                assert raw[1552:].decode("utf-16-le") == expected
                values[leaf] = raw
            prefix = LEGACY + "/Registry/"
            additional = next(e.path.decode()[len(prefix):] for e in source.volume.entries
                              if e.kind == 1 and e.path.decode().startswith(prefix)
                              and e.path.decode().rsplit("/", 1)[-1].startswith("v")
                              and e.path.decode()[len(prefix):] not in values)
            unknown = read(source, prefix + additional)
            target = StoppedDisk(disk, lib)
            try:
                payloads = ("SumatraPDF.exe", "libmupdf.dll", "PdfFilter.dll", "PdfPreview.dll")
                ensure(target, PRODUCT + "/System/System32")
                for name in payloads:
                    target.put(PRODUCT + "/" + name, read(source, PRODUCT + "/" + name))
                target.put(PRODUCT + "/isolation.exe", (fixture_dir / "isolation.exe").read_bytes())
                target.put(PRODUCT + "/System/System32/bundle-test.dll",
                           (fixture_dir / "B/bundle-test.dll").read_bytes())
                ensure(target, RECORD.rsplit("/", 1)[0])
                target.put(RECORD, owner_record)
                for leaf, raw in {**values, additional: unknown}.items():
                    path = prefix + leaf
                    ensure(target, path.rsplit("/", 1)[0])
                    target.put(path, raw)
            finally:
                target.close()
        finally:
            source.close()

        boot = ui.guest(work / "start", disk, media="installed", ready="M7_DESKTOP_READY", ram=128)
        ui.s.normal_boot(boot)
        with boot as g:
            pointer = ui.Pointer(g)
            pointer.drain()
            c.key(g, "esc")
            t.close_all(g, pointer)
            t.launch(g, pointer, "windows apps", 19)
            pointer.desktop(12208, True)
            pointer.desktop(12300, True)
            pointer.desktop(12301, True)
            row = f.entries(g)[PRODUCT + "/isolation.exe"]["index"]
            for _ in range(128):
                if any(item[5] == 55000 + row for item in f.controls(g)):
                    break
                pointer.desktop(54023, True)
            pointer.desktop(55000 + row, True)
            assert "M1410_PRIVATE_APP_B_PASS" in task(g, pointer, 54011)
            (out / "serial.log").write_text(g.log(), encoding="utf-8")

        target = StoppedDisk(disk, lib)
        try:
            assert read(target, PRIVATE + "/$legacy-migration") == committed
            assert read(target, RECORD) == owner_record
            for leaf, raw in values.items():
                assert read(target, PRIVATE + "/" + OWNER + "/" + leaf) == raw
                assert read(target, prefix + leaf) == raw
            assert read(target, prefix + additional) == unknown
            assert not any(e.kind and e.path.decode() == PRIVATE + "/" + OWNER + "/" + additional
                           for e in target.volume.entries)
        finally:
            target.close()
        report.update(passed=True, migrated_values=len(values), unattributed_values_preserved=1,
                      receipt_sha256=committed.hex())
        (out / "results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2), flush=True)
    finally:
        sys.meta_path.remove(loader)


if __name__ == "__main__":
    main()
