# Repository Structure Policy

## 1. Purpose

This document defines the **standard repository structure** used across
the IRIDIC ecosystem.

The goals are:

-   consistent project organization
-   easier navigation across repositories
-   reproducible research workflows
-   separation between **code**, **data**, **documentation**, and
    **runtime artifacts**

These conventions apply to repositories such as:

-   RASCAL
-   TAALCR
-   ALASTR
-   CLATR
-   IRIDIC
-   related research tooling

------------------------------------------------------------------------

## 2. Design Principles

Repository structures should satisfy several guiding principles.

### Clarity

Directory names should clearly reflect their purpose.

### Separation of Concerns

Different artifact types should remain separated:

  Artifact type        Location
  -------------------- ----------------
  source code          `src/`
  documentation        `manual/`
  test code            `tests/`
  runtime data         `*_data/`
  packaging metadata   root directory

### Reproducibility

Projects should support reproducible workflows where:

-   input data
-   configuration
-   output artifacts

are clearly organized and discoverable.

### Minimal Root Directory

The repository root should remain relatively uncluttered and contain
only:

-   project metadata
-   packaging configuration
-   top‑level documentation

------------------------------------------------------------------------

## 3. Standard Repository Layout

A typical repository should follow a structure similar to the following.

    repo_name/
    │
    ├── src/
    │   └── package_name/
    │       ├── __init__.py
    │       ├── cli.py
    │       ├── main.py
    │       ├── run_wrappers.py
    │       ├── utils/
    │       ├── module_a/
    │       └── module_b/
    │
    ├── tests/
    │
    ├── manual/
    │
    ├── images/
    │
    ├── webapp/                (optional)
    │
    ├── package_data/          (project‑specific name recommended)
    │   ├── input/
    │   └── output/
    │
    ├── example_config.yaml
    ├── config.yaml            (gitignored)
    │
    ├── README.md
    ├── LICENSE.txt
    ├── pyproject.toml
    ├── requirements.in
    ├── requirements.txt
    ├── pytest.ini
    │
    └── .gitignore

Not every repository will contain every directory, but the overall
pattern should remain consistent.

------------------------------------------------------------------------

## 4. Source Code Layout (`src/`)

All importable Python code should live inside the `src/` directory.

Example:

    src/
    └── rascal/

This **src‑layout packaging pattern** prevents accidental imports from
the working directory and ensures the installed package behaves the same
way as the development version.

Within the package directory, modules should be organized by functional
area.

Example:

    src/rascal/
    ├── cli.py
    ├── main.py
    ├── run_wrappers.py
    ├── coding/
    ├── transcripts/
    └── utils/

------------------------------------------------------------------------

## 5. CLI and Execution Architecture

Many IRIDIC tools use a layered execution structure.

Typical pattern:

    CLI entry point
        ↓
    Argument parser
        ↓
    Main orchestration module
        ↓
    Run wrapper functions
        ↓
    Feature modules

### `cli.py`

Contains the command‑line interface entry point.

Responsibilities:

-   register CLI commands
-   load the argument parser
-   invoke the main execution logic

### `main.py`

Orchestrates the pipeline and coordinates high‑level workflow steps.

### `run_wrappers.py`

Contains wrapper functions responsible for:

-   importing heavy dependencies only when needed
-   executing feature modules
-   keeping the main pipeline modular

This pattern improves:

-   modularity
-   import performance
-   code organization

------------------------------------------------------------------------

## 6. Argument Parser SSOT

Command‑line argument definitions should follow a **single source of
truth** principle.

Instead of duplicating parser definitions across modules, argument
construction should occur in a shared utility module.

Example location:

    utils/auxiliary.py

Both `cli.py` and other modules can import the same parser builder
function.

This avoids:

-   argument drift
-   inconsistent CLI behavior
-   duplicated code.

------------------------------------------------------------------------

## 7. Data Directories

Projects that operate on datasets should include a dedicated **data
directory**.

Example:

    rascal_data/
    ├── input/
    └── output/

Guidelines:

  Directory   Purpose
  ----------- ------------------------------
  `input/`    raw or user‑provided data
  `output/`   generated analysis artifacts

Naming conventions typically follow:

    projectname_data/

Example:

    rascal_data/
    clatr_data/

These directories may be partially or fully ignored by git depending on
workflow requirements.

------------------------------------------------------------------------

## 8. Configuration Files

Two configuration files are typically present.

### `example_config.yaml`

Committed to the repository.

Purpose:

-   provide a template configuration
-   document available settings
-   allow new users to start quickly

### `config.yaml`

User‑specific runtime configuration.

This file is typically included in `.gitignore`.

------------------------------------------------------------------------

## 9. Documentation (`manual/`)

Detailed documentation should live in a dedicated `manual/` directory.

Example:

    manual/
    ├── 00_outline.md
    ├── 01_introduction.md
    ├── 02_installation.md
    ├── 03_workflow/
    └── manual_pdf.yaml

This keeps long‑form documentation separate from the README.

The README should remain concise and link to the manual when necessary.

------------------------------------------------------------------------

## 10. Tests

Unit tests and integration tests should reside in:

    tests/

Example:

    tests/
    ├── test_cli.py
    ├── test_transcripts.py
    └── test_utils.py

Testing configuration is typically stored in:

    pytest.ini

------------------------------------------------------------------------

## 11. Packaging Files

Python packaging metadata resides at the repository root.

Key files include:

|  File                | Purpose
|  --------------------| ------------------------
|  `pyproject.toml`    | package configuration
|  `requirements.in`   | top‑level dependencies
|  `requirements.txt`  | pinned dependencies
|  `LICENSE.txt`       | license declaration

Version numbers should exist **only in `pyproject.toml`**.

------------------------------------------------------------------------

## 12. Web Application Directory

Projects that include an interactive interface may include:

    webapp/

This typically contains:

-   Streamlit apps
-   UI wrappers for the CLI pipeline

The web application should act as a thin interface over the same backend
modules used by the CLI.

------------------------------------------------------------------------

## 13. Miscellaneous Files

Common supporting files include:

  File               Purpose
  ------------------ -------------------------------
  `.gitignore`       ignored files and directories
  `.vscode/`         optional development settings
  `.pytest_cache/`   testing cache (ignored)
  `images/`          documentation images

------------------------------------------------------------------------

## 14. Summary

A consistent repository structure provides several benefits:

-   easier onboarding for collaborators
-   predictable navigation across projects
-   cleaner packaging workflows
-   improved reproducibility

Maintaining consistent conventions across the IRIDIC ecosystem ensures
that tools such as **DIAAD, TAALCR, ALASTR, and CLATR** share a
coherent development architecture.
