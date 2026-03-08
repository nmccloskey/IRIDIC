from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable, Optional


MD_EXTS = {".md", ".markdown"}


def normalize_exts(exts: set[str] | None) -> set[str]:
    """
    Normalize extension strings to lowercase dotted forms.
    """
    if not exts:
        return set(MD_EXTS)

    normalized = {e.strip().lower() for e in exts if e and e.strip()}
    return {("." + e) if not e.startswith(".") else e for e in normalized}


def resolve_executable(name: str) -> str:
    """
    Resolve an executable from PATH or raise a helpful error.
    """
    resolved = shutil.which(name)
    if not resolved:
        raise FileNotFoundError(
            f"Required executable not found on PATH: {name}"
        )
    return resolved


def iter_markdown_files(
    manual_dir: Path,
    *,
    include_exts: set[str] | None = None,
    include_outline: bool = False,
    outline_name: str = "00_outline.md",
) -> list[Path]:
    """
    Collect markdown files under manual_dir in stable lexical/path order.

    Hidden paths and __pycache__ are skipped.
    """
    manual_dir = manual_dir.resolve()
    include_exts = normalize_exts(include_exts)

    paths: list[Path] = []
    for path in manual_dir.rglob("*"):
        if not path.is_file():
            continue

        rel = path.relative_to(manual_dir)

        if any(part.startswith(".") for part in rel.parts):
            continue
        if "__pycache__" in rel.parts:
            continue
        if path.suffix.lower() not in include_exts:
            continue
        if not include_outline and path.name == outline_name:
            continue

        paths.append(path)

    paths.sort(key=lambda p: tuple(part.lower() for part in p.relative_to(manual_dir).parts))
    return paths


def strip_leading_heading_numbers(text: str) -> str:
    """
    Remove leading numeric prefixes from ATX headings.

    Examples
    --------
    '# 03 Overview' -> '# Overview'
    '## 03_02 Methods' -> '## Methods'
    """
    import re

    lines = []
    pattern = re.compile(r"^(#{1,6}\s+)\d+(?:[_-]\d+)*\s*[-:)]?\s*")
    for line in text.splitlines():
        lines.append(pattern.sub(r"\1", line))
    return "\n".join(lines)


def add_pagebreaks_between_sections(chunks: list[str]) -> str:
    """
    Join section chunks with LaTeX page breaks for Pandoc PDF compilation.
    """
    if not chunks:
        return ""

    pagebreak = "\n\n\\newpage\n\n"
    return pagebreak.join(chunks).strip() + "\n"


def assemble_markdown(
    files: Iterable[Path],
    *,
    manual_dir: Path,
    strip_heading_numbers: bool = True,
    pagebreaks: bool = True,
    file_dividers: bool = False,
) -> str:
    """
    Assemble multiple markdown files into one markdown document.
    """
    chunks: list[str] = []

    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")

        if strip_heading_numbers:
            text = strip_leading_heading_numbers(text)

        rel = path.relative_to(manual_dir).as_posix()

        if file_dividers:
            divider = [
                f"<!-- BEGIN FILE: {rel} -->",
                "",
                text.strip(),
                "",
                f"<!-- END FILE: {rel} -->",
            ]
            chunk = "\n".join(divider)
        else:
            chunk = text.strip()

        if chunk:
            chunks.append(chunk)

    if pagebreaks:
        return add_pagebreaks_between_sections(chunks)

    return "\n\n".join(chunks).strip() + ("\n" if chunks else "")


def run_pandoc(
    *,
    markdown_path: Path,
    output_path: Path,
    pandoc: str = "pandoc",
    pdf_engine: str = "xelatex",
    yaml_path: Path | None = None,
    extra_args: list[str] | None = None,
) -> None:
    """
    Run pandoc to compile a markdown file to PDF.
    """
    pandoc_exec = resolve_executable(pandoc)

    cmd = [
        pandoc_exec,
        str(markdown_path),
        "-o",
        str(output_path),
        "--pdf-engine",
        pdf_engine,
    ]

    if yaml_path is not None:
        cmd.extend(["--metadata-file", str(yaml_path)])

    if extra_args:
        cmd.extend(extra_args)

    proc = subprocess.run(
        cmd,
        check=False,
        capture_output=True,
        text=True,
    )

    if proc.returncode != 0:
        stderr = proc.stderr.strip()
        stdout = proc.stdout.strip()
        details = "\n".join(part for part in [stdout, stderr] if part)
        raise RuntimeError(
            f"Pandoc compilation failed with exit code {proc.returncode}.\n{details}"
        )


