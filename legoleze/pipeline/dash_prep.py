#!/usr/bin/env python3
"""Coverage dashboard datasets -> dash/{omraader,maalt,vurderet,fremdrift,mangler}.json"""
import json, os, glob
from collections import Counter, defaultdict
from pathlib import Path
SP = Path(__file__).resolve().parent
OUT = SP / "dash"; OUT.mkdir(exist_ok=True)
KD = SP / "dk-regulering" / "katalog"
WF = Path('/root/.claude/projects/-home-user-ai-job-search-fork/9c9ad245-1536-5d87-980d-1a4837c57ed1/subagents/workflows')
GROUPS = [
    ("Stat og forvaltning", [("statsret", "Statsret"), ("kommuner", "Kommuner og regioner"), ("valg", "Valg"), ("offentlig-oekonomi", "Offentlig økonomi og personale"), ("digitalisering-tele", "Digitalisering og tele"), ("persondata", "Persondata")]),
    ("Ret, sikkerhed og udland", [("strafferet-politi", "Strafferet og politi"), ("retspleje", "Retspleje og domstole"), ("familie-person", "Familie- og personret"), ("forsvar", "Forsvar"), ("beredskab-brand", "Beredskab og brand"), ("udlaendinge", "Udlændinge og integration"), ("international", "Internationale aftaler")]),
    ("Erhverv, økonomi og transport", [("erhvervsret", "Erhvervsret"), ("finansiel", "Finansiel regulering"), ("skat", "Skat og afgifter"), ("forbruger-konkurrence", "Forbruger og konkurrence"), ("soefart", "Søfart"), ("transport", "Transport")]),
    ("Arbejde, velfærd og sundhed", [("arbejdsmarked", "Arbejdsmarked og ydelser"), ("arbejdsmiljoe", "Arbejdsmiljø"), ("social", "Social"), ("aeldre", "Ældre"), ("boern-dagtilbud", "Børn og dagtilbud"), ("sundhed", "Sundhed")]),
    ("Uddannelse, kultur og kirke", [("undervisning", "Undervisning"), ("forskning-videregaaende", "Forskning og videregående uddannelse"), ("kultur-medier", "Kultur og medier"), ("kirke", "Kirke og trossamfund")]),
    ("Byggeri, bolig og plan", [("byggeri", "Byggeri"), ("bolig", "Bolig"), ("plan-landdistrikter", "Plan og landdistrikter")]),
    ("Energi, klima og forsyning", [("energi-forsyning", "Energi og forsyning"), ("klima", "Klima"), ("el-gas-vvs", "El, gas og VVS")]),
    ("Miljø, natur og fødevarer", [("miljoe", "Miljø"), ("affald", "Affald"), ("natur-vandmiljoe", "Natur og vandmiljø"), ("landbrug-dyr", "Landbrug og dyr"), ("foedevarer", "Fødevarer"), ("fiskeri", "Fiskeri")]),
    ("Øvrigt", [("andet", "Andet"), ("ikke-klassificeret", "Endnu ikke klassificeret")]),
]
NAVN = {c: l for _, it in GROUPS for c, l in it}
DOMAIN_AREAS = {"byggeri", "bolig", "plan-landdistrikter", "energi-forsyning", "klima", "el-gas-vvs", "miljoe", "affald", "natur-vandmiljoe", "arbejdsmiljoe", "beredskab-brand"}
REGT = {"bekendtgørelse", "ændringsbekendtgørelse", "ikrafttrædelsesbekendtgørelse", "anordning", "ændringsanordning", "ikrafttrædelsesanordning", "bekendtgørelse-af-anordning"}
reg = json.load(open(SP / "data" / "final.json"))
RQ = json.load(open(SP / "data" / "ressort_quality.json")) if (SP / "data" / "ressort_quality.json").exists() else {}
kat_hjemmel = set()
nodes = {n["id"]: n for n in reg["nodes"]}
for e in reg["edges"]:
    if e["type"] == "hjemmel_for" and nodes.get(e["to"], {}).get("katalog_id"): kat_hjemmel.add(nodes[e["to"]]["katalog_id"])
