from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ADDRESS_LINE = re.compile(r"^([0-9A-Fa-f]{8}):\s*(.*)$")


def kana_count(text: str) -> int:
    return sum(
        1
        for char in text
        if "\u3040" <= char <= "\u30ff" or "\uff65" <= char <= "\uff9f"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract kana-heavy candidate rows from a GCCODE2 F3 dump"
    )
    parser.add_argument("dump", type=Path, help="GCCODE2 saved text dump")
    parser.add_argument("output", type=Path, help="UTF-8 CSV output path")
    parser.add_argument(
        "--min-kana", type=int, default=8, help="minimum kana characters per row"
    )
    parser.add_argument(
        "--min-density",
        type=float,
        default=0.25,
        help="minimum kana fraction among non-space characters",
    )
    parser.add_argument(
        "--start",
        type=lambda value: int(value, 0),
        help="only include rows at or after this hexadecimal or decimal ROM offset",
    )
    parser.add_argument(
        "--end",
        type=lambda value: int(value, 0),
        help="only include rows before this hexadecimal or decimal ROM offset",
    )
    args = parser.parse_args()

    text = args.dump.read_bytes().decode("cp932", errors="replace")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with args.output.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("offset", "kana_count", "kana_density", "candidate_text"))
        for line in text.splitlines():
            match = ADDRESS_LINE.match(line)
            if not match:
                continue
            offset = int(match.group(1), 16)
            if args.start is not None and offset < args.start:
                continue
            if args.end is not None and offset >= args.end:
                continue
            row_text = match.group(2).strip()
            kana = kana_count(row_text)
            visible = sum(not char.isspace() for char in row_text)
            density = kana / visible if visible else 0.0
            if kana < args.min_kana or density < args.min_density:
                continue
            writer.writerow(
                (f"0x{offset:08X}", kana, f"{density:.3f}", row_text)
            )
            count += 1
    print(f"Wrote {count} candidate rows to {args.output}")


if __name__ == "__main__":
    main()