def build_manual_pdf(
    manual_dir: Path,
    *,
    yaml_path: Path | None = None,
    output_path: Path | None = None,
    pandoc: str = "pandoc",
    pdf_engine: str = "xelatex",
    pagebreaks: bool = True,
    strip_heading_numbers: bool = True,
    include_outline: bool = False,
    outline_name: str = "00_outline.md",
    include_exts: set[str] | None = None,
    file_dividers: bool = False,
    extra_pandoc_args: list[str] | None = None,
    keep_temp_md: bool = False,
    temp_md_path: Path | None = None,
) -> Path:
    """
    Build a PDF manual from modular markdown files.

    Parameters
    ----------
    manual_dir
        Root manual directory to scan.
    yaml_path
        Optional Pandoc metadata YAML.
    output_path
        Destination PDF path. Defaults to <manual_dir>/<manual_dir_name>.pdf
    pandoc
        Pandoc executable name or path.
    pdf_engine
        Pandoc PDF engine, e.g. xelatex.
    pagebreaks
        Insert page breaks between assembled sections.
    strip_heading_numbers
        Remove numeric prefixes from headings before compilation.
    include_outline
        Whether to include 00_outline.md in the compiled PDF.
    outline_name
        Outline filename to optionally exclude/include.
    include_exts
        Markdown-like file extensions to include.
    file_dividers
        Insert HTML comments marking file boundaries in the assembled markdown.
    extra_pandoc_args
        Additional args passed through to pandoc.
    keep_temp_md
        Keep the assembled temporary markdown file.
    temp_md_path
        Explicit path for the assembled markdown file.

    Returns
    -------
    Path
        Written PDF path.
    """
    manual_dir = manual_dir.resolve()
    if not manual_dir.exists() or not manual_dir.is_dir():
        raise FileNotFoundError(f"manual_dir does not exist or is not a directory: {manual_dir}")

    yaml_path = yaml_path.resolve() if yaml_path is not None else None

    if output_path is None:
        output_path = (manual_dir / f"{manual_dir.name}.pdf").resolve()
    else:
        output_path = output_path.resolve()

    files = iter_markdown_files(
        manual_dir,
        include_exts=include_exts,
        include_outline=include_outline,
        outline_name=outline_name,
    )

    if not files:
        raise FileNotFoundError(f"No markdown files found under: {manual_dir}")

    assembled = assemble_markdown(
        files,
        manual_dir=manual_dir,
        strip_heading_numbers=strip_heading_numbers,
        pagebreaks=pagebreaks,
        file_dividers=file_dividers,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if temp_md_path is not None:
        temp_md_path = temp_md_path.resolve()
        temp_md_path.parent.mkdir(parents=True, exist_ok=True)
        temp_md_path.write_text(assembled, encoding="utf-8")
        md_path = temp_md_path
        cleanup = False
    else:
        tmp = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".md",
            prefix="iridic_manual_",
            delete=False,
            encoding="utf-8",
        )
        try:
            tmp.write(assembled)
            tmp.flush()
        finally:
            tmp.close()
        md_path = Path(tmp.name)
        cleanup = not keep_temp_md

    try:
        run_pandoc(
            markdown_path=md_path,
            output_path=output_path,
            pandoc=pandoc,
            pdf_engine=pdf_engine,
            yaml_path=yaml_path,
            extra_args=extra_pandoc_args,
        )
    finally:
        if cleanup and md_path.exists():
            md_path.unlink(missing_ok=True)

    return output_path


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compile a modular markdown manual to PDF with Pandoc.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("manual_dir", type=Path, help="Path to the manual directory.")
    parser.add_argument(
        "-y",
        "--yaml",
        dest="yaml_path",
        type=Path,
        default=None,
        help="Optional Pandoc metadata YAML file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_path",
        type=Path,
        default=None,
        help="Output PDF path. Default: <manual_dir>/<manual_dir_name>.pdf",
    )
    parser.add_argument(
        "--pandoc",
        default="pandoc",
        help="Pandoc executable name or path.",
    )
    parser.add_argument(
        "--pdf-engine",
        default="xelatex",
        help="Pandoc PDF engine.",
    )
    parser.add_argument(
        "--no-pagebreaks",
        action="store_true",
        help="Do not insert page breaks between manual sections.",
    )
    parser.add_argument(
        "--keep-heading-numbers",
        action="store_true",
        help="Keep numeric prefixes in headings.",
    )
    parser.add_argument(
        "--include-outline",
        action="store_true",
        help="Include 00_outline.md in the assembled PDF.",
    )
    parser.add_argument(
        "--outline-name",
        default="00_outline.md",
        help="Outline filename to exclude/include.",
    )
    parser.add_argument(
        "--exts",
        default=".md,.markdown",
        help="Comma-separated list of included file extensions.",
    )
    parser.add_argument(
        "--file-dividers",
        action="store_true",
        help="Insert HTML file-boundary comments into the assembled markdown.",
    )
    parser.add_argument(
        "--extra-pandoc-arg",
        dest="extra_pandoc_args",
        action="append",
        default=None,
        help="Extra argument to pass through to Pandoc. Repeat as needed.",
    )
    parser.add_argument(
        "--keep-temp-md",
        action="store_true",
        help="Keep the assembled temporary markdown file.",
    )
    parser.add_argument(
        "--temp-md-path",
        type=Path,
        default=None,
        help="Write assembled markdown to this path instead of a temporary file.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)

    include_exts = normalize_exts(set(args.exts.split(",")))

    try:
        output = build_manual_pdf(
            args.manual_dir,
            yaml_path=args.yaml_path,
            output_path=args.output_path,
            pandoc=args.pandoc,
            pdf_engine=args.pdf_engine,
            pagebreaks=not args.no_pagebreaks,
            strip_heading_numbers=not args.keep_heading_numbers,
            include_outline=args.include_outline,
            outline_name=args.outline_name,
            include_exts=include_exts,
            file_dividers=args.file_dividers,
            extra_pandoc_args=args.extra_pandoc_args,
            keep_temp_md=args.keep_temp_md,
            temp_md_path=args.temp_md_path,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote PDF: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
