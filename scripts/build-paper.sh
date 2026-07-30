#!/usr/bin/env bash
set -euo pipefail

paper_root="$(cd "$(dirname "$0")/.." && pwd)"
paperforge_bin="$paper_root/.paperforge-venv/bin/paperforge"

if [[ ! -x "$paperforge_bin" ]]; then
  echo "Paperforge environment not found at $paperforge_bin" >&2
  exit 1
fi

export PATH="$paper_root/.paperforge-venv/bin:$PATH"

python3 "$paper_root/scripts/build-lean-knowls.py" "$paper_root"

(
  cd "$paper_root/inputs/draft"
  latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
)

cd "$paper_root"
"$paperforge_bin" doctor

# PreTeXt updates the knowls needed by the current source but does not remove
# obsolete xref knowls from an earlier build.  Clear only this generated
# directory so withdrawn statements cannot survive into the Pages snapshot.
if [[ -d "$paper_root/output/web/knowl/xref" ]]; then
  find "$paper_root/output/web/knowl/xref" -type f -name '*.html' -delete
fi

"$paperforge_bin" build web

# GitHub Pages may cache detail-ui.js across deployments.  This file also
# contains the generated Lean-knowl registry, so stale copies leave new Lean
# badges visible but inert.  Give the built copy a content-addressed filename.
detail_ui_hash="$(
  shasum -a 256 "$paper_root/output/web/detail-ui.js" | cut -c1-12
)"
detail_ui_filename="detail-ui.$detail_ui_hash.js"
find "$paper_root/output/web" -maxdepth 1 -type f \
  -name 'detail-ui.*.js' -delete
cp "$paper_root/output/web/detail-ui.js" \
  "$paper_root/output/web/$detail_ui_filename"
DETAIL_UI_FILENAME="$detail_ui_filename" perl -0pi -e \
  's/src="detail-ui(?:\.[0-9a-f]{12})?\.js(?:\?v=[^"]*)?"/src="$ENV{DETAIL_UI_FILENAME}"/g' \
  "$paper_root/output/web/paper.html"

mkdir -p "$paper_root/output/web/lean"
rsync -a --delete "$paper_root/web-assets/lean/" "$paper_root/output/web/lean/"
"$paperforge_bin" check
"$paperforge_bin" build arxiv --pdf

mkdir -p "$paper_root/output/pdf"
cp "$paper_root/inputs/draft/main.pdf" \
  "$paper_root/output/pdf/uniform_sheafy_tate_domains.pdf"

echo "Primary PDF: $paper_root/output/pdf/uniform_sheafy_tate_domains.pdf"
echo "Paperforge PDF: $paper_root/output/arxiv/main.pdf"
echo "Web edition: $paper_root/output/web/paper.html"
