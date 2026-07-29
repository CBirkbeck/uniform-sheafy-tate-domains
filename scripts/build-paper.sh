#!/usr/bin/env bash
set -euo pipefail

paper_root="$(cd "$(dirname "$0")/.." && pwd)"
paperforge_bin="$paper_root/.paperforge-venv/bin/paperforge"

if [[ ! -x "$paperforge_bin" ]]; then
  echo "Paperforge environment not found at $paperforge_bin" >&2
  exit 1
fi

export PATH="$paper_root/.paperforge-venv/bin:$PATH"

(
  cd "$paper_root/inputs/draft"
  latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
)

cd "$paper_root"
"$paperforge_bin" doctor
"$paperforge_bin" build web
"$paperforge_bin" check
"$paperforge_bin" build arxiv --pdf

mkdir -p "$paper_root/output/pdf"
cp "$paper_root/inputs/draft/main.pdf" \
  "$paper_root/output/pdf/uniform_sheafy_tate_domains.pdf"

echo "Primary PDF: $paper_root/output/pdf/uniform_sheafy_tate_domains.pdf"
echo "Paperforge PDF: $paper_root/output/arxiv/main.pdf"
echo "Web edition: $paper_root/output/web/paper.html"
