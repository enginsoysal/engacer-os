"""Retain the parser corpus and verify the actual original helper templates."""
import ctypes as c
import hashlib
import json
import os
import struct
from pathlib import Path
import dialog145_host as retained
from resource144_host import mapped, entries

ROOT = Path(__file__).resolve().parents[2]


def main():
    retained.main()
    out = ROOT / 'build/m14-native/stage6/dialog-host'
    helper = Path(os.environ['LOCALAPPDATA']) / 'EngacerOS/Research/M14/0/7zip/_7zG.exe'
    digest = hashlib.sha256(helper.read_bytes()).hexdigest()
    assert digest == '5eb5d21003927be4d53401b9b6bbe8a787caabb38eaafaf0d429a136d7031621'
    image, directory, _ = mapped(helper)
    lib = c.CDLL(str(out / 'dialog.dll'))
    lib.inspect145.argtypes = [c.c_void_p, c.c_uint32, c.POINTER(c.c_uint64), c.c_uint32]
    lib.inspect145.restype = c.c_uint32
    results = []
    for kind, names in entries(image, directory, 0):
        if kind != 5:
            continue
        for name, languages in entries(image, directory, names & 0x7fffffff):
            for language, record in entries(image, directory, languages & 0x7fffffff):
                at, size = struct.unpack_from('<II', image, directory + record)
                raw = bytes(image[at:at + size])
                source = c.create_string_buffer(raw)
                storage = (c.c_uint64 * 1602)()
                marker = 0x93f17a218a4cb920
                storage[0] = storage[1601] = marker
                status = lib.inspect145(source, size, c.cast(c.byref(storage, 8), c.POINTER(c.c_uint64)), 1600)
                assert storage[0] == storage[1601] == marker
                assert status == 0, (name, language, status)
                results.append(dict(resource=name, language=language, controls=storage[2],
                                    sha256=hashlib.sha256(raw).hexdigest()))
    assert any(row['resource'] == 4000 and row['controls'] == 50 for row in results)
    path = out / 'results.json'
    report = json.loads(path.read_text())
    assert report['passed'] and report['control_quota'] == 127
    report['original_helper_sha256'] = digest
    report['original_helper_templates'] = results
    report['helper_observer_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    path.write_bytes((json.dumps(report, indent=2) + '\n').encode())
    print('PASS original helper templates:', len(results), '; Add to Archive: 50 controls')


if __name__ == '__main__':
    main()
