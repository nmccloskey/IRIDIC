from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from .manual_index import build_manual_index, render_generated_tree_text, search_manual
from .manual_outline import build_manual_outline, ensure_manual_outline, normalize_exts as normalize_outline_exts
from .manual_chars import check_manual_chars, normalize_exts as normalize_char_exts
from .manual_pdf import build_manual_pdf, normalize_exts as normalize_pdf_exts


def _resolve_path(pathlike: str | Path) -> Path:
    return Path(pathlike).expanduser().resolve()


def _confirm(prompt: str) -> bool:
    while True:
        response = input(f"{prompt} [y/n]: ").strip().lower()
        if response in {"y", "yes"}:
            return True
        if response in {"n", "no"}:
            return False
        print("Please enter 'y' or 'n'.")


def _print_lines(lines: list[str]) -> None:
    for line in lines:
        print(line)


def _parse_csv_exts(raw: Optional[str], normalizer) -> set[str] | None:
    if raw is None:
        return None
    return normalizer(set(part.strip() for part in raw.split(",") if part.strip()))


def cmd_tree(args: argparse.Namespace) -> int:
    manual_dir = _resolve_path(args.manual_dir)

    if not manual_dir.exists():
        print(f"[iridic] Manual directory not found: {manual_dir}", file=sys.stderr)
        return 1

    tree, flat = build_manual_index(manual_dir)

    if not flat:
        print(f"[iridic] No markdown files found under: {manual_dir}", file=sys.stderr)
        return 1

    print(render_generated_tree_text(tree))
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    manual_dir = _resolve_path(args.manual_dir)

    if not manual_dir.exists():
        print(f"[iridic] Manual directory not found: {manual_dir}", file=sys.stderr)
        return 1

    _, flat = build_manual_index(manual_dir)

    if not flat:
        print(f"[iridic] No markdown files found under: {manual_dir}", file=sys.stderr)
        return 1

    results = search_manual(flat, args.query, limit=args.limit)

    if not results:
        print(f"[iridic] No matches for: {args.query}")
        return 0

    for rel_str, score in results:
        mf = flat[rel_str]
        print(f"{score:>3}  {rel_str}  --  {mf.title}")

    return 0


def cmd_index(args: argparse.Namespace) -> int:
    manual_dir = _resolve_path(args.manual_dir)

    if not manual_dir.exists():
        print(f"[iridic] Manual directory not found: {manual_dir}", file=sys.stderr)
        return 1

    tree, flat = build_manual_index(manual_dir)

    print(f"manual_dir: {manual_dir}")
    print(f"files_indexed: {len(flat)}")
    print(f"top_level_nodes: {len(tree)}")

    if args.show_files:
        for rel_str in flat:
            print(rel_str)

    return 0


def cmd_outline(args: argparse.Namespace) -> int:
    manual_dir = _resolve_path(args.manual_dir)
    output_path = _resolve_path(args.output) if args.output else None
    include_exts = _parse_csv_exts(args.exts, normalize_outline_exts)

    try:
        if args.if_missing_only:
            output = ensure_manual_outline(
                manual_dir,
                output_path=output_path,
                manual_title=args.title,
                manual_version=args.version,
                include_exts=include_exts,
                max_depth=args.max_depth,
                if_missing_only=True,
            )
        else:
            output = build_manual_outline(
                manual_dir,
                output_path=output_path,
                manual_title=args.title,
                manual_version=args.version,
                include_exts=include_exts,
                max_depth=args.max_depth,
            )
    except Exception as exc:
        print(f"[iridic] ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote outline: {output}")
    return 0


def cmd_chars(args: argparse.Namespace) -> int:
    root = _resolve_path(args.root)
    exts = _parse_csv_exts(args.exts, normalize_char_exts)

    try:
        result = check_manual_chars(
            root,
            exts=exts,
            include_hidden=args.include_hidden,
            report_nonascii=args.report_nonascii,
            fail_on_nonascii=args.fail_on_nonascii,
            check_trailing=args.check_trailing,
            strip_trailing=args.strip_trailing,
            check_line_endings=args.check_line_endings,
            fix_line_endings=args.fix_line_endings,
            max_nonascii=args.max_nonascii,
            warnings_as_errors=args.warnings_as_errors,
        )
    except Exception as exc:
        print(f"[iridic] ERROR: {exc}", file=sys.stderr)
        return 1

    if args.summary_only:
        _print_lines(result.summary_lines())
    else:
        _print_lines(result.report_lines(show_lines=not args.no_line_context))

    return 0 if result.ok else 1


