#!/usr/bin/env python
"""
build_manual_pdf.py

Build a PDF from a modular Markdown manual directory (manual/).

Core behavior
-------------
- Recursively scans manual/ for Markdown files
- Sorts them using numeric-prefix-aware ordering (e.g., 03_02_*.md < 03_10_*.md)
- Concatenates them into a single temporary Markdown "assembly" file
- Optionally inserts page breaks between files (default: ON)
- Calls Pandoc to render a PDF

Requirements
------------
- Pandoc installed and discoverable on PATH (or pass --pandoc <path-to-pandoc>)
- A LaTeX engine installed (recommended: xelatex via TeX Live / MiKTeX)

Typical usage
-------------
python build_manual_pdf.py manual/ --yaml manual/manual_pdf.yaml --output dist/MyManual.pdf
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple


MD_EXTS = {".md", ".markdown"}
_NUM_RE = re.compile(r"^\d+(?:[_-]\d+)*")


@dataclass(frozen=True)
class MdFile:
    rel_path: Path
    abs_path: Path


def numeric_key(name: str) -> Tuple:
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


def resolve_executable(exe: str) -> Optional[str]:
    """
    Resolve an executable using PATH lookup.
    Returns an absolute path string if found, else None.
    """
    # If user passed a direct path, accept it.
    p = Path(exe)
    if p.exists() and p.is_file():
        return str(p.resolve())

    found = shutil.which(exe)
    return found


def iter_markdown_files(
    manual_dir: Path,
    include_exts: set[str],
    include_outline: bool,
    outline_name: str,
) -> List[MdFile]:
    out: List[MdFile] = []
    manual_dir = manual_dir.resolve()

    for p in manual_dir.rglob("*"):
        rel = p.relative_to(manual_dir)

        if any(part.startswith(".") for part in rel.parts):
            continue
        if "__pycache__" in rel.parts:
            continue

        if p.is_file() and p.suffix.lower() in include_exts:
            if (not include_outline) and (p.name == outline_name):
                continue
            out.append(MdFile(rel_path=rel, abs_path=p.resolve()))

    out.sort(key=lambda f: tuple(numeric_key(s) for s in f.rel_path.parts))
    return out


def assemble_markdown(
    files: List[MdFile],
    add_pagebreaks: bool,
    include_file_dividers: bool,
) -> str:
    chunks: List[str] = []

    for f in files:
        if add_pagebreaks:
            chunks.append("\n\n\\newpage\n\n")
        else:
            chunks.append("\n\n")

        if include_file_dividers:
            chunks.append(f"\n\n---\n\n<!-- source: {f.rel_path.as_posix()} -->\n\n")
        else:
            chunks.append(f"\n\n<!-- source: {f.rel_path.as_posix()} -->\n\n")

        try:
            text = f.abs_path.read_text(encoding="utf-8", errors="strict")
        except UnicodeDecodeError:
            text = f.abs_path.read_text(encoding="utf-8", errors="ignore")

        text = text.replace("\r\n", "\n").replace("\r", "\n")
        chunks.append(text.strip() + "\n")

    return "\n".join(chunks).strip() + "\n"


def run_pandoc(
    pandoc_exe: str,
    assembly_md_path: Path,
    output_pdf_path: Path,
    yaml_path: Optional[Path],
    pdf_engine: str,
    extra_pandoc_args: List[str],
) -> None:
    cmd = [pandoc_exe, str(assembly_md_path)]

    if yaml_path is not None:
        cmd.extend(["--metadata-file", str(yaml_path)])

    if pdf_engine:
        cmd.extend(["--pdf-engine", pdf_engine])

    cmd.extend(["--standalone"])
    cmd.extend(extra_pandoc_args)
    cmd.extend(["-o", str(output_pdf_path)])

    proc = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if proc.returncode != 0:
        msg = [
            "Pandoc failed.",
            "",
            "Command:",
            "  " + " ".join(cmd),
            "",
            "STDOUT:",
            proc.stdout.strip() or "(empty)",
            "",
            "STDERR:",
            proc.stderr.strip() or "(empty)",
        ]
        raise RuntimeError("\n".join(msg))


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Build a PDF from a modular Markdown manual directory.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("manual_dir", type=Path, help="Path to the manual/ directory.")
    p.add_argument("-y", "--yaml", type=Path, default=None, help="Pandoc metadata YAML file. Default: <manual_dir>/manual_pdf.yaml if present.")
    p.add_argument("-o", "--output", type=Path, default=None, help="Output PDF path. Default: <manual_dir.parent>/dist/<manual_dir.name>.pdf")

    p.add_argument("--pandoc", type=str, default="pandoc", help="Pandoc executable name or full path.")
    p.add_argument("--pdf-engine", type=str, default="xelatex", help="Pandoc PDF engine (e.g., xelatex, lualatex, pdflatex).")

    p.add_argument("--pagebreaks", action="store_true", default=True, help="Insert a page break between each file (default ON).")
    p.add_argument("--no-pagebreaks", dest="pagebreaks", action="store_false", help="Do not insert page breaks between files.")

    p.add_argument("--include-outline", action="store_true", default=False, help="Include 00_outline.md in the PDF (default OFF).")
    p.add_argument("--outline-name", type=str, default="00_outline.md", help="Name of the outline file to exclude/include.")

    p.add_argument("--exts", type=str, default=".md,.markdown", help="Comma-separated list of file extensions to include.")
    p.add_argument("--file-dividers", action="store_true", default=False, help="Insert horizontal-rule dividers (and source comments) between files.")
    p.add_argument("--pandoc-arg", action="append", default=[], help="Extra pandoc arg (repeatable). Example: --pandoc-arg=--toc")
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    manual_dir: Path = args.manual_dir.resolve()

    if not manual_dir.exists() or not manual_dir.is_dir():
        print(f"ERROR: manual_dir does not exist or is not a directory: {manual_dir}", file=os.sys.stderr)
        return 1

    pandoc_path = resolve_executable(args.pandoc)
    if pandoc_path is None:
        print(
            "ERROR: Could not find 'pandoc' on PATH.\n\n"
            "Fix options (Windows):\n"
            "  1) Install via conda:\n"
            "     conda install -c conda-forge pandoc\n"
            "  2) Install Pandoc system-wide and restart your terminal.\n"
            "  3) Pass an explicit path:\n"
            "     python build_manual_pdf.py manual/ --pandoc \"C:\\\\Path\\\\to\\\\pandoc.exe\"\n\n"
            "Quick check:\n"
            "  where pandoc\n"
            "  pandoc --version\n",
            file=os.sys.stderr,
        )
        return 1

    # Warn if PDF engine isn't discoverable; pandoc will also error if missing.
    engine_path = resolve_executable(args.pdf_engine)
    if engine_path is None:
        print(
            f"WARNING: Could not find PDF engine '{args.pdf_engine}' on PATH. "
            "Pandoc will fail unless a LaTeX engine is installed and discoverable.\n"
            "Windows suggestions:\n"
            "  - Install MiKTeX (recommended) and ensure its bin folder is on PATH, OR\n"
            "  - Install TeX Live.\n"
            "Quick check:\n"
            f"  where {args.pdf_engine}\n",
            file=os.sys.stderr,
        )

    include_exts = {e.strip().lower() for e in args.exts.split(",") if e.strip()}
    include_exts = {("." + e) if not e.startswith(".") else e for e in include_exts}

    yaml_path: Optional[Path] = args.yaml
    if yaml_path is None:
        candidate = manual_dir / "manual_pdf.yaml"
        if candidate.exists():
            yaml_path = candidate

    if args.output is not None:
        out_pdf = args.output.resolve()
    else:
        dist_dir = manual_dir.parent / "dist"
        dist_dir.mkdir(parents=True, exist_ok=True)
        out_pdf = (dist_dir / f"{manual_dir.name}.pdf").resolve()

    files = iter_markdown_files(
        manual_dir=manual_dir,
        include_exts=include_exts,
        include_outline=args.include_outline,
        outline_name=args.outline_name,
    )

    if not files:
        print("ERROR: No Markdown files found to compile.", file=os.sys.stderr)
        return 1

    assembled_text = assemble_markdown(
        files=files,
        add_pagebreaks=args.pagebreaks,
        include_file_dividers=args.file_dividers,
    )

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        assembly_md = td_path / "manual_assembly.md"
        assembly_md.write_text(assembled_text, encoding="utf-8")

        try:
            run_pandoc(
                pandoc_exe=pandoc_path,
                assembly_md_path=assembly_md,
                output_pdf_path=out_pdf,
                yaml_path=yaml_path.resolve() if yaml_path else None,
                pdf_engine=args.pdf_engine,
                extra_pandoc_args=args.pandoc_arg,
            )
        except RuntimeError as ex:
            print(str(ex), file=os.sys.stderr)
            return 1

    print(f"Wrote PDF: {out_pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
