# Deep links — every address in the catalogue

_Generated from the app by `scripts/vibe-reference.mjs` on 2026-09-03 (app 0.1.0). Do not edit; regenerate._

A deep link names something the app already has. It rides in the fragment, so
the path is always `/` and nothing reaches a server. Live base: **https://guitarza.netlify.app/**

| Section | Route | Example |
| --- | --- | --- |
| Lessons | `#/lessons/<id>` | `https://guitarza.netlify.app/#/lessons/first-chords` |
| Chords | `#/chords/<root>/<quality>` | `https://guitarza.netlify.app/#/chords/A/min` — sharps URL-encode: `F%23` |
| Picking | `#/picking/<id>` | `https://guitarza.netlify.app/#/picking/travis` |
| Progressions | `#/progressions/<id>/<key>[?feel=&position=&lead=&run=&repeats=]` | `https://guitarza.netlify.app/#/progressions/pop-axis/A?feel=eighths&lead=scale` |
| Songs | `#/songs/<id>` | `https://guitarza.netlify.app/#/songs/campfire-four-chord` |
| Drums | `#/drums/<id>` | `https://guitarza.netlify.app/#/drums/backbeat` |

A progressions link says only what differs from the defaults
(`feel=boom-chuck`, `position=open`, `lead=off`, `run=ascending`, `repeats=2`).
An id the app does not have falls back to the section's first entry — it never errors.

## Lessons
| id | title | level | tags |
| --- | --- | --- | --- |
| `first-chords` | Your First Four Chords | beginner | open chords, strumming, changes |
| `sus-chords` | Sus Chords | beginner | open chords, colour, one finger |
| `major-scale` | The Major Scale | beginner | scales, major, position playing |
| `pentatonic-box-one` | Minor Pentatonic, Box 1 | beginner | scales, pentatonic, lead, blues |
| `power-chords` | Power Chords & Palm Muting | beginner | rock, power chords, right hand, palm mute |
| `barre-chords` | Barre Chords | intermediate | barre, movable shapes, CAGED |
| `travis-picking` | Travis Picking | intermediate | fingerpicking, right hand, folk |
| `legato` | Hammer-ons & Pull-offs | intermediate | technique, legato, pentatonic, lead |
| `blues-shuffle` | 12-Bar Blues in A | intermediate | blues, shuffle, riff, 12-bar |

## Chords
Roots: `C` `Db` `D` `Eb` `E` `F` `F#` `G` `Ab` `A` `Bb` `B`
Qualities: `maj` `min` `7` `m7` `maj7` `sus4` `5` `dim`

## Picking
| id | name | pattern |
| --- | --- | --- |
| `travis` | Travis — alternating bass | p i m · 8ths |
| `forward-roll` | Forward roll | p i m a |
| `backward-roll` | Backward roll | a m i p |
| `pinch-roll` | Pinch & roll | p+a together |
| `waltz-roll` | Waltz roll — 6/8 | p i m a m i |
| `ballad-arpeggio` | Ballad arpeggio | p i m i · 8ths |
| `monotonic-bass` | Monotonic bass | p on every beat |
| `cascade` | Cascade | p a m i |
| `inside-roll` | Inside roll | p m i a |
| `threes` | Threes — 6/8 | p i m · twice |

## Progressions
| id | name | numbers | default bpm |
| --- | --- | --- | --- |
| `pop-axis` | The four-chord song | `1 5 6m 4` | 92 |
| `three-chord` | Three chords and the truth | `1 4 5` | 104 |
| `fifties` | Fifties changes | `1 6m 4 5` | 84 |
| `two-five-one` | ii – V – I | `2m 5 1` | 100 |
| `twelve-bar` | 12-bar blues | `1 4 1 5 4 1 5` | 88 |
| `minor-blues` | Minor blues | `1m 4m 1m 5m 1m` | 76 |
| `mixolydian-rock` | Rock mixolydian | `1 b7 4` | 112 |
| `andalusian` | Andalusian cadence | `1m b7 b6 5` | 96 |
| `one-four-five-four` | Round trip | `1 4 5 4` | 108 |
| `one-three-five` | Rising thirds | `1 3m 5` | 96 |
| `one-three-four` | Step up to four | `1 3m 4` | 92 |
| `six-four-one-five` | The sensitive one | `6m 4 1 5` | 88 |
| `one-five-four` | Down the stairs | `1 5 4` | 120 |
| `one-four-six-five` | Long way home | `1 4 6m 5` | 96 |
| `minor-one-flat-seven` | Minor vamp | `1m b7` | 100 |