def cmd_pdf(args: argparse.Namespace) -> int:
    manual_dir = _resolve_path(args.manual_dir)
    yaml_path = _resolve_path(args.yaml_path) if args.yaml_path else None
    output_path = _resolve_path(args.output_path) if args.output_path else None
    temp_md_path = _resolve_path(args.temp_md_path) if args.temp_md_path else None
    include_exts = _parse_csv_exts(args.exts, normalize_pdf_exts)

    if not manual_dir.exists():
        print(f"[iridic] Manual directory not found: {manual_dir}", file=sys.stderr)
        return 1

    # Optional outline step
    if not args.skip_outline:
        try:
            outline_output = ensure_manual_outline(
                manual_dir,
                output_path=None,
                manual_title=args.outline_title,
                manual_version=args.outline_version,
                include_exts=None,
                max_depth=args.outline_max_depth,
                if_missing_only=not args.rebuild_outline,
            )
            print(f"[iridic] Outline ready: {outline_output}")
        except Exception as exc:
            print(f"[iridic] ERROR during outline step: {exc}", file=sys.stderr)
            return 1

    # Optional character preflight
    if not args.skip_chars:
        try:
            char_result = check_manual_chars(
                manual_dir,
                exts=None,
                include_hidden=args.include_hidden,
                report_nonascii=args.report_nonascii,
                fail_on_nonascii=args.fail_on_nonascii,
                check_trailing=args.check_trailing,
                strip_trailing=args.strip_trailing,
                check_line_endings=args.check_line_endings,
                fix_line_endings=args.fix_line_endings,
                max_nonascii=args.max_nonascii,
                warnings_as_errors=args.warnings_as_errors,
            )
        except Exception as exc:
            print(f"[iridic] ERROR during character check: {exc}", file=sys.stderr)
            return 1

        if args.summary_only:
            _print_lines(char_result.summary_lines())
        else:
            _print_lines(char_result.report_lines(show_lines=not args.no_line_context))

        has_issues = bool(char_result.warnings or char_result.errors)

        if has_issues and not args.force:
            if args.non_interactive:
                print(
                    "[iridic] Character/content issues were found. "
                    "Aborting in non-interactive mode.",
                    file=sys.stderr,
                )
                return 1

            if not _confirm("Issues were found. Proceed to PDF compilation anyway?"):
                print("[iridic] Aborted.")
                return 0

    try:
        output = build_manual_pdf(
            manual_dir,
            yaml_path=yaml_path,
            output_path=output_path,
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
            temp_md_path=temp_md_path,
        )
    except Exception as exc:
        print(f"[iridic] ERROR during PDF build: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote PDF: {output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="iridic",
        description="Utilities for indexing, viewing, validating, and compiling project manuals.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_tree = subparsers.add_parser("tree", help="Print the generated manual tree.")
    p_tree.add_argument(
        "manual_dir",
        nargs="?",
        default="manual",
        help="Path to the manual directory.",
    )
    p_tree.set_defaults(func=cmd_tree)

    p_search = subparsers.add_parser("search", help="Search manual titles and content.")
    p_search.add_argument("query", help="Search query.")
    p_search.add_argument(
        "manual_dir",
        nargs="?",
        default="manual",
        help="Path to the manual directory.",
    )
    p_search.add_argument(
        "--limit",
        type=int,
        default=25,
        help="Maximum number of results to display.",
    )
    p_search.set_defaults(func=cmd_search)

    p_index = subparsers.add_parser("index", help="Summarize the indexed manual.")
    p_index.add_argument(
        "manual_dir",
        nargs="?",
        default="manual",
        help="Path to the manual directory.",
    )
    p_index.add_argument(
        "--show-files",
        action="store_true",
        help="Print indexed relative file paths.",
    )
    p_index.set_defaults(func=cmd_index)

    p_outline = subparsers.add_parser("outline", help="Build or refresh the manual outline.")
    p_outline.add_argument(
        "manual_dir",
        nargs="?",
        default="manual",
        help="Path to the manual directory.",
    )
    p_outline.add_argument(
        "-o",
        "--output",
        default=None,
        help="Optional output outline path.",
    )
    p_outline.add_argument(
        "--title",
        default="Instruction Manual",
        help="Manual title for the outline header.",
    )
    p_outline.add_argument(
        "--version",
        default="0.0.0",
        help="Manual version string for the outline header.",
    )
    p_outline.add_argument(
        "--exts",
        default=".md,.markdown",
        help="Comma-separated list of file extensions to include.",
    )
    p_outline.add_argument(
        "--max-depth",
        type=int,
        default=None,
        help="Maximum directory depth to render in the tree.",
    )
    p_outline.add_argument(
        "--if-missing-only",
        action="store_true",
        help="Only build the outline if it does not already exist.",
    )
    p_outline.set_defaults(func=cmd_outline)

    p_chars = subparsers.add_parser("chars", help="Run character/content checks on documentation files.")
    p_chars.add_argument(
        "root",
        nargs="?",
        default="manual",
        help="Root directory to scan.",
    )
    p_chars.add_argument(
        "--exts",
        default=".md,.markdown,.txt,.yaml,.yml,.toml,.json,.py",
        help="Comma-separated list of file extensions to include.",
    )
    p_chars.add_argument(
        "--include-hidden",
        action="store_true",
        help="Include hidden files and directories.",
    )
    p_chars.add_argument(
        "--report-nonascii",
        action="store_true",
        help="Report non-ASCII characters as warnings.",
    )
    p_chars.add_argument(
        "--fail-on-nonascii",
        action="store_true",
        help="Report non-ASCII characters as errors.",
    )
    p_chars.add_argument(
        "--check-trailing",
        action="store_true",
        help="Check for trailing whitespace.",
    )
    p_chars.add_argument(
        "--strip-trailing",
        action="store_true",
        help="Strip trailing whitespace in place before scanning.",
    )
    p_chars.add_argument(
        "--check-line-endings",
        action="store_true",
        help="Check for CRLF line endings.",
    )
    p_chars.add_argument(
        "--fix-line-endings",
        choices=["lf", "crlf"],
        default=None,
        help="Normalize line endings before scanning.",
    )
    p_chars.add_argument(
        "--max-nonascii",
        type=int,
        default=50,
        help="Maximum unique non-ASCII characters to list per line.",
    )
    p_chars.add_argument(
        "--warnings-as-errors",
        action="store_true",
        help="Promote warnings to errors for exit status purposes.",
    )
    p_chars.add_argument(
        "--no-line-context",
        action="store_true",
        help="Do not print offending line text in the report.",
    )
    p_chars.add_argument(
        "--summary-only",
        action="store_true",
        help="Print only the summary.",
    )
    p_chars.set_defaults(func=cmd_chars)

    p_pdf = subparsers.add_parser("pdf", help="Compile the manual PDF.")
    p_pdf.add_argument(
        "manual_dir",
        nargs="?",
        default="manual",
        help="Path to the manual directory.",
    )
    p_pdf.add_argument(
        "-y",
        "--yaml",
        dest="yaml_path",
        default=None,
        help="Optional Pandoc metadata YAML file.",
    )
    p_pdf.add_argument(
        "-o",
        "--output",
        dest="output_path",
        default=None,
        help="Optional output PDF path.",
    )
    p_pdf.add_argument(
        "--pandoc",
        default="pandoc",
        help="Pandoc executable name or path.",
    )
    p_pdf.add_argument(
        "--pdf-engine",
        default="xelatex",
        help="Pandoc PDF engine.",
    )
    p_pdf.add_argument(
        "--no-pagebreaks",
        action="store_true",
        help="Do not insert page breaks between sections.",
    )
    p_pdf.add_argument(
        "--keep-heading-numbers",
        action="store_true",
        help="Keep numeric prefixes in headings.",
    )
    p_pdf.add_argument(
        "--include-outline",
        action="store_true",
        help="Include 00_outline.md in the compiled PDF.",
    )
    p_pdf.add_argument(
        "--outline-name",
        default="00_outline.md",
        help="Outline filename to exclude/include.",
    )
    p_pdf.add_argument(
        "--exts",
        default=".md,.markdown",
        help="Comma-separated list of file extensions to include in the PDF build.",
    )
    p_pdf.add_argument(
        "--file-dividers",
        action="store_true",
        help="Insert HTML comments marking file boundaries.",
    )
    p_pdf.add_argument(
        "--extra-pandoc-arg",
        dest="extra_pandoc_args",
        action="append",
        default=None,
        help="Extra argument to pass through to Pandoc. Repeat as needed.",
    )
    p_pdf.add_argument(
        "--keep-temp-md",
        action="store_true",
        help="Keep the assembled markdown file.",
    )
    p_pdf.add_argument(
        "--temp-md-path",
        default=None,
        help="Explicit path for the assembled markdown file.",
    )

    p_pdf.add_argument(
        "--skip-outline",
        action="store_true",
        help="Skip outline generation/checking before compilation.",
    )
    p_pdf.add_argument(
        "--rebuild-outline",
        action="store_true",
        help="Always rebuild the outline before compilation.",
    )
    p_pdf.add_argument(
        "--outline-title",
        default="Instruction Manual",
        help="Manual title for the outline header when outline is ensured.",
    )
    p_pdf.add_argument(
        "--outline-version",
        default="0.0.0",
        help="Manual version for the outline header when outline is ensured.",
    )
    p_pdf.add_argument(
        "--outline-max-depth",
        type=int,
        default=None,
        help="Maximum directory depth for the ensured outline tree.",
    )

    p_pdf.add_argument(
        "--skip-chars",
        action="store_true",
        help="Skip character/content validation before compilation.",
    )
    p_pdf.add_argument(
        "--include-hidden",
        action="store_true",
        help="Include hidden files in the char-check step.",
    )
    p_pdf.add_argument(
        "--report-nonascii",
        action="store_true",
        help="Report non-ASCII characters as warnings during char check.",
    )
    p_pdf.add_argument(
        "--fail-on-nonascii",
        action="store_true",
        help="Report non-ASCII characters as errors during char check.",
    )
    p_pdf.add_argument(
        "--check-trailing",
        action="store_true",
        help="Check for trailing whitespace during char check.",
    )
    p_pdf.add_argument(
        "--strip-trailing",
        action="store_true",
        help="Strip trailing whitespace in place before PDF compilation.",
    )
    p_pdf.add_argument(
        "--check-line-endings",
        action="store_true",
        help="Check for CRLF line endings during char check.",
    )
    p_pdf.add_argument(
        "--fix-line-endings",
        choices=["lf", "crlf"],
        default=None,
        help="Normalize line endings before PDF compilation.",
    )
    p_pdf.add_argument(
        "--max-nonascii",
        type=int,
        default=50,
        help="Maximum unique non-ASCII characters to list per line during char check.",
    )
    p_pdf.add_argument(
        "--warnings-as-errors",
        action="store_true",
        help="Treat warnings as errors for the preflight decision.",
    )
    p_pdf.add_argument(
        "--no-line-context",
        action="store_true",
        help="Do not print offending line text in the char-check report.",
    )
    p_pdf.add_argument(
        "--summary-only",
        action="store_true",
        help="Print only the char-check summary before PDF compilation.",
    )
    p_pdf.add_argument(
        "--non-interactive",
        action="store_true",
        help="Do not prompt; abort if issues are found and --force is not set.",
    )
    p_pdf.add_argument(
        "--force",
        action="store_true",
        help="Proceed to PDF compilation even if issues are found.",
    )

    p_pdf.set_defaults(func=cmd_pdf)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
