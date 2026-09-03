#!/usr/bin/env python3
"""Guitarza share codec — document JSON <-> #gz= URL.

Identical transform to src/share/codec.ts: base64url(raw-deflate(minified JSON)),
'=' padding stripped. The minified JSON byte-matches JSON.stringify (no spaces,
ensure_ascii=False, insertion key order). The deflate bytes MAY differ from a
given JS runtime's — zlib builds differ — but every code is mutually decodable,
and decode(encode(x)) == x holds across both languages; scripts/test-share.mjs
checks a Python code decodes in JS and a JS code decodes here, every build.
No third-party deps. Bundled unchanged into the guitarza-vibe plugin.
"""
import argparse
import base64
import json
import sys
import zlib

KINDS = ('song', 'groove', 'lesson', 'practice')
LIVE_BASE = 'https://guitarza.netlify.app/'
LOCAL_BASE = 'http://localhost:5273/'
ID_RE = r'^[a-z0-9][a-z0-9-]*$'

# The house shortener: shortlink-headless on Netlify, fronting a47l.com. One
# bearer token, one POST. Read from the environment the /shortlink skill and
# the MCP server already use, so there is one place a token lives.
SHORTLINK_API_URL = 'https://a47l.netlify.app'
SHORTLINK_DOMAIN = 'a47l.com'


