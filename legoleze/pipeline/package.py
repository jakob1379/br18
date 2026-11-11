#!/usr/bin/env python3
"""Build dk-regulering-data.zip: deliverables, catalog, dashboard data, audits, intermediates, raw workflow results, pipeline and harvester."""
import hashlib, json, os, zipfile
from datetime import datetime, timezone
from pathlib import Path
SP = Path(__file__).resolve().parent
WF = Path('/root/.claude/projects/-home-user-ai-job-search-fork/9c9ad245-1536-5d87-980d-1a4837c57ed1')
OUT = SP / 'dk-regulering-data.zip'
files = []  # (archive path, source path, description)
def add(arc, src, desc=''): files.append((arc, Path(src), desc))
R = 'dk-regulering-data/'
# 1 deliverables
for p in sorted((SP / 'dk-regulering').rglob('*')):
    if p.is_file(): add(R + 'dk-regulering/' + str(p.relative_to(SP / 'dk-regulering')), p)
# 2 dashboard
for n in ('omraader', 'maalt', 'vurderet', 'fremdrift', 'mangler'): add(R + f'dashboard/{n}.json', SP / 'dash' / f'{n}.json')
add(R + 'dashboard/index.html', SP / 'dash' / 'index.html')
# 3 audits and quality
for n, d in (('audit_raw.json', 'audit'), ('indeks_raw.json', 'audit'), ('ressort_quality.json', 'audit'), ('coverage.json', 'audit'), ('provenance_stats.json', 'audit')):
    add(R + f'{d}/{n}', SP / 'data' / n)
add(R + 'audit/opus_sample.json', SP / 'corpus' / 'data' / 'opus_sample.json')
# 4 intermediates
for n in ('final.json', 'merged.json', 'merge_report.json', 'seen_urls.json', 'alias.json', 'disputed_decisions.json', 'url_fixes.json', 'replacement_edges.json', 'v3_removed_edges.json', 'viz_data.json', 'viz_kat.json', 'viz_pos.json'):
    if (SP / 'data' / n).exists(): add(R + f'intermediate/registry/{n}', SP / 'data' / n)
for n in ('docs.jsonl', 'resolved.json', 'prefixes.json', 'udsteder.json', 'ressort.json'):
    add(R + f'intermediate/corpus/{n}', SP / 'corpus' / 'data' / n)
for p in sorted((SP / 'corpus' / 'jobs').rglob('*')):
    if p.is_file(): add(R + 'intermediate/corpus/jobs/' + str(p.relative_to(SP / 'corpus' / 'jobs')), p)
# 5 raw workflow results (journals) and workflow scripts
for p in sorted((WF / 'subagents' / 'workflows').glob('*/journal.jsonl')): add(R + f'raw/workflows/{p.parent.name}.jsonl', p)
for p in sorted((WF / 'workflows' / 'scripts').glob('*.js')): add(R + f'pipeline/workflows/{p.name}', p)
for p in sorted(SP.glob('dk-reg-*.js')): add(R + f'pipeline/workflows/{p.name}', p)
# 6 pipeline code
for n in ('run_all.sh', 'merge.py', 'finalize.py', 'seen_urls.py', 'provenance.py', 'manual_fixes.py', 'consolidate_huller.py', 'registry_sync.py', 'write_registry.py', 'write_readme.py',
          'viz_prep.py', 'viz_kat.py', 'viz_build.py', 'viz_template.html', 'viz_script.js', 'coverage_prep.py', 'dash_prep.py', 'package.py'):
    add(R + f'pipeline/{n}', SP / n)
for n in ('extract.py', 'prefixes.py', 'udsteder.py', 'make_jobs.py', 'resolve.py', 'resolve_keys.py', 'ressort_import.py', 'ressort_quality.py', 'katalog.py', 'census.py', 'run_corpus.sh'):
    add(R + f'pipeline/corpus/{n}', SP / 'corpus' / n)
for n in ('layout.js', 'shot.js', 'kshot.js', 'kint.js', 'qa2.js', 'package.json'):
    if (SP / 'mmd' / n).exists(): add(R + f'pipeline/mmd/{n}', SP / 'mmd' / n)
# 7 harvester
for n in ('harvest.py', 'run_harvest.sh', 'README.md'): add(R + f'harvest/{n}', SP / 'harvest' / n)
add(R + 'harvest/test_harvest.py', SP / 'harvest_test' / 'test_harvest.py')

