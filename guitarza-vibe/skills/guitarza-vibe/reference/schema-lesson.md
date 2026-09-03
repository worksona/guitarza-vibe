# `lesson` — the raw contract: steps, shapes, coaching

Everything else in the app compiles *to* this. A song becomes a lesson, a
groove becomes a lesson, a play-along is generated as one. Author a lesson
directly when you need control the other kinds do not give: exact fingerings,
a scale lit behind a shape, a strum written per subdivision, an authored score.

Use it sparingly — a sheet or a groove is almost always the right kind, and far
less to get wrong.

## The document

```json
{
  "id": "three-shapes-of-g",
  "title": "Three shapes of G",
  "subtitle": "Open, then the E-shape barre, then the A-shape",
  "level": "beginner",
  "tags": ["chords", "CAGED"],
  "tuning": "standard",
  "tempo": 76,
  "timeSignature": [4, 4],
  "key": "G major",
  "intro": "One chord, three places on the neck.",
  "steps": [
    {
      "id": "open",
      "label": "G, open",
      "beats": 4,
      "shape": { "frets": [3, 2, 0, 0, 0, 3], "fingers": [2, 1, 0, 0, 0, 3], "root": "G", "name": "G" },
      "coach": "Second finger on the low E. Let every string ring."
    },
    {
      "id": "e-shape",
      "label": "G, E-shape barre at 3",
      "beats": 4,
      "shape": { "frets": [3, 5, 5, 4, 3, 3], "barre": { "fret": 3, "fromString": 0, "toString": 5, "finger": 1 }, "root": "G", "name": "G" },
      "coach": "The barre does the work of the nut."
    }
  ],
  "theory": [{ "heading": "CAGED", "body": "…" }]
}
```

| field | required | notes |
| --- | --- | --- |
| `id`, `title` | yes | id lowercase-hyphen; namespaced `shared-…` on load |
| `level` | yes | **lowercase** here: `beginner` · `intermediate` · `advanced` |
| `tags` | yes | a list, may be empty |
| `tuning` | yes | a tuning id from `catalog.json` — `standard` unless you mean otherwise |
| `capo` | no | fret |
| `tempo`, `timeSignature` | yes | |
| `key` | no | display text |
| `steps` | yes, ≥1 | see below |
| `alphaTex` | no | an authored score; omitted, the app strums the shapes one bar per step |
| `theory` | no | `[{ heading, body }]` |

## Steps

| field | notes |
| --- | --- |
| `id`, `label` | required |
| `beats` | how long the step holds, in beats |
| `shape` | what the fretting hand does — see below |
| `strum` | `{ subdivision, pattern }` — `subdivision` 2 = eighths, 4 = sixteenths; `pattern` of `D` `U` `-` `x` |
| `coach` | the line shown while the step is active |
| `scale` | a scale to light behind the shape, e.g. `"A minor pentatonic"` |
| `bar` | 1-based bar in an authored `alphaTex` score, for cursor sync |

## Shapes — LOW → HIGH, and the bug this app was bitten by

```json
{ "frets": [null, 0, 2, 2, 2, 0], "fingers": [null, 0, 1, 2, 3, 0], "root": "A", "name": "A" }
```

- `frets` has **six entries, index 0 = the low E**, index 5 = the high e.
  `null` = not played. `0` = open.
- `fingers` parallel to `frets`: `1`–`4` index to pinky, `0` open, `"T"` thumb,
  `null` unused.
- `barre`: `{ fret, fromString, toString, finger }`, string indexes LOW → HIGH.
- `root` (note name) drives interval colouring; `name` is the display symbol.

This ordering is the opposite of how tab and alphaTex number strings (1 = high
e). The app converts in exactly one place; **you never write string numbers, only
this LOW → HIGH list**. A mirrored shape still parses, renders and plays — it is
simply the wrong chord — which is why the app's validator compares every shape
against the score it produced. Get this right and everything downstream is.

Common open shapes, LOW → HIGH:

| chord | frets |
| --- | --- |
| C | `[null, 3, 2, 0, 1, 0]` |
| D | `[null, null, 0, 2, 3, 2]` |
| E | `[0, 2, 2, 1, 0, 0]` |
| G | `[3, 2, 0, 0, 0, 3]` |
| A | `[null, 0, 2, 2, 2, 0]` |
| Am | `[null, 0, 2, 2, 1, 0]` |
| Em | `[0, 2, 2, 0, 0, 0]` |
| F (barre) | `[1, 3, 3, 2, 1, 1]` + `barre {fret:1, fromString:0, toString:5}` |

## `alphaTex` — only if you must

If you author a score, the app prepends the header (title, tempo, time
signature, tuning, instrument); you supply bars only. String numbers in alphaTex
are **1 = high e** — the reverse of `frets`. Prefer letting the app generate the
score from the shapes; an authored score that disagrees with its shapes is the
exact class of bug the app's validator exists to catch, and a shared lesson
does not get that check.