def shorten(long_url, slug=None, notes='guitarza'):
    """POST the long URL to a47l; return (short_url, None) or (None, reason).

    Never raises: a shortener being down is not a reason to withhold the link
    that works. The caller prints the long one either way.
    """
    import os
    import urllib.request
    import urllib.error
    token = os.environ.get('SHORTLINK_TOKEN')
    base = os.environ.get('SHORTLINK_API_URL', SHORTLINK_API_URL).rstrip('/')
    if not token:
        return None, 'SHORTLINK_TOKEN is not set (export it, as the /shortlink skill does)'
    body = {'url': long_url, 'notes': notes}
    if slug:
        body['slug'] = slug
    req = urllib.request.Request(
        f'{base}/api/links', data=minify(body).encode('utf-8'), method='POST',
        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            rec = json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        detail = e.read().decode('utf-8', 'replace')[:120]
        return None, f'a47l refused ({e.code}): {detail or e.reason}'
    except (urllib.error.URLError, TimeoutError, ValueError) as e:
        return None, f'a47l unreachable: {e}'
    # Prefer a URL the service names; otherwise assemble it from the record.
    short = rec.get('short_url') or rec.get('shortUrl')
    if not short:
        host = rec.get('hostname') or rec.get('domain') or os.environ.get('SHORTLINK_DOMAIN', SHORTLINK_DOMAIN)
        s = rec.get('slug')
        if not s:
            return None, f'a47l answered without a slug: {minify(rec)[:120]}'
        short = f'https://{host}/{s}'
    return short, None


def find_catalog(explicit=None):
    """The generated vocabulary, if it is next to this script (plugin layout)."""
    from pathlib import Path
    here = Path(__file__).resolve().parent
    candidates = [Path(explicit)] if explicit else [
        here.parent / 'skills' / 'guitarza-vibe' / 'reference' / 'catalog.json',
        here / 'catalog.json',
    ]
    for c in candidates:
        if c.is_file():
            return json.loads(c.read_text(encoding='utf-8'))
    return None


def check(kind, doc, catalog):
    """Shape problems the app's loader would refuse. Enum membership comes from
    catalog.json — the app's own lists — never from a copy typed in here."""
    import re
    problems = []
    need = lambda k, msg: problems.append(f'{k}: {msg}') if k not in doc else None
    enums = (catalog or {}).get('enums', {})
    in_enum = lambda name, value: (name not in enums) or (value in enums[name])

    if kind == 'practice':
        need('progression', 'required'); need('key', 'required')
        if catalog:
            ids = [p['id'] for p in catalog['progressions']]
            if doc.get('progression') not in ids: problems.append(f"progression: not one of {', '.join(ids)}")
            if doc.get('key') not in catalog['keys']: problems.append(f"key: not one of {', '.join(catalog['keys'])}")
        for k in ('feel', 'position', 'lead', 'run', 'repeats'):
            if k in doc and not in_enum(k, doc[k]):
                problems.append(f"{k}: not one of {', '.join(map(str, enums[k]))}")
        return problems

    if not re.match(ID_RE, str(doc.get('id', ''))): problems.append('id: lowercase letters, digits and hyphens')
    ts = doc.get('timeSignature')
    if not (isinstance(ts, list) and len(ts) == 2 and all(isinstance(n, int) and n > 0 for n in ts)):
        problems.append('timeSignature: [beats, unit], e.g. [4, 4]')
    if not isinstance(doc.get('tempo'), (int, float)): problems.append('tempo: a number')

    if kind == 'song':
        for k in ('title', 'key', 'sections'): need(k, 'required')
        if not in_enum('level', doc.get('level')): problems.append("level: Beginner, Intermediate or Advanced")
        for i, sec in enumerate(doc.get('sections') or []):
            if not sec.get('name'): problems.append(f'sections[{i}].name: required')
            if not sec.get('bars'): problems.append(f'sections[{i}].bars: at least one chord symbol')
        problems.append('note: chord spellings are checked by the app on load (voicing engine) — --decode and open the link')
    elif kind == 'groove':
        for k in ('name', 'lanes', 'coach'): need(k, 'required')
        if not in_enum('grooveKind', doc.get('kind')): problems.append('kind: groove or rudiment')
        if not in_enum('level', doc.get('level')): problems.append('level: Beginner, Intermediate or Advanced')
        if doc.get('stepValue') not in (8, 16): problems.append('stepValue: 8 or 16')
        lanes = doc.get('lanes') or []
        widths = {len(l.get('pattern', '')) for l in lanes}
        if len(widths) > 1: problems.append(f'lanes: patterns disagree on length {sorted(widths)}')
        cells = set(enums.get('cell', ['-', 'x', 'X', 'o', 'f', 'd', 'z']))
        pieces = {p['id'] for p in enums.get('kitPiece', [])} if 'kitPiece' in enums else None
        for i, l in enumerate(lanes):
            bad = sorted({c for c in l.get('pattern', '') if c not in cells})
            if bad: problems.append(f"lanes[{i}].pattern: unknown character(s) {bad}")
            if not any(c != '-' for c in l.get('pattern', '')): problems.append(f"lanes[{i}]: never sounds")
            if pieces is not None and l.get('piece') not in pieces: problems.append(f"lanes[{i}].piece: not one of {', '.join(sorted(pieces))}")
        if ts and doc.get('stepValue') in (8, 16) and len(widths) == 1:
            beats, unit = ts
            want = beats * (1 if unit == 8 else 2) if doc['stepValue'] == 8 else beats * 4
            if widths and next(iter(widths)) != want:
                problems.append(f"lanes: {next(iter(widths))} columns but {beats}/{unit} at 1/{doc['stepValue']} needs {want}")
        st = doc.get('sticking')
        if st is not None:
            if widths and len(st) != next(iter(widths)): problems.append('sticking: must be as long as the grid')
            if any(c not in 'RL-' for c in st): problems.append('sticking: only R, L and -')
    elif kind == 'lesson':
        for k in ('title', 'tuning', 'steps', 'tags'): need(k, 'required')
        if not in_enum('lessonLevel', doc.get('level')): problems.append('level: beginner, intermediate or advanced')
        if not in_enum('tuning', doc.get('tuning')): problems.append('tuning: not a tuning the app has')
        for i, step in enumerate(doc.get('steps') or []):
            if not step.get('id') or not step.get('label'): problems.append(f'steps[{i}]: needs id and label')
            if 'shape' in step and not isinstance(step['shape'].get('frets'), list): problems.append(f'steps[{i}].shape.frets: a list, LOW → HIGH')
    return problems


def minify(obj):
    return json.dumps(obj, separators=(',', ':'), ensure_ascii=False)


def encode(envelope):
    raw = minify(envelope).encode('utf-8')
    co = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -15)
    packed = co.compress(raw) + co.flush()
    return base64.urlsafe_b64encode(packed).decode('ascii').rstrip('=')


