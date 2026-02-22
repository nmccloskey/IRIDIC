# GitHub Workflow & Update Policy

## 1. Purpose

This document defines standardized conventions for:

-   Branch management
-   Commit structure and granularity
-   Commit message formatting
-   Tagging and release policy
-   Relationship between GitHub, PyPI, and deployed applications

The aim is consistency, transparency, reversibility, and alignment with
widely accepted Git and open-source practices.

This policy follows conventions informed by:

-   Git documentation (https://git-scm.com/docs)
-   GitHub Flow principles
-   Conventional Commits specification
    (https://www.conventionalcommits.org)
-   Semantic Versioning (https://semver.org)

------------------------------------------------------------------------

## 2. Branching Model

### 2.1 Two-Branch System

All repositories use a **main + dev** model.

-   `main` → stable, release-ready branch
-   `dev` → active development branch

No additional long-lived branches are maintained unless collaboration or
complexity requires it.

------------------------------------------------------------------------

### 2.2 Development Workflow

All feature work, refactors, and experiments occur on `dev`.

Workflow:

1.  Implement changes on `dev`
2.  Perform informal testing (local CLI, environment testing, manual
    verification)
3.  Perform formal testing when applicable (pytest, regression tests,
    install tests)
4.  Confirm expected behavior
5.  Merge `dev` → `main`

Merges to `main` occur only after verification that changes behave as
intended.

------------------------------------------------------------------------

### 2.3 Exception: Version Bump Before PyPI Upload

The only permissible case where `main` may be updated prior to `dev`
synchronization:

-   Version bump immediately preceding PyPI upload

The typical pattern:

1.  Merge `dev` → `main`
2.  Update version number on `main`
3.  Tag release
4.  Build & upload to PyPI
5.  Merge `main` → `dev` (to synchronize version metadata)

This prevents accidental version divergence.

------------------------------------------------------------------------

### 2.4 Deployment Alignment

The stable public-facing version always corresponds to `main`.

-   **PyPI releases reflect `main`***
-   **Streamlit or web deployments reflect `main`***
-   Temporary linking of a web app to `dev` is allowed for controlled
    testing but must not persist

\* or a recent stable version thereof - multiple iterations of updates to `dev` and merges on `main` may precede deployment.

------------------------------------------------------------------------

## 3. Commit Granularity Policy

Commits should represent:

-   A logical unit of change
-   A reversible conceptual step
-   A state worth potentially reverting to

Heuristic: \> "Would I want to revert to this exact state if necessary?"

Avoid:

-   Massive multi-purpose commits
-   Mixing refactors with feature additions
-   Silent breaking changes

Preferred:

-   Small but meaningful units
-   Structural clarity
-   Clean history

------------------------------------------------------------------------

## 4. Commit Message Conventions

This project loosely follows the **Conventional Commits** structure for
clarity and tooling compatibility.

Format:

    type(scope): concise summary

    Optional extended description.

Common types:

-   `feat:` new feature
-   `fix:` bug fix
-   `refactor:` code restructuring without behavioral change
-   `docs:` documentation changes
-   `test:` adding or updating tests
-   `chore:` maintenance tasks
-   `build:` packaging or dependency updates
-   `perf:` performance improvement

Examples:

    feat(ngrams): add sentence-level entropy calculation
    refactor(pipeline): decouple IOManager from SQLDaemon
    fix(cli): correct argument parsing for --just_c2
    docs(readme): clarify installation instructions

Guidelines:

-   Use present tense
-   Be specific but concise
-   Avoid vague phrases ("updates", "changes")
-   Prioritize clarity over cleverness

------------------------------------------------------------------------

## 5. Tagging & Release Policy

### 5.1 Semantic Versioning

All repositories follow Semantic Versioning (SemVer):

    MAJOR.MINOR.PATCH

-   MAJOR → breaking changes
-   MINOR → new features (backward compatible)
-   PATCH → bug fixes

Pre-release versions allowed:

    0.0.1a1
    0.2.0b2
    1.0.0rc1

------------------------------------------------------------------------

### 5.2 Tagging Conventions

Tags must:

-   Match version exactly
-   Be annotated tags
-   Be created only from `main`

Example:

    git tag -a v0.2.0 -m "Release v0.2.0"
    git push origin v0.2.0

No tagging from `dev`.

------------------------------------------------------------------------

## 6. Pull Requests (Even If Solo)

Even when working independently:

-   Prefer merging via pull request instead of direct branch
    fast-forward
-   Use PR description to summarize changes
-   Document rationale for structural changes

This creates a durable project history and improves later reviewability.

------------------------------------------------------------------------

## 7. Reproducibility Safeguards

Before merging to `main`, verify:

-   Package installs in a clean environment
-   CLI entry points work
-   Web app launches
-   Tests pass
-   Documentation reflects new behavior
-   Version numbers are consistent

No merge without install verification.

------------------------------------------------------------------------

## 8. Optional Future Extensions

Potential additions as projects scale:

-   Code review standards
-   Issue labeling conventions
-   GitHub Actions CI/CD rules
-   Protected branch rules
-   Required status checks
-   Automated version bump workflows

------------------------------------------------------------------------

## 9. Philosophical Principle

The Git history is not merely archival---it is part of scholarly infrastructure.

A clean history:

-   Protects reproducibility
-   Enables refactoring
-   Improves collaboration
-   Signals professional maturity
-   Reduces cognitive load for future self

The aim is not punctilious formality but durable clarity.
