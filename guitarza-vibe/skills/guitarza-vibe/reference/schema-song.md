# `song` — a chord sheet: sections, one chord per bar

The app turns a sheet into a play-through: one step per bar, the chord's
voicing on the neck, the section's lyric line as the coaching, a backing
strummed from the sheet, and the sections listed as theory notes.

## The document

```json
{
  "id": "harvest-moon-sketch",
  "title": "Harvest moon sketch",
  "desc": "A two-section sheet in D — verse on the I–IV, chorus lifting to the vi.",
  "key": "D major",
  "tempo": 84,
  "level": "Beginner",
  "timeSignature": [4, 4],
  "chords": ["D", "G", "Bm", "A"],
  "sections": [
    { "name": "Verse",  "bars": ["D", "G", "D", "G", "D", "G", "A", "A"], "lyric": "— verse lines here —" },
    { "name": "Chorus", "bars": ["Bm", "G", "D", "A", "Bm", "G", "A", "D"], "lyric": "— the lift —" }
  ]
}
```

| field | required | notes |
| --- | --- | --- |
| `id` | yes | lowercase-hyphen; namespaced `shared-…` on load |
| `title`, `desc` | title yes | `desc` is the card's line |
| `key` | yes | free text the app displays, e.g. `"G major"`, `"A minor"` |
| `tempo` | yes | bpm, 30–260 |
| `level` | yes | `Beginner` · `Intermediate` · `Advanced` |
| `timeSignature` | yes | `[4,4]`; `[3,4]` for a waltz; `[12,8]` for a slow blues — a bar lasts that many beats |
| `chords` | recommended | the distinct symbols in order of first appearance — the card's tag row |
| `sections` | yes, ≥1 | each `{ name, bars[], lyric? }`; `bars` is **one chord symbol per bar** |

## Chord symbols — what the voicing engine can spell

Root: `C D E F G A B` with `#` or `b` (`F#`, `Bb`, `Eb`, `Ab`, `Db`).
Qualities the library carries: major (`G`), minor (`Am`), `7`, `m7`, `maj7`,
`sus4`, `sus2`, `5` (power), `dim` — written as `G7`, `Am7`, `Dmaj7`, `Dsus4`,
`Asus2`, `E5`, `Bdim`.

**Not spellable:** slash chords (`C/G`), extensions beyond the seventh (`Am9`,
`G13`), altered dominants (`E7#9`), `aug`, `6`, `add9`. A bar the engine cannot
voice is **refused on load with the symbol named** — the app never drops a bar
silently. Rewrite the harmony in what the library has (`Am9` → `Am7`,
`C/G` → `C`) and say you did.

The voicing is the engine's call: open shapes preferred, barre shapes when a
root has no open form. To pin a specific fingering, author a `lesson` instead.

## Vibe → sheet

| words | do |
| --- | --- |
| "a campfire song", "four chords" | I–V–vi–IV, 8 bars a section |
| "a 12-bar", "blues in E" | `E7 E7 E7 E7 A7 A7 E7 E7 B7 A7 E7 B7`, `[12,8]` if slow |
| "a waltz" | `[3,4]`, every bar three beats |
| "lift to the vi", "the sad chord" | the relative minor where the chorus turns |
| "doo-wop", "50s" | I–vi–IV–V |
| "jazzy" | the 2–5–1: `Dm7 G7 Cmaj7 Cmaj7` |

Put the lyric or cue for a section in `lyric`; it becomes the coaching line the
player reads while that section plays. Placeholders are fine — the user fills
them in.
