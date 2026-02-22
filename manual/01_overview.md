# General Context & Development Philosophy

## 1. Development Environment

Primary workstation setup:

-   **Operating System:** Windows
-   **Editor:** VS Code
-   **Python Environment Manager:** Anaconda
-   **Repository Location:** OneDrive-synced `GitRepos` folder
-   **Git Integration:** VS Code built-in GitHub features
-   **Terminal Usage:** VS Code integrated terminal (used for builds,
    PyPI uploads, pip-tools, etc.)

This workflow prioritizes:

-   Local clarity
-   Reproducible command-line operations
-   Direct visibility of packaging and release steps
-   Minimal abstraction layers

------------------------------------------------------------------------

## 2. Core Technology Preferences

### 2.1 Primary Languages

-   **Python** → software engineering, pipelines, packaging
-   **SQLite** → lightweight, embedded relational storage
-   **R** → statistical workflows and modeling

Python is used for:
- CLI tools
- Modular analysis pipelines
- Database-backed workflows
- Streamlit applications
- Packaging and distribution

SQLite is preferred because:
- It is file-based and portable
- It supports relational structure without deployment overhead
- It aligns well with reproducible research workflows

R is preferred when:
- Statistical modeling is primary
- Publication-ready analysis scripts are needed
- Advanced statistical tooling is more mature

------------------------------------------------------------------------

## 3. Python Version Philosophy

The default practice is to use a **recent but not bleeding-edge** Python
version.

Rationale:

-   Newly released Python versions may require ecosystem stabilization.
-   Some libraries lag behind in compatibility updates.
-   Using a version that has "settled" improves reliability.

Current working version: **Python 3.12**.

General rule:

> Avoid .0 release-week adoption.\
> Prefer versions with demonstrated ecosystem stability.

------------------------------------------------------------------------

## 4. Packaging & Distribution Philosophy

Where possible, repositories include:

-   PyPI distribution
-   Streamlit web application
-   Zenodo archived datasets
-   PDF manuals
-   Example datasets

This supports:

-   Transparency
-   Reproducibility
-   Citation stability
-   Academic dissemination

Public-facing artifacts reflect the `main` branch.

------------------------------------------------------------------------

## 5. Academic Context

Projects are developed within an academic research environment
characterized by:

-   Open-source ethos
-   MIT licensing
-   Emphasis on replicability
-   Transparency in methodology
-   Durable research infrastructure

Repositories are treated as:

-   Scholarly artifacts
-   Methodological documentation
-   Reproducible research tools
-   Long-term intellectual infrastructure

------------------------------------------------------------------------

## 6. Naming & Identity

Repository naming reflects:

-   Acronym purity
-   Orthographic distinctiveness
-   Semantic accuracy
-   Occasional whimsy (with awareness of tone)

Whimsy is stylistic, not structural.

Utility and rigor are primary.

------------------------------------------------------------------------

## 7. One Source of Truth (SSOT)

Across repositories, a general principle applies:

> Functional metadata must exist in exactly one authoritative location.

Examples:

-   Version → `pyproject.toml`
-   Dependencies → `pyproject.toml`
-   Lock resolution → generated lockfiles
-   Configuration → central config file (e.g., YAML)

Duplication is permitted only for aesthetic display (e.g., README
badges).

------------------------------------------------------------------------

## 8. LLM-Augmented Development

Large language models (primarily ChatGPT) are used extensively for:

-   Architectural iteration
-   Refactoring
-   Packaging guidance
-   Policy drafting
-   Debugging
-   Documentation drafting

LLM assistance is treated as:

-   Collaborative scaffolding
-   Iterative refinement support
-   A productivity amplifier

Final responsibility for correctness, reproducibility, and design
coherence remains with the human author.

------------------------------------------------------------------------

## 9. Design Aesthetic

Preferred qualities in repositories:

-   Modular architecture
-   Clear separation of concerns
-   Reversible commits
-   Clean Git history
-   Minimal hidden magic
-   Explicit configuration
-   Boring release processes

Complexity is accepted when justified, but avoided when ornamental.

------------------------------------------------------------------------

## 10. Long-Term Objective

The broader goal of IRIDIC and related repositories is to build:

-   Durable research infrastructure
-   Reproducible analytic ecosystems
-   Modular, composable toolchains
-   Tools that scale from local experimentation to published research

This aim is useful infrastructure that ages well.

------------------------------------------------------------------------