def decode(code_or_url):
    s = code_or_url.strip()
    if '#gz=' in s:
        s = s.split('#gz=', 1)[1]
    s = s.split('&')[0]
    pad = '=' * (-len(s) % 4)
    packed = base64.urlsafe_b64decode(s + pad)
    env = json.loads(zlib.decompress(packed, -15).decode('utf-8'))
    if env.get('v') != 1 or env.get('kind') not in KINDS or 'doc' not in env:
        raise SystemExit('error: decoded payload is not a v1 Guitarza share envelope')
    return env


def main():
    p = argparse.ArgumentParser(description='document JSON <-> #gz= share URL (codec.ts-compatible)')
    p.add_argument('file', nargs='?', help='document JSON file, or - for stdin')
    p.add_argument('--kind', choices=KINDS, help='wrap a bare document into the v1 envelope as this kind')
    p.add_argument('--live', action='store_true', help=f'base {LIVE_BASE}')
    p.add_argument('--local', action='store_true', help=f'base {LOCAL_BASE}')
    p.add_argument('--base', help='base URL override')
    p.add_argument('--code', action='store_true', help='print just the code (paste into Share ▾ → Load)')
    p.add_argument('--json', action='store_true', help='print the minified envelope JSON (the exact compressed bytes)')
    p.add_argument('--decode', metavar='URL_OR_CODE', help='decode a share URL or code, print pretty JSON')
    p.add_argument('--short', action='store_true', help=f'also mint a {SHORTLINK_DOMAIN} short link (needs SHORTLINK_TOKEN)')
    p.add_argument('--slug', help='the short link slug to ask for, with --short')
    p.add_argument('--check', action='store_true', help='report shape problems the app would refuse, and stop')
    p.add_argument('--catalog', help='path to reference/catalog.json (found automatically in the plugin layout)')
    args = p.parse_args()

    if args.decode is not None:
        print(json.dumps(decode(args.decode), indent=2, ensure_ascii=False))
        return

    if not args.file:
        p.error('a document file (or -) is required unless --decode is used')
    text = sys.stdin.read() if args.file == '-' else open(args.file, encoding='utf-8').read()
    obj = json.loads(text)

    if isinstance(obj, dict) and obj.get('v') == 1 and 'kind' in obj and 'doc' in obj:
        env = obj
    elif args.kind:
        env = {'v': 1, 'kind': args.kind, 'doc': obj}
    else:
        raise SystemExit('error: a bare document needs --kind <song|groove|lesson|practice>')

    catalog = find_catalog(args.catalog)
    problems = check(env['kind'], env['doc'], catalog)
    hard = [x for x in problems if not x.startswith('note:')]
    if args.check:
        for x in problems:
            print(('  ! ' if not x.startswith('note:') else '  · ') + x)
        if not catalog:
            print('  · catalog.json not found: enum values were not verified')
        print('ok' if not hard else f'{len(hard)} problem(s)')
        sys.exit(0 if not hard else 1)
    if hard:
        for x in hard:
            print('  ! ' + x, file=sys.stderr)
        raise SystemExit(f'error: {len(hard)} problem(s) the app would refuse — fix them, or run --check')

    if args.json:
        print(minify(env))
        return
    code = encode(env)
    if args.code:
        print(code)
        return

    base = args.base or (LIVE_BASE if args.live else LOCAL_BASE)
    base = base.split('#', 1)[0]
    long_url = f'{base}#gz={code}'
    if not args.short:
        print(long_url)
        return
    short, why = shorten(long_url, args.slug)
    if short:
        print(short)
        print(long_url)
    else:
        print(long_url)
        print(f'(no short link: {why})', file=sys.stderr)


if __name__ == '__main__':
    main()
