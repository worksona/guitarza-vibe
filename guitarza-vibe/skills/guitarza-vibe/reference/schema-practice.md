# `practice` — a play-along loop, and why you usually want a deep link instead

A play-along is a catalogue progression in a key with five knobs. Every
combination of those is already addressable as a **deep link**:

```
#/progressions/<progression>/<key>?feel=&position=&lead=&run=&repeats=
https://guitarza.netlify.app/#/progressions/twelve-bar/E?feel=shuffle&lead=arpeggio&run=thirds
```

Only what differs from the defaults is written, so
`#/progressions/pop-axis/A` is the four-chord song in A, boom-chuck, open
chords, no lead, two repeats. **Reach for the deep link first.** It is shorter,
permanent, and cannot be malformed.

## When a `practice` share document is worth it

One thing the link cannot carry: a **tempo**. If the ask names a bpm ("at 88"),
share a document:

```json
{ "progression": "twelve-bar", "key": "E", "feel": "shuffle", "lead": "arpeggio", "run": "thirds", "repeats": 2, "tempo": 88 }
```

| field | required | values (from `catalog.json`) |
| --- | --- | --- |
| `progression` | yes | a catalogue id — `pop-axis`, `twelve-bar`, `two-five-one`, … |
| `key` | yes | `C G D A E B F# Db Ab Eb Bb F` (circle of fifths) |
| `feel` | no | `boom-chuck` · `strum` · `eighths` · `shuffle` (shuffle writes the score in 12/8) |
| `position` | no | `open` · `sixth` (barre, E-shape) · `fifth` (barre, A-shape) |
| `lead` | no | `off` · `scale` · `arpeggio` (chord tones) · `targets` (one note per chord) |
| `run` | no | `ascending` · `thirds` · `fours` — only means anything with a lead |
| `repeats` | no | `1` · `2` · `4` · `8` |
| `tempo` | no | bpm; omitted, the progression's own default |

Defaults: `feel=boom-chuck position=open lead=off run=ascending repeats=2`.

On load the app selects a lead's fader automatically, so "with the scale
showing" is audible as well as visible. A play-along that came by link stops
being "the link's" the moment a knob is touched by hand; the URL then goes back
to being a deep link for whatever is now set.

## Vibe → knobs

| words | do |
| --- | --- |
| "just the chords", "backing only" | `lead=off` (default) |
| "show me the scale", "where to solo" | `lead=scale`, `run=ascending`; `run=thirds` for something more melodic |
| "the chord tones", "arpeggios" | `lead=arpeggio` |
| "which note to land on", "target notes" | `lead=targets` |
| "up the neck", "barre chords" | `position=sixth` or `fifth` |
| "eighths", "driving" | `feel=eighths` |
| "shuffle", "swing", "blues feel" | `feel=shuffle` |
| "loop it longer" | `repeats=4` or `8` |
