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

IRIDIC is a meta-repository.

It does not contain software tools themselves.\
Instead, it defines the policies, conventions, and operational standards
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

## Core Philosophies

### 1. Single Source of Truth (SSOT)

Functional metadata (versions, dependencies, configuration) must exist
in exactly one authoritative location.

Duplication is allowed only for aesthetic or display purposes.

------------------------------------------------------------------------

### 2. Boring Releases Are Good Releases

Releases should be:

-   Verified
-   Reproducible
-   Install-tested
-   Tagged
-   Deliberate

No hidden state. No guesswork.

------------------------------------------------------------------------

### 3. Whimsy with Rigor

Repository names may be playful.

Architecture and implementation are not.

------------------------------------------------------------------------

### 4. LLM-Augmented Development

Large language models (primarily ChatGPT) are used extensively for:

-   Architectural iteration
-   Refactoring
-   Policy drafting
-   Packaging guidance
-   Documentation synthesis

Final responsibility for correctness and design coherence remains with
the human author.

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
