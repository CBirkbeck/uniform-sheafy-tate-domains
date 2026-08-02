#!/usr/bin/env bash
set -euo pipefail

paper_root="$(cd "$(dirname "$0")/.." && pwd)"
paperforge_bin="$paper_root/.paperforge-venv/bin/paperforge"

if [[ ! -x "$paperforge_bin" ]]; then
  echo "Paperforge environment not found at $paperforge_bin" >&2
  exit 1
fi

export PATH="$paper_root/.paperforge-venv/bin:$PATH"
exec "$paperforge_bin" build web "$paper_root" "$@"
