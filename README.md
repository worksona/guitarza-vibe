# guitarza-vibe

A Claude Code plugin for [Guitarza](https://guitarza.netlify.app): say what you
want to play, get a link that opens the studio with it loaded.

Two kinds of link, both in the URL fragment so nothing reaches a server:

| link | what it is | example |
| --- | --- | --- |
| **deep link** `#/…` | the address of something in the catalogue | `https://guitarza.netlify.app/#/drums/moeller` |
| **share code** `#gz=…` | a song, groove, play-along or lesson that is *not* — it lives in the URL | `https://guitarza.netlify.app/#gz=XZBNTs…` |

Install from this marketplace, then `/guitarza-vibe` — or just ask:

> "link me the paradiddle" · "a 3-3-2 groove at 96" · "a two-section sheet in D
> with a lift to the vi" · "the 12-bar in E as a shuffle with chord tones showing"

The skill reads the app's own vocabulary (`reference/catalog.json`, generated
from the app's source), authors the smallest document that says what you asked,
encodes it with the bundled codec, decodes its own link to check it, and hands
you the link plus two or three things to ask for next.

```bash
python3 guitarza-vibe/scripts/encode.py song.json --kind song --live          # → a #gz= URL
python3 guitarza-vibe/scripts/encode.py song.json --kind song --live --short  # → an a47l.com short link, then the long one
python3 guitarza-vibe/scripts/encode.py --decode '<url or code>'              # the reverse
```

`--short` needs `SHORTLINK_TOKEN` in the environment (the same variable the
`/shortlink` skill uses); without it the long link is printed and the reason
goes to stderr.

The reference tree is regenerated from the app repo with
`node scripts/vibe-reference.mjs`; the hand-written guides in
`skills/guitarza-vibe/reference/schema-*.md` describe what the tables cannot —
how a grid reads, which chord spellings the voicing engine knows, why a
lesson's strings are numbered from the low E.
