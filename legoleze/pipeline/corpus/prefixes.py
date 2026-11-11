#!/usr/bin/env python3
"""Prefix (DocumentId) -> evidence table: period, dominant minister mention, purity, sample titles."""
import json, re, os, random
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
CUT = re.compile(r' (kan|skal|kunne|med|udpeger|nedsætter|fastsætter|fastsætte|giver|give|efter|i|om|på|til|eller|at|har|bemyndiges|bestemmer|træffer|offentliggør|godkender|fører|afgør|udarbejder|indhenter|underretter|bliver|vil|samt|får|kunne|må|beslutter|meddeler|opretter|fastlægger|en|et|den|det|de|af|ved|som|for)\b')
TWO = {('videregående', 'uddannelser'), ('sociale', 'forhold'), ('offentlig', 'innovation'), ('grøn', 'trepart'), ('nordisk', 'samarbejde'), ('økonomiske', 'anliggender')}
def normmin(s):
    s = s.lower().strip()
    if s.startswith('ministeren for '):
        w = s[len('ministeren for '):].split()
        out = []; i = 0
        while i < len(w):
            t = w[i]; out.append(t.rstrip(','))
            if i + 1 < len(w) and (t, w[i + 1]) in TWO: out[-1] = t + ' ' + w[i + 1]; i += 1
            if t.endswith(','): i += 1; continue
            if i + 2 < len(w) + 1 and i + 1 < len(w) and w[i + 1] == 'og' and i + 2 < len(w):
                out.append('og'); nxt = w[i + 2].rstrip(',.')
                if i + 3 < len(w) and (w[i + 2], w[i + 3]) in TWO: nxt = w[i + 2] + ' ' + w[i + 3]
                out.append(nxt)
            break
        name = ' '.join(x for x in out if x)
        name = re.sub(r'[^a-zæøå ,\-]', '', name).strip(' ,')
        if not name or name.split()[0] in ('at', 'det', 'den', 'de', 'en', 'et', 'og'): return None
        out2 = []
        for i, x in enumerate(out):
            out2.append(x + (',' if i + 1 < len(out) and out[i + 1] != 'og' and x != 'og' else ''))
        return 'ministeren for ' + ' '.join(out2).strip(' ,')
    if s in ('ressortministeren', 'vedkommende ministeren', 'ministeren', 'minister'): return None
    return s
def top_min(d):
    c = Counter()
    for k, v in d['f']['min'].items():
        k2 = normmin(k)
        if k2: c[k2] += v
    for k in d['f']['tmin']:
        k2 = normmin(k)
        if k2: c[k2] += 3
    return c
if __name__ == '__main__':
    P = defaultdict(lambda: {'n': 0, 'v': 0, 'years': Counter(), 'top': Counter(), 'all': Counter(), 'titles': []})
    random.seed(1)
    for l in open(os.path.join(HERE, 'data', 'docs.jsonl')):
        d = json.loads(l); p = P[d['prefix'] or '?']
        p['n'] += 1; p['v'] += d['status_2026_06'] == 'gældende'; p['years'][d['aar']] += 1
        c = top_min(d)
        if c: p['top'][c.most_common(1)[0][0]] += 1; p['all'].update(c)
        p['titles'].append((d['aar'], d['titel'][:110], d['status_2026_06']))
    out = []
    for k, p in sorted(P.items(), key=lambda x: -x[1]['n']):
        ys = sorted(p['years']); tot = sum(p['top'].values())
        dom, dn = (p['top'].most_common(1)[0] if p['top'] else (None, 0))
        t = p['titles']; random.shuffle(t)
        g = [x for x in t if x[2] == 'gældende'][:10]; h = [x for x in t if x[2] != 'gældende'][:6]
        out.append({'prefix': k, 'n': p['n'], 'gaeldende': p['v'], 'aar_fra': ys[0], 'aar_til': ys[-1],
                    'aar_p10_p90': [sorted(p['years'].elements())[int(p['n'] * .1)], sorted(p['years'].elements())[int(p['n'] * .9) - 1]],
                    'dominerende_minister': dom, 'renhed': round(dn / tot, 2) if tot else None, 'dok_med_ministernavn': tot,
                    'top_ministre': p['top'].most_common(5), 'eksempeltitler': [f"{a}: {b}" for a, b, _ in sorted(g + h)]})
    json.dump(out, open(os.path.join(HERE, 'data', 'prefixes.json'), 'w'), ensure_ascii=False, indent=1)
    for o in out: print(o['prefix'], o['n'], o['gaeldende'], o['aar_p10_p90'], o['dominerende_minister'], o['renhed'], o['dok_med_ministernavn'])
