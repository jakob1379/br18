# BR18

A local copy of [bygningsreglementet.dk](https://www.bygningsreglementet.dk/), the Danish building regulations (Bygningsreglementet 2018), rebuilt as a static [Zensical](https://zensical.org/) site that you can build and read offline.

<p align="center">
  <img src=".github/assets/br18-pipeline.svg" width="100%" alt="Diagram: pages from bygningsreglementet.dk are fetched, converted to Markdown, cross-linked by paragraph reference and built with zensical build --strict. Each finished page lights up the part of a building section it regulates: Konstruktioner (§ 340–357), Brand (§ 82–158), Lys og udsyn (§ 377–384) and Ventilation (§ 420–452).">
</p>

The goal is information parity with the current, non-historical regulation: every page, tab and downloadable file the origin serves, in a layout close to the original. The authoritative text is still the one on bygningsreglementet.dk.

## What you get

- **The full regulation as Markdown** under `docs/`: administrative, technical and other provisions, penalties and commencement, annexes (bilag), national annexes and guides (vejledninger). That is about 1,200 pages.
- **The downloadable files** (PDFs, spreadsheets, images) the pages link to, mostly in `docs/media/`. Files on other sites stay external links.
- **Linked § references.** References like `§ 82` or `byggelovens § 16` link to the right BR18 section or to the current version of the law on retsinformation.dk.
- **Stable anchors.** The anchors listed in `required-anchors.tsv` are kept, so deep links into the clone keep working.
- **A strict build.** `zensical build --strict`, an anchor and reference check, and `lychee` link checking all run on every build.

## Quick start

Everything runs inside the Nix dev shell, which provides `uv`, `lychee`, `pandoc`, Chromium and the other tools. Python dependencies are managed with `uv` (Python 3.14).

```bash
# build the site into site/ and run every check
nix develop -c ./scripts/build-docs.sh

# preview locally
nix develop -c uv run zensical serve
```

Set `CHECK_EXTERNAL_LINKS=1` to let `lychee` check external links too. By default it runs with `--offline`.

## How the clone is made

The pipeline in the diagram above, one script per step:

| Step | Script | What it does |
| --- | --- | --- |
| Fetch | `scripts/fetch_origin_pages.py` | Downloads origin pages, throttled, or reads them from an audit snapshot (`--cache-dir`). |
| Convert | `scripts/convert_br18_docs.py` | Turns the origin HTML into Zensical Markdown, including tables and Krav/Vejledning tabs. |
| Chapter hubs | `scripts/build_chapter_hubs.py` | Rebuilds the chapter landing pages. |
| Link references | `scripts/link_references.py` | Links `§` references to BR18 sections and to laws on retsinformation.dk. |
| Keep anchors | `scripts/keep_anchors.py` | Restores anchors listed in `required-anchors.tsv`. |
| Fix links | `scripts/fix_broken_links.py` | Repairs internal links, including links the origin itself gets wrong. |
| Sync files | `scripts/sync_referenced_files.py` | Downloads the files pages reference; `--check-versions` fetches again any file whose origin version differs from `media-versions.tsv`. |
| Audit | `scripts/audit_br18_parity.py` | Compares the clone with the origin page by page and writes a parity report. |
| Check | `scripts/check_references.py` | Verifies linked references; `--laws-online` checks that linked laws are still current. |

`scripts/regenerate_docs.sh` chains these steps for part of the corpus:

```bash
# regenerate one chapter from the live origin
nix develop -c ./scripts/regenerate_docs.sh tekniske-bestemmelser/15

# or from a parity audit snapshot, without hitting the origin
nix develop -c ./scripts/regenerate_docs.sh --cache-dir .cache/parity-origin tekniske-bestemmelser/15
```

## Reviewed data files

Decisions that a rule cannot make are kept as reviewed data in the repository root:

| File | Holds |
| --- | --- |
| `xref-laws.toml` | Laws that references link to, with their current ELI URL and paragraph ids. |
| `xref-page-scope.toml` | The default law for bare `§ N` references, by docs path. |
| `xref-overrides.toml` | Per-page decisions for references the rules get wrong. |
| `xref-unresolved.tsv` | References that stay unlinked. |
| `required-anchors.tsv` | Anchors the build must keep. |
| `parity-allowlist.toml` | Reviewed exceptions to the parity audit, each with a reason. |
| `origin-dead-links.toml` | Links that 404 on the origin, mapped to the page the clone links instead. |
| `local-pages.txt` | Pages the clone has that the origin does not serve. |
| `media-versions.tsv` | The origin version of each downloaded file. |

## Tests and CI

```bash
nix develop -c uv run python -m unittest discover -s tests
```

GitHub Actions builds the site with `scripts/build-docs.sh` on every pull request and push to `main`. A weekly job checks external links and whether the linked laws are still the current versions on retsinformation.dk.

## Credits

The regulation text, figures and downloadable files are published by Social- og Boligstyrelsen on [bygningsreglementet.dk](https://www.bygningsreglementet.dk/). This repository only mirrors them and builds them with [Zensical](https://zensical.org/).
