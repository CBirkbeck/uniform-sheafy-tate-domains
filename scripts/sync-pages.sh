#!/usr/bin/env bash
set -euo pipefail

paper_root="$(cd "$(dirname "$0")/.." && pwd)"
web_output="$paper_root/output/web"
paper_pdf="$paper_root/output/pdf/uniform_sheafy_tate_domains.pdf"
pages_dir="$paper_root/docs"

if [[ ! -f "$web_output/paper.html" || ! -f "$paper_pdf" ]]; then
  echo "Build the paper first with scripts/build-paper.sh" >&2
  exit 1
fi

# docs/ is a generated GitHub Pages snapshot. Preserve future custom-domain
# metadata while removing files left behind by an older Paperforge build.
# Source maps are unnecessary in production and can contain build-machine
# paths, so they are deliberately omitted.
mkdir -p "$pages_dir"
rsync -a --delete --delete-excluded \
  --filter "P CNAME" \
  --exclude ".nojekyll" \
  --exclude "._*" \
  --exclude "*.map" \
  --exclude "*.map.gz" \
  "$web_output/" "$pages_dir/"

cp "$web_output/paper.html" "$pages_dir/index.html"
cp "$paper_pdf" "$pages_dir/paper.pdf"
touch "$pages_dir/.nojekyll"

echo "GitHub Pages snapshot: $pages_dir"
