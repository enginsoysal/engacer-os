"""Collect repeatable Windows observations using test-owned files and API requests."""
import ctypes
import hashlib
import json
import platform
import struct
import sys
import tempfile
from ctypes import wintypes
from pathlib import Path

kernel = ctypes.WinDLL("kernel32", use_last_error=True)
load = kernel.LoadLibraryExW
load.argtypes = (wintypes.LPCWSTR, wintypes.HANDLE, wintypes.DWORD)
load.restype = wintypes.HMODULE
free = kernel.FreeLibrary
free.argtypes = (wintypes.HMODULE,)
free.restype = wintypes.BOOL


def collect():
    with tempfile.TemporaryDirectory(prefix="engacer-reference-") as directory:
        root = Path(directory)
        absent = root / "absent.dll"
        invalid = root / "invalid.dll"
        invalid.write_bytes(b"Engacer owned invalid image\n")
        cases = {}
        for name, path in (("absent_image", absent), ("invalid_image", invalid)):
            ctypes.set_last_error(0)
            handle = load(str(path), None, 0)
            error = ctypes.get_last_error()
            if handle:
                free(handle)
            cases[name] = {"loaded": bool(handle), "last_error": error}
        fixture = root / "MiXeD.txt"
        fixture.write_bytes(b"reference")
        cases["case_lookup"] = {"alternate_case_read": (root / "mixed.txt").is_file()}
    version = sys.getwindowsversion()
    return {
        "system": list(version.platform_version),
        "reported_version": [version.major, version.minor, version.build],
        "machine": platform.machine(),
        "process_bits": struct.calcsize("P") * 8,
        "python": platform.python_version(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "cases": cases,
    }


if __name__ == "__main__":
    print(json.dumps(collect(), indent=2))
