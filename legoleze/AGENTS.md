# legoleze: working conventions

A map of Danish authorities and legal sources. `MANIFEST.md` says what each file is; the `meta` block of `dk-regulering/registry.yaml` says how the data was made and what its limits are. Read the part that covers your area before you change it.

## Source and generated files

- **Source**: `dk-regulering/registry.yaml` (the registry, written only by `pipeline/populate.py` or by hand), `pipeline/`, `raw/`, `dk-regulering/eval/rettelser.json`, `dk-regulering/eval/instruks.md`, `dashboard/mangler.json` (one line of JSON; keep it one line).
- **Generated**: everything under `dk-regulering/katalog/`, `dk-regulering/README.md`, `huller.md`, the diagrams, `reguleringskort.html`, `intermediate/registry/`, `dk-regulering/eval/README.md` and `facit.jsonl`. Change the generator, then regenerate.

After a change, regenerate in this order and commit the result with the change:

1. `eksport.py katalog` when the registry's nodes, the readers or the catalog code changed
2. `eval.py saml` then `eval.py maal x` when answers, corrections or catalog edges changed
3. `bash pipeline/views.sh`
4. `python dk-regulering/scripts/build.py --check` must print `OK`

## Running things

Run from `legoleze/`, with this prefix for every Python script and for `views.sh`:

    env UV_CACHE_DIR=$TMPDIR/uv-cache uv run -q --offline --no-project --with pyyaml==6.0.3 python pipeline/corpus/eksport.py katalog
    env UV_CACHE_DIR=$TMPDIR/uv-cache uv run -q --offline --no-project --with pyyaml==6.0.3 bash pipeline/views.sh

Each script lists its commands in its docstring and has a `selftest` command. New logic gets a case in the module's `selftest`; run the selftest of every module you touched. Lint with `nix develop -c ruff check <files>`; `dk-regulering/scripts/build.py` has two old findings that stay.

## Fetching from Retsinformation

- Every call goes through `populate.get`: one call per 10.5 seconds under a lock shared by all sessions, cached for 7 days. A second fetching job waits for the first; plan for it.
- Fetch only between 03:00 and 23:45 Danish time.
- Use only addresses and API routes that already appear in the code or that a fetched page links to. When a source cannot be found, write "ikke fundet".
- Keep the client's own User-Agent.
- A command that fetches needs the host allowed in the sandbox (`www.retsinformation.dk`).

## Claims in the registry

- Every node and edge has a source and a certainty mark: `verificeret`, `sandsynlig` or `ukendt`. `verificeret` needs a verbatim quote that `populate.py apply` has checked against the source.
- Edge types: `ressortansvar`, `delegation`, `hjemmel_for`, `udsteder`, `klageinstans`, `domstolsproevelse`, `tilsyn`, `implementerer_EU`, `henviser_til`. A `klageinstans` edge between authorities runs from the complaint body to the deciding body.
- `domstolsproevelse` is court review of a decision by an authority or board, and runs from the court to the body or the act. It is not a complaint: use it only where an act gives a special route (a named court, a deadline, a right to demand the case brought, or a duty on the authority). An appeal from one court to another stays `klageinstans`.
- An abolished or renamed body is recorded on its successor with "tidligere navn".
- Registry text is in Danish.
- `populate.py apply` writes the findings file's `omraade` as the edge's domain tag; replace it with real domain tags afterwards.
- A data gap that stays open goes in the registry's `huller` list.

## Git

Large files are in Git LFS, so run git inside the dev shell, outside the sandbox:

    nix develop -c bash -c 'git add legoleze && git commit -q -F <message file>'

Stage `legoleze` (or named paths), never everything. Conventional commit messages. Pushing is the user's step.