docs = [json.loads(l) for l in open(KD / "retsinformation_lta.jsonl", encoding="utf-8")]
ef = defaultdict(set)
for l in open(KD / "kanter.jsonl", encoding="utf-8"):
    e = json.loads(l)
    if e["type"] == "henviser_til" and e["to"].startswith("lta-") and e.get("beskrivelse", "").startswith("nævner loven"): ef[e["from"]].add("lov")
gd = [d for d in docs if d["status"]["vaerdi"] == "gældende"]
A = defaultdict(Counter)
for d in gd:
    a = d.get("retsomraade") or "ikke-klassificeret"
    A[a]["alle"] += 1
    if d.get("territorium") != "DK": A[a]["gl_fo"] += 1; continue
    if d.get("dokumentrolle") != "hoved": A[a]["aendr_ikraft"] += 1; continue
    c = A[a]; c["n"] += 1
    c["udsteder"] += d["udstedt_af"]["vaerdi"] != "ukendt"
    c["ressort"] += (d.get("ministerium") or {}).get("sikkerhed") == "sandsynlig"
    c["lovhenv"] += "lov" in ef[d["id"]]
    c["registry"] += bool(d.get("registry_ids"))
    if d["type"] in REGT:
        c["reg"] += 1; c["hjemmel"] += d["id"] in kat_hjemmel
    c["love"] += d["type"] in ("lov", "lovbekendtgørelse", "ændringslov")
pct = lambda a, b: round(100 * a / b) if b else None
omr, maalt = [], []
LAG_M = [("udsteder", "Udsteder kendt"), ("ressort", "Ressort klassificeret"), ("lovhenv", "Lovhenvisninger"), ("hjemmel", "Hjemmel kendt"), ("registry", "Koblet til registry")]
order = 0
for g, items in GROUPS:
    for code, label in items:
        c = A.get(code, Counter()); order += 1
        omr.append({"omraade": code, "navn": label, "gruppe": g, "orden": order, "gaeldende": c["n"], "gaeldende_alle": c["alle"], "gl_fo": c["gl_fo"], "aendring_ikraft_ophaev": c["aendr_ikraft"],
                    "love": c["love"], "regulering": c["reg"],
                    "dybde_domaene": code in DOMAIN_AREAS})
        for k, lab in LAG_M:
            den = c["reg"] if k == "hjemmel" else c["n"]
            maalt.append({"omraade": code, "lag": k, "lag_navn": lab, "daekning": pct(c[k], den), "taeller": c[k], "naevner": den})
# judged layers (Opus audit); null until the audit has returned
LAG_V = [("myndigheder", "Myndigheder"), ("klage_tilsyn", "Klage og tilsyn"), ("vejledninger", "Vejledninger"), ("praksis", "Praksis"), ("eu_kobling", "EU-kobling"), ("kommunalt", "Kommunalt")]
audit = {}; mangler = []; audit_done = False
J = WF / "wf_6bf57053-453" / "journal.jsonl"
if J.exists():
    labels = {}
    for l in open(J):
        x = json.loads(l)
        if x.get("type") == "started": labels[x["agentId"]] = x.get("label")
        if x.get("type") == "result" and x.get("result"):
            lab = labels.get(x["agentId"], "")
            if lab == "syntese:matrix":
                for c in x["result"]["celler"]: audit[(c["omraade"], c["lag"])] = c
            if lab == "syntese:mangler":
                audit_done = True
                for i, m in enumerate(sorted(x["result"]["mangler"], key=lambda m: -m["prioritet"])):
                    mangler.append({"id": f"m{i + 1:03d}", "prioritet": m["prioritet"], "omraade": m["omraade"], "omraade_navn": NAVN.get(m["omraade"], "Tværgående" if m["omraade"] == "tvaergaaende" else m["omraade"]), "kategori": m["kategori"], "emne": m["emne"],
                                    "tilgaengelighed": m["tilgaengelighed"], "volumen": m["volumen"], "naeste_skridt": m["naeste_skridt"], "sikkerhed": m["sikkerhed"],
                                    "beskrivelse": m["beskrivelse"]})
