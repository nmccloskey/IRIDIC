#!/usr/bin/env python
"""
check_manual_chars.py

Scan a manual/ directory (or any directory) for character/encoding issues that tend
to break PDF compilation (Pandoc/LaTeX) or cause subtle rendering problems.

What it checks
--------------
1) UTF-8 decodability (strict) for *.md / *.markdown by default
2) Presence of "forbidden" control characters
   - C0 controls: U+0000–U+001F (except TAB, LF, CR)
   - DEL: U+007F
   - C1 controls: U+0080–U+009F (includes U+0081 which often triggers cp1252 issues)
3) Optional checks (off by default):
   - Non-ASCII characters (report only, not an error unless requested)
   - Trailing whitespace
   - Mixed line endings (CRLF vs LF) report

Exit codes
----------
0 = no problems found (or only warnings, depending on flags)
1 = problems found (or warnings treated as errors)

Typical usage
-------------
python check_manual_chars.py manual/
python check_manual_chars.py manual/ --fail-on-nonascii
python check_manual_chars.py manual/ --fix-line-endings lf --strip-trailing

Integration tips
----------------
- Use in CI (GitHub Actions) and/or pre-commit.
- Make it part of your manual compilation protocol: run this before pandoc.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple


DEFAULT_EXTS = {".md", ".markdown"}

# Allowed C0 whitespace controls commonly present in text files
_ALLOWED_CONTROLS = {0x09, 0x0A, 0x0D}  # TAB, LF, CR

# Control character ranges to flag (excluding allowed)
_CONTROL_RANGES: List[Tuple[int, int]] = [
    (0x00, 0x1F),   # C0
    (0x7F, 0x7F),   # DEL
    (0x80, 0x9F),   # C1
]


@dataclass(frozen=True)
class Finding:
    path: Path
    line: Optional[int]
    col: Optional[int]
    codepoint: Optional[int]
    kind: str  # "decode", "control", "nonascii", "trailing", "lineendings"
    message: str


def iter_target_files(root: Path, exts: set[str], include_hidden: bool) -> List[Path]:
    files: List[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in exts:
            continue
        rel = p.relative_to(root)
        if not include_hidden and any(part.startswith(".") for part in rel.parts):
            continue
        if "__pycache__" in rel.parts:
            continue
        files.append(p)
    files.sort()
    return files


def is_control(cp: int) -> bool:
    for lo, hi in _CONTROL_RANGES:
        if lo <= cp <= hi:
            return True
    return False


def find_controls(text: str, path: Path) -> List[Finding]:
    findings: List[Finding] = []
    line = 1
    col = 0
    for ch in text:
        cp = ord(ch)
        if ch == "\n":
            line += 1
            col = 0
            continue
        col += 1
        if is_control(cp) and cp not in _ALLOWED_CONTROLS:
            findings.append(
                Finding(
                    path=path,
                    line=line,
                    col=col,
                    codepoint=cp,
                    kind="control",
                    message=f"Forbidden control character U+{cp:04X} at line {line}, col {col}.",
                )
            )
    return findings


def find_nonascii(text: str, path: Path) -> List[Finding]:
    findings: List[Finding] = []
    line = 1
    col = 0
    for ch in text:
        if ch == "\n":
            line += 1
            col = 0
            continue
        col += 1
        cp = ord(ch)
        if cp > 0x7F:
            findings.append(
                Finding(
                    path=path,
                    line=line,
                    col=col,
                    codepoint=cp,
                    kind="nonascii",
                    message=f"Non-ASCII character U+{cp:04X} at line {line}, col {col}: {repr(ch)}",
                )
            )
    return findings


def find_trailing_whitespace(lines: Sequence[str], path: Path) -> List[Finding]:
    findings: List[Finding] = []
    for i, ln in enumerate(lines, start=1):
        if ln.endswith(" ") or ln.endswith("\t"):
            findings.append(
                Finding(
                    path=path,
                    line=i,
                    col=len(ln),
                    codepoint=None,
                    kind="trailing",
                    message=f"Trailing whitespace at line {i}.",
                )
            )
    return findings


def detect_line_endings(raw: bytes) -> str:
    """
    Returns: "lf", "crlf", "cr", or "mixed"
    """
    has_lf = b"\n" in raw
    has_crlf = b"\r\n" in raw
    has_cr = b"\r" in raw

    # If has CRLF, it also has LF, so check patterns
    if has_crlf:
        # Mixed if there exist bare LF not part of CRLF
        raw_no_crlf = raw.replace(b"\r\n", b"")
        if b"\n" in raw_no_crlf:
            return "mixed"
        return "crlf"

    if has_cr and not has_lf:
        return "cr"
    if has_lf and not has_cr:
        return "lf"
    if has_cr and has_lf:
        return "mixed"
    return "lf"  # empty file case


def normalize_line_endings(text: str, target: str) -> str:
    # Normalize first to \n
    t = text.replace("\r\n", "\n").replace("\r", "\n")
    if target == "lf":
        return t
    if target == "crlf":
        return t.replace("\n", "\r\n")
    raise ValueError(f"Unsupported line ending target: {target}")


def strip_trailing_ws(text: str) -> str:
    # Preserve final newline if present
    ends_with_nl = text.endswith("\n") or text.endswith("\r\n")
    t = text.replace("\r\n", "\n").replace("\r", "\n")
    t2 = "\n".join([ln.rstrip(" \t") for ln in t.split("\n")])
    if ends_with_nl and not t2.endswith("\n"):
        t2 += "\n"
    return t2


def scan_file(
    path: Path,
    root: Path,
    report_nonascii: bool,
    check_trailing: bool,
    check_line_endings: bool,
) -> Tuple[List[Finding], Optional[str], Optional[str]]:
    """
    Returns (findings, text_if_decoded, raw_line_endings)
    """
    findings: List[Finding] = []

    raw = path.read_bytes()
    line_endings = detect_line_endings(raw) if check_line_endings else None

    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as e:
        # Pinpoint failure position
        findings.append(
            Finding(
                path=path,
                line=None,
                col=None,
                codepoint=None,
                kind="decode",
                message=(
                    "UTF-8 decode failed (strict). "
                    f"Byte offset {e.start}..{e.end}; reason: {e.reason}."
                ),
            )
        )
        return findings, None, line_endings

    findings.extend(find_controls(text, path))

    if report_nonascii:
        findings.extend(find_nonascii(text, path))

    if check_trailing:
        # Use normalized newlines for line indexing
        norm = text.replace("\r\n", "\n").replace("\r", "\n")
        lines = norm.split("\n")
        # Drop the final empty split if file ends with newline (keeps numbering sensible)
        if lines and lines[-1] == "":
            lines = lines[:-1]
        findings.extend(find_trailing_whitespace(lines, path))

    if check_line_endings and line_endings in {"mixed", "cr"}:
        findings.append(
            Finding(
                path=path,
                line=None,
                col=None,
                codepoint=None,
                kind="lineendings",
                message=f"Line endings detected: {line_endings}. Consider normalizing to lf or crlf.",
            )
        )

    return findings, text, line_endings


def apply_fixes(
    path: Path,
    text: str,
    fix_line_endings: Optional[str],
    strip_trailing: bool,
) -> bool:
    """
    Apply requested fixes. Returns True if file content changed.
    """
    original = text
    t = text

    if strip_trailing:
        t = strip_trailing_ws(t)

    if fix_line_endings is not None:
        t = normalize_line_endings(t, fix_line_endings)

    if t != original:
        path.write_text(t, encoding="utf-8", newline="")
        return True

    return False


def format_finding(f: Finding, root: Path) -> str:
    rel = f.path.resolve()
    try:
        rel = f.path.resolve().relative_to(root.resolve())
    except Exception:
        rel = f.path

    loc = ""
    if f.line is not None and f.col is not None:
        loc = f":{f.line}:{f.col}"
    elif f.line is not None:
        loc = f":{f.line}"

    cp = ""
    if f.codepoint is not None:
        cp = f" [U+{f.codepoint:04X}]"

    return f"{rel.as_posix()}{loc}: {f.kind}{cp}: {f.message}"


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Scan Markdown manuals for UTF-8/control character issues that can break PDF compilation.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("root", type=Path, help="Directory to scan (e.g., manual/).")

    p.add_argument("--exts", type=str, default=".md,.markdown", help="Comma-separated file extensions to include.")
    p.add_argument("--include-hidden", action="store_true", default=False, help="Include hidden files/directories.")

    p.add_argument("--report-nonascii", action="store_true", default=False, help="Report all non-ASCII characters (warnings by default).")
    p.add_argument("--fail-on-nonascii", action="store_true", default=False, help="Treat non-ASCII findings as errors.")

    p.add_argument("--check-trailing", action="store_true", default=False, help="Report trailing whitespace.")
    p.add_argument("--strip-trailing", action="store_true", default=False, help="Auto-fix: strip trailing whitespace.")

    p.add_argument("--check-line-endings", action="store_true", default=False, help="Report mixed/CR line endings.")
    p.add_argument("--fix-line-endings", choices=["lf", "crlf"], default=None, help="Auto-fix: normalize line endings.")

    p.add_argument("--max-nonascii", type=int, default=50, help="Limit non-ASCII findings per file (for readability).")

    p.add_argument("--warnings-as-errors", action="store_true", default=False, help="Treat warnings as errors (nonascii/trailing/lineendings).")

    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()

    if not root.exists() or not root.is_dir():
        print(f"ERROR: root is not a directory: {root}", file=sys.stderr)
        return 2

    exts = {e.strip().lower() for e in args.exts.split(",") if e.strip()}
    exts = {("." + e) if not e.startswith(".") else e for e in exts}

    targets = iter_target_files(root, exts=exts, include_hidden=args.include_hidden)
    if not targets:
        print("No files matched. Nothing to do.")
        return 0

    all_findings: List[Finding] = []
    fixed_files: List[Path] = []

    for fp in targets:
        findings, text, _ = scan_file(
            path=fp,
            root=root,
            report_nonascii=args.report_nonascii or args.fail_on_nonascii,
            check_trailing=args.check_trailing or args.strip_trailing,
            check_line_endings=args.check_line_endings or (args.fix_line_endings is not None),
        )

        # Cap non-ascii spam per file (unless failing on it)
        if (args.report_nonascii or args.fail_on_nonascii) and args.max_nonascii is not None:
            nonascii = [f for f in findings if f.kind == "nonascii"]
            if len(nonascii) > args.max_nonascii:
                keep = nonascii[: args.max_nonascii]
                dropped = len(nonascii) - len(keep)
                findings = [f for f in findings if f.kind != "nonascii"] + keep
                findings.append(
                    Finding(
                        path=fp,
                        line=None,
                        col=None,
                        codepoint=None,
                        kind="nonascii",
                        message=f"Non-ASCII findings truncated for readability (+{dropped} more).",
                    )
                )

        all_findings.extend(findings)

        # Apply fixes only if decoding succeeded
        if text is not None and (args.strip_trailing or args.fix_line_endings is not None):
            changed = apply_fixes(
                path=fp,
                text=text,
                fix_line_endings=args.fix_line_endings,
                strip_trailing=args.strip_trailing,
            )
            if changed:
                fixed_files.append(fp)

    # Emit findings
    errors: List[Finding] = []
    warnings: List[Finding] = []

    for f in all_findings:
        if f.kind in {"decode", "control"}:
            errors.append(f)
        elif f.kind == "nonascii" and args.fail_on_nonascii:
            errors.append(f)
        elif args.warnings_as_errors:
            errors.append(f)
        else:
            warnings.append(f)

    if fixed_files:
        print("Fixed files:")
        for fp in fixed_files:
            try:
                rel = fp.resolve().relative_to(root)
            except Exception:
                rel = fp
            print(f"  - {rel.as_posix()}")
        print("")

    if warnings:
        print("Warnings:")
        for f in warnings:
            print("  " + format_finding(f, root))
        print("")

    if errors:
        print("Errors:")
        for f in errors:
            print("  " + format_finding(f, root))
        print("")
        return 1

    print("OK: No errors found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
