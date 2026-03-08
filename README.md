# IRIDIC

## Idiosyncratic Repository of Initialization and Development Itineraries for Codebases

> IRIDIC documents one developer's deliberately chosen workflows, with
> the goal of making implicit practices explicit, reproducible, and
> durable.

**Status:** Early-stage, active development\
**License Philosophy:** MIT-first, open infrastructure\
**Primary Context:** Academic research software development

------------------------------------------------------------------------

## What IRIDIC Is

IRIDIC is a mostly a meta-repository with some utilities (see below).

It defines the policies, conventions, and operational standards
that govern:

-   Repository naming
-   Branching workflows
-   Versioning and PyPI releases
-   Dependency management and locking
-   Single Source of Truth (SSOT) principles
-   Documentation structure
-   Release discipline
-   Reproducibility standards

IRIDIC exists to make engineering choices intentional rather than
accidental.

------------------------------------------------------------------------

## Development Context

The policies in this repository reflect a specific working environment:

-   Windows workstation
-   VS Code
-   Anaconda-managed Python environments
-   GitHub-integrated workflows
-   SQLite for data storage
-   Python for software
-   R for statistical workflows
-   Streamlit for web interfaces
-   Zenodo for archival datasets
-   PyPI for distribution

The emphasis is on:

-   Reproducibility
-   Transparency
-   Modular design
-   Clean Git history
-   Durable research infrastructure

------------------------------------------------------------------------


## Why This Exists

Academic software often evolves organically.

IRIDIC attempts to:

-   Arrest drift
-   Formalize implicit habits
-   Improve reproducibility
-   Reduce cognitive load
-   Build infrastructure that ages well

It is a system for preventing future confusion.

------------------------------------------------------------------------

## Developmental Trajectory Note

IRIDIC is forward-looking.

Many policies in this repository represent standards that are being
progressively adopted.\
Earlier repositories --- particularly those developed prior to February
2026 --- may not conform fully to these protocols.

This is expected, and IRIDIC exists precisely to reduce such inconsistencies over time.

------------------------------------------------------------------------

## Long-Term Objective

To build a coherent, reproducible ecosystem of research-grade software
tools that scale from:

-   Local experimentation\
    to
-   Public distribution\
    to
-   Citable, archival research artifacts

IRIDIC is intended as 'infrastructure for infrastructure'.

------------------------------------------------------------------------

# IRIDIC – Manual Infrastructure Utilities

IRIDIC provides lightweight tools for **indexing, viewing, validating, and compiling project manuals** that are organized as modular Markdown files.  
It is designed to support reproducible documentation workflows inside research or software repositories.

The package focuses on four core capabilities:

- **Manual indexing** – build a navigable structure from Markdown files.
- **Outline generation** – auto-generate a table-of-contents style outline.
- **Character / formatting checks** – detect non‑ASCII characters, trailing whitespace, and line‑ending issues.
- **PDF compilation** – assemble modular Markdown files and compile them to PDF using Pandoc.

A lightweight **Streamlit viewer** is also included for interactive manual browsing.

---

## Installation

Install from PyPI:

```bash
pip install iridic
```

Or install from a local repository:

```bash
pip install -e .
```

---

## Command Line Usage

IRIDIC provides a CLI once installed.

```bash
iridic --help
```

Common commands:

### View manual tree

```bash
iridic tree manual/
```

### Search the manual

```bash
iridic search "configuration"
```

### Build or refresh outline

```bash
iridic outline manual/
```

### Run character checks

```bash
iridic chars manual/
```

### Compile PDF manual

```bash
iridic pdf manual/
```

---

## Streamlit Manual Viewer

The Streamlit viewer allows interactive navigation of Markdown manuals directly within a web interface.

Because IRIDIC keeps the core package lightweight, the viewer is **not imported at the package top level**.

Instead import it explicitly:

```python
from iridic.manual_viewer import render_manual_ui
```

Example Streamlit usage:

```python
import streamlit as st
from iridic.manual_viewer import render_manual_ui

render_manual_ui(
    repo_root=".",
    manual_rel_dir="manual"
)
```

This renders a collapsible manual viewer with:

- searchable sections
- folder tree navigation
- automatic section rendering
- optional outline generation

---

## Package Structure

Core modules:

```
iridic/
│
├── manual_index.py     # manual indexing and search
├── manual_outline.py   # outline / TOC generation
├── manual_chars.py     # character and formatting checks
├── manual_pdf.py       # PDF compilation with Pandoc
└── manual_viewer.py    # Streamlit manual viewer
```

The package API intentionally exports **core processing utilities** at the top level while keeping UI components separate.

Example:

```python
from iridic import build_manual_pdf
from iridic import check_manual_chars
```

Viewer usage:

```python
from iridic.manual_viewer import render_manual_ui
```

---

## Typical Workflow

A common documentation workflow may look like:

1. Maintain modular Markdown files under `manual/`
2. Generate or refresh the outline

```bash
iridic outline manual/
```

3. Validate documentation formatting

```bash
iridic chars manual/
```

4. Compile a PDF manual

```bash
iridic pdf manual/
```

5. Optionally embed the Streamlit viewer inside an application.

---

## Requirements

- Python 3.10+
- Pandoc (for PDF compilation)
- LaTeX engine such as `xelatex` (for Pandoc PDF builds)

Streamlit is required only when using the viewer.