STATUS = [
    ("m.v.'-normaliseringen", "løst", "Rettet 2. nov.: titelnøgler og fraser normaliseres ens; umatchede 'lov om …'-fraser faldt fra 13.187 til {lovom}."),
    ("Henvisninger samles til nyeste version", "løst", "Kanter peger nu på den citerede version (nr.+dato) eller versionen der gjaldt ved udstedelsen; nuværende version står i gaeldende_version."),
    ("implementerer_EU", "delvist", "Kun direktiver med et gennemførelsesudsagn i samme bestemmelse giver implementerer_EU; forordninger får henviser_til. Citater uden '(EU) nr.' er stadig åbne."),
    ("Fejl i ressortguiden", "delvist", "De usikre er genklassificeret af Opus med skærpet guide, og titelregler retter ressortfordeling og dobbeltbeskatning. Stikprøve: {ok} % korrekt ministerium."),
    ("Grundlaget for heatmappet", "løst", "Heatmappet er genberegnet efter fuld klassifikation og tæller kun normative danske dokumenter; registry-dybden vurderes pr. unik node."),
    ("Territorium er ikke markeret", "delvist", "Feltet territorium (DK/GL/FO) er udledt af titlen, og heatmappet tæller kun DK. Kanttypen for ikrafttræden i Grønland/Færøerne er ikke tilladt; anordningerne peger i stedet på loven med henviser_til."),
    ("overvurderer reguleringen", "delvist", "Feltet dokumentrolle (hoved/ændring/ikrafttræden/ophævelse) er tilføjet, og heatmappet tæller kun hoveddokumenter. Tidsbegrænsede ordninger er ikke markeret."),
    ("Linkeren mellem registry og katalog", "løst", "Lovtidende-nummeret bruges før ELI, ændringsdokumenter afvises for lov/bek-noder, og råd/tilsyn kobles ikke længere til en retsakt."),
    ("Feltet 'ikraft'", "delvist", "Felterne er omdøbt til ri_registreret og ri_aendret; den reelle ikrafttræden kræver ELI-XML."),
    ("Versionskæder for bekendtgørelser", "delvist", "Ændrings- og ikrafttrædelsesdokumenter peger nu på det, de ændrer eller sætter i kraft. Ophæver/afløser er ikke tilladte kanttyper og mangler."),
    ("Klassifikationens fejlrate", "delvist", "Målt i en uafhængig Opus-stikprøve på {n}: {ok} % korrekt ministerium og {omr} % korrekt retsområde."),
]
RS = json.load(open(SP / "corpus" / "data" / "resolved.json")).get("stats", {})
for m in mangler:
    m["status"], m["status_note"] = "åben", ""
    for key, st, note in STATUS:
        if key in m["emne"]:
            m["status"] = st
            m["status_note"] = note.format(lovom=f"{RS.get('lovom_unmatched', 0):,}".replace(",", "."), ok=RQ.get("sample_ok_pct", "?"), n=RQ.get("sample_n", "?"), omr=RQ.get("sample_omr_ok_pct", "?"))
            break
vurderet = []
for o in omr:
    if o["omraade"] == "ikke-klassificeret": continue
    for k, lab in LAG_V:
        c = audit.get((o["omraade"], k))
        vurderet.append({"omraade": o["omraade"], "lag": k, "lag_navn": lab, "daekning": c["daekning"] if c else None,
                         "har": c["har"] if c else "", "mangler": c["mangler"] if c else "", "sikkerhed": c["sikkerhed"] if c else "afventer"})
