# Uniform sheafy Tate rings

This directory is a Paperforge instance for the paper
*Uniform sheafy Tate rings that are not stably uniform*.  The editable
source of truth remains the LaTeX draft:

- `inputs/draft/main.tex`
- `inputs/draft/lstlean_paper.tex`

Interactive edition:
<https://cbirkbeck.github.io/uniform-sheafy-tate-domains/>

The appendix prints the finite-rational-cover definition of sheafiness, its
all-open equivalent, the completion- and plus-ring-independent variants,
strong noetherianity, and the two example constructions.  For both examples
it records the completed formalisation of uniformity, sheafiness, the
distinguished rational chart, and failure of stable uniformity.  It also
records the formalised finite-jet witnesses for Scottish Book Problems 24
and 28, together with the strong-sheafiness theorems for both examples.  The
finite-jet strong theorem currently uses the Laurent-series model, while the
weighted-parity theorem has the paper's DVR-base scope.  The other declarations
use an abstract complete ultrametric base with a
chosen pseudouniformizer, with both Laurent-series and p-adic instances.  The
appendix keeps this separate from the additional noetherian-base hypothesis
used by the newer sheafiness interface.  It also credits William Coram's
restricted-series code, Fabrizio Barroero's
univariate Gauss-norm code, and Bingyu Xia's power-series equivalences.

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

The core Paperforge steps are:

```sh
(cd inputs/draft && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex)
source .paperforge-venv/bin/activate
paperforge doctor
python3 scripts/build-lean-knowls.py .
paperforge build web
paperforge check
paperforge build arxiv --pdf
```

The wrapper also regenerates the Lean knowls, removes obsolete generated
knowl files, gives the interactive JavaScript a content-addressed name, copies
the archival Lean pages, and installs the primary PDF in `output/pdf/`.

To refresh the GitHub Pages snapshot after a successful build:

```sh
scripts/sync-pages.sh
```

The Paperforge checkout used for this paper is based on upstream commit
`e6affebffbcc5eb05f17cc3ba57cdf3ff5c618ad`.  Paperforge is installed
editable, so the exact base commit and the local compatibility patch together
define the tool version.  The patch at
`patches/paperforge-compatibility.patch` preserves `\href` and `\url`, reads
all `\author` commands, recognises Lean `class` declarations, emits the pinned
commit on each Lean badge, and validates declarations against those exact Git
objects.

For a fresh local setup, start from a clean Paperforge checkout and run:

```sh
paper_root="$PWD"
paperforge_checkout=/path/to/paperforge
git -C "$paperforge_checkout" checkout e6affebffbcc5eb05f17cc3ba57cdf3ff5c618ad
git -C "$paperforge_checkout" apply --check \
  "$paper_root/patches/paperforge-compatibility.patch"
git -C "$paperforge_checkout" apply \
  "$paper_root/patches/paperforge-compatibility.patch"
python3 -m venv .paperforge-venv
.paperforge-venv/bin/python -m pip install -r requirements.txt
.paperforge-venv/bin/python -m pip install -e "$paperforge_checkout" \
  -e "$paperforge_checkout/validators"
PATH="$paper_root/.paperforge-venv/bin:$PATH" paperforge selftest
PATH="$paper_root/.paperforge-venv/bin:$PATH" paperforge doctor
.paperforge-venv/bin/python -m pip install -r requirements-dev.txt
.paperforge-venv/bin/python -m pytest "$paperforge_checkout/tests" \
  "$paperforge_checkout/validators/tests" -q
```

`requirements.txt` pins the exercised PreTeXt CLI.  The Paperforge package
itself still reports version `0.1.0`, so the Git commit is the meaningful pin.
The setup requires Python 3.11 or later.

The untracked `.paperforge.local.toml` must point to the local formalisation
checkout, for example:

```toml
[formalizations.primary]
root = "/absolute/path/to/aintlib/projects/AdicSpaces"
```

That AINTLIB checkout must contain all five Git objects listed below.  A
shallow clone may therefore be insufficient.  All five snapshots are reachable
from public AINTLIB branches.

See `PAPERFORGE_CHECK.md` for the reference audit and `STYLE_REVIEW.md` for the
first author-voice pass.

## Lean source and publication note

The interactive code is extracted from five audited AINTLIB snapshots:

```text
finite-jet branch: fjp/cdvf-lemma51
finite-jet commit: b007a4f3d4226f00a684b402715aa542e2f0bcdc
weighted-parity branch: wp/reduced-example
weighted-parity commit: 090a289211deb69117413e329325fe819aa7dbc2
sheaf-comparison branch: dev/adic-spaces
sheaf-comparison commit: d92f96504f949ca43a27a817cb8d2f70b6486744
Scottish Book branch: dev/adic-spaces
abstract-base Scottish Book commit: 01116aca6070283726008536cba16d165a01b505
strong-sheafiness branch: wp/strengthenings
strong-sheafiness commit: 870d0eed2c48a020109d766d2af89c3f47469a94
project: projects/AdicSpaces
```

All five commits are publicly reachable in AINTLIB.  To keep the interactive
paper independent of branch movement,
`scripts/build-lean-knowls.py` extracts each declaration from the Git object
recorded for that declaration.  Every Paperforge Lean badge opens that code
inline, Roe-style, and its ordinary link opens a standalone archival page under
`lean/AdicSpaces/declarations/`.

No AINTLIB branch is pushed by the paper build.
