# `groove` — a drum groove or rudiment, written as a grid

The app derives everything from the grid: the score (percussion clef, accents,
ghost parentheses, grace notes, tremolo marks), the kit diagram, the beat-by-beat
walkthrough, the stroke row, and the audio. You write rows; it does the rest.

Ids, pieces, cells and enums are in `catalog.json` — this guide is how to read
and write the grid, not a second copy of those lists.

## The document

```json
{
  "id": "tresillo",
  "name": "Tresillo",
  "subtitle": "3-3-2 on the kick, hats straight",
  "kind": "groove",
  "level": "Intermediate",
  "tempo": 96,
  "timeSignature": [4, 4],
  "stepValue": 8,
  "lanes": [
    { "piece": "hatClosed", "pattern": "X-x-X-x-" },
    { "piece": "snare",     "pattern": "----X---" },
    { "piece": "kick",      "pattern": "x--x--x-" }
  ],
  "sticking": "R-R-R-R-",
  "intro": "The kick divides eight into three, three and two.",
  "coach": [
    "Beat 1 — kick on the one.",
    "Beat 2 — kick on the and of two: the second three.",
    "Beat 3 — the snare lands, kick waits.",
    "Beat 4 — kick on four closes the two."
  ],
  "theory": [{ "heading": "Why 3-3-2", "body": "Eight eighths split unevenly…" }]
}
```

| field | required | notes |
| --- | --- | --- |
| `id` | yes | lowercase, digits, hyphens; namespaced `shared-…` on load |
| `name`, `subtitle` | name yes | subtitle is the card's one line |
| `kind` | yes | `groove` (a part a band hears) or `rudiment` (what the hands do) |
| `family` | rudiments | `stroke` · `diddle` · `grace` · `colour` · `kit` — groups the card |
| `level` | yes | `Beginner` · `Intermediate` · `Advanced` |
| `tempo` | yes | bpm |
| `timeSignature` | yes | `[4,4]` or `[12,8]` are the two the catalogue uses |
| `stepValue` | yes | what one column is worth: `8` an eighth, `16` a sixteenth |
| `lanes` | yes | top row first, as a drummer writes it; every pattern the same length |
| `sticking` | optional | one character per column: `R`, `L`, or `-` |
| `intro`, `coach`, `theory` | coach yes | coach is **one line per beat** — 4 for 4/4, 4 for 12/8 (it counts dotted quarters) |

## Grid width — the rule that refuses most documents

`columns = beats × (columns per beat)`:

| time | stepValue | columns | one beat is |
| --- | --- | --- | --- |
| 4/4 | 8 | **8** | 2 columns |
| 4/4 | 16 | **16** | 4 columns |
| 12/8 | 8 | **12** | 3 columns (triplet feel — shuffles, Moeller, double paradiddle) |

Every lane must be exactly that long. A lane that never sounds (`--------`) is
refused: do not list a drum you do not play.

## Cells — how the stick lands, not just when

| char | mark | plays at | notation |
| --- | --- | --- | --- |
| `-` | nothing | — | rest |
| `x` | tap | the passage level (mp) | plain note |
| `X` | accent | louder | `>` over the note |
| `o` | ghost note | much quieter, felt not heard | parenthesised head |
| `f` | flam | one grace note 26 ms ahead, other hand | grace note |
| `d` | drag | two grace notes, a crushed double ahead | two grace notes |
| `z` | buzz | one stroke let bounce — 8 strokes decaying across the note | tremolo marks |

Accents and ghosts are **per drum**: a ghosted snare under an accented hat in the
same column plays at two different volumes. That is the point of the ghost-note
study; use it.

## Sticking and the stroke row

`sticking` says which hand plays each column. It is what turns a pattern into a
technique — two drummers can play identical notes with different sticking and
only one of them will manage it at speed.

- A letter may sit under a column **only where a hand piece sounds** (`snare`,
  `hatClosed`, toms, cymbals — not `kick` or `hatPedal`). `-` elsewhere.
- The reverse is allowed: a column a hand strikes may carry `-`. In a groove the
  row typically tracks *one* hand (the snare hand through a ghost-note study; the
  hat arm through a Moeller study) while the other rides.
- The app derives the **stroke row** — Down / Tap / Up / Full — from the accents
  and the sticking: loud-then-quiet is a down stroke, quiet-then-loud an up
  stroke. `XooXoo` on one hand reads `D T U D T U`, which *is* the Moeller whip.
  Never author strokes; author accents and hands and let it fall out.

## Kit pieces

Twelve, by id — `kick snare sideStick hatClosed hatPedal hatOpen tomHigh tomMid
tomFloor crash ride rideBell` (see `catalog.json` `enums.kitPiece` for names and
limbs). `hatOpen`/`hatClosed` are one piece of metal; `sideStick` is the snare
played as a click.

## Vibe → grid

| words | do |
| --- | --- |
| backbeat, rock, "just a beat" | hats `X-x-X-x-`, snare `--x---x-`, kick `x---x---` |
| boom bap, "with ghosts" | 1/16, snare `-oo-X-o--oo-X-o-` under straight hats |
| four on the floor, house, disco | kick `x-x-x-x-`, `hatOpen` on the off-beats `-x-x-x-x` |
| shuffle, blues, swing | `[12,8]`, hats `X-xX-xX-xX-x` (the middle triplet missing) |
| half-time, heavy | 1/16, one snare on beat 3 `--------X-------` |
| tresillo, 3-3-2, Latin push | kick `x--x--x-` |
| "the fill", "walk it round the kit" | a sticking on the snare, then the same sticking moved a drum per beat |
| a rudiment (paradiddle, flam, drag, buzz…) | `kind: rudiment`, one snare lane, a full `sticking` |

Keep grooves to 3–4 lanes. Accent the beat (`X` on 1 and 3 of the hats) or it
turns to mush; ghost the rest when the feel wants it.
