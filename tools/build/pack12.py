"""Original bounded LZ4 block encoder for independent 4096-byte install pages.

No dictionary survives a page. Legacy raw/zero records remain valid; only M12
opts into compressed records. The decoder validates the whole page before I/O.
"""
import struct


def compress(page):
    assert len(page) == 4096
    out = bytearray(); matches = {}; anchor = i = 0
    def length(n):
        while n >= 255: out.append(255); n -= 255
        out.append(n)
    while i + 4 <= len(page):
        key = page[i:i+4]; old = matches.get(key); matches[key] = i
        if old is None: i += 1; continue
        end = i + 4
        while end < len(page) and page[old + end-i] == page[end]: end += 1
        literals = i-anchor; count = end-i-4
        out.append((min(literals,15)<<4)|min(count,15))
        if literals >= 15: length(literals-15)
        out.extend(page[anchor:i]); out.extend(struct.pack('<H',i-old))
        if count >= 15: length(count-15)
        i = anchor = end
    literals = len(page)-anchor
    out.append(min(literals,15)<<4)
    if literals >= 15: length(literals-15)
    out.extend(page[anchor:])
    return bytes(out)


def record(lba, page):
    assert lba < 0x40000000 and len(page) == 4096
    if not any(page): return struct.pack('<I',lba|0x80000000)
    data = compress(page)
    if len(data)+2 < 4096:
        return struct.pack('<IH',lba|0x40000000,len(data))+data
    return struct.pack('<I',lba)+page
