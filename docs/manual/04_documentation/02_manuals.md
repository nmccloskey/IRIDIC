# Manuals Policy

## 1. Purpose

This policy defines standards for structuring, naming, organizing, and
maintaining long‑form technical manuals written in Markdown within
IRIDIC‑governed repositories.

It is designed to:

-   Prevent monolithic, unwieldy manuals
-   Support modular growth over time
-   Facilitate PDF compilation (e.g., Zenodo archiving)
-   Enable web presentation (e.g., Streamlit navigation)
-   Preserve clarity, traceability, and version integrity

This document governs *structure*. Presentation protocols (PDF
compilation, web rendering, etc.) are addressed separately.

------------------------------------------------------------------------

## 2. Guiding Principles

### 2.1 Modular by Default

Manuals exceeding \~300--400 lines should be segmented into logically
coherent units.

### 2.2 Hierarchical Clarity

Directory structure should mirror conceptual structure.

### 2.3 Stable Referencing

File names must be predictable and ordered.

### 2.4 Growth Without Rewriting

Adding a new feature should require adding a new file---not
restructuring the entire manual.

### 2.5 Compilation Neutrality

Manuals must remain usable: - As independent Markdown files - As a
compiled PDF - As web-rendered documentation

------------------------------------------------------------------------

## 3. Directory Structure Standard

### 3.1 Root Structure

Example for RASCAL:

    RASCAL/
    │
    ├── manual/
    │   ├── 00_outline.md
    │   ├── 01_introduction.md
    │   ├── 02_installation.md
    │   ├── 03_workflow/
    │   │   ├── 03_01_overview.md
    │   │   ├── 03_02_transcript_tables.md
    │   │   ├── 03_03_cu_coding.md
    │   │   └── 03_04_blinding.md
    │   ├── 04_outputs.md
    │   ├── 05_database_logic.md
    │   ├── 06_examples.md
    │   ├── 99_appendix.md
    │   └── manual_pdf.yaml
    │
    └── README.md

------------------------------------------------------------------------

## 4. File Naming Conventions

### 4.1 Numeric Prefixing (Required)

Format:

    NN_title.md

or nested:

    NN_MM_title.md

Where:

-   `NN` = primary section (00--99)
-   `MM` = subsection (01--99)
-   Lowercase
-   Underscores instead of spaces
-   No special characters

### 4.2 Reserved Numbers

|  Prefix  | Purpose
|  ------- | ------------------------
|  00      | Outline / master index
|  01--89  | Core manual content
|  90--98  | Advanced / optional
|  99      | Appendix

------------------------------------------------------------------------

## 5. Outline File (00_outline.md)

The outline file should include:

-   Hierarchical list of sections
-   Brief description of each
-   Version number
-   Last updated date

It functions as:

-   Human-readable map
-   Anchor for PDF compilation
-   Web navigation backbone

------------------------------------------------------------------------

## 6. Section Design Rules

Each section file should:

-   Be internally coherent
-   Avoid duplicating other sections
-   Use consistent heading depth
-   Remain \< 400--500 lines when possible

If a section exceeds \~600 lines, it should be subdivided.

------------------------------------------------------------------------

## 7. Cross-Referencing Rules

Use relative links:

    See [Transcript Tables](03_workflow/03_02_transcript_tables.md).

Do not use absolute GitHub URLs inside manuals.

------------------------------------------------------------------------

## 8. Versioning the Manual

Manual version should align with:

-   Major software releases (X.0.0)
-   Structural manual changes (minor bump)
-   Typos or clarification edits (patch bump)

Manual version may be stored in:

-   00_outline.md
-   A dedicated VERSION.md
-   PDF front matter (for compiled distributions)

------------------------------------------------------------------------

## 9. Migration Protocol (Monolith → Modular)

When refactoring an 800+ line manual:

1.  Create `manual/` directory.

2.  Extract logical sections into numbered files.

3.  Create `00_outline.md`.

4.  Validate internal links.

5.  Archive original monolithic manual as:

        manual_archive_vX_Y_Z.md

------------------------------------------------------------------------

## 10. Anti-Patterns to Avoid

-   One 1000-line Markdown file
-   Inconsistent numbering
-   Deep nesting (\>3 folder levels)
-   Mixing policy and protocol content
-   Embedding compilation YAML inside every section

------------------------------------------------------------------------

## 11. Rationale

This modular approach enables:

-   Cleaner Git diffs
-   Easier collaboration
-   Incremental feature growth
-   Flexible presentation (CLI, PDF, Web)
-   Long-term maintainability

------------------------------------------------------------------------

## 12. Future Extensions

Separate protocol documents may define:

-   PDF compilation workflows
-   Zenodo packaging standards
-   Streamlit navigation integration
-   Automated TOC generation

------------------------------------------------------------------------

## 13. Manual Export (to PDF)

### 13.1 Encoding

- **Encoding rule:** All manual .md files MUST be saved as UTF-8 (no BOM preferred).

- **Forbidden characters:** Avoid “invisible” control characters from copy/paste (especially from PDFs/Word/Slack). If suspected, retype the line or paste via a plain-text intermediate.

- **Normalization:** Prefer standard ASCII punctuation in headings/filenames; Unicode is allowed in body text, but keep it intentional.

- **Optional check:** use `check_manual_chars.py` to:
    - verify UTF-8 decodability
    - flag C0/C1 control chars (except `\n`, `\t`)
    - report the file + byte offset


### 13.2 Header

Include a `manual_pdf.yaml` under manual/ to:
- specify formatting
- toggle table of contents
- ensure proper line wrapping (see below)

The file templates/manual/`manual_pdf_template.yaml` can be modified as needed.

### 13.3 Code Blocks

Command/YAML lines auto-wrap if the below is included in `manual_pdf.yaml`:

```yaml
header-includes:
  - \usepackage{fvextra}
  - \fvset{breaklines=true,breakanywhere=true}
```

Nonetheless,

- Keep command lines reasonably short when possible.
- When a command is long, prefer a readable multi-line version, e.g.:

```bash
python -m pip install \
  -i https://test.pypi.org/simple \
  --extra-index-url https://pypi.org/simple \
  psair
```

That improves both GitHub and PDF rendering, but the LaTeX wrapping is still desirable for edge cases (e.g., long URLs).

------------------------------------------------------------------------

## References

-   Pandoc Documentation (https://pandoc.org/)
-   CommonMark Specification (https://commonmark.org/)
-   Semantic Versioning (https://semver.org/)
-   Write the Docs Documentation Guide
    (https://www.writethedocs.org/guide/)