batches = len(glob.glob(str(SP / "corpus" / "jobs" / "ressort" / "batch_*.jsonl")))
done_ids = json.load(open(SP / "corpus" / "data" / "ressort.json")) if (SP / "corpus" / "data" / "ressort.json").exists() else {}
inp = {}
for f in glob.glob(str(SP / "corpus" / "jobs" / "ressort" / "batch_*.jsonl")):
    for l in open(f): inp[json.loads(l)["id"]] = f
done_batches = sum(1 for f in set(inp.values()) if all(i in done_ids for i, ff in inp.items() if ff == f))
klass = sum(1 for d in gd if d.get("retsomraade"))
CF = ("hjemmel", "dokumenttyper", "url", "adgang", "identifikatorer", "licens", "opdatering")
cert = Counter(n[f]["sikkerhed"] for n in reg["nodes"] for f in CF) + Counter(e["sikkerhed"] for e in reg["edges"])
fremdrift = [
    {"metric": "katalog_dokumenter", "navn": "Dokumenter i Lovtidende A-kataloget", "vaerdi": len(docs), "total": None},
    {"metric": "katalog_gaeldende", "navn": "Gældende dokumenter", "vaerdi": len(gd), "total": len(docs)},
    {"metric": "normative_dk", "navn": "Gældende normative dokumenter for Danmark (uden ændrings-, ikrafttrædelses- og ophævelsesdokumenter og uden Grønland/Færøerne)",
     "vaerdi": sum(1 for d in gd if d.get("territorium") == "DK" and d.get("dokumentrolle") == "hoved"), "total": len(gd)},
    {"metric": "klass_sikker_pct", "navn": "Stikprøve: ministerium korrekt (%)", "vaerdi": RQ.get("sample_ok_pct"), "total": 100},
    {"metric": "klassificeret", "navn": "Gældende dokumenter med ressort og retsområde", "vaerdi": klass, "total": len(gd)},
    {"metric": "klassificeret_pct", "navn": "Andel klassificeret (%)", "vaerdi": round(100 * klass / len(gd)), "total": 100},
    {"metric": "batches", "navn": "Klassifikationsbatches færdige", "vaerdi": done_batches, "total": batches},
    {"metric": "registry_noder", "navn": "Noder i registry", "vaerdi": len(reg["nodes"]), "total": None},
    {"metric": "registry_verificeret_pct", "navn": "Registry-påstande verificeret (%)", "vaerdi": round(100 * cert["verificeret"] / sum(cert.values())), "total": 100},
    {"metric": "dybde_omraader", "navn": "Retsområder med registry-dybde", "vaerdi": len(DOMAIN_AREAS), "total": sum(len(i) for _, i in GROUPS) - 1},
    {"metric": "audit_faerdig", "navn": "Opus-audit færdig (1 = ja)", "vaerdi": 1 if audit_done else 0, "total": 1},
    {"metric": "mangler", "navn": "Mangler fundet af Opus-audit", "vaerdi": len(mangler) if audit_done else None, "total": None},
    {"metric": "mangler_p5", "navn": "Heraf prioritet 5", "vaerdi": sum(1 for m in mangler if m["prioritet"] == 5) if audit_done else None, "total": None},
    {"metric": "mangler_loest", "navn": "Mangler løst eller delvist løst", "vaerdi": sum(1 for m in mangler if m.get("status") != "åben") if audit_done else None, "total": len(mangler) if audit_done else None},
]
for name, rows in (("omraader", omr), ("maalt", maalt), ("vurderet", vurderet), ("fremdrift", fremdrift), ("mangler", mangler)):
    (OUT / f"{name}.json").write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
print({k: len(v) for k, v in (("omraader", omr), ("maalt", maalt), ("vurderet", vurderet), ("mangler", mangler))}, "klass", klass, "batches", done_batches, "/", batches, "audit", audit_done)
