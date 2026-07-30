# Uniform sheafy Tate domains

This directory is a Paperforge instance for the paper
*Uniform sheafy Tate domains that are not stably uniform*.  The editable
source of truth remains the LaTeX draft:

- `inputs/draft/main.tex`
- `inputs/draft/lstlean_paper.tex`

Interactive edition:
<https://cbirkbeck.github.io/uniform-sheafy-tate-domains/>

The appendix prints the finite-rational-cover definition of sheafiness, its
all-open equivalent, the completion- and plus-ring-independent variants,
strong noetherianity, and the two example constructions.  For the
weighted-parity example it distinguishes the verified uniformity, sheafiness,
domain chart, and failure of stable uniformity from the still incomplete
iterated-reducedness argument.  It also credits the Coram/Xia
restricted-series infrastructure.

## Outputs

- `output/pdf/uniform_sheafy_tate_domains.pdf` — the primary AMS PDF.
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
python3 scripts/build-lean-knowls.py .
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

The interactive code is extracted from two audited local AINTLIB snapshots:

```text
finite-jet branch: fjp/cdvf-lemma51
finite-jet commit: b007a4f3d4226f00a684b402715aa542e2f0bcdc
weighted-parity branch: wp/reduced-example
weighted-parity commit: 090a289211deb69117413e329325fe819aa7dbc2
project: projects/AdicSpaces
```

At the time of this build, GitHub did not serve either pinned snapshot.  To
keep the interactive paper usable, `scripts/build-lean-knowls.py` extracts
each declaration from the Git object recorded for that declaration.  Every
Paperforge Lean badge opens that code inline, Roe-style, and its ordinary link
opens a standalone archival declaration page under
`lean/AdicSpaces/declarations/`.  The reducedness theorem for all finite
iterated rational localisations has no completion badge because its current
Lean endpoints still depend on `sorryAx`.

Before archival publication, both AINTLIB snapshots should be published under
permanent branches or tags.  No AINTLIB branch is pushed by the paper build.
