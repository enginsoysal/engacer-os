"""Exercise the production generation allocator with a simulated volume."""
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess

source = (Path(__file__).resolve().parents[2] / "kernel/windows8/process.c").read_text()
start = source.index("static unsigned app_generation1410(")
end = source.index("/* Both strings", start)

fixture = r"""
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#define WIN_PRODUCT_BASE147 "/Applications/Windows/"
enum { V6_OK, V6_INVALID, V6_FULL, V6_IO };
typedef struct { unsigned kind, size; } v6_entry;
static v6_entry entry;
static uint64_t disk;
static unsigned damaged, fail_write;
static const char expected[] = "/Data/Windows/InstallGenerations/{app}";
static void copy8(char *out, const char *in, size_t size) {
    snprintf(out, size, "%s", in);
}
static void path_append143(char *out, const char *in, size_t size) {
    size_t used = strlen(out);
    copy8(out + used, in, size - used);
}
static const v6_entry *find8(const char *path) {
    assert(!strcmp(path, expected));
    return entry.kind ? &entry : NULL;
}
static void *m6_volume(void) { return &entry; }
static unsigned v6_verify(void *volume, const char *path) {
    assert(volume == &entry && !strcmp(path, expected));
    return damaged;
}
static unsigned exact8(const char *path, unsigned offset, void *out, unsigned bytes) {
    assert(!strcmp(path, expected) && offset == 0 && bytes == sizeof(disk));
    memcpy(out, &disk, bytes);
    return 0;
}
static unsigned protected_prepare143(const char *path) {
    assert(!strcmp(path, "/Data/Windows/InstallGenerations"));
    return 0;
}
static void memory_source8(void) {}
static unsigned v6_put(void *volume, const char *path, unsigned bytes,
                       void (*source)(void), void *value) {
    assert(volume == &entry && !strcmp(path, expected));
    assert(bytes == sizeof(disk) && source == memory_source8);
    if (fail_write) return V6_IO;
    memcpy(&disk, value, bytes);
    entry = (v6_entry){1, bytes};
    return V6_OK;
}
""" + source[start:end] + r"""
int main(void) {
    const char root[] = WIN_PRODUCT_BASE147 "{app}";
    uint64_t epoch;
    assert(!app_generation1410(root, 0, &epoch) && epoch == 0);
    assert(!app_generation1410(root, 1, &epoch) && epoch == 1);
    assert(!app_generation1410(root, 0, &epoch) && epoch == 1);
    fail_write = 1;
    assert(app_generation1410(root, 1, &epoch) == V6_IO);
    assert(!app_generation1410(root, 0, &epoch) && epoch == 1);
    fail_write = 0;
    assert(!app_generation1410(root, 1, &epoch) && epoch == 2);
    damaged = 1;
    assert(app_generation1410(root, 1, &epoch) == V6_INVALID && disk == 2);
    damaged = 0;
    disk = UINT64_MAX;
    assert(app_generation1410(root, 1, &epoch) == V6_FULL && disk == UINT64_MAX);
    return 0;
}
"""

with TemporaryDirectory() as scratch:
    path = Path(scratch) / "generation.c"
    executable = path.with_suffix(".exe")
    path.write_text(fixture, encoding="utf-8")
    subprocess.run(["clang", "-Wall", "-Wextra", "-Werror", str(path), "-o", str(executable)], check=True)
    subprocess.run([str(executable)], check=True)
print("Installation generation allocation, failed write, corruption and exhaustion passed")
