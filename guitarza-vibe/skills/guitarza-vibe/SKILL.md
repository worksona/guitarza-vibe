---
name: guitarza-vibe
description: Vibe Guitarza from natural language. Hand someone a deep link to anything in the catalogue — a lesson, a chord, a picking pattern, a play-along in a key, a song sheet, a drum groove or rudiment — or author a NEW song sheet, drum groove, play-along or lesson against the app's own vocabulary and deliver a #gz= share link that opens https://guitarza.netlify.app with it already loaded on the neck (or kit), in the tab, and in the audio. Trigger on /guitarza-vibe, "link me the paradiddle", "send me the 12-bar in E", "make me a groove", "a 3-3-2 beat", "write a sheet for", "a song in D with", "a play-along over", "a lesson that", "what's the link for", or any request to share, generate, remix or deep-link Guitarza content.
---

## Before you start — what you need

This plugin is self-contained. Describe what you want to play, get a link that
opens the studio with it loaded. The codec is bundled; nothing else is required.

| you want to… | you need |
| --- | --- |
| link something the app already has | `reference/deep-links.md` — the address table |
| author a new song, groove, play-along or lesson and share it | this plugin: the schema guides, `reference/catalog.json`, `scripts/encode.py` |
| play it, tweak it by hand, change the instrument | a browser — open the link; everything is in the page |
| regenerate the reference from the app | the Guitarza app repo: `node scripts/vibe-reference.mjs` *(app repo)* |

Encode with the bundled codec:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/encode.py" doc.json --kind groove --live     # → https://guitarza.netlify.app/#gz=…
python3 "$CLAUDE_PLUGIN_ROOT/scripts/encode.py" doc.json --kind groove --check    # shape problems the app would refuse
python3 "$CLAUDE_PLUGIN_ROOT/scripts/encode.py" --decode '<url or code>'          # the reverse — verify your own link
```

# Guitarza Vibe

Turn a sentence into a **link**. Two kinds, both in the URL fragment, so nothing
you author ever reaches a server:

| link | what it is | opens |
| --- | --- | --- |
| **deep link** `#/section/…` | the *address* of something in the catalogue | that thing, in its section |
| **share code** `#gz=…` | a *document* the app has never seen — it lives in the URL | the document, loaded as catalogue content **and kept in the player's library** |

Opening a `#gz=` link saves it: it gets a "Yours" card in its section, an entry
in the Library menu, and it is still there next time. So the link you hand back
is not a one-off — it is how something gets *into* someone's app.

The app: **https://guitarza.netlify.app**. Six sections, one studio: Lessons ·
Chords · Picking · Progressions (play-along) · Songs · Drums. Whatever loads is on
the neck (or the kit), in the tab, in the notation and in the audio at once.

---

## 1. ROUTER — read the ask, pick the kind

| the ask sounds like | do this | read |
| --- | --- | --- |
| "link me the paradiddle", "the F#m7 page", "the 12-bar in E, shuffle, with chord tones" — something that **exists** | a **deep link** | `reference/deep-links.md` |
| "a groove with the kick on 1 and the and of 2", "a 3-3-2", "hats in sixteenths with ghosts" — a **beat or rudiment** | share a `groove` | `reference/schema-groove.md` |
| "a sheet in D, verse and chorus", "write out my song's chords", "a 12-bar with sevenths" — a **song sheet** | share a `song` | `reference/schema-song.md` |
| "loop the four-chord song in A as eighths", "a play-along over the 2-5-1, target notes showing" — a **backing loop with knobs** | a deep link if it is a catalogue progression (it usually is); share a `practice` doc only when you need a tempo the link cannot carry | `reference/schema-practice.md` |
| "a lesson that walks through these three shapes", "coach me through…" — hand-authored **steps with shapes and coaching** | share a `lesson` | `reference/schema-lesson.md` |

**Prefer the deep link.** If what they want is in the catalogue, the address is
shorter, permanent, and cannot be wrong. Only author a document when the catalogue
does not have it.

---

## 2. THE WORKFLOW

### 1 — Read the reference FIRST, every run
`reference/catalog.json` is generated from the app's source: every id, every
enum, every range. `reference/deep-links.md` is the same for addresses. The
`schema-*.md` guides say what the tables cannot — how a grid is read, which
chord spellings the voicing engine knows. **Never invent a kit piece, a grid
character, a feel, a quality, a tuning or a progression id.** If it is not in
the catalog, the app does not have it.

