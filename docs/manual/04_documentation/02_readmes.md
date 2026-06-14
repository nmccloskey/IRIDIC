# Repository README Policy

## 1. Purpose

This document defines the **standard structure and conventions for
repository README files** within the IRIDIC framework.\
The goal is to ensure that every repository presents:

-   a clear project identity
-   minimal friction for installation
-   consistent navigation to documentation and research artifacts
-   professional presentation aligned with open‑source best practices

These guidelines apply to repositories such as **DIAAD, TAALCR, ALASTR,
CLATR, IRIDIC**, and related projects.

------------------------------------------------------------------------

## 2. Design Philosophy

A README should function as the **front door to a repository**.

It must satisfy three audiences simultaneously:

1.  **New users** -- need quick orientation and installation
    instructions
2.  **Researchers / collaborators** -- need conceptual understanding and
    citations
3.  **Developers** -- need links to documentation and architecture
    details

Accordingly, README files should:

-   communicate the project purpose within seconds
-   allow installation within a few commands
-   provide navigation to deeper documentation rather than duplicating
    it

Detailed manuals belong in `/manual/` directories or documentation
sites, not in the README itself.

------------------------------------------------------------------------

## 3. Standard README Structure

Every repository README should follow this general order:

    Title
    Badges

    Short description / tagline

    Development status notice (if relevant)

    Installation

    Quick start or pipeline overview

    Links (docs, web app, paper, Zenodo)

    Detailed sections

This structure ensures that the most important information appears
**above the fold** on GitHub.

------------------------------------------------------------------------

## 4. Title and Badges

The repository title should appear as a top‑level heading, like:

``` markdown
# RASCAL – Resources for Analyzing Speech in Clinical Aphasiology Labs
```

Immediately beneath the title, include a **standardized badge block**.

Example badge set (RASCAL):

``` markdown
![PyPI version](https://img.shields.io/pypi/v/rascal-speech)
![Python](https://img.shields.io/pypi/pyversions/rascal-speech)
![License](https://img.shields.io/github/license/nmccloskey/RASCAL)
![Zenodo DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17624073.svg)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rascal.streamlit.app/)
```

### Badge Conventions

Badges should follow a consistent order:

1.  **PyPI version**
2.  **Python versions**
3.  **License**
4.  **Zenodo DOI** (if applicable)
5.  **Web application badge** (Streamlit or other UI)
6.  Optional CI/test badges

This ordering prioritizes information relevant to installation and
research citation.

------------------------------------------------------------------------

## 5. Short Description / Tagline

Immediately beneath the badges, include a **concise one‑sentence
description** of the project.

Example:

    DIAAD is a database‑oriented workflow for managing transcription,
    reliability coding, and discourse analysis in clinical aphasiology research.

Guidelines:

-   one sentence preferred
-   avoid technical implementation details
-   emphasize **purpose and research niche**

------------------------------------------------------------------------

## 6. Development Status Notice

If a repository is in early development or undergoing major refactoring,
include a short status note.

Example:

    ⚠️ This repository is under active development. APIs may change between releases.

This section helps manage user expectations.

It may be omitted for mature projects.

------------------------------------------------------------------------

## 7. Installation Section

The installation section should prioritize **pip installation from
PyPI**.

Example:

``` bash
pip install rascal-speech
```

If the project recommends a specific Python version, environment
manager, or external dependency, specify & include a short example.

See the TAACLR installation excerpt below. Installation instructions should remain **minimal and copy‑paste
friendly**.

## Installation

TAALCR is currently developed and tested with **Python 3.12**.

A dedicated virtual environment using Anaconda is recommended:

### 1. Create and activate your environment:

```bash
conda create --name taalcr python=3.12
conda activate taalcr
```

### 2. Install TAALCR:
```bash
# Install from PyPI
pip install taalcr

# or install the latest development version
pip install git+https://github.com/nmccloskey/taalcr.git@main
```

### 3. Install the spaCy transformer model

(required for automated POWERS coding)

```bash
python -m spacy download en_core_web_trf
```

------------------------------------------------------------------------

## 8. Quick Start / Pipeline Overview

After installation instructions, provide a short **usage overview**.

Example:

``` bash
rascal run config.yaml
```

This section may include:

-   a minimal command example
-   a short pipeline diagram
-   a brief list of workflow stages

The goal is to allow users to **confirm the software runs
successfully**.

------------------------------------------------------------------------

## 9. Links Section

Provide links to major project resources.

Typical items include:

-   documentation/manual
-   web application interface
-   research article
-   Zenodo archive
-   dataset resources

Example:

    Documentation: https://github.com/nmccloskey/RASCAL/manual
    Web App: https://rascal.streamlit.app/
    Zenodo Archive: https://doi.org/10.5281/zenodo.xxxxxx

These links allow the README to remain concise while pointing to richer
resources.

------------------------------------------------------------------------

## 10. Detailed Sections

After the links section, the README may contain more detailed material.

Examples include:

-   architecture overview
-   workflow description
-   example outputs
-   development roadmap
-   contributing guidelines

However, the README should **not become a full manual**.

Long technical documentation belongs in:

    manual/
    docs/

------------------------------------------------------------------------

## 11. Recommended Additional Components

Repositories may also include the following sections when appropriate:

### Citation

If the project corresponds to a research paper:

    ## Citation

Provide BibTeX or DOI references.

------------------------------------------------------------------------

### Contributing

For collaborative repositories:

    ## Contributing

Link to `CONTRIBUTING.md`.

------------------------------------------------------------------------

### License

A short license section is recommended:

    ## License

Example:

    This project is licensed under the MPL‑2.0 License.

------------------------------------------------------------------------

# 12. Style Conventions

README files should follow these stylistic guidelines:

-   clear headings with `##`
-   short paragraphs
-   minimal prose before installation instructions
-   consistent badge ordering across repositories
-   command examples formatted with fenced code blocks

Avoid:

-   long theoretical explanations
-   duplicate documentation already present in manuals
-   version numbers written directly in text

------------------------------------------------------------------------

## 13. Summary

A well‑structured README should allow a reader to:

1.  Understand the project purpose in seconds
2.  Install the software within minutes
3.  Locate detailed documentation easily

Maintaining consistent README conventions across repositories improves:

-   usability
-   professional presentation
-   research reproducibility
