# Versioning Policy

## 1. Purpose

This document defines versioning conventions for IRIDIC-governed
repositories.\
Its goals are:

-   Clear communication of stability
-   Predictable release structure
-   Reduced ambiguity about which number to bump
-   Alignment with Python packaging standards (PEP 440)
-   Separation of development, main, and release states

------------------------------------------------------------------------

## 2. Governing Standard

IRIDIC repositories follow:

-   **Semantic Versioning (SemVer)**
-   Adapted to **PEP 440** for Python packaging compatibility

Core format:

    MAJOR.MINOR.PATCH

Optional pre-release suffix:

    MAJOR.MINOR.PATCHaN   # alpha
    MAJOR.MINOR.PATCHbN   # beta
    MAJOR.MINOR.PATCHrcN  # release candidate

Examples:

    0.0.1a1
    0.2.0
    1.0.0
    1.4.3
    2.0.0

------------------------------------------------------------------------

## 3. Version Components

### 3.1 MAJOR (X.0.0)

Increment when introducing **breaking changes**.

Breaking changes include:

-   Removing or renaming public APIs
-   Changing database schemas
-   Altering expected input/output structure
-   Redesigning configuration formats
-   Modifying CLI commands incompatibly
-   Changing default behavior affecting outputs

Guiding question:

> Would upgrading require users to modify existing scripts, configs, or
> workflows?

If yes → bump MAJOR.

------------------------------------------------------------------------

### 3.2 MINOR (0.X.0)

Increment when adding **new, backward-compatible functionality**.

Examples:

-   New analysis modules
-   New CLI flags
-   New config parameters (non-breaking)
-   Additional output formats
-   Performance improvements without behavioral change

Guiding question:

> Is this backward compatible but meaningfully extends functionality?

If yes → bump MINOR.

------------------------------------------------------------------------

### 3.3 PATCH (0.0.X)

Increment for **bug fixes or internal improvements**.

Examples:

-   Fixing parsing errors
-   Correcting column naming issues
-   Improving logging
-   Refining edge-case handling
-   Documentation corrections

Guiding question:

> Would users notice this change unless something was broken before?

If yes → bump PATCH.

------------------------------------------------------------------------

## 4. Special Case: Major Version 0

Before `1.0.0`, the API is considered unstable.

Rules during `0.y.z` phase:

-   Breaking changes → bump MINOR
-   New features → bump MINOR
-   Fixes → bump PATCH

Effectively:

-   MINOR behaves like MAJOR
-   PATCH remains PATCH

------------------------------------------------------------------------

## 5. Pre-Release Versions

### 5.1 Alpha (`aN`)

Example:

    1.2.0a1

Use when:

-   Architecture is still evolving
-   Core features incomplete
-   Internal testing phase

------------------------------------------------------------------------

### 5.2 Beta (`bN`)

Example:

    1.2.0b1

Use when:

-   Feature complete
-   Entering stabilization phase
-   Broader testing desired

------------------------------------------------------------------------

### 5.3 Release Candidate (`rcN`)

Example:

    1.2.0rc1

Use when:

-   Final verification stage
-   Only critical fixes allowed
-   Expectation of imminent stable release

------------------------------------------------------------------------

## 6. Development vs Main vs PyPI

IRIDIC repositories distinguish between:

### dev branch

-   Frequent commits
-   Experimental changes
-   Refactoring
-   No version bump required

### main branch

-   Stable merges from dev
-   Tests passing
-   Documentation synchronized
-   No automatic version bump required

### PyPI release

Version bump occurs **only** when creating a release artifact.

Never bump version solely because main was updated.

------------------------------------------------------------------------

## 7. Clean Release Workflow

1.  Merge dev → main

2.  Update version in `pyproject.toml`

3.  Commit:

        chore: bump version to X.Y.Z

4.  Tag:

        git tag vX.Y.Z
        git push --tags

5.  Build:

        python -m build

6.  Upload:

        twine upload dist/*

------------------------------------------------------------------------

## 8. Decision Framework

When uncertain:

1.  Did this break user workflows?
    -   Yes → MAJOR (or MINOR if \< 1.0)
2.  Did this add capability without breaking compatibility?
    -   Yes → MINOR
3.  Did this fix or refine existing behavior?
    -   Yes → PATCH
4.  Not stable yet?
    -   Use alpha or beta

------------------------------------------------------------------------

## 9. Stub / Scaffold Versions

Early packaging tests may use:

    0.0.1a1

Appropriate when:

-   Testing packaging pipeline
-   Verifying installation
-   Repository scaffolding phase

Once functional capability exists → move to `0.1.0`.

------------------------------------------------------------------------

## 10. Frequency Guidance

Healthy pattern:

-   Commit frequently
-   Merge deliberately
-   Release intentionally

Release only when:

> You would be comfortable citing that version in a publication.

------------------------------------------------------------------------

## 11. References

-   Semantic Versioning Specification: https://semver.org/
-   PEP 440 -- Version Identification and Dependency Specification:
    https://peps.python.org/pep-0440/
-   Python Packaging User Guide: https://packaging.python.org/
