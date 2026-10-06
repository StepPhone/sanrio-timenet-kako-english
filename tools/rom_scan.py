from __future__ import annotations

import hashlib
import sys
from pathlib import Path


def decode_byte(value: int) -> str:
    """Decode the known portion of the game's one-byte text table."""
    if value <= 0x11:
        return "6789CDeESJLMPrsUVX"[value]
    symbols = {
        0x12: "ﾞ",
        0x13: "ﾟ",
        0x14: "ー",
        0x15: "…",
        0x16: "・",
        0x17: ".",
        0x18: "!",
        0x19: "?",
        0x1A: ":",
        0x1B: "/",
        0x1C: "『",
        0x1D: "❤",
        0x1E: "★",
        0x1F: "▷",
        0x20: " ",
    }
    if value in symbols:
        return symbols[value]
    kana = (
        "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほ"
        "まみむめもやゆよわんらりるれろをゃゅょっ"
        "アイウエオ"
    )
    if 0x91 <= value <= 0xC7:
        return kana[value - 0x91]
    return f"<{value:02X}>"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        raise SystemExit("usage: rom_scan.py ROM")
    path = Path(sys.argv[1])
    data = path.read_bytes()
    print(f"ROM size: {len(data)} bytes")
    print(f"MD5: {hashlib.md5(data).hexdigest()}")
    print(f"Title field: {data[0x134:0x13F].decode('ascii', errors='replace')}")
    print("\nLongest runs from the known Japanese character range:")

    # Candidate strings are short, kana-heavy runs of mapped characters. A
    # permissive scan across all low bytes produces many false positives in
    # graphics and lookup tables, so zero-filled gaps split runs here.
    valid = set(range(0x00, 0x21)) | set(range(0x91, 0xC8))
    runs: list[tuple[int, bytes]] = []
    start: int | None = None
    zero_run = 0
    for index, value in enumerate(data + b"\xff"):
        if value in valid:
            zero_run = zero_run + 1 if value == 0 else 0
            if zero_run >= 3:
                if start is not None:
                    chunk = data[start:index - 2]
                    kana = sum(0x91 <= byte <= 0xC7 for byte in chunk)
                    if 8 <= len(chunk) <= 200 and kana >= 4 and kana / len(chunk) >= 0.3:
                        runs.append((start, chunk))
                start = None
                continue
            if start is None:
                start = index
        elif start is not None:
            chunk = data[start:index]
            kana = sum(0x91 <= byte <= 0xC7 for byte in chunk)
            if 8 <= len(chunk) <= 200 and kana >= 4 and kana / len(chunk) >= 0.3:
                runs.append((start, chunk))
            start = None
            zero_run = 0

    runs.sort(key=lambda row: (-len(row[1]), row[0]))
    for offset, chunk in runs[:160]:
        text = "".join(decode_byte(byte) for byte in chunk)
        print(f"{offset:06X} [{len(chunk):3}]  {text}")

    print(f"\nKana-heavy candidate runs: {len(runs)}")
    print("\nMost common mapped-byte values:")
    from collections import Counter

    counts = Counter(data)
    print(" ".join(f"{value:02X}:{counts[value]}" for value in range(0x91, 0xC8)))


if __name__ == "__main__":
    main()
