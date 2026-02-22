# Manual Export Protocol

## IRIDIC -- Manual Compilation & Archival Workflow

**Version:** 0.1.0\
**Date:** 2026-02-21\
**Applies to:** All IRIDIC-governed modular manuals

------------------------------------------------------------------------

## 1. Purpose

This protocol defines the standardized workflow for exporting a modular
Markdown manual to an archival-ready PDF.

It integrates the following IRIDIC scripts:

-   `build_manual_outline.py`
-   `check_manual_chars.py`
-   `build_manual_pdf.py`

This ensures:

-   Clean encoding
-   Stable ordering
-   Reproducible compilation
-   Archival consistency (e.g., Zenodo)

------------------------------------------------------------------------

## 2. Pre-Export Requirements

Before exporting:

-   All manual files must be UTF-8 encoded.
-   Numeric prefixes must reflect intended ordering.
-   `manual_pdf.yaml` must exist inside `manual/` (unless explicitly
    overridden).
-   Pandoc must be installed and accessible.
-   A LaTeX engine (e.g., `xelatex`) must be installed.

------------------------------------------------------------------------

## 3. Standard Export Workflow

### Step 1 --- Character & Encoding Check

Scan for encoding problems and forbidden control characters:

``` bash
python src/check_manual_chars.py manual/
```

Optional stricter checks:

``` bash
python src/check_manual_chars.py manual/ --check-trailing --check-line-endings
```

Auto-fix common hygiene issues:

``` bash
python src/check_manual_chars.py manual/ --strip-trailing --fix-line-endings lf
```

If errors are reported, correct them before proceeding.

------------------------------------------------------------------------

### Step 2 --- Generate or Refresh Outline

Rebuild `00_outline.md`:

``` bash
python src/build_manual_outline.py manual/ --title "IRIDIC Instruction Manual" --version "0.1.0"
```

This ensures predictable structure and consistent PDF assembly.

------------------------------------------------------------------------

### Step 3 --- Compile PDF

Generate the PDF:

``` bash
python src/build_manual_pdf.py manual/ --yaml manual/manual_pdf.yaml
```

Default behavior:

-   Recursively collects Markdown files
-   Sorts via numeric prefixes
-   Inserts page breaks between sections
-   Produces output in `dist/`

Custom output:

``` bash
python src/build_manual_pdf.py manual/ --output dist/IRIDIC_Manual_v0.1.0.pdf
```

Include outline in final PDF:

``` bash
python src/build_manual_pdf.py manual/ --include-outline
```

------------------------------------------------------------------------

## 4. Output Location

By default:

    IRIDIC/dist/manual.pdf

Recommended naming convention:

    <ProjectName>_Manual_vX.Y.Z.pdf

Example:

    IRIDIC_Manual_v0.1.0.pdf

------------------------------------------------------------------------

## 5. Code Block Wrapping (LaTeX Requirement)

To ensure long Bash commands wrap properly, `manual_pdf.yaml` must
include:

``` yaml
header-includes:
  - \usepackage{fvextra}
  - \DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaklines,breakanywhere,commandchars=\\\{\}}
```

Without this, long commands may run off the page.

------------------------------------------------------------------------

## 6. Recommended Full Export Command Sequence

For reproducible builds:

``` bash
python src/check_manual_chars.py manual/ &&
python src/build_manual_outline.py manual/ --title "IRIDIC Instruction Manual" --version "0.1.0" &&
python src/build_manual_pdf.py manual/ --yaml manual/manual_pdf.yaml --output dist/IRIDIC_Manual_v0.1.0.pdf
```

------------------------------------------------------------------------

## 7. Archival Preparation (Zenodo)

Before upload:

-   Verify version number matches repository tag.
-   Ensure `manual_pdf.yaml` version field matches PDF filename.
-   Confirm no warnings from character check.
-   Commit generated `00_outline.md` (if policy requires).
-   Archive PDF alongside repository snapshot.

------------------------------------------------------------------------

## 8. Optional CI Integration

This protocol may be automated in CI:

1.  Run `check_manual_chars.py`
2.  Regenerate outline
3.  Compile PDF
4.  Upload artifact

Future enhancement: IRIDIC CLI wrapper to unify all three steps.

------------------------------------------------------------------------

## 9. Anti-Patterns

-   Skipping character validation
-   Manually concatenating files
-   Hardcoding file order in scripts
-   Embedding YAML front matter in every manual section
-   Using inconsistent numeric prefixes

------------------------------------------------------------------------

## 10. Summary

This protocol formalizes a reproducible documentation pipeline:

Modular Markdown → Validation → Structured Outline → PDF Compilation →
Archival Output

It separates:

-   Structure (policy)
-   Validation (hygiene)
-   Compilation (protocol)
-   Presentation (future web protocol)
