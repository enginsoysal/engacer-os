"""Lossless packet masks and exact Latin glyph residuals; build-time only."""
import unicodedata
from PIL import Image, ImageDraw, ImageFont

CODES = tuple(range(160, 256)) + (0x11e, 0x11f, 0x130, 0x131, 0x15e, 0x15f, 0x20ac)
CODES = tuple(sorted(CODES))


def encode(raw):
    result = bytearray()
    at = 0
    while at < len(raw):
        value = raw[at]
        end = at + 1
        if value in (0, 255):
            limit = 128 if value == 0 else 64
            while end < len(raw) and end - at < limit and raw[end] == value:
                end += 1
            result.append(end - at - 1 if value == 0 else end - at + 127)
        else:
            while end < len(raw) and end - at < 64 and raw[end] not in (0, 255):
                end += 1
            result.append(end - at + 191)
            result.extend(raw[at:end])
        at = end
    return bytes(result)


def decode(raw):
    result = bytearray()
    at = 0
    while at < len(raw):
        token = raw[at]
        at += 1
        if token < 128:
            result.extend(bytes(token + 1))
        elif token < 192:
            result.extend(bytes([255]) * (token - 127))
        else:
            count = token - 191
            if count > len(raw) - at:
                raise ValueError('Truncated glyph literal')
            result.extend(raw[at:at + count])
            at += count
    return bytes(result)


def repack(folder, faces, glyphs, old_data):
    data = bytearray()
    updated = []
    originals = []
    for offset, count, width, height, x, y, advance in glyphs:
        source = old_data[offset:offset + count]
        if len(source) != count or count % 2:
            raise ValueError('Invalid retained glyph run bounds')
        pixels = bytearray()
        for at in range(0, count, 2):
            if not source[at]:
                raise ValueError('Empty retained glyph run')
            pixels.extend(bytes([source[at + 1]]) * source[at])
        if len(pixels) != width * height:
            raise ValueError('Retained glyph pixel count differs')
        originals.append(bytes(pixels))
        packet = encode(pixels)
        assert decode(packet) == pixels
        updated.append((len(data), len(packet), width, height, x, y, advance))
        data.extend(packet)
    ascii_bytes = len(data)
    selected = {face[0]: face for face in faces if face[0] <= 475}
    if tuple(sorted(selected)) != (0, 95, 190, 285, 380, 475):
        raise ValueError('Review the changed ordinary/secondary face layout')
    extras = []
    composites = 0
    for first in sorted(selected):
        _, size, _, _ = selected[first]
        font = ImageFont.truetype(str(folder / 'Inter.ttf'), size)
        font.set_variation_by_axes([min(32, max(14, size)), 400])
        for code in CODES:
            char = chr(code)
            x, y, right, bottom = font.getbbox(char, anchor='ls')
            width, height = right - x, bottom - y
            advance = round(font.getlength(char))
            if not (0 <= width <= 255 and 0 <= height <= 255 and
                    -128 <= x <= 127 and -128 <= y <= 127 and 0 <= advance <= 255):
                raise ValueError('Glyph metrics exceed the retained descriptor')
            canvas = Image.new('L', (max(1, width), max(1, height)))
            ImageDraw.Draw(canvas).text((-x, -y), char, font=font, fill=255, anchor='ls')
            pixels = canvas.tobytes() if width and height else b''
            base_index = 65535
            base_pixels = bytes(len(pixels))
            decomposition = unicodedata.normalize('NFD', char)
            if (len(decomposition) > 1 and 32 <= ord(decomposition[0]) < 127 and
                    all(unicodedata.combining(mark) for mark in decomposition[1:])):
                base_index = first + ord(decomposition[0]) - 32
                _, _, bw, bh, bx, by, _ = glyphs[base_index]
                base = Image.new('L', canvas.size)
                if bw and bh:
                    mask = Image.frombytes('L', (bw, bh), originals[base_index])
                    base.paste(mask, (bx - x, by - y))
                base_pixels = base.tobytes() if width and height else b''
                composites += 1
            residual = bytes(a ^ b for a, b in zip(pixels, base_pixels))
            packet = encode(residual)
            assert bytes(a ^ b for a, b in zip(decode(packet), base_pixels)) == pixels
            descriptor = (len(data), len(packet), width, height, x, y, advance)
            extras.append((code, base_index, descriptor))
            data.extend(packet)
    if len(data) > 1024 * 1024:
        raise ValueError('Packet mask atlas exceeds its static bound')
    report = dict(format='packet-xor146', retained_glyphs=len(updated),
                  extra_glyphs=len(extras), extra_codepoints=list(CODES),
                  extra_faces=[selected[first][1] for first in sorted(selected)],
                  exact_composite_glyphs=composites, retained_pair_bytes=len(old_data),
                  packet_ascii_bytes=ascii_bytes, coverage_bytes=len(data))
    return updated, data, extras, report


def extra_header(extras):
    text = '#define FONT146_PACKET 1\n#define FONT146_CODES ' + str(len(CODES)) + 'u\n'
    text += 'typedef struct {unsigned short codepoint,base;font73_glyph glyph;} font146_extra;\n'
    text += 'static const font146_extra font146_extras[]={'
    text += ','.join('{' + str(code) + ',' + str(base) + ',{' +
                     ','.join(map(str, glyph)) + '}}' for code, base, glyph in extras)
    return text + '};\n'
