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
and translated images have the same size. The site applies an IPS patch in the
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
