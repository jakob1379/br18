"""Name -> law-family keys (same normalisation as resolve.py) for registry node names like 'Lov om planlægning (planloven)'."""
import re
def _norm(s):
    s = re.sub(r'\b(m\.v\.|mv\.|m\.m\.|m\.fl\.)', ' ', s)
    s = re.sub(r'[^a-zæøåé0-9\- ]', ' ', s); return re.sub(r'\s+', ' ', s).strip()
def keys_for_name(name):
    t = name.lower(); ks = set()
    for k in re.findall(r'\(([a-zæøå\-]+loven)[^)]*\)', t): ks.add('#' + k)
    for k in re.findall(r'\b([a-zæøå\-]{4,}loven)\b', t): ks.add('#' + k)
    m = re.search(r'\blov om ([^()]+)', t)
    if m: ks.add(_norm(m.group(1)))
    return ks
