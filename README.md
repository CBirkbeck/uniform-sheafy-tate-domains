# Uniform sheafy Tate domains

This directory is a Paperforge instance for the paper
*Uniform sheafy Tate domains that are not stably uniform*.  The editable
source of truth remains the LaTeX draft:

- `inputs/draft/main.tex`
- `inputs/draft/lstlean_paper.tex`

Interactive edition:
<https://cbirkbeck.github.io/uniform-sheafy-tate-domains/>

The appendix now prints the Lean definitions of sheafiness and strong
noetherianity, gives the finite-jet pullback example, and explains how each
declaration corresponds to the mathematical notion used in the paper.  Long
proofs are linked rather than reproduced.

## Outputs

- `output/pdf/uniform_sheafy_tate_domains.pdf` — the primary 24-page AMS PDF.
- `output/arxiv/main.pdf` — Paperforge/PreTeXt's 11pt `amsart` PDF.
- `output/web/paper.html` — the interactive Paperforge edition.

The `output/` directory is generated and is intentionally ignored by Git.
The public GitHub Pages snapshot is generated under `docs/`.

## Build and check

The local Paperforge environment is `.paperforge-venv`.  From the repository
root, the complete build is:

```sh
scripts/build-paper.sh
```

The equivalent individual commands are:

```sh
(cd inputs/draft && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex)
source .paperforge-venv/bin/activate
paperforge doctor
paperforge build web
paperforge check
paperforge build arxiv --pdf
```

To refresh the GitHub Pages snapshot after a successful build:

```sh
scripts/sync-pages.sh
```

The external Paperforge checkout used for this pass is at commit
`726cc7d679441e28f39cfd52d3e2dd0251c79a6d`.  Its LaTeX ingester did not
preserve `\href` or `\url`, so the small tested compatibility patch is kept at
`patches/paperforge-href-support.patch`.  All 15 upstream tests pass with the
patch applied.

See `PAPERFORGE_CHECK.md` for the reference audit and `STYLE_REVIEW.md` for the
first author-voice pass.

## Lean source and publication note

The audited formalisation is the existing local AINTLIB worktree:

```text
branch: fjp/cdvf-lemma51
audited commit: b007a4f3d4226f00a684b402715aa542e2f0bcdc
project: projects/AdicSpaces
```

The appendix links every displayed declaration to that full commit.  At the
time of this build, however, GitHub did not serve that commit and the branch
was absent from `git ls-remote`.  The links are therefore publication targets,
not presently live links.  Before circulating the paper, publish the audited
commit (or create a permanent tag) and test the links again.  No AINTLIB
branch was pushed as part of this work.  Paperforge's automatic declaration
badges are intentionally inert until a doc-gen4 bundle for this snapshot is
published; the source-file links in the appendix remain visible.
