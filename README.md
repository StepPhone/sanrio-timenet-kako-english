# Sanrio Timenet: Kako Hen — English Translation

An English fan-translation project for the Japanese Game Boy Color release of
*Sanrio Timenet: Kako Hen* (Past Edition).

## Status

The supported Rev 1 ROM is identified, and GCCODE2 has confirmed Japanese text
in the ROM, including dialogue and the opening story recap. The full script and
its control markers still need to be extracted and checked. Research on the
related Future Edition suggests the font may lack a complete English alphabet;
the target ROM's glyphs still need to be mapped. No playable patch is released
yet.
The `docs/` folder is configured for GitHub Pages and includes a client-side
patching page that can apply the IPS release when one is available.

## Supported source ROM

The ROM supplied for this project is 1 MiB and has MD5
`4505fd4df8eb721cf2f5b5be93682874` and SHA-256
`d341925328066ac8bb90b6886c7366ebd61af6b1a341e1bad350127cf3edfa4c`. This is
the only revision currently identified. Keep your own legally obtained ROM; do
not commit or publish it.

## Patch format

The intended release format is IPS. Once an English ROM build is available,
create a patch without distributing either ROM:

```powershell
python tools/create_ips_patch.py "clean Japanese.gbc" "translated.gbc" `
  docs/patches/kako-english.ips
```

The script accepts the known source revision only and checks that the original
and translated images have the same size. It recalculates the Game Boy header
checksums before creating the patch. The site applies an IPS patch in the
browser; the ROM file stays on the user's device.

To make a review CSV from a GCCODE2 F3 dump, narrow it to a region first; a
whole-ROM dump includes graphics and other binary data:

```powershell
python tools/parse_gccode_dump.py work/kako-b0-dump.txt work/candidates.csv `
  --start 0x8F600 --end 0x90000
```

## GitHub Pages

The site source is in `docs/`. The workflow at
`.github/workflows/pages.yml` deploys it from GitHub Actions. In the GitHub
repository settings, set **Pages → Build and deployment → Source** to **GitHub
Actions**.

## Project files

- `tools/rom_scan.py` — experimental raw-byte scanner; its output is only
  candidate text and is not a verified script dump.
- `tools/parse_gccode_dump.py` — extracts kana-heavy candidate rows from a
  GCCODE2 F3 dump for review; it does not certify that a row is dialogue.
- `tools/create_ips_patch.py` — builds an IPS patch from the clean ROM and an
  English build.
- `docs/` — GitHub Pages site and eventual patch download.

## Text-extraction research

Confirmed offsets, sample decoding, and remaining encoding questions are
recorded in [docs/research.md](docs/research.md).

The publicly available [character table](https://datacrystal.tcrf.net/wiki/Sanrio_Timenet:_Kako_Hen_and_Mirai_Hen/TBL)
is an incomplete draft for the original Kako Hen release, not this Rev 1 ROM.
It is not sufficient to identify every dialogue character or control marker.
Direct byte scans also match graphics and lookup data, so those results are not
safe to translate as dialogue without checking their context.

Community notes describe building a custom table and using
[GCCODE2](https://i486.mods.jp/ichild/get-character-code-type-ii-gccode2) to
extract text. The available [dialogue-offset analysis](https://tetuhatoplus03game.blogspot.com/2024/08/blog-post_28.html)
covers Mirai Hen (Future Edition); its offsets have not been confirmed for
Kako Hen Rev 1. These are research leads, not a verified script dump. The
project will publish a patch after the Japanese text, English replacements,
and resulting game data can be checked against the supported ROM.
