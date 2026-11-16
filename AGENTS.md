# Goal
- we are making a local clone of https://bygningsreglementet.dk using zensical (formerly mkdocs-material)
- include downloadable files into the local clone as well
- crawling the page recursively should stop at the boundary of the domain i.e. include links to external references e.g. bygningsreglementet.dk has a link to dmi.dk, in which case we should not download any dmi.dk resources.
- we require information parity in non-historical pages of bygningsreglementet, though omitting "historisk" this only aims to clone the current active version of bygningsreglementet.

## development
- execute commands inside the nix devshell using `nix develop -c <command>`
- add programs to devshell in flake.nix when you need them
- manage python dependencies using uv (`nix develop -c uv ...`)
- prefer using bash tools over custom python scripts.

## references
use context 7 or the @librarian of simply websearch
- make full usage of the features in [zensical](https://zensical.org/docs/authoring/) to make a similar layout as the origin

## Agent skills

### Issue tracker

Issues live in Linear: team `Jgalabs`, label `br18`, project `Legoleze` for legoleze work. Open issues are the list of what to do next, also after a context compaction. See `.agents/issue-tracker.md`.

### Triage labels

The five default triage labels, in the Linear label group `triage`. See `.agents/triage-labels.md`.

### Domain docs

Single-context, with ADRs in `adr/` at the repo root because `docs/` is the published site. See `.agents/domain.md`.