missing = [f for f in files if not f[1].exists()]
assert not missing, missing
files = [f for f in files if f[1].exists()]
cat = json.load(open(SP / 'data' / 'coverage.json'))['katalog']
reg = json.load(open(SP / 'data' / 'final.json'))
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
rows = [(a, s.stat().st_size, sha(s)) for a, s, _ in files]
now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
manifest = f"""# Dansk regulering – datapakke

Bygget {now}. Kortlægning af danske myndigheder og retskilder til et RAG-korpus (udvidelse af jakob1379/br18).
Status for registry'et pr. 2026-10-28; katalogets dokumentstatus pr. 2026-06-12 (udstedelser til 2026-02-12).

## Indhold

| Mappe | Hvad |
|---|---|
| `dk-regulering/` | **Leverancen.** `registry.yaml` (sandheden: {len(reg['nodes'])} noder, {len(reg['edges'])} kanter, {len(reg['huller'])} huller), `README.md`, `datakilder.md`, `huller.md`, `diagrammer/` (Mermaid), `reguleringskort.html` (interaktivt kort, kan åbnes direkte i en browser), `scripts/build.py` (validering og views). |
| `dk-regulering/katalog/` | Katalog over hele Lovtidende A: `retsinformation_lta.jsonl` ({cat['dokumenter']} dokumenter, {cat['gaeldende']} gældende), `kanter.jsonl` (henviser_til, implementerer_EU, ressortansvar), `eu_index.jsonl` (EU-retsakter med CELEX), `README.md` (genereret oversigt). |
| `dashboard/` | Data og side bag dækningsdashboardet (heatmap pr. retsområde, fremdrift, 69 mangler med status). |
| `audit/` | Opus-auditten (fire linser + syntese og dækningsmatrix), vurderingen af danskelove.dk og Jurabibliotek, stikprøvekontrollen af ressort-klassifikationen og kvalitetstal. |
| `intermediate/registry/` | Flettet og efterbehandlet registry som JSON (`final.json`), flettelog, proveniens (alle URL'er set i søgeresultater) og visualiseringsdata. |
| `intermediate/corpus/` | Udtræk fra de 62.762 seed-filer (`docs.jsonl`: metadata og tekstfeatures), opløste referencer og lovfamilier (`resolved.json`), DocumentId-præfikser, udstedende ministerium, ressort-klassifikationen og de batches, Haiku/Opus klassificerede. |
| `raw/workflows/` | Rå resultater fra alle {len(list((WF / 'subagents' / 'workflows').glob('*/journal.jsonl')))} agent-workflows (én JSON-linje pr. agent med label og struktureret svar). |
| `pipeline/` | Al kode: fletning, verifikation, proveniensfilter, katalog, klassifikation, views, HTML og dashboard, plus workflow-scripts. Scriptsene forventer den oprindelige mappestruktur og workflow-stierne fra sessionen; brug dem som opskrift. |
| `harvest/` | Høster til Retsinformation (sitemap, XML, præambel/hjemmel, ministerium, EU-note), testet offline. Kræver adgang til www.retsinformation.dk og api.retsinformation.dk. |

## Ikke med

- Bulk-høstens 62.762 seed-filer (ca. 1,7 GB): hent dem fra github.com/Ansvar-Systems/danish-law-mcp (commit da22657b7aa604e0a900d69b2b60a7b0c424b0cb, `data/seed/`).
- Fuld lovtekst: kataloget har metadata og krydsreferencer; teksten ligger i seed-filerne eller hentes med `harvest/`.
- Sessionens samtale- og agent-transskripter.

## Licens og kilder

- Love, bekendtgørelser og andre offentlige aktstykker er ikke genstand for ophavsret (ophavsretslovens § 9). Bulk-høsten er Apache-2.0 (kode) og "DK-Statutory-PD" (data).
- Registry'ets påstande har egne kilder (URL'er set i søgeresultater) og sikkerhed (verificeret/sandsynlig/ukendt) pr. felt og kant.
- Katalog-kilderne er datasættets egne Retsinformation-URL'er.

## Filer ({len(rows)})

| Fil | Bytes | SHA-256 |
|---|---:|---|
""" + '\n'.join(f'| `{a[len(R):]}` | {n:,} | `{h[:16]}…` |'.replace(',', '.') for a, n, h in rows) + '\n'
with zipfile.ZipFile(OUT, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    z.writestr(R + 'MANIFEST.md', manifest)
    for a, s, _ in files: z.write(s, a)
print(OUT, f'{OUT.stat().st_size / 1e6:.1f} MB', len(files) + 1, 'filer', f'{sum(n for _, n, _ in rows) / 1e6:.0f} MB ukomprimeret')
