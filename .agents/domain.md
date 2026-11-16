# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

`docs/` in this repo is the source of the published site (the clone of bygningsreglementet.dk). Nothing for agents goes there: decision records live in `adr/` at the repo root, not `docs/adr/`.

## Before exploring, read these

- **`GLOSSARY.md`** at the repo root.
- **`adr/`** at the repo root: read the ADRs that touch the area you're about to work in.
- For work under `legoleze/`: **`legoleze/MANIFEST.md`** (what each file is and how it was made) and the `meta` block of **`legoleze/dk-regulering/registry.yaml`** (method, evaluation and known limits).

If `GLOSSARY.md` or `adr/` don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The `/domain-modeling` skill creates them lazily when terms or decisions actually get resolved, and must write ADRs to `adr/`.

## File structure

Single-context repo:

```
/
├── GLOSSARY.md
├── adr/
│   └── 0001-<decision>.md
├── docs/        ← published site source, not for agent docs
└── legoleze/
```

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `GLOSSARY.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal: either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/domain-modeling`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0007 (event-sourced orders), but worth reopening because…_
