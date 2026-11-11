# Retsinformation-høster

Henter Retsinformations dokument-XML i prioriteret rækkefølge og udtrækker metadata, præambel (hjemmel), EU-note, underskrift (udstedende myndighed) og tekst.

- Højst én forespørgsel pr. 10,5 s og kun i åbningstiden 03:00–23:45 dansk tid; backoff ved HTTP 429/5xx.
- Kan stoppes og genoptages: alt gemmes under `data/` (sitemap, plan, XML som .xml.gz, status, log).
- Prioritet: 1 Lovtidende A der mangler i bulk-høsten (efter 2026-02-12 og før 1852) · 2 gældende uden tekst · 3 øvrige gældende (hjemmel, ministerium, EU-note) · 4 andre serier (vejledninger, cirkulærer, skrivelser, FOB m.fl.) · 5 historiske.

Kræver adgang til `www.retsinformation.dk` og `api.retsinformation.dk`.

    ./run_harvest.sh /sti/til/danish-law-mcp/data/seed     # start/genoptag i baggrunden
    python3 harvest.py status                              # fremdrift
    python3 harvest.py fetch --max-pri 2                   # kun prioritet 1-2
    python3 harvest.py parse                               # XML -> data/parsed.jsonl
