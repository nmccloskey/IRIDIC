#!/usr/bin/env python
"""
build_manual_outline.py

Auto-generate a 00_outline.md file for a modular Markdown manual.

What it does
------------
- Walks a manual/ directory recursively
- Finds Markdown files (default: *.md)
- Sorts them in a predictable "numeric-prefix-aware" order (e.g., 03_02_*.md < 03_10_*.md)
- Emits an outline Markdown file containing:
    1) A directory/file tree (with links)
    2) A grouped outline list (with optional extracted titles)

Notes
-----
- Dependency-free (stdlib only).
- This script generates the outline/index file only (no PDF/web protocols here).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, List


MD_EXTS = {".md", ".markdown"}
_NUM_RE = re.compile(r"^\d+(?:[_-]\d+)*")


@dataclass(frozen=True)
class Entry:
    rel_path: Path          # relative to manual_dir
    title: Optional[str]    # first heading, if available


def numeric_key(name: str) -> Tuple:
    """
    Sort key that respects leading numeric prefixes like:
      00_outline.md
      03_workflow
      03_02_transcript_tables.md

    Falls back to lexicographic order when no prefix exists.
    """
    stem = name
    if "." in stem:
        stem = stem.rsplit(".", 1)[0]

    m = _NUM_RE.match(stem)
    if not m:
        return (1, stem.lower())

    prefix = m.group(0)
    parts = re.split(r"[_-]", prefix)
    nums = tuple(int(p) for p in parts if p.isdigit())
    rest = stem[len(prefix):].lstrip("_-").lower()
    return (0, nums, rest)


def extract_title(md_path: Path) -> Optional[str]:
    """
    Extract the first Markdown heading from a file.

    Strategy:
    - First ATX heading (# Title)
    - Else first plausible Setext heading (Title + ====)
    """
    try:
        text = md_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None

    # ATX headings
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("#"):
            title = s.lstrip("#").strip()
            if title:
                return title

    # Setext headings (light heuristic)
    lines = text.splitlines()
    for i in range(len(lines) - 1):
        t = lines[i].strip()
        u = lines[i + 1].strip()
        if not t:
            continue
        if set(u) <= {"="} or set(u) <= {"-"}:
            if len(u) >= max(3, len(t) // 2):
                return t

    return None


def iter_markdown_entries(manual_dir: Path, include_exts: set[str]) -> List[Entry]:
    """
    Collect Markdown files under manual_dir, skipping hidden paths and __pycache__.
    """
    out: List[Entry] = []
    for p in manual_dir.rglob("*"):
        rel = p.relative_to(manual_dir)
        if any(part.startswith(".") for part in rel.parts):
            continue
        if "__pycache__" in rel.parts:
            continue
        if p.is_file() and p.suffix.lower() in include_exts:
            out.append(Entry(rel_path=rel, title=extract_title(p)))
    return out


def build_tree(entries: List[Entry]) -> dict:
    """
    Build nested dict tree; dirs are dicts, files are Entry objects.
    """
    tree: dict = {}
    for e in entries:
        cur = tree
        parts = list(e.rel_path.parts)
        for seg in parts[:-1]:
            cur = cur.setdefault(seg, {})
        cur[parts[-1]] = e
    return tree


def render_tree(
    tree: dict,
    base_rel: Path,
    prefix: str = "",
    max_depth: Optional[int] = None,
    depth: int = 0,
    *,
    links: bool = False,
    show_titles: bool = False,
    indent_mid = "│   ",
    indent_last = "    "
) -> List[str]:
    """Render tree dict into unicode tree lines.

    Parameters
    ----------
    links:
        If True, render Markdown links for files.
    show_titles:
        If True, append extracted titles to file labels (only used when links=True).
    indent_mid / indent_last:
        Indentation fragments used to build the prefix for child nodes.

    Notes
    -----
    The default tree rendering is intentionally *clean* (no links, no titles) so it
    reads like a conventional filesystem tree.
    """
    if max_depth is not None and depth > max_depth:
        return []

    keys = sorted(tree.keys(), key=numeric_key)
    lines: List[str] = []

    for i, k in enumerate(keys):
        last = (i == len(keys) - 1)
        branch = "└── " if last else "├── "
        next_prefix = prefix + (indent_last if last else indent_mid)
        node = tree[k]

        if isinstance(node, dict):
            lines.append(f"{prefix}{branch}{k}/")
            lines.extend(
                render_tree(
                    node,
                    base_rel / k,
                    prefix=next_prefix,
                    max_depth=max_depth,
                    depth=depth + 1,
                    links=links,
                    show_titles=show_titles,
                    indent_mid=indent_mid,
                    indent_last=indent_last,
                )
            )
        else:
            if not links:
                lines.append(f"{prefix}{branch}{k}")
            else:
                rel_link = (base_rel / k).as_posix()
                label = k
                if show_titles and node.title:
                    label = f"{k} — {node.title}"
                lines.append(f"{prefix}{branch}[{label}]({rel_link})")

    return lines


def render_grouped_outline(entries: List[Entry]) -> List[str]:
    """
    Render a grouped bullet outline (grouped by directory).
    """
    entries_sorted = sorted(entries, key=lambda e: tuple(numeric_key(s) for s in e.rel_path.parts))
    lines: List[str] = []

    cur_dir: Optional[Path] = None
    for e in entries_sorted:
        d = e.rel_path.parent
        if cur_dir != d:
            if lines:
                lines.append("")
            heading = "Manual root" if str(d) == "." else f"{d.as_posix()}/"
            lines.append(f"### {heading}")
            cur_dir = d

        link = e.rel_path.as_posix()
        fname = e.rel_path.name
        if e.title:
            lines.append(f"- [{fname} — {e.title}]({link})")
        else:
            lines.append(f"- [{fname}]({link})")

    return lines


def generate_outline_md(
    manual_dir: Path,
    output_path: Path,
    manual_title: str,
    manual_version: str,
    include_exts: set[str],
    max_depth: Optional[int],
) -> None:
    manual_dir = manual_dir.resolve()
    if not manual_dir.exists() or not manual_dir.is_dir():
        raise FileNotFoundError(f"manual_dir does not exist or is not a directory: {manual_dir}")

    entries = iter_markdown_entries(manual_dir, include_exts=include_exts)

    # Exclude the output file itself if it is inside manual_dir
    try:
        out_rel = output_path.resolve().relative_to(manual_dir)
        entries = [e for e in entries if e.rel_path != out_rel]
    except Exception:
        pass

    tree = build_tree(entries)
    tree_lines = render_tree(tree, base_rel=Path("."), max_depth=max_depth)
    outline_lines = render_grouped_outline(entries)

    now = _dt.date.today().isoformat()

    md: List[str] = []
    md.append(f"# {manual_title}")
    md.append("")
    md.append(f"**Version:** {manual_version}  ")
    md.append(f"**Generated:** {now}  ")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## Manual Map (Tree)")
    md.append("")
    md.append("```")
    md.extend(tree_lines if tree_lines else ["(No Markdown files found.)"])
    md.append("```")
    md.append("")
    md.append("## Outline (Links)")
    md.append("")
    md.extend(outline_lines if outline_lines else ["(No Markdown files found.)"])
    md.append("")
    md.append("---")
    md.append("")
    md.append("## Notes")
    md.append("")
    md.append("- Regenerate this file after adding/renaming manual sections.")
    md.append("- Keep numeric prefixes stable to preserve predictable ordering.")
    md.append("- For PDF builds, use this file as the “assembly” index (protocol-defined).")
    md.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(md), encoding="utf-8")


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Auto-generate 00_outline.md for a modular Markdown manual.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("manual_dir", type=Path, help="Path to the manual/ directory to scan.")
    p.add_argument("-o", "--output", type=Path, default=None, help="Output outline file path. Default: <manual_dir>/00_outline.md")
    p.add_argument("--title", type=str, default="Instruction Manual", help="Manual title for the outline header.")
    p.add_argument("--version", type=str, default="0.0.0", help="Manual version string for the outline header.")
    p.add_argument("--exts", type=str, default=".md,.markdown", help="Comma-separated list of file extensions to include.")
    p.add_argument("--max-depth", type=int, default=None, help="Maximum directory depth to render in the tree (None = unlimited).")
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    manual_dir: Path = args.manual_dir
    output: Path = args.output if args.output else (manual_dir / "00_outline.md")

    include_exts = {e.strip().lower() for e in args.exts.split(",") if e.strip()}
    include_exts = {("." + e) if not e.startswith(".") else e for e in include_exts}

    try:
        generate_outline_md(
            manual_dir=manual_dir,
            output_path=output,
            manual_title=args.title,
            manual_version=args.version,
            include_exts=include_exts,
            max_depth=args.max_depth,
        )
    except Exception as ex:
        print(f"ERROR: {ex}", file=os.sys.stderr)
        return 1

    print(f"Wrote outline: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
