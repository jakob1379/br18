# Goal
- we are making a local clone of https://bygningsreglementet.dk using zensical (formerly mkdocs-material)
- include downloadable files into the local clone as well
- crawling the page recursively should stop at the boundary of the domain i.e. include links to external references e.g. bygningsreglementet.dk has a link to dmi.dk, in which case we should not download any dmi.dk resources.

## development
- execute commands inside the nix devshell using `nix develop -c <command>`
- add programs to devshell in flake.nix when you need them
- manage python dependencies using uv (`nix develop -c uv ...`)
- prefer using bash tools over custom python scripts, unless the gains are substantial
