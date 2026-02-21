# PyPI Release & Update Policy

**Project:** IRIDIC -- Idiosyncratic Repository of Initialization &
Development Itineraries for Codebases\
**Document:** pypi_updates.md\
**Last Updated:** 2026-02-21

------------------------------------------------------------------------

## 1. Purpose

This document defines the standardized workflow for:

-   Preparing a release
-   Building distributions
-   Testing installations
-   Uploading to PyPI/TestPyPI
-   Synchronizing branches
-   Managing version numbers

This policy aligns with:

-   PEP 440 (Version Identification)
-   Semantic Versioning (https://semver.org)
-   PyPA packaging guide (https://packaging.python.org)

------------------------------------------------------------------------

# 2. High-Level Release Workflow

### Development Cycle

1.  Implement changes on `dev`
2.  Test CLI locally
3.  Iterate as needed
4.  Merge `dev` → `main`
5.  Test web app (if applicable)
6.  Iterate if necessary (repeat merge cycle)
7.  Bump version on `main`
8.  Build + test locally
9.  Upload to PyPI
10. Merge `main` → `dev`

Public releases always reflect the `main` branch.

------------------------------------------------------------------------

# 3. Branch Discipline During Release

### Upload From `main` Only

PyPI packaging uses whatever files are in your working directory at
build time.

When you run:

``` bash
python -m build
python -m twine upload dist/*
```

You are publishing the currently checked-out branch.

✔ Always upload from `main`\
✘ Do not upload from `dev` (unless explicitly publishing a pre-release)

------------------------------------------------------------------------

# 4. Canonical Release Sequence

### STEP 1 --- Finish Work in `dev`

Ensure:

-   All features are complete
-   Tests pass
-   Version is still the previous one (e.g., `1.0.0`)

------------------------------------------------------------------------

### STEP 2 --- Merge `dev` → `main`

``` bash
git checkout main
git merge dev
```

------------------------------------------------------------------------

### STEP 3 --- Bump Version on `main`

Update version in:

-   `pyproject.toml`
-   `__init__.py` (if applicable)

Example:

``` toml
version = "1.0.1"
```

Commit:

``` bash
git commit -am "Bump version to 1.0.1"
```

------------------------------------------------------------------------

### STEP 4 --- Clean & Build

``` bash
rm -rf dist build *.egg-info
python -m pip install -U pip build
python -m build
```

This produces:

    dist/
      package-1.0.1.tar.gz
      package-1.0.1-py3-none-any.whl

------------------------------------------------------------------------

### STEP 5 --- Clean Environment Install Test

``` bash
conda create --name test_env python=3.12
conda activate test_env
python -m pip install -U pip
python -m pip install dist/*.whl
```

Minimal smoke test:

``` bash
python -c "import package; print('ok', package.__version__)"
package --help
```

No release without install verification.

------------------------------------------------------------------------

### STEP 6 --- Upload

``` bash
python -m twine upload dist/*
```

------------------------------------------------------------------------

### STEP 7 --- Sync `main` → `dev`

``` bash
git checkout dev
git merge main
```

This prevents version divergence.

------------------------------------------------------------------------

# 5. TestPyPI Loop (Recommended for Early Releases)

### Local Fast Test

``` bash
python -m build
pip install dist/package-0.0.1a1-py3-none-any.whl
python -c "import package; print(package.__version__)"
```

### TestPyPI Test

``` bash
twine upload --repository testpypi dist/*
pip install -i https://test.pypi.org/simple package==0.0.1a1
```

Fix → bump → rebuild → reupload → retest.

------------------------------------------------------------------------

# 6. Versioning Rules

## 6.1 Versions Are Immutable

Once uploaded to PyPI or TestPyPI:

-   You cannot overwrite
-   You cannot re-upload
-   You cannot "fix in place"

Every upload requires a new version string.

If `0.0.1a1` contains a typo → next version must be `0.0.1a2`.

------------------------------------------------------------------------

## 6.2 Pre-Release Scheme (PEP 440)

Valid progression:

    0.0.1a1  <  0.0.1a2  <  0.0.1b1  <  0.0.1rc1  <  0.0.1

Behavior:

-   `pip install package` → does NOT install pre-releases
-   `pip install package --pre` → includes pre-releases
-   `pip install package==0.0.1a2` → explicit works

This is desirable behavior.

------------------------------------------------------------------------

# 7. Minimal Safe Release Checklist

Before uploading:

-   [ ] On `main`
-   [ ] Version bumped
-   [ ] Tag created
-   [ ] Clean build succeeds
-   [ ] Fresh environment install works
-   [ ] CLI works
-   [ ] Web app launches
-   [ ] Dependencies verified
-   [ ] README updated if needed

------------------------------------------------------------------------

# 8. Dependency Policy (Cross-Reference)

A separate `dependency_policy.md` should define:

-   Version spec philosophy
-   When to pin vs. range
-   Optional dependencies
-   Heavy NLP libraries placement in `[project.optional-dependencies]`
-   Avoiding over-specification early in lifecycle

Guiding principle:

> Tightening later is easy. Loosening later is painful.

Especially for ecosystem tools like CLATR.

------------------------------------------------------------------------

# 9. Philosophical Principle

A release is not just a build artifact.

It is:

-   A reproducible research object
-   A citation anchor
-   A dependency contract
-   A public commitment

Releases should be deliberate, verified, and boring - boring releases are good releases.