Keys (circle of fifths): `C` `G` `D` `A` `E` `B` `F#` `Db` `Ab` `Eb` `Bb` `F`

## Songs
| id | title | key | bpm | chords |
| --- | --- | --- | --- | --- |
| `campfire-four-chord` | Campfire four-chord | G major | 92 | G D Em C |
| `slow-blues-in-a` | Slow blues in A | A major | 72 | A7 D7 E7 |
| `waltz-for-beginners` | Waltz for beginners | C major | 96 | C Am F G |
| `fifties-changes` | Fifties changes | C major | 84 | C Am F G |
| `the-long-way-round` | The long way round | C major | 76 | Am F C G |
| `mixolydian-rocker` | Mixolydian rocker | E major | 120 | E D A |
| `country-boom-chuck` | Country boom-chuck | G major | 100 | G C D |
| `fingerstyle-ballad` | Fingerstyle ballad | C major | 72 | C G Am F |
| `barre-workout` | Barre workout | F major | 80 | F Bb C Dm |
| `two-five-one-study` | ii–V–I study | C major | 108 | Dm7 G7 Cmaj7 Am7 |

## Drums
| id | name | kind | family | level | grid | sticking |
| --- | --- | --- | --- | --- | --- | --- |
| `backbeat` | The backbeat | groove |  | Beginner | 4/4 · 1/8 |  |
| `sixteenth-hats` | Sixteenth hats | groove |  | Intermediate | 4/4 · 1/16 |  |
| `four-on-the-floor` | Four on the floor | groove |  | Beginner | 4/4 · 1/8 |  |
| `shuffle` | Shuffle | groove |  | Intermediate | 12/8 · 1/8 |  |
| `half-time` | Half-time | groove |  | Intermediate | 4/4 · 1/16 |  |
| `fill-and-crash` | Fill and crash | groove |  | Intermediate | 4/4 · 1/16 |  |
| `single-strokes` | Single strokes | rudiment | stroke | Beginner | 4/4 · 1/16 | yes |
| `double-strokes` | Double strokes | rudiment | stroke | Intermediate | 4/4 · 1/16 | yes |
| `paradiddle` | Paradiddle | rudiment | diddle | Intermediate | 4/4 · 1/16 | yes |
| `accent-and-tap` | Accent and tap | rudiment | stroke | Beginner | 4/4 · 1/16 | yes |
| `ghost-notes` | Ghost notes | rudiment | colour | Intermediate | 4/4 · 1/16 | yes |
| `flams` | Flams | rudiment | grace | Intermediate | 4/4 · 1/8 | yes |
| `buzz-roll` | Buzz roll | rudiment | stroke | Advanced | 4/4 · 1/8 | yes |
| `cross-stick` | Cross-stick | rudiment | colour | Beginner | 4/4 · 1/8 | yes |
| `tom-sticking` | Moving it round the kit | rudiment | kit | Intermediate | 4/4 · 1/16 | yes |
| `double-paradiddle` | Double paradiddle | rudiment | diddle | Intermediate | 12/8 · 1/8 | yes |
| `triple-paradiddle` | Triple paradiddle | rudiment | diddle | Advanced | 4/4 · 1/16 | yes |
| `paradiddle-diddle` | Paradiddle-diddle | rudiment | diddle | Intermediate | 12/8 · 1/8 | yes |
| `inverted-paradiddle` | Inverted paradiddle | rudiment | diddle | Advanced | 4/4 · 1/16 | yes |
| `moeller` | The Moeller whip | rudiment | stroke | Advanced | 12/8 · 1/8 | yes |
| `moeller-hats` | Moeller on the hats | rudiment | stroke | Advanced | 12/8 · 1/8 | yes |
| `five-stroke-roll` | Five-stroke roll | rudiment | stroke | Intermediate | 4/4 · 1/16 | yes |
| `flam-tap` | Flam tap | rudiment | grace | Advanced | 4/4 · 1/8 | yes |
| `drags` | Drags | rudiment | grace | Intermediate | 4/4 · 1/8 | yes |
| `hat-foot` | The hi-hat foot | rudiment | colour | Intermediate | 4/4 · 1/8 |  |

Families: `stroke` Stroke control · `diddle` The paradiddle family · `grace` Grace notes · `colour` Sounds and feet · `kit` Around the kit
