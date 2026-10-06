from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


EXPECTED_BASE_MD5 = "4505fd4df8eb721cf2f5b5be93682874"
MAX_RECORD_LENGTH = 0xFFFF
MAX_OFFSET = 0xFFFFFF


def md5(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


def fix_game_boy_checksums(rom: bytes) -> bytes:
    if len(rom) < 0x150:
        raise ValueError("File is too small to contain a Game Boy ROM header")
    fixed = bytearray(rom)
    header_checksum = 0
    for value in fixed[0x134:0x14D]:
        header_checksum = (header_checksum - value - 1) & 0xFF
    fixed[0x14D] = header_checksum

    global_checksum = sum(fixed[:0x14E]) + sum(fixed[0x150:])
    fixed[0x14E:0x150] = (global_checksum & 0xFFFF).to_bytes(2, "big")
    return bytes(fixed)


def make_ips(original: bytes, translated: bytes) -> bytes:
    if len(original) != len(translated):
        raise ValueError("IPS build requires source and translated ROMs of equal size")

    out = bytearray(b"PATCH")
    pos = 0
    limit = len(original)
    while pos < limit:
        if original[pos] == translated[pos]:
            pos += 1
            continue

        start = pos
        pos += 1
        while (
            pos < limit
            and translated[pos] != original[pos]
            and pos - start < MAX_RECORD_LENGTH
        ):
            pos += 1

        if start > MAX_OFFSET:
            raise ValueError(f"IPS cannot represent changed offset 0x{start:X}")
        payload = translated[start:pos]
        out.extend(start.to_bytes(3, "big"))
        out.extend(len(payload).to_bytes(2, "big"))
        out.extend(payload)

    out.extend(b"EOF")
    return bytes(out)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an IPS patch for Kako Hen")
    parser.add_argument("original", type=Path, help="clean Japanese .gbc ROM")
    parser.add_argument("translated", type=Path, help="English build .gbc ROM")
    parser.add_argument("output", type=Path, help="output .ips path")
    args = parser.parse_args()

    original = args.original.read_bytes()
    translated = fix_game_boy_checksums(args.translated.read_bytes())
    actual_md5 = md5(original)
    if actual_md5 != EXPECTED_BASE_MD5:
        raise SystemExit(
            "Unsupported source ROM. Expected MD5 "
            f"{EXPECTED_BASE_MD5}; found {actual_md5}."
        )
    if original == translated:
        raise SystemExit("The English build is identical to the source; refusing to create a no-op patch.")

    patch = make_ips(original, translated)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(patch)
    print(f"Wrote {args.output} ({len(patch)} bytes)")


if __name__ == "__main__":
    main()
