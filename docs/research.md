# Text extraction notes

## Confirmed findings

- The target ROM is the 1 MiB Japanese Rev 1 image documented in the README.
- GCCODE2's relative search for `ﾀｽｹﾃｰﾎｼｲﾉ` returned two candidates. The saved
  conversion dump shows `たすけてーほしいの` at `0x8F665`; this is a useful
  dialogue lead, but surrounding marker bytes still need decoding.
- Repeating that search in GCCODE2 with the ROM loaded, difference `B0`, and
  **Byte Search** returns two hits at `0x8F665` and `0x8F841`. Double-clicking
  the first hit jumps to the passage. A B0 F3 dump contains a legible kana
  fragment there; nearby rows also include control markers and non-dialogue
  text, so they still need review.
- GCCODE2's **Create difference kana TBL** button saves a sequential `00`–`FF`
  template. It does not fill the character mapping; the glyph assignments
  must be added before loading that file as a useful table.
- A second region around `0x89640` contains the opening story recap. The bytes
  at `0x8964F` decode as `たすけをもとめる` (“asking for help”) with the table
  mapping used by this region.
- The public Data Crystal table is explicitly marked as an incomplete draft
  for an earlier ROM revision. Its known kana mapping helps interpret some
  bytes, but the whole table and its control codes have not been confirmed for
  Rev 1.

## Translation sample

The opening recap's first sentence is partially represented in the ROM near
`0x89640`. The bytes at `0x8964F` are a confirmed fragment: `たすけをもとめる`
(“asking for help”). Reading the surrounding line alongside the community
story-recap reference gives the provisional sentence “I received a message
asking for help from an old man inside the computer.” The opening phrase
contains codes that are not yet identified, so the full sentence remains
provisional.

The draft translation ledger is [opening-dialogue.csv](translation-data/opening-dialogue.csv).

## Repeatable GCCODE2 search

1. Press **F1** and select the supported ROM.
2. Leave **Use table file** unchecked, keep **1 byte** and addition selected,
   set **Difference (hex)** to `B0`, and search for the halfwidth string
   `ﾀｽｹﾃｰﾎｼｲﾉ` with **Byte Search**.
3. The two results are at `0x8F665` and `0x8F841`. Double-click the first to
   jump to the matching text.
4. Press **F3** to save a full-ROM dump. The dump also contains graphics and
   other binary data; use it as a source for review, not as a finished script.

## Remaining work before a playable patch

1. Identify each text encoding and separate dialogue from names, variables,
   graphics, and other binary data.
2. Decode the message-control markers and locate the text pointers.
3. Map the target game's font. Community analysis of the related Future Edition
   reports that its in-game font does not include the full A–Z alphabet; check
   this against the target ROM and add missing glyphs if needed.
4. Translate and reinsert the text, then check it in an emulator before
   building and releasing an IPS patch.

## References

- [Data Crystal character table](https://datacrystal.tcrf.net/wiki/Sanrio_Timenet:_Kako_Hen_and_Mirai_Hen/TBL)
- [Community story-recap transcript](https://wikiwiki.jp/timenet/%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AA%E3%83%BC%E5%9B%9E%E6%83%B3) — the page notes that its recap is for Mirai Hen and may differ from Kako Hen.
- [Community font-table analysis](https://note.com/tetuhatoch810/n/n69a66ad169f7) — covers Mirai Hen and is a research lead, not a verified Rev 1 font map.
- [GCCODE2 text-converter information](https://i486.mods.jp/ichild/get-character-code-type-ii-gccode2)
