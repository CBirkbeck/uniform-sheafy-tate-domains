#!/usr/bin/env python3
"""Build self-contained Lean declaration knowls from pinned formalisation snapshots.

Paperforge normally builds its inline Lean registry from doc-gen4 output.  The
formalization snapshot used by this paper is not currently published with
doc-gen4 pages, so this script extracts the declaration source directly with
``git show``.  It produces both:

* ``web-assets/lean-knowls-AdicSpaces.js`` for the inline knowls; and
* ``web-assets/lean/AdicSpaces/declarations/*.html`` for ordinary/new-tab
  navigation.

The generated pages are fixed source snapshots: they do not depend on the
pinned commits being reachable on GitHub at run time.  Entries may override
the primary snapshot with a ``commit`` field.

Reader-facing mathematical summaries may be supplied in
``crosswalk/lean-knowl-doc-overrides.json``.  The inline knowl uses the curated
summary, while the standalone archival page keeps the original Lean docstring
in a collapsed disclosure.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

try:
    import tomllib
except ModuleNotFoundError as exc:  # pragma: no cover - Python < 3.11
    raise SystemExit("build-lean-knowls.py requires Python 3.11 or newer") from exc


# The formalisation now lives in its own repository, so declarations are pinned
# to a single snapshot there rather than to the five AINTLIB commits the paper
# used while the code was still part of that monorepo.
REPO_URL = "https://github.com/CBirkbeck/uniform-sheafy-tate-domains-lean"
PRIMARY_COMMIT = "e3514f12e382a8ef8f0d2b8822ed9b792bcaf838"
PROJECT = "AdicSpaces"

# The Scottish Book declarations (Problems 24 and 28, the abstract-base class
# `IsFJPBase`, and the p-adic instance) are the one exception.  They live on
# AINTLIB's `dev/adic-spaces` branch, whose FJP tower rests on a different base
# abstraction and a different mathlib pin, so they cannot be carried into the
# standalone repository without merging two branches that are ~1000 commits
# apart.  They stay pinned in the monorepo, and `[formalizations.legacy]` in
# paper.toml says where to read them from.
LEGACY_COMMIT = "01116aca6070283726008536cba16d165a01b505"
LEGACY_REPO_URL = "https://github.com/CBirkbeck/AINTLIB"

PUBLIC_COMMITS = {PRIMARY_COMMIT, LEGACY_COMMIT}


class SourceRepo:
    """A git checkout a pinned declaration can be read out of."""

    def __init__(self, repo: Path, prefix: str | None, url: str) -> None:
        self.repo = repo
        self.prefix = prefix
        self.url = url

    def path_for(self, file: str) -> str:
        return file if self.prefix is None else f"{self.prefix}/{file}"


def repo_url_for(commit: str) -> str:
    return LEGACY_REPO_URL if commit == LEGACY_COMMIT else REPO_URL

DECL_LINE_RE = re.compile(
    r"^(?P<indent>[ \t]*)"
    r"(?:@\[[^\]]*\]\s*)*"
    r"(?P<mods>(?:(?:noncomputable|protected|private|unsafe|opaque)\s+)*)"
    r"(?P<kind>class|structure|def|abbrev|theorem|lemma)\s+"
    r"(?P<name>[^\s(:\[{]+)"
)
TOP_COMMAND_RE = re.compile(
    r"^(?:@\[[^\]]*\]\s*)*"
    r"(?:(?:noncomputable|protected|private|unsafe|opaque)\s+)*"
    r"(?:class|structure|def|abbrev|theorem|lemma|instance|example|axiom|"
    r"inductive|namespace|section|end|variable|include|omit|open|attribute|"
    r"local|scoped|syntax|macro|notation|universe)\b"
)


def run_git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode:
        detail = proc.stderr.strip() or proc.stdout.strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {detail}")
    return proc.stdout


def deep_merge(base: dict, overlay: dict) -> dict:
    result = dict(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config(root: Path) -> dict:
    with (root / "paper.toml").open("rb") as handle:
        config = tomllib.load(handle)
    local = root / ".paperforge.local.toml"
    if local.is_file():
        with local.open("rb") as handle:
            config = deep_merge(config, tomllib.load(handle))
    return config


def formalization_root(root: Path, override: str | None) -> Path:
    if override:
        candidate = Path(override).expanduser()
    else:
        config = load_config(root)
        candidate = Path(
            config.get("formalizations", {})
            .get("primary", {})
            .get("root")
            or config.get("inputs", {}).get("lean_project")
            or "/Users/mcu22seu/Documents/GitHub/aintlib-adic-fjp/projects/AdicSpaces"
        ).expanduser()
    if not candidate.is_absolute():
        candidate = root / candidate
    candidate = candidate.resolve()
    if not candidate.is_dir():
        raise RuntimeError(f"Lean project root does not exist: {candidate}")
    return candidate


def build_source(lean_root: Path, url: str) -> "SourceRepo":
    """Wrap a Lean project checkout, working out its path prefix inside its repo."""
    repo = Path(run_git(lean_root, "rev-parse", "--show-toplevel").strip())
    prefix = lean_root.relative_to(repo).as_posix()
    # In the standalone formalisation repository the Lean project *is* the repo
    # root, so relative_to yields "." and there is no prefix to prepend.
    return SourceRepo(repo, None if prefix in ("", ".") else prefix, url)


def legacy_source(root: Path) -> "SourceRepo":
    """The monorepo checkout holding the Scottish Book declarations."""
    config = load_config(root)
    legacy = config.get("formalizations", {}).get("legacy", {})
    candidate = legacy.get("root")
    if not candidate:
        raise RuntimeError(
            "paper.toml has no [formalizations.legacy] root; it is needed for the "
            f"declarations pinned at {LEGACY_COMMIT[:9]}"
        )
    path = Path(candidate).expanduser()
    if not path.is_absolute():
        path = root / path
    path = path.resolve()
    if not path.is_dir():
        raise RuntimeError(f"legacy Lean project root does not exist: {path}")
    return build_source(path, legacy.get("url", LEGACY_REPO_URL))


def collect_declarations(root: Path, declmap_path: Path, extra_path: Path) -> list[dict]:
    declmap = json.loads((root / declmap_path).read_text())
    # The legacy formalization keeps its own declmap so that paperforge emits one
    # badge per declaration rather than one per formalization; its declarations
    # still need knowls, so merge it in here.
    legacy_map = root / "crosswalk" / "lean-decl-map-legacy.json"
    if legacy_map.is_file():
        for label, entries in json.loads(legacy_map.read_text()).items():
            declmap.setdefault(label, []).extend(entries)
    extra_data = json.loads((root / extra_path).read_text())
    if extra_data.get("commit") not in (None, PRIMARY_COMMIT):
        raise RuntimeError(
            f"{extra_path} pins {extra_data['commit']}, expected {PRIMARY_COMMIT}"
        )

    merged: dict[str, dict] = {}
    uses: dict[str, list[str]] = {}

    def add(entry: dict) -> None:
        entry = dict(entry)
        entry.setdefault("commit", PRIMARY_COMMIT)
        decl = entry.get("decl")
        if not decl or not entry.get("file"):
            raise RuntimeError(f"declaration entry needs decl and file: {entry!r}")
        if decl in merged and merged[decl]["file"] != entry["file"]:
            raise RuntimeError(
                f"{decl} is assigned to two files: "
                f"{merged[decl]['file']} and {entry['file']}"
            )
        merged.setdefault(decl, {}).update(entry)
        cited = entry.get("cited")
        if cited and cited not in uses.setdefault(decl, []):
            uses[decl].append(cited)

    for entries in declmap.values():
        for entry in entries:
            if not entry.get("private"):
                add(entry)
    for entry in extra_data.get("declarations", []):
        add(entry)

    for decl, entry in merged.items():
        entry["uses"] = uses.get(decl, [])
    return [merged[name] for name in sorted(merged)]


def load_doc_overrides(root: Path, override_path: Path) -> dict[str, str]:
    path = root / override_path
    if not path.is_file():
        return {}
    data = json.loads(path.read_text())
    if data.get("commit") not in (None, PRIMARY_COMMIT):
        raise RuntimeError(
            f"{override_path} pins {data['commit']}, expected {PRIMARY_COMMIT}"
        )
    if data.get("schema") not in (None, 1):
        raise RuntimeError(f"{override_path}: unsupported schema {data['schema']}")
    overrides = data.get("overrides", {})
    if not isinstance(overrides, dict):
        raise RuntimeError(f"{override_path}: overrides must be a JSON object")
    for decl, doc in overrides.items():
        if not isinstance(decl, str) or not isinstance(doc, str) or not doc.strip():
            raise RuntimeError(
                f"{override_path}: every override needs a declaration name "
                "and nonempty text"
            )
        word_count = len(doc.split())
        if word_count > 120:
            raise RuntimeError(
                f"{override_path}: {decl} has {word_count} words; "
                "reader-facing summaries are limited to 120"
            )
        if re.search(r"</?[A-Za-z][^>]*>", doc):
            raise RuntimeError(f"{override_path}: {decl} contains raw HTML")
        internal_markers = (
            "campaign",
            "ticket",
            "WO3",
            "P0.4",
            "K8b",
            "layer 1",
            "layer 2",
            "public endpoint",
            "handover",
            "maxHeartbeats",
            "docs/plans",
            "kept as-is",
        )
        found = [marker for marker in internal_markers if marker.lower() in doc.lower()]
        if found:
            raise RuntimeError(
                f"{override_path}: {decl} contains internal marker(s): "
                + ", ".join(found)
            )
    return overrides


def line_offsets(source: str) -> tuple[list[str], list[int]]:
    lines = source.splitlines(keepends=True)
    offsets: list[int] = []
    offset = 0
    for line in lines:
        offsets.append(offset)
        offset += len(line)
    return lines, offsets


def declaration_at(source: str, decl: str, line_hint: int | None) -> tuple[int, int, str, str]:
    lines, offsets = line_offsets(source)
    candidates: list[tuple[int, re.Match[str]]] = []
    for index, line in enumerate(lines):
        match = DECL_LINE_RE.match(line)
        if not match:
            continue
        written_name = match.group("name")
        if decl == written_name or decl.endswith("." + written_name):
            candidates.append((index, match))
    if not candidates:
        raise RuntimeError(f"could not locate declaration {decl}")
    if line_hint:
        index, match = min(candidates, key=lambda item: abs(item[0] + 1 - line_hint))
    elif len(candidates) == 1:
        index, match = candidates[0]
    else:
        where = ", ".join(str(i + 1) for i, _ in candidates)
        raise RuntimeError(f"ambiguous declaration {decl}; candidates at lines {where}")
    return offsets[index], index, match.group("kind"), match.group("name")


def preceding_doc_comment(source: str, start: int) -> str:
    prefix = source[:start]
    trimmed = prefix.rstrip()
    if not trimmed.endswith("-/"):
        return ""
    doc_start = trimmed.rfind("/--")
    if doc_start < 0:
        return ""
    doc_end = trimmed.find("-/", doc_start)
    if doc_end != len(trimmed) - 2:
        return ""
    return trimmed[doc_start + 3 : doc_end].strip()


def declaration_block(source: str, start: int, line_index: int) -> str:
    lines, offsets = line_offsets(source)
    end = len(source)
    for index in range(line_index + 1, len(lines)):
        line = lines[index]
        if line.startswith("/-!"):
            end = offsets[index]
            break
        if line[:1].isspace():
            continue
        if TOP_COMMAND_RE.match(line):
            end = offsets[index]
            break
    block = source[start:end].rstrip()
    # A doc comment for the following declaration can precede a modifier such
    # as ``include ... in``; never absorb that comment into this declaration.
    trailing_doc = block.rfind("\n/--")
    if trailing_doc >= 0:
        after = block.find("-/", trailing_doc)
        if after >= 0 and not block[after + 2 :].strip():
            block = block[:trailing_doc].rstrip()
    return block


def body_marker(block: str, name: str) -> int | None:
    """Return the top-level definition/proof marker in a declaration block."""
    name_at = block.find(name)
    pos = name_at + len(name) if name_at >= 0 else 0
    depth = 0
    in_string = False
    escaped = False
    line_comment = False
    block_comment = 0
    while pos < len(block):
        pair = block[pos : pos + 2]
        char = block[pos]
        if line_comment:
            if char == "\n":
                line_comment = False
            pos += 1
            continue
        if block_comment:
            if pair == "/-":
                block_comment += 1
                pos += 2
            elif pair == "-/":
                block_comment -= 1
                pos += 2
            else:
                pos += 1
            continue
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            pos += 1
            continue
        if pair == "--":
            line_comment = True
            pos += 2
            continue
        if pair == "/-":
            block_comment = 1
            pos += 2
            continue
        if char == '"':
            in_string = True
            pos += 1
            continue
        if char in "([{":
            depth += 1
            pos += 1
            continue
        if char in ")]}":
            depth = max(0, depth - 1)
            pos += 1
            continue
        if depth == 0 and pair == ":=":
            line_prefix = block[block.rfind("\n", 0, pos) + 1 : pos]
            is_local_binding = bool(
                re.search(r"\b(?:let|letI|have|haveI)\b", line_prefix)
            )
            # A dependent theorem statement may split a local instance across
            # several lines, for example
            #
            #   haveI : @CompleteSpace ...
            #     (...) := someInstance
            #
            # The proof marker is not this assignment.  If the marker lies on
            # a continuation line, find the nearest less-indented line; a
            # leading have/let there identifies the enclosing local binder.
            if not is_local_binding:
                line_start = block.rfind("\n", 0, pos) + 1
                current_line = block[line_start:pos]
                current_indent = len(current_line) - len(current_line.lstrip())
                previous_end = line_start - 1
                while previous_end >= 0:
                    previous_start = block.rfind("\n", 0, previous_end) + 1
                    previous_line = block[previous_start:previous_end].rstrip()
                    previous_end = previous_start - 1
                    if not previous_line.strip():
                        continue
                    previous_indent = len(previous_line) - len(previous_line.lstrip())
                    if previous_indent < current_indent:
                        is_local_binding = bool(
                            re.match(
                                r"\s*(?:let|letI|have|haveI)\b", previous_line
                            )
                        )
                        break
            if not is_local_binding:
                return pos
            pos += 2
            continue
        if depth == 0 and block.startswith("where", pos):
            before = block[pos - 1] if pos else " "
            after = block[pos + 5] if pos + 5 < len(block) else " "
            if not (before.isalnum() or before in "_'") and not (
                after.isalnum() or after in "_'"
            ):
                return pos
        pos += 1
    return None


def doc_html(doc: str, *, curated: bool = False) -> str:
    if not doc:
        return ""

    parts = re.split(r"\n\s*\n", doc)
    rendered: list[str] = []
    for part in parts:
        lines = [line.strip() for line in part.splitlines()]
        text = "\n".join(lines)
        chunks = text.split("`")
        inline = "".join(
            f"<code>{html.escape(chunk)}</code>" if index % 2 else html.escape(chunk)
            for index, chunk in enumerate(chunks)
        )
        inline = re.sub(
            r"\*\*(.+?)\*\*", r"<strong>\1</strong>", inline, flags=re.S
        )
        rendered.append("<p>" + inline.replace("\n", "<br>") + "</p>")
    classes = "lean-doc lean-doc-curated" if curated else "lean-doc"
    label = (
        '<p class="lean-doc-label"><strong>Mathematical summary.</strong></p>'
        if curated
        else ""
    )
    return f'<div class="{classes}">' + label + "".join(rendered) + "</div>"


def slug_for(decl: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", decl) + ".html"


def inline_html(
    decl: str,
    kind: str,
    code: str,
    doc: str,
    repo_path: str,
    line_start: int,
    line_end: int,
    curated_doc: bool,
    commit: str,
) -> str:
    return (
        '<div class="lean-knowl-head">'
        f'<span class="lean-decl-kind">{html.escape(kind)}</span> '
        f"<code>{html.escape(decl)}</code></div>"
        + doc_html(doc, curated=curated_doc)
        + '<pre class="lean-source"><code class="language-lean">'
        + html.escape(code)
        + "</code></pre>"
        + '<div class="lean-source-meta">'
        + html.escape(repo_path)
        + f":{line_start}–{line_end} · commit {commit[:12]}"
        + "</div>"
    )


def standalone_html(
    decl: str,
    kind: str,
    code: str,
    doc: str,
    repo_path: str,
    line_start: int,
    line_end: int,
    uses: list[str],
    curated_doc: bool,
    source_doc: str,
    commit: str,
) -> str:
    development = (
        "The weighted-parity development"
        if decl.startswith("WeightedParity.")
        else "The finite-jet development"
    )
    uses_html = ""
    if uses:
        uses_html = (
            '<p class="used-for"><strong>Used in the paper for:</strong> '
            + "; ".join(html.escape(item) for item in uses)
            + "</p>"
        )
    summary_note = ""
    if curated_doc:
        summary_note = (
            '<p class="meta">The mathematical summary is editorial text for '
            "this paper. The declaration below is extracted verbatim from the "
            "pinned source.</p>\n  "
        )
    source_doc_details = ""
    if curated_doc and source_doc:
        source_doc_details = (
            '<details class="source-doc"><summary>Original Lean docstring</summary>'
            + doc_html(source_doc)
            + "</details>\n  "
        )
    if commit in PUBLIC_COMMITS:
        github_url = (
            repo_url_for(commit)
            + "/blob/"
            + commit
            + "/"
            + quote(repo_path, safe="/")
            + f"#L{line_start}-L{line_end}"
        )
        source_access = (
            '<p class="meta"><a href="'
            + html.escape(github_url, quote=True)
            + '">View this pinned source on GitHub</a>. The declaration above '
            "is also embedded here so that the paper remains independent of "
            "branch movement.</p>"
        )
    else:
        source_access = (
            '<p class="meta">This is the archival declaration extracted from '
            "the pinned\n  source tree.  The corresponding upstream commit was "
            "not publicly reachable\n  when this page was built, so no external "
            "upstream link is offered here.</p>"
        )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(decl)} · Lean source</title>
  <style>
    :root {{ color-scheme: light dark; }}
    body {{ margin: 0; font: 16px/1.55 system-ui, sans-serif; }}
    main {{ max-width: 72rem; margin: 0 auto; padding: 2rem 1.2rem 4rem; }}
    nav {{ margin-bottom: 1.5rem; }}
    a {{ color: #176b43; }}
    @media (prefers-color-scheme: dark) {{ a {{ color: #84d8aa; }} }}
    h1 {{ overflow-wrap: anywhere; font: 650 1.45rem/1.25 ui-monospace, monospace; }}
    .kind {{ color: #176b43; font-size: .82rem; text-transform: uppercase;
             letter-spacing: .06em; }}
    .doc {{ max-width: 62rem; }}
    details.source-doc {{ max-width: 62rem; margin: 1rem 0; }}
    details.source-doc summary {{ cursor: pointer; }}
    pre {{ padding: 1rem; overflow-x: auto; border-radius: .45rem;
           background: color-mix(in srgb, CanvasText 7%, Canvas); }}
    code {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }}
    .meta, .used-for {{ color: color-mix(in srgb, CanvasText 70%, Canvas);
                        font-size: .9rem; }}
    .provenance {{ margin-top: 2rem; padding-top: 1rem;
                   border-top: 1px solid color-mix(in srgb, CanvasText 18%, Canvas);
                   font-size: .9rem; }}
  </style>
</head>
<body>
<main>
  <nav><a href="../../../paper.html">← Return to the paper</a></nav>
  <div class="kind">{html.escape(kind)}</div>
  <h1>{html.escape(decl)}</h1>
  <div class="doc">{doc_html(doc, curated=curated_doc)}</div>
  {summary_note}{source_doc_details}{uses_html}
  <pre><code>{html.escape(code)}</code></pre>
  <p class="meta">Pinned source: <code>{html.escape(repo_path)}:{line_start}–{line_end}</code><br>
  Commit <code>{commit}</code>.</p>
  {source_access}
  <aside class="provenance"><strong>Restricted-series infrastructure.</strong>
  {development} uses restricted power-series code adapted from
  <a href="https://github.com/WilliamCoram/PhD/tree/e8fcf8fbff848a95475ab62ae2568cbb73961de8">William Coram's repository</a>,
  whose univariate Gauss-norm layer builds on
  <a href="https://github.com/leanprover-community/mathlib4/blob/fd1d54bcac5caba4eff2ea3421c47d907333f515/Mathlib/RingTheory/PowerSeries/GaussNorm.lean">Fabrizio Barroero's mathlib code</a>.
  It separately uses
  <a href="https://github.com/leanprover-community/mathlib4/pull/36507">Bingyu Xia's multivariable power-series equivalences</a>.
  This is infrastructure provenance, not an attribution of this paper-specific
  declaration.</aside>
</main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "instance", nargs="?", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument("--lean-root", help="override the configured Lean project root")
    parser.add_argument(
        "--declmap", type=Path, default=Path("crosswalk/lean-decl-map.json")
    )
    parser.add_argument(
        "--extra", type=Path, default=Path("crosswalk/lean-knowl-extra.json")
    )
    parser.add_argument(
        "--doc-overrides",
        type=Path,
        default=Path("crosswalk/lean-knowl-doc-overrides.json"),
    )
    args = parser.parse_args()

    root = args.instance.resolve()
    primary = build_source(formalization_root(root, args.lean_root), REPO_URL)
    sources = {LEGACY_COMMIT: legacy_source(root)}
    declarations = collect_declarations(root, args.declmap, args.extra)
    commits = sorted({entry["commit"] for entry in declarations})
    for commit in commits:
        src = sources.get(commit, primary)
        run_git(src.repo, "cat-file", "-e", commit + "^{commit}")
    doc_overrides = load_doc_overrides(root, args.doc_overrides)
    declaration_names = {entry["decl"] for entry in declarations}
    unknown_overrides = sorted(set(doc_overrides) - declaration_names)
    if unknown_overrides:
        raise RuntimeError(
            f"{args.doc_overrides}: overrides unknown declarations: "
            + ", ".join(unknown_overrides)
        )

    pages = root / "web-assets" / "lean" / PROJECT / "declarations"
    pages.mkdir(parents=True, exist_ok=True)
    registry: dict[str, dict[str, str]] = {}
    expected_pages: set[str] = set()

    for entry in declarations:
        commit = entry["commit"]
        src = sources.get(commit, primary)
        repo_path = src.path_for(entry["file"])
        source = run_git(src.repo, "show", f"{commit}:{repo_path}")
        start, line_index, kind, written_name = declaration_at(
            source, entry["decl"], entry.get("line")
        )
        block = declaration_block(source, start, line_index)
        if not entry.get("include_body", False):
            marker = body_marker(block, written_name)
            if marker is not None:
                block = block[:marker].rstrip()
        source_doc = preceding_doc_comment(source, start)
        curated_doc = entry["decl"] in doc_overrides
        doc = doc_overrides.get(entry["decl"], source_doc)
        if not doc:
            raise RuntimeError(
                f"{entry['decl']} has no Lean docstring and no curated summary"
            )
        line_start = source.count("\n", 0, start) + 1
        line_end = line_start + block.count("\n")
        slug = slug_for(entry["decl"])
        href = f"./lean/{PROJECT}/declarations/{slug}"
        registry[entry["decl"]] = {
            "html": inline_html(
                entry["decl"],
                kind,
                block,
                doc,
                repo_path,
                line_start,
                line_end,
                curated_doc,
                commit,
            ),
            "href": href,
        }
        (pages / slug).write_text(
            standalone_html(
                entry["decl"],
                kind,
                block,
                doc,
                repo_path,
                line_start,
                line_end,
                entry["uses"],
                curated_doc,
                source_doc,
                commit,
            )
        )
        expected_pages.add(slug)

    for stale in pages.glob("*.html"):
        if stale.name not in expected_pages:
            stale.unlink()

    registry_path = root / "web-assets" / f"lean-knowls-{PROJECT}.js"
    registry_path.write_text(
        "// Generated by scripts/build-lean-knowls.py from pinned commits "
        + ", ".join(commits)
        + ".\nwindow.PAPERFORGE_LEAN_KNOWLS = Object.assign(\n"
        + "  window.PAPERFORGE_LEAN_KNOWLS || {},\n  "
        + json.dumps(registry, ensure_ascii=False, indent=2)
        + "\n);\n"
    )
    print(
        f"lean-knowls: {len(registry)} declarations from "
        f"{', '.join(commit[:12] for commit in commits)} "
        f"-> {registry_path.relative_to(root)}"
    )
    print(
        f"lean-doc-overrides: {len(doc_overrides)} curated summaries from "
        f"{args.doc_overrides}"
    )
    print(f"lean-pages: {len(expected_pages)} -> {pages.relative_to(root)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"build-lean-knowls: error: {exc}", file=sys.stderr)
        raise SystemExit(1)