### 2a — If they gave you a document, read it
This is the main way new material arrives: a `.txt` or `.md` of tab, a chord
sheet, a page of a book, a screenshot, a paste. **You are the parser** — the
app has no tab importer and does not need one. Read the document and author
the document kind that fits it:

| what they gave you | author | why |
| --- | --- | --- |
| chords over lyrics, `[Am] Nobody knows`, a chord chart | `song` | one chord per bar; there is no rhythm to guess |
| ASCII tab with a repeating riff or a worked-out part | `lesson` with `alphaTex` | you can write the rhythm the tab implies |
| ASCII tab that is really just the chord changes | `song` | do not invent a rhythm you were not given |
| drum tab (`HH\|x-x-x-x-\|`, `SD\|----o---\|`) | `groove` | the rows *are* the grid; this is close to a transcription |
| "play along with this" over a known progression | a deep link, or a `practice` doc | |

**ASCII tab does not carry rhythm.** Columns are suggestive, not authoritative;
`--0---3--` does not say whether those are quarters or eighths. So:

- If the source **does** imply rhythm (bar lines, a count, consistent spacing,
  a tempo marking, a song you know), write it and **say what you assumed**.
- If it does not, prefer `song` — a sheet is one chord per bar and needs no
  rhythm — or ask for the tempo and feel rather than inventing them.
- Never quietly pick a rhythm. The whole app is built on the neck, the tab and
  the audio agreeing; a guessed rhythm is the first place it would lie.

Tab notation maps onto things the app already plays: `h` hammer-on, `p`
pull-off, `/` `\\` slides, `b` bend, `~` vibrato, `x` dead note, `PM` palm
mute. Chord names above the staff are the shapes for the neck. String labels
give the tuning (`D` on the bottom line is drop D). Frets in tab are numbers
per string — but in a `lesson` shape you write `frets` **LOW → HIGH**, which
is the reverse of how tab is printed, so read `schema-lesson.md` before
authoring one.

### 2 — Interpret the vibe
Map words to the vocabulary. "Boom bap" is a backbeat with a ghosted snare;
"lift to the vi" is a `Bm` in a D sheet; "with the chord tones showing" is
`lead=arpeggio`. Say the smallest thing that is true.

### 3 — Author a MINIMAL document
Only what the ask demands. The app fills defaults. A groove is its lanes and
four lines of coaching; a song is its sections. Ids are lowercase-hyphen and
get namespaced `shared-…` on load, so they can never collide with the catalogue.

### 4 — Check, then encode
```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/encode.py" doc.json --kind <song|groove|lesson|practice> --check
python3 "$CLAUDE_PLUGIN_ROOT/scripts/encode.py" doc.json --kind <kind> --live
```
`--check` reports shape problems against the catalog (lane lengths, grid
characters, unknown pieces, bad enums) and refuses to encode past them. Two
things only the app can judge, and it does so **on load, naming the problem in
the Share panel**: whether a chord symbol can be voiced, and whether a lesson's
shapes are playable. `--local` targets `http://localhost:5273/`; `--base` anything
else; `--code` prints just the code for **Share ▾ → Load** in the app.

### 5 — Verify your own link
```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/encode.py" --decode '<the url>'
```
Always. A link that does not decode is a link that does not open. If you can
open a browser, open it: the Share panel's status line reports anything the
loader refused.

### 6 — Shortlink on a47l.com
```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/encode.py" doc.json --kind groove --live --short [--slug tresillo]
# → https://a47l.com/ab12          (the short link, first)
#   https://guitarza.netlify.app/#gz=…   (the long one, always)
```
`--short` mints on **a47l.com** through the house shortener
(`shortlink-headless`), reading `SHORTLINK_TOKEN` (and optionally
`SHORTLINK_API_URL`) from the environment — the same variables the `/shortlink`
skill and the shortlink MCP use, so there is one place a token lives. Without a
token it prints the long link and says why on stderr; never withhold the link
that works. The `shortlink_create` MCP tool does the same job when present.
**Lead with the short link, keep the long one as the fallback.** A deep link is
already short — leave it. The app's own Share panel has a **Shorten** button
that does this server-side, so a person at the keyboard never needs the token.

