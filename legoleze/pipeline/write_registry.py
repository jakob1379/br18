#!/usr/bin/env python3
"""data/final.json -> dk-regulering/registry.yaml (with meta)."""
import json
from pathlib import Path

import yaml

SP = Path(__file__).resolve().parent
OUT = SP / "dk-regulering" / "registry.yaml"


class Dumper(yaml.SafeDumper):
    pass


def _str(dumper, data):
    style = "|" if "\n" in data else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


Dumper.add_representer(str, _str)

META = {
    "titel": "Kortlægning af dansk regulering: byggeri, bolig, plan, energi, miljø, arbejdsmiljø, brand, el/gas/VVS – plus katalog over hele Lovtidende A",
    "dato": "2026-10-28",
    "opdateret": "2026-11-02 (katalog-lag over al offentlig lovgivning i Lovtidende A)",
    "formaal": "Kortlægning (ikke indhentning) af myndigheder, retsakter, klage-/tilsynsveje, EU-retsakter og dokumentkilder "
               "til et krydsrefereret RAG-korpus (udvidelse af jakob1379/br18), så søgning kan følge hjemmelskæder "
               "lov → bekendtgørelse → vejledning → praksis.",
    "scope": {
        "domaener": ["byggeri", "bolig", "plan", "energi", "miljø", "arbejdsmiljø", "brand", "el/gas/VVS"],
        "niveauer": {"stat": "ja", "kommunalt": "ja (kommuner og regioner som aggregerede noder: kommune-alle, region-alle)", "eu": "ja"},
        "praksis": "ja (klagenævn, Ankestyrelsen, Ombudsmanden, domstole)",
        "standarder_og_branchevejledninger": "kun metadata",
        "note": "Scope-felterne i opgaven var ikke udfyldt. Første mulighed i hver parentes er valgt.",
        "udvidelse_2026_11": "Al offentlig lovgivning er relevant: hele Lovtidende A (love, lovbekendtgørelser, bekendtgørelser, anordninger) er med i katalog-laget (katalog/), uanset domæne. Registry'et forbliver den dybe, verificerede graf for de otte domæner.",
    },
    "katalog": {
        "filer": {"dokumenter": "katalog/retsinformation_lta.jsonl", "kanter": "katalog/kanter.jsonl", "eu_index": "katalog/eu_index.jsonl", "oversigt": "katalog/README.md (genereret)"},
        "kilde": "kilde-danish-law-mcp (https://github.com/Ansvar-Systems/danish-law-mcp, commit da22657b7aa604e0a900d69b2b60a7b0c424b0cb)",
        "id": "lta-<år>-<nummer> (Lovtidende A år og nummer, samme som ELI-stien /eli/lta/<år>/<nummer>)",
        "felter": "id, navn, type, kilder[ELI-XML-URL fra datasættet], status{vaerdi gældende|historisk, pr, sikkerhed}, identifikatorer{lovtidende, document_id, accession, unique_document_id, sikkerhed}, "
                  "datoer{udstedt, historisk_markeret, ri_registreret, ri_aendret}, territorium (DK/GL/FO/GL+FO ud fra titlen), dokumentrolle (hoved/ændring/ikrafttræden/ophævelse), udstedt_af{vaerdi, metode, praefiks, sikkerhed}, ministerium{vaerdi, sikkerhed, metode} og retsomraade/domaener (kun gældende), "
                  "gaeldende_version / nyeste_version_afloeser_mangler / afloeser_mangler, aendrer[], eu_referencer[], registry_ids[], seed_fil, n_paragraffer, n_definitioner",
        "kanter": "Samme kanttyper og påstandsstruktur som registry'et: henviser_til (lov/dokument/EU-retsakt nævnt i teksten; mål = citeret version ved nr.+dato, ellers versionen der gjaldt ved udstedelsen, med gaeldende_version ved siden af), implementerer_EU (direktiv + gennemførelsesudsagn i samme bestemmelse), ressortansvar (ministerium → gældende dokument; fra registry-noden når den findes, ellers klassifikation). Endepunkter er katalog-id'er, registry-id'er eller eu_index-id'er.",
        "sikkerhed": "verificeret = står direkte i datasættets felter eller tekst (status, Lovtidende-nr., henvisning med nummer og dato, EU-retsakt nævnt). sandsynlig = udledt (udstedende ministerium fra DocumentId-præfiks, titel-/navnematch, ressort klassificeret af Haiku, implementerer_EU fra samforekomst). ukendt = intet grundlag.",
        "datoer_note": "Den reelle ikrafttrædelsesdato findes ikke i bulk-kilden (ukendt). ri_registreret er datasættets start_date/in_force_date (Retsinformations databasedato; for dokumenter fra før 1990 typisk en dato i 1990'erne), ri_aendret er end_date med udokumenteret betydning – ingen af dem må bruges som gyldighedsperiode.",
    },
    "metode": [
        "Fase 1: To uafhængige agenter kortlagde regering, ministerier og område → myndighed pr. 2026-10-28. En tredje afstemte dem til en baseline med kanoniske id'er.",
        "Fase 2: 13 domæner (byggeri, bolig, plan, energi, miljø, natur-vand-kyst, arbejdsmiljø, brand, el-gas-vvs, klage-tilsyn-praksis, eu, datakilder-standarder, kommunalt). Hvert domæne fik én research-agent og to uafhængige adversarielle verifikatorer: en for organisation/ressort/hjemmel/klageveje og en for kilder/URL'er/identifikatorer. En konsolidator anvendte rettelserne som patch.",
        "Fase 3: Noder fra alle domæner er flettet på id. Feltværdier blev valgt efter højeste sikkerhed, og kilderne er slået sammen. Kendte dublet-id'er er aliaseret.",
        "Fase 4: Udfyldning af kanoniske URL'er, ELI og CELEX samt adgang for noder uden fundne kilder. Derefter en completeness-kritiker pr. ministerområde, som tilføjede manglende noder og kanter med kilde.",
        "Fase 5: Alle påstande med sikkerhed sandsynlig eller ukendt er efterprøvet node for node i 75 batches med cirka 25 søgninger hver. Generelle forhold er belagt én gang pr. nodeklasse med officielle kilder; feltet 'regel' viser hvilken regel. Det gælder ophavsretslovens § 9, EU's genbrugsregler og opdatering/adgang på Retsinformation og EUR-Lex.",
        "Proveniens: Alle kilde-URL'er er tjekket mod de URL'er, der faktisk optrådte i sessionens søgeresultater. Kilder, der ikke optrådte, er fjernet, og påstanden er nedgraderet.",
        "Fase 6 (katalog): Alle 62.762 seed-filer i danish-law-mcp er læst lokalt (ingen websøgning). Dokumenttype, Lovtidende-nr., status og datoer er taget direkte fra datasættet. Udstedende ministerium er udledt af DocumentId-præfikset og ministertitler i teksten. Nuværende ressort og retsområde for gældende dokumenter er klassificeret af Haiku-agenter (effort high) med en ressortguide for kgl. res. 3/6/2026. Krydsreferencer er udtrukket med regex og titelmatch mod lovfamilier. Registry-noderne er koblet til katalogposter, og 14 forældede versionshenvisninger er markeret eller rettet. Katalog-kilderne er datasættets egne URL'er og falder uden for proveniensfilteret, som kun gælder søgeresultater.",
    ],
    "begraensninger": [
        "WebFetch var blokeret af sessionens netværkspolitik for alle eksterne domæner, herunder retsinformation.dk, eur-lex.europa.eu og ministeriernes sider. Al evidens stammer derfor fra WebSearch-resultater (titel, URL, uddrag). En URL markeret verificeret er set i et søgeresultat, men siden er ikke åbnet direkte.",
        "URL'er er aldrig konstrueret. Er en side ikke set i søgeresultater, står der 'ikke fundet', også når et mønster (fx ELI) gør adressen forudsigelig.",
        "ELI'erne for 16 love/bekendtgørelser stammer fra jakob1379/br18 xref-laws.toml, tjekket mod retsinformation 2026-10-26.",
        "Katalog-laget dækker kun Lovtidende A til og med udstedelser 2026-02-12 og mangler præambel, underskrift og EU-noter; hjemmel_for er derfor ikke udledt for katalog-dokumenter.",
        "Ressortforhold ændrer sig ofte. Seneste kendte ændringer er regeringsdannelsen 2026-06-03 (BEK nr. 514 af 08/06/2026) og ministerskiftet 2026-10-27. Se 'ressortomlaegninger' og 'uafklarede_konflikter'.",
    ],
    "sikkerhed": {
        "verificeret": "Fremgår direkte af et søgeresultat fra en officiel/primær kilde (retsinformation.dk, lovtidende.dk, ft.dk, myndighedens eget domæne, eur-lex) eller af to uafhængige troværdige sekundærkilder, og afspejler tilstanden pr. 2026-10-28.",
        "sandsynlig": "Én sekundærkilde, en officiel kilde der kan være forældet, eller en stærk faglig slutning (forklaret i note).",
        "ukendt": "Ingen evidens fundet.",
    },
    "kanttyper": {
        "ressortansvar": "ministerium → instans/lov: ministeriet har ressortansvaret",
        "delegation": "ministerium/styrelse → styrelse/kommune: kompetence delegeret (delegationsbekendtgørelse i beskrivelse)",
        "hjemmel_for": "lov/bekendtgørelse → bekendtgørelse/vejledning/instans/plan: giver hjemmel til / opretter",
        "udsteder": "instans → retsakt/vejledning/dokumentkilde: udsteder, udgiver eller driver",
        "klageinstans": "klageinstans → førsteinstans: from behandler klager over to's afgørelser (lov i beskrivelse)",
        "tilsyn": "tilsynsmyndighed → tilsynsobjekt",
        "implementerer_EU": "dansk retsakt → EU-retsakt",
        "henviser_til": "dokument → dokument: typisk krydsreference i teksten",
    },
    "felter": {
        "noder": "id, navn, type, ministerium (id eller 'ingen'), status, domaener, tidligere_navne[], hjemmel, dokumenttyper, url, adgang, identifikatorer, licens, opdatering, krydsref_moenstre[], ingest{vaerdi,besvaer,begrundelse}, note, baseline{kilder,sikkerhed}",
        "paastandsfelter": "hjemmel, dokumenttyper, url, adgang, identifikatorer, licens, opdatering og hver tidligere_navne-post har egne kilder[] og sikkerhed. Det samme gælder hver kant.",
        "ingest": "vaerdi 1-5 (nytte for RAG/hjemmelskæder) og besvaer 1-5 (1 = API/bulk med åben licens, 5 = betalingsmur/scannede PDF'er). Prioritet = vaerdi ÷ besvaer.",
    },
    "id_konventioner": {
        "ministerier": "min-<slug>", "styrelser/direktorater": "sty-<slug>", "nævn": "naevn-<slug>", "tilsyn": "tilsyn-<slug>",
        "råd": "raad-<slug>", "fonde": "fond-<slug>", "domstole": "dom-<slug>", "ombudsmand": "ombud-<slug>", "øvrige organisationer": "org-<slug>",
        "love": "lov-<kortnavn> (én node pr. lov; identifikatorer peger på gældende LBK/LOV)", "bekendtgørelser": "bek-<kortnavn>",
        "vejledninger": "vejl-<slug> (samlinger som én node)", "tekniske forskrifter": "tf-<slug>", "planer": "plan-<slug>", "regulativer": "reg-<slug>",
        "EU": "eu-dir-ÅÅÅÅ-N, eu-reg-ÅÅÅÅ-N, eu-dec-ÅÅÅÅ-N", "dokumentkilder": "kilde-<slug>", "standarder": "std-<slug>", "branchevejledninger": "bv-<slug>",
        "kommunalt": "kommune-alle, region-alle (aggregerede)",
    },
}


def main():
    m = json.load(open(SP / "data" / "final.json"))
    bl = m["baseline"]
    reg = {
        "meta": META,
        "regering": bl["regering"],
        "ressortomlaegninger": bl["ressortomlaegninger"],
        "uafklarede_konflikter": bl["uafklarede_konflikter"],
        "nodes": m["nodes"],
        "edges": m["edges"],
        "huller": m["huller"],
    }
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", encoding="utf-8") as fh:
        fh.write("# Kortlægning af dansk regulering – registry (sandheden). Genereret 2026-10-28.\n"
                 "# Diagrammer, datakilder.md og huller.md genereres herfra med scripts/build.py.\n")
        yaml.dump(reg, fh, Dumper=Dumper, allow_unicode=True, sort_keys=False, width=140, default_flow_style=False)
    print(OUT, OUT.stat().st_size)


if __name__ == "__main__":
    main()
