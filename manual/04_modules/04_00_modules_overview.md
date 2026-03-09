
# Manual Modules Overview

## Purpose

The IRIDIC **manual modules** provide a small, modular toolkit for managing, validating, and distributing project documentation written as structured Markdown manuals.

Rather than maintaining large monolithic documents, IRIDIC manuals are designed as **filesystem‑native documentation trees**. Each manual section is an individual Markdown file organized in a predictable directory structure.

The manual modules provide tools that allow these modular documents to function as a **coherent documentation system** that supports:

- interactive browsing inside applications
- command‑line exploration and search
- automated validation of documentation hygiene
- deterministic outline generation
- compilation of full manuals into distributable PDFs

Together, these modules transform a simple directory of Markdown files into a **reproducible documentation pipeline**.

---

# Manual Architecture

An IRIDIC manual is typically organized as a directory tree such as:

```
manual/
    00_outline.md
    01_introduction.md
    02_installation.md
    03_workflow/
        03_01_overview.md
        03_02_transcript_tables.md
    04_outputs.md
    manual_pdf.yaml
```

Key design principles include:

**Modular documentation**  
Each section is written as an independent Markdown file.

**Deterministic ordering**  
Numeric prefixes (`01_`, `02_`, `03_01_`) define the manual's structure.

**Filesystem transparency**  
The manual remains readable and navigable directly from the repository.

**Derived artifacts**  
Files such as `00_outline.md` and compiled PDFs are generated automatically.

---

# Manual Module Ecosystem

The IRIDIC manual system is composed of several modules that operate at different stages of the documentation lifecycle.

| Module | Role |
|------|------|
| `manual_index` | Index manual files and enable search |
| `manual_outline` | Generate navigation outlines |
| `manual_chars` | Validate documentation formatting |
| `manual_pdf` | Compile manuals into PDFs |
| `manual_viewer` | Render manuals interactively in Streamlit |

These modules can be used independently or combined into automated workflows.

---

# Typical Documentation Workflow

The modules are usually used in the following order:

```
Write manual sections (Markdown)
        ↓
manual_chars validation
        ↓
manual_outline generation
        ↓
manual_pdf compilation
        ↓
manual_viewer browsing (optional)
```

### 1. Write manual sections

Documentation is written as Markdown files organized within a `manual/` directory.

### 2. Validate documentation

```
iridic chars manual
```

This stage detects issues such as:

- trailing whitespace
- inconsistent line endings
- non‑ASCII characters

Optional automatic fixes may be applied.

### 3. Generate outline

```
iridic outline manual
```

This generates the file:

```
00_outline.md
```

which contains a navigable overview of the manual.

### 4. Compile PDF

```
iridic pdf manual
```

This produces a single compiled manual suitable for distribution.

### 5. Interactive viewing (optional)

The Streamlit viewer can render the manual directly inside applications.

---

# CLI Interface

The IRIDIC manual toolkit exposes several commands:

```
iridic tree
iridic search
iridic index
iridic outline
iridic chars
iridic pdf
```

These commands allow users to explore, validate, and compile manuals entirely from the command line.

---

# Streamlit Integration

The manual viewer module enables manuals to be embedded directly inside Streamlit tools.

Example usage:

```
from iridic.manual_viewer import render_manual_ui

render_manual_ui(repo_root=".")
```

This creates an interactive documentation browser with:

- folder navigation
- search functionality
- inline document rendering

This feature allows IRIDIC tools to ship with **built‑in interactive documentation**.

---

# Recommended Manual Configuration (YAML)

When compiling manuals into PDFs, IRIDIC strongly recommends maintaining a **Pandoc metadata YAML file** alongside the manual.

Example:

```
manual_pdf.yaml
```

This configuration file controls aspects such as:

- title and author metadata
- page geometry
- fonts
- line spacing
- syntax highlighting
- PDF layout settings

Using a YAML configuration provides several advantages:

**Separation of concerns**  
Manual styling is separated from manual content.

**Reproducible builds**  
Manual formatting remains consistent across environments.

**Override flexibility**  
CLI arguments can override YAML settings when needed.

---

# Documentation Philosophy

The IRIDIC manual system is designed around several principles.

### Filesystem‑native documentation

Documentation should remain simple Markdown files that can be edited with standard tools.

### Derived navigation artifacts

Navigation files such as outlines should be generated automatically rather than maintained manually.

### Reproducible documentation builds

Compiled manuals should be deterministic and reproducible.

### Embedded documentation

Applications should be able to ship with integrated manuals.

---

# Summary

The IRIDIC manual modules provide a lightweight system for managing modular documentation.

Key capabilities include:

- indexing manual files
- searching documentation
- generating outlines
- validating documentation formatting
- compiling manuals into PDFs
- embedding manuals inside applications

Together these modules enable IRIDIC projects to maintain **clean, navigable, and reproducible instruction manuals while preserving a simple Markdown‑based documentation workflow**.