### 7 — Deliver
- the clickable link (it opens the studio with the thing loaded),
- one line on what you built,
- **2–3 knobs** they can ask you to turn ("ghost the ands", "half-time it",
  "swap the chorus to the IV", "show target notes instead"),
- for a share code: that opening it **saves it to their library** — a "Yours"
  card in the section, and an entry in the Library menu, kept in that browser.
  The link is also the backup and the way to move it to another machine.
- when you read a document to make it: what you assumed about tempo and feel,
  in one line, so they can correct it.

### 8 — Iterate by document-diff, never by rewrite
On follow-ups, `--decode` the previous link (or the code they pasted) and patch
that document. Change only what their words point at, re-check, re-encode,
re-verify.

---

## 3. RULES

- **Only what the catalog lists.** Kit pieces, grid characters, feels, positions,
  leads, runs, repeats, qualities, tunings, progression ids, keys.
- **A groove's lanes are all the same length**, and the length is fixed by the
  time signature and `stepValue`: 4/4 at 1/8 is 8 columns, at 1/16 is 16; 12/8 at
  1/8 is 12. A lane that never sounds is refused — do not list a drum you do
  not play.
- **Sticking only where a hand plays.** `R`/`L` may sit under a column only if a
  hand piece sounds there; `-` elsewhere. The stroke row (down/tap/up/full) is
  derived by the app from the accents and the sticking — never author it.
- **Chords must be spellable by the voicing engine**: `C`, `Am`, `F#`, `Bb`, `G7`,
  `Am7`, `Dmaj7`, `Dsus4`, `Asus2`, `E5`, `Bdim`. No slash chords, no `Hm9#11`.
  A bar the engine cannot voice is refused with the symbol named; it is never
  silently dropped.
- **Lesson shapes are LOW → HIGH**: `frets[0]` is the low E. Six entries, `null`
  for a string not played. This is the single most common way a lesson goes
  wrong and the app has been bitten by it — see `schema-lesson.md`.
- **Keep documents minimal.** Do not emit defaults you did not choose. A
  play-along that is a catalogue progression at a catalogue key is a deep link,
  not a document.
- **Remix input:** if the user pastes a `#gz=` URL, a bare code, or a `#/…`
  link — **decode/read it first** and patch from their actual current state,
  never from memory.
- **Additive-only.** Never rely on a field the catalog does not list; new
  optional keys are ignored by the app, unknown enum values are refused.
- **Publishing leaves the machine.** A share link is delivery. Posting it
  anywhere public is the user's call.
- Open the link in a browser only if the user asks — or to verify a refusal.

---

## 4. WHAT THIS SKILL CANNOT DO

- **It cannot hear.** Every claim about how a groove or a sheet sounds is an
  inference from the document and the app's documented behaviour. "Feels like a
  freight train" is an intent, not a measurement. Build it, deliver it, ask.
- **It cannot add to the instrument.** No new kit pieces, tunings, chord
  qualities, feels or progressions — those are app changes. Say so.
- **A library is per browser.** Opening a link saves the document there, but
  nothing is uploaded and nothing syncs between machines — the link is how it
  travels. A `#/songs/shared-…` deep link only resolves in the browser that
  has it saved; to hand something to someone else, always send the `#gz=` code.
- **Voicing is the app's call.** Which fingering a song's `Am7` gets is decided
  by the voicing engine on load (open shape preferred). A share cannot pin a
  particular voicing; a `lesson` with explicit shapes can.
- **Custom kits, samples, audio: no.** The kit is synthesised from twelve
  pieces; a groove is placement and stroke, not sound design.
- **No short link without a token.** If `SHORTLINK_TOKEN` is not set and no
  shortlink MCP is present, deliver the long link and say so — never a
  made-up a47l.com URL.

---

## 5. REFERENCES

- Addresses: [`reference/deep-links.md`](reference/deep-links.md) — generated
- Vocabulary: [`reference/catalog.json`](reference/catalog.json) — generated
- Guides: [`schema-groove.md`](reference/schema-groove.md) ·
  [`schema-song.md`](reference/schema-song.md) ·
  [`schema-practice.md`](reference/schema-practice.md) ·
  [`schema-lesson.md`](reference/schema-lesson.md)
- The codec: `scripts/encode.py` (base64url · raw-deflate · minified JSON;
  identical to the app's `src/share/codec.ts`, cross-checked every build)
