# Sanrio Timenet: Kako Hen — English Translation

An English fan-translation project for the Japanese Game Boy Color release of
*Sanrio Timenet: Kako Hen* (Past Edition).

## Status

The ROM has been identified, but the game text has not yet been reliably
extracted. The available character table is an incomplete draft and produces
false matches in graphics and lookup data. No English patch is released yet.
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

## GitHub Pages

The site source is in `docs/`. The workflow at
`.github/workflows/pages.yml` deploys it from GitHub Actions. In the GitHub
repository settings, set **Pages → Build and deployment → Source** to **GitHub
Actions**.

## Project files

- `tools/rom_scan.py` — exploratory scanner for the known portion of the
  game's text table; results are candidates, not a verified script dump.
- `tools/create_ips_patch.py` — builds an IPS patch from the clean ROM and an
  English build.
- `docs/` — GitHub Pages site and eventual patch download.

## Text-extraction research

The publicly available [character table](https://datacrystal.tcrf.net/wiki/Sanrio_Timenet:_Kako_Hen_and_Mirai_Hen/TBL)
is an incomplete draft for the original Kako Hen release, not this Rev 1 ROM.
It is not sufficient to identify every dialogue character. Direct byte scans
also match graphics and lookup data, so those results are not safe to translate
as dialogue.

Community notes describe building a custom table and using
[GCCODE2](https://i486.mods.jp/ichild/get-character-code-type-ii-gccode2) to
extract text. The available [dialogue-offset analysis](https://tetuhatoplus03game.blogspot.com/2024/08/blog-post_28.html)
covers Mirai Hen (Future Edition); its offsets have not been confirmed for
Kako Hen Rev 1. These are research leads, not a verified script dump. The
project will publish a patch after the Japanese text, English replacements,
and resulting game data can be checked against the supported ROM.
